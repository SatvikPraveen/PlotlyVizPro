"""Outlier and anomaly detection for 1-D series.

Three detectors with different assumptions:

- :func:`zscore_outliers` -- global Gaussian assumption (or robust MAD variant).
- :func:`iqr_outliers` -- Tukey's fences, distribution-free.
- :func:`hampel_filter` -- rolling median / MAD, for time series with drift.
- :func:`generalized_esd` -- Rosner's (1983) test for up to ``max_outliers``
  outliers with a controlled false-positive rate.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy import stats as sps

from plotlyvizpro._typing import ArrayLike, FloatArray
from plotlyvizpro._validation import as_float_array, require_in_unit_interval, require_positive_int

MAD_SCALE = 1.4826  # makes MAD consistent with sigma under normality


@dataclass
class AnomalyResult:
    """Boolean mask plus per-point score and the thresholds used."""

    mask: np.ndarray
    score: FloatArray
    lower: FloatArray
    upper: FloatArray
    method: str

    @property
    def indices(self) -> np.ndarray:
        """Positions flagged as anomalous."""
        return np.flatnonzero(self.mask)

    @property
    def n_anomalies(self) -> int:
        """Number of flagged points."""
        return int(self.mask.sum())


def zscore_outliers(y: ArrayLike, threshold: float = 3.0, *, robust: bool = False) -> AnomalyResult:
    """Flag |z| > ``threshold`` using the mean/SD or median/MAD."""
    if threshold <= 0:
        raise ValueError("threshold must be positive")
    arr = as_float_array(y, "y")
    finite = arr[~np.isnan(arr)]
    if finite.size < 2:
        raise ValueError("Need at least two finite observations")
    if robust:
        centre = float(np.median(finite))
        scale = MAD_SCALE * float(np.median(np.abs(finite - centre)))
    else:
        centre = float(finite.mean())
        scale = float(finite.std(ddof=1))
    scale = scale or np.finfo(float).eps
    score = (arr - centre) / scale
    mask = np.abs(score) > threshold
    mask &= ~np.isnan(arr)
    n = arr.size
    return AnomalyResult(
        mask,
        score,
        np.full(n, centre - threshold * scale),
        np.full(n, centre + threshold * scale),
        f"{'robust ' if robust else ''}z-score > {threshold:g}",
    )


def iqr_outliers(y: ArrayLike, k: float = 1.5) -> AnomalyResult:
    """Tukey's fences: outside ``[Q1 - k*IQR, Q3 + k*IQR]``."""
    if k <= 0:
        raise ValueError("k must be positive")
    arr = as_float_array(y, "y")
    finite = arr[~np.isnan(arr)]
    if finite.size < 4:
        raise ValueError("Need at least four finite observations")
    q1, q3 = np.percentile(finite, [25, 75])
    iqr = q3 - q1
    lo, hi = q1 - k * iqr, q3 + k * iqr
    score = np.where(arr < lo, (lo - arr) / (iqr or 1), np.where(arr > hi, (arr - hi) / (iqr or 1), 0.0))
    mask = ((arr < lo) | (arr > hi)) & ~np.isnan(arr)
    n = arr.size
    return AnomalyResult(mask, score, np.full(n, lo), np.full(n, hi), f"IQR fences (k={k:g})")


def hampel_filter(y: ArrayLike, window: int = 7, n_sigmas: float = 3.0) -> AnomalyResult:
    """Flag points where |y - rolling median| > n_sigmas * 1.4826 * rolling MAD (Hampel identifier).

    ``window`` is the half-width; each point is compared with the ``2*window+1``
    neighbours centred on it (edges use the available neighbours).
    """
    window = require_positive_int(window, "window")
    if n_sigmas <= 0:
        raise ValueError("n_sigmas must be positive")
    arr = as_float_array(y, "y")
    n = arr.size
    med = np.empty(n)
    mad = np.empty(n)
    for i in range(n):
        lo, hi = max(0, i - window), min(n, i + window + 1)
        seg = arr[lo:hi]
        seg = seg[~np.isnan(seg)]
        if seg.size == 0:
            med[i], mad[i] = np.nan, np.nan
            continue
        med[i] = np.median(seg)
        mad[i] = MAD_SCALE * np.median(np.abs(seg - med[i]))
    with np.errstate(invalid="ignore", divide="ignore"):
        score = np.abs(arr - med) / np.where(mad > 0, mad, np.nan)
    mask = np.nan_to_num(score, nan=0.0) > n_sigmas
    return AnomalyResult(mask, score, med - n_sigmas * mad, med + n_sigmas * mad, f"Hampel (w={window}, {n_sigmas:g}σ)")


def generalized_esd(y: ArrayLike, max_outliers: int = 10, alpha: float = 0.05) -> AnomalyResult:
    r"""Apply Rosner's generalized extreme Studentized deviate test.

    Iteratively removes the most extreme point and compares its Studentized
    deviation with the critical value

    .. math:: \\lambda_i = \\frac{(n-i)\\, t_{p,\\,n-i-1}}{\\sqrt{(n-i-1+t^2_{p,\\,n-i-1})(n-i+1)}},
              \\quad p = 1 - \\frac{\\alpha}{2(n-i+1)}

    The number of outliers is the largest ``i`` for which the statistic
    exceeds its critical value (Rosner 1983; NIST/SEMATECH e-Handbook 1.3.5.17.3).
    """
    max_outliers = require_positive_int(max_outliers, "max_outliers")
    alpha = require_in_unit_interval(alpha, "alpha")
    arr = as_float_array(y, "y")
    finite_idx = np.flatnonzero(~np.isnan(arr))
    x = arr[finite_idx]
    n = x.size
    if n < max_outliers + 3:
        raise ValueError(f"Need at least max_outliers + 3 = {max_outliers + 3} observations, got {n}")
    remaining = np.arange(n)
    removed: list[int] = []
    n_out = 0
    for i in range(1, max_outliers + 1):
        sub = x[remaining]
        mu, sd = sub.mean(), sub.std(ddof=1)
        if sd == 0:
            break
        dev = np.abs(sub - mu) / sd
        j = int(np.argmax(dev))
        r_i = float(dev[j])
        m = n - i + 1  # sample size at this step
        p = 1 - alpha / (2 * m)
        t = sps.t.ppf(p, m - 2)
        lam = (m - 1) * t / np.sqrt((m - 2 + t**2) * m)
        removed.append(int(remaining[j]))
        remaining = np.delete(remaining, j)
        if r_i > lam:
            n_out = i
    mask = np.zeros(arr.size, dtype=bool)
    mask[finite_idx[removed[:n_out]]] = True
    mu, sd = x.mean(), x.std(ddof=1)
    score = (arr - mu) / (sd or np.finfo(float).eps)
    return AnomalyResult(
        mask, score, np.full(arr.size, np.nan), np.full(arr.size, np.nan), f"generalized ESD (α={alpha:g})"
    )
