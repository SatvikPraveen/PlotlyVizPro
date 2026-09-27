r"""Regression estimators: ordinary least squares and LOWESS.

Ordinary least squares is solved with a QR decomposition on a polynomial
design matrix; confidence and prediction intervals follow the classical
Student-t formulas (e.g. Montgomery, Peck & Vining, *Introduction to Linear
Regression Analysis*, ch. 2-3):

.. math::

    \\hat{y}_0 \\pm t_{\\alpha/2, n-p}\\, s \\sqrt{\\mathbf{x}_0^T (X^T X)^{-1} \\mathbf{x}_0}
    \\quad\\text{(mean response)}

    \\hat{y}_0 \\pm t_{\\alpha/2, n-p}\\, s \\sqrt{1 + \\mathbf{x}_0^T (X^T X)^{-1} \\mathbf{x}_0}
    \\quad\\text{(new observation)}

LOWESS is Cleveland's (1979) locally weighted regression with tricube weights
and optional robustifying iterations using bisquare weights on the residuals.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd
from scipy import stats as sps

from plotlyvizpro._typing import ArrayLike, FloatArray
from plotlyvizpro._validation import (
    as_float_array,
    require_in_unit_interval,
    require_positive_int,
    require_same_length,
)


def _x_display(x: ArrayLike) -> np.ndarray:
    """Keep datetime x for plotting while the numeric copy is used for fitting."""
    if isinstance(x, pd.Series):
        return x.to_numpy()
    return np.asarray(x)


def _design(x: FloatArray, degree: int) -> FloatArray:
    return np.vander(x, degree + 1, increasing=True)


@dataclass
class OLSFit:
    """Result of :func:`ols_fit`.

    Attributes
    ----------
    x:
        The original x values (datetime preserved) in input order.
    y_hat:
        Fitted values at ``x``.
    ci_lower, ci_upper:
        Confidence band for the mean response.
    pi_lower, pi_upper:
        Prediction band for a new observation.
    coef:
        Polynomial coefficients in increasing order (intercept first).
    stderr:
        Standard errors of ``coef``.
    r_squared, adj_r_squared:
        Coefficient of determination and its degrees-of-freedom adjusted form.
    residual_std:
        Residual standard error ``s``.
    dof:
        Residual degrees of freedom ``n - p``.
    p_values:
        Two-sided p-values for each coefficient (H0: coefficient = 0).
    confidence:
        The confidence level used for the bands.
    """

    x: np.ndarray
    y_hat: FloatArray
    ci_lower: FloatArray
    ci_upper: FloatArray
    pi_lower: FloatArray
    pi_upper: FloatArray
    coef: FloatArray
    stderr: FloatArray
    r_squared: float
    adj_r_squared: float
    residual_std: float
    dof: int
    p_values: FloatArray
    confidence: float
    residuals: FloatArray = field(repr=False)

    @property
    def slope(self) -> float:
        """First-order coefficient (only meaningful for ``degree=1``)."""
        return float(self.coef[1]) if self.coef.size > 1 else 0.0

    @property
    def intercept(self) -> float:
        """Zeroth-order coefficient."""
        return float(self.coef[0])

    def equation(self, precision: int = 3) -> str:
        """Human-readable fitted polynomial, e.g. ``y = 1.20 + 0.50x``."""
        terms = [f"{self.coef[0]:.{precision}f}"]
        for k, c in enumerate(self.coef[1:], start=1):
            sign = "+" if c >= 0 else "-"
            power = "x" if k == 1 else f"x^{k}"
            terms.append(f"{sign} {abs(c):.{precision}f}{power}")
        return "y = " + " ".join(terms)


def ols_fit(x: ArrayLike, y: ArrayLike, degree: int = 1, confidence: float = 0.95) -> OLSFit:
    """Fit a polynomial by ordinary least squares with confidence and prediction bands.

    Parameters
    ----------
    x, y:
        Samples. ``x`` may be datetime-like; it is converted to days since the
        first observation for numerical stability and kept as-is for display.
    degree:
        Polynomial degree (1 = straight line).
    confidence:
        Two-sided confidence level for the bands.

    Notes
    -----
    Rows containing NaN in either input are dropped before fitting; the
    returned arrays are aligned to the *kept* rows.
    """
    degree = require_positive_int(degree, "degree")
    confidence = require_in_unit_interval(confidence, "confidence")
    require_same_length(x, y, names=("x", "y"))
    x_disp = _x_display(x)
    xf = as_float_array(x, "x")
    yf = as_float_array(y, "y")
    keep = ~(np.isnan(xf) | np.isnan(yf))
    xf, yf, x_disp = xf[keep], yf[keep], x_disp[keep]
    n = xf.size
    p = degree + 1
    if n <= p:
        raise ValueError(f"Need more than {p} finite observations for degree {degree}, got {n}")

    # Centre + scale x for conditioning (datetime ns -> days would otherwise be 1e14).
    x_centre = xf.mean()
    x_scale = xf.std() or 1.0
    z = (xf - x_centre) / x_scale
    X = _design(z, degree)
    q, r = np.linalg.qr(X)
    beta_z = np.linalg.solve(r, q.T @ yf)
    y_hat = X @ beta_z
    resid = yf - y_hat
    dof = n - p
    s2 = float(resid @ resid / dof)
    s = float(np.sqrt(s2))
    xtx_inv = np.linalg.inv(r.T @ r)
    leverage = np.einsum("ij,jk,ik->i", X, xtx_inv, X)
    t_crit = float(sps.t.ppf(0.5 + confidence / 2, dof))
    ci_half = t_crit * s * np.sqrt(leverage)
    pi_half = t_crit * s * np.sqrt(1.0 + leverage)

    ss_tot = float(((yf - yf.mean()) ** 2).sum())
    r2 = 1.0 - float(resid @ resid) / ss_tot if ss_tot > 0 else 1.0
    adj_r2 = 1.0 - (1.0 - r2) * (n - 1) / dof

    # Map coefficients back to the original x scale via a Vandermonde re-fit on the
    # already-fitted values (exact for polynomials; avoids binomial expansion code).
    beta = np.asarray(np.polynomial.polynomial.polyfit(xf, y_hat, degree), dtype=np.float64)
    # Standard errors on the original scale: transform the covariance of beta_z.
    # For degree 1 this is analytic; for higher degrees we reuse the numeric Jacobian.
    cov_z = s2 * xtx_inv
    jac = _scale_jacobian(degree, x_centre, x_scale)
    cov = jac @ cov_z @ jac.T
    stderr = np.sqrt(np.diag(cov))
    with np.errstate(divide="ignore", invalid="ignore"):
        t_stats = beta / stderr
    p_values = 2.0 * sps.t.sf(np.abs(t_stats), dof)

    return OLSFit(
        x=x_disp,
        y_hat=y_hat,
        ci_lower=y_hat - ci_half,
        ci_upper=y_hat + ci_half,
        pi_lower=y_hat - pi_half,
        pi_upper=y_hat + pi_half,
        coef=beta,
        stderr=stderr,
        r_squared=r2,
        adj_r_squared=adj_r2,
        residual_std=s,
        dof=dof,
        p_values=p_values,
        confidence=confidence,
        residuals=resid,
    )


def _scale_jacobian(degree: int, centre: float, scale: float) -> FloatArray:
    """Jacobian d(beta_original)/d(beta_z) for z = (x - centre)/scale.

    Polynomial in z, sum_k b_k z^k, expands to sum_j a_j x^j with
    a_j = sum_{k>=j} b_k C(k, j) (-centre)^(k-j) / scale^k.
    """
    from math import comb

    J = np.zeros((degree + 1, degree + 1))
    for k in range(degree + 1):
        for j in range(k + 1):
            J[j, k] = comb(k, j) * (-centre) ** (k - j) / scale**k
    return J


@dataclass
class LowessFit:
    """Result of :func:`lowess`.

    ``x`` and ``y_hat`` are sorted by ``x`` (LOWESS is evaluated in x order).
    """

    x: np.ndarray
    y_hat: FloatArray
    frac: float
    iterations: int


def lowess(x: ArrayLike, y: ArrayLike, frac: float = 0.3, iterations: int = 3, delta: float = 0.0) -> LowessFit:
    """Locally weighted scatterplot smoothing (Cleveland 1979).

    Parameters
    ----------
    x, y:
        Samples; ``x`` may be datetime-like.
    frac:
        Fraction of points used for each local fit (the smoothing span).
    iterations:
        Number of robustifying iterations (0 = plain local linear regression).
    delta:
        Points closer than ``delta`` (in x units) to the last evaluated point
        reuse a linear interpolation instead of a fresh local fit, which speeds
        up large inputs. ``0`` disables this.

    Returns
    -------
    LowessFit
        Sorted ``x`` and the smoothed values.
    """
    frac = require_in_unit_interval(frac, "frac", inclusive=False)
    if iterations < 0:
        raise ValueError("iterations must be >= 0")
    require_same_length(x, y, names=("x", "y"))
    x_disp = _x_display(x)
    xf = as_float_array(x, "x")
    yf = as_float_array(y, "y")
    keep = ~(np.isnan(xf) | np.isnan(yf))
    xf, yf, x_disp = xf[keep], yf[keep], x_disp[keep]
    order = np.argsort(xf, kind="stable")
    xf, yf, x_disp = xf[order], yf[order], x_disp[order]
    n = xf.size
    if n < 3:
        raise ValueError("lowess needs at least 3 finite observations")
    k = max(int(np.ceil(frac * n)), 2)
    x_span = xf.max() - xf.min() or 1.0
    delta_scaled = delta * (x_span if xf.max() - xf.min() == 0 else 1.0)

    robust = np.ones(n)
    y_hat = np.empty(n)
    for _ in range(iterations + 1):
        last_i = -1
        last_x = -np.inf
        for i in range(n):
            if delta_scaled > 0 and i > 0 and xf[i] - last_x < delta_scaled and i < n - 1:
                continue
            y_hat[i] = _local_fit(xf, yf, robust, i, k)
            if delta_scaled > 0:
                if last_i >= 0 and i - last_i > 1:
                    y_hat[last_i + 1 : i] = np.interp(
                        xf[last_i + 1 : i], [xf[last_i], xf[i]], [y_hat[last_i], y_hat[i]]
                    )
                last_i, last_x = i, xf[i]
        resid = yf - y_hat
        mad = np.median(np.abs(resid))
        if mad <= 0:
            break
        u = resid / (6.0 * mad)
        robust = np.where(np.abs(u) < 1, (1 - u**2) ** 2, 0.0)
    return LowessFit(x=x_disp, y_hat=y_hat, frac=frac, iterations=iterations)


def _local_fit(xf: FloatArray, yf: FloatArray, robust: FloatArray, i: int, k: int) -> float:
    dist = np.abs(xf - xf[i])
    h = np.partition(dist, k - 1)[k - 1]
    if h <= 0:
        return float(np.average(yf[dist == 0], weights=robust[dist == 0]) if robust[dist == 0].sum() else yf[i])
    w = np.clip(dist / h, 0.0, 1.0)
    w = (1 - w**3) ** 3 * robust
    sw = w.sum()
    if sw <= 0:
        return float(yf[i])
    xw = (w * xf).sum() / sw
    yw = (w * yf).sum() / sw
    var = (w * (xf - xw) ** 2).sum()
    if var <= 1e-12 * max(h**2, 1.0):
        return float(yw)
    slope = (w * (xf - xw) * (yf - yw)).sum() / var
    return float(yw + slope * (xf[i] - xw))
