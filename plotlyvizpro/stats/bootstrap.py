"""Non-parametric bootstrap confidence intervals.

Implements the percentile, basic (reverse-percentile) and bias-corrected and
accelerated (BCa) intervals of Efron & Tibshirani (1993), *An Introduction to
the Bootstrap*, chapters 13-14. BCa is the default because it is second-order
accurate and transformation-respecting.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Literal

import numpy as np
from scipy import stats as sps

from plotlyvizpro._typing import ArrayLike, FloatArray
from plotlyvizpro._validation import as_float_array, require_in_unit_interval, require_positive_int

Method = Literal["percentile", "basic", "bca"]
Statistic = Callable[[FloatArray], float]


@dataclass
class BootstrapResult:
    """Point estimate, interval and the bootstrap distribution."""

    estimate: float
    lower: float
    upper: float
    confidence: float
    method: str
    n_resamples: int
    distribution: FloatArray

    @property
    def half_width(self) -> float:
        """Half the interval width (useful for symmetric error bars)."""
        return (self.upper - self.lower) / 2


def bootstrap_ci(
    data: ArrayLike,
    statistic: Statistic = np.mean,
    *,
    confidence: float = 0.95,
    n_resamples: int = 2000,
    method: Method = "bca",
    seed: int | np.random.Generator | None = None,
) -> BootstrapResult:
    """Bootstrap confidence interval for a one-sample statistic.

    Parameters
    ----------
    data:
        Observations (NaN dropped).
    statistic:
        Function mapping a 1-D array to a scalar.
    confidence:
        Two-sided confidence level.
    n_resamples:
        Number of bootstrap replicates.
    method:
        ``"percentile"``, ``"basic"`` or ``"bca"``.
    seed:
        Seed or Generator for reproducibility.
    """
    confidence = require_in_unit_interval(confidence, "confidence")
    n_resamples = require_positive_int(n_resamples, "n_resamples", minimum=100)
    x = as_float_array(data, "data")
    x = x[~np.isnan(x)]
    n = x.size
    if n < 2:
        raise ValueError("bootstrap_ci needs at least two finite observations")
    rng = np.random.default_rng(seed)
    theta = float(statistic(x))
    idx = rng.integers(0, n, size=(n_resamples, n))
    boots = np.array([statistic(x[row]) for row in idx], dtype=np.float64)
    alpha = 1 - confidence

    if method == "percentile":
        lo, hi = np.quantile(boots, [alpha / 2, 1 - alpha / 2])
    elif method == "basic":
        q_lo, q_hi = np.quantile(boots, [alpha / 2, 1 - alpha / 2])
        lo, hi = 2 * theta - q_hi, 2 * theta - q_lo
    elif method == "bca":
        lo, hi = _bca(x, boots, theta, statistic, alpha)
    else:
        raise ValueError(f"Unknown method {method!r}")
    return BootstrapResult(theta, float(lo), float(hi), confidence, method, n_resamples, boots)


def _bca(x: FloatArray, boots: FloatArray, theta: float, statistic: Statistic, alpha: float) -> tuple[float, float]:
    n = x.size
    prop = np.mean(boots < theta)
    if prop in (0.0, 1.0):  # degenerate: all replicates on one side
        lo_q, hi_q = np.quantile(boots, [alpha / 2, 1 - alpha / 2])
        return float(lo_q), float(hi_q)
    z0 = sps.norm.ppf(prop)
    # Jackknife for the acceleration constant.
    jack = np.array([statistic(np.delete(x, i)) for i in range(n)], dtype=np.float64)
    jm = jack.mean()
    num = ((jm - jack) ** 3).sum()
    den = 6.0 * (((jm - jack) ** 2).sum()) ** 1.5
    a = num / den if den > 0 else 0.0
    z_lo, z_hi = sps.norm.ppf(alpha / 2), sps.norm.ppf(1 - alpha / 2)
    a_lo = sps.norm.cdf(z0 + (z0 + z_lo) / (1 - a * (z0 + z_lo)))
    a_hi = sps.norm.cdf(z0 + (z0 + z_hi) / (1 - a * (z0 + z_hi)))
    lo, hi = np.quantile(boots, [a_lo, a_hi])
    return float(lo), float(hi)


def bootstrap_groups(
    values: ArrayLike,
    groups: ArrayLike,
    statistic: Statistic = np.mean,
    **kwargs: object,
) -> dict[str, BootstrapResult]:
    """Bootstrap a statistic independently within each group label.

    Returns a mapping ``group -> BootstrapResult`` ordered by first appearance.
    """
    v = as_float_array(values, "values")
    g = np.asarray(groups)
    if v.size != g.size:
        raise ValueError("values and groups must have the same length")
    out: dict[str, BootstrapResult] = {}
    for label in dict.fromkeys(g.tolist()):
        out[str(label)] = bootstrap_ci(v[g == label], statistic, **kwargs)  # type: ignore[arg-type]
    return out
