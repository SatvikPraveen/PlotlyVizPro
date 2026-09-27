"""Distribution summaries: kernel density, ECDF, Q-Q points, histogram bin rules."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np
from scipy import stats as sps

from plotlyvizpro._typing import ArrayLike, FloatArray
from plotlyvizpro._validation import as_float_array, require_positive_int

Bandwidth = Literal["scott", "silverman"] | float
BinRule = Literal["sturges", "scott", "fd", "rice", "sqrt", "auto"]


def _finite(y: ArrayLike, minimum: int = 2) -> FloatArray:
    arr = as_float_array(y, "y")
    arr = arr[~np.isnan(arr)]
    if arr.size < minimum:
        raise ValueError(f"Need at least {minimum} finite observations")
    return arr


@dataclass
class KDEResult:
    """Evaluated kernel density estimate."""

    x: FloatArray
    density: FloatArray
    bandwidth: float
    n: int


def kde(y: ArrayLike, bandwidth: Bandwidth = "scott", grid_size: int = 256, cut: float = 3.0) -> KDEResult:
    """Gaussian kernel density estimate on an evenly spaced grid.

    Parameters
    ----------
    bandwidth:
        ``"scott"``, ``"silverman"`` or a numeric factor multiplying the
        sample standard deviation (SciPy's ``bw_method`` semantics).
    grid_size:
        Number of evaluation points.
    cut:
        Grid extends ``cut`` bandwidths past the data range.
    """
    grid_size = require_positive_int(grid_size, "grid_size", minimum=8)
    arr = _finite(y)
    if arr.std() == 0:
        raise ValueError("kde is undefined for constant data")
    est = sps.gaussian_kde(arr, bw_method=bandwidth)
    bw = float(est.factor * arr.std(ddof=1))
    lo, hi = arr.min() - cut * bw, arr.max() + cut * bw
    grid = np.linspace(lo, hi, grid_size)
    return KDEResult(grid, np.asarray(est(grid), dtype=np.float64), bw, arr.size)


@dataclass
class ECDFResult:
    """Empirical cumulative distribution with optional DKW confidence band."""

    x: FloatArray
    cdf: FloatArray
    lower: FloatArray | None
    upper: FloatArray | None
    confidence: float | None


def ecdf(y: ArrayLike, confidence: float | None = None) -> ECDFResult:
    """Empirical CDF evaluated at the sorted sample values.

    When ``confidence`` is given, a simultaneous band is added using the
    Dvoretzky-Kiefer-Wolfowitz inequality with Massart's constant:
    ``epsilon = sqrt(ln(2/alpha) / (2n))``.
    """
    arr = np.sort(_finite(y, minimum=1))
    n = arr.size
    cdf = np.arange(1, n + 1) / n
    if confidence is None:
        return ECDFResult(arr, cdf, None, None, None)
    if not 0 < confidence < 1:
        raise ValueError("confidence must lie in (0, 1)")
    eps = np.sqrt(np.log(2 / (1 - confidence)) / (2 * n))
    return ECDFResult(arr, cdf, np.clip(cdf - eps, 0, 1), np.clip(cdf + eps, 0, 1), confidence)


@dataclass
class QQResult:
    """Theoretical vs sample quantiles plus the fitted reference line."""

    theoretical: FloatArray
    sample: FloatArray
    slope: float
    intercept: float
    r_squared: float
    dist: str


def qq_points(y: ArrayLike, dist: str = "norm", **dist_params: float) -> QQResult:
    """Quantile-quantile points against a SciPy distribution (default normal).

    The reference line is a least-squares fit of sample on theoretical
    quantiles, as in :func:`scipy.stats.probplot`.
    """
    arr = _finite(y, minimum=3)
    (theo, samp), (slope, intercept, r) = sps.probplot(
        arr, dist=dist, sparams=tuple(dist_params.values()) or (), fit=True
    )
    return QQResult(np.asarray(theo), np.asarray(samp), float(slope), float(intercept), float(r**2), dist)


def histogram_bins(y: ArrayLike, rule: BinRule = "fd") -> int:
    """Return the number of histogram bins from a named rule (via :func:`numpy.histogram_bin_edges`)."""
    arr = _finite(y)
    if rule not in {"sturges", "scott", "fd", "rice", "sqrt", "auto"}:
        raise ValueError(f"Unknown rule {rule!r}")
    return int(len(np.histogram_bin_edges(arr, bins=rule)) - 1)


def describe(y: ArrayLike) -> dict[str, float]:
    """Compact numeric summary (n, mean, sd, min, quartiles, max, skew, kurtosis)."""
    arr = _finite(y, minimum=1)
    q1, med, q3 = np.percentile(arr, [25, 50, 75])
    return {
        "n": float(arr.size),
        "mean": float(arr.mean()),
        "std": float(arr.std(ddof=1)) if arr.size > 1 else float("nan"),
        "min": float(arr.min()),
        "q1": float(q1),
        "median": float(med),
        "q3": float(q3),
        "max": float(arr.max()),
        "skew": float(sps.skew(arr, bias=False)) if arr.size > 2 else float("nan"),
        "kurtosis": float(sps.kurtosis(arr, bias=False)) if arr.size > 3 else float("nan"),
    }
