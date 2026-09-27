"""Classical seasonal decomposition of an evenly spaced series.

``y = trend + seasonal + residual`` (additive) or
``y = trend * seasonal * residual`` (multiplicative), following the moving-average
procedure in Hyndman & Athanasopoulos, *Forecasting: Principles and Practice*,
§3.4. The trend is a centred ``2 x m``-MA for even periods and an ``m``-MA for
odd periods; the seasonal component is the period-wise mean of the detrended
series, normalised to sum to zero (additive) or average to one (multiplicative).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np

from plotlyvizpro._typing import ArrayLike, FloatArray
from plotlyvizpro._validation import as_float_array, require_positive_int

Model = Literal["additive", "multiplicative"]


@dataclass
class Decomposition:
    """Components of a seasonal decomposition, each aligned with the input."""

    observed: FloatArray
    trend: FloatArray
    seasonal: FloatArray
    residual: FloatArray
    period: int
    model: str

    @property
    def seasonal_strength(self) -> float:
        """Strength of seasonality in [0, 1] (Wang, Smith & Hyndman 2006)."""
        return _strength(
            self.residual, self.seasonal + self.residual if self.model == "additive" else self.seasonal * self.residual
        )

    @property
    def trend_strength(self) -> float:
        """Strength of trend in [0, 1]."""
        return _strength(
            self.residual, self.trend + self.residual if self.model == "additive" else self.trend * self.residual
        )


def _strength(resid: FloatArray, combined: FloatArray) -> float:
    ok = ~(np.isnan(resid) | np.isnan(combined))
    if ok.sum() < 3:
        return float("nan")
    v_r, v_c = np.var(resid[ok]), np.var(combined[ok])
    return float(max(0.0, 1.0 - v_r / v_c)) if v_c > 0 else 0.0


def _centered_ma(y: FloatArray, period: int) -> FloatArray:
    n = y.size
    if period % 2 == 1:
        kernel = np.full(period, 1.0 / period)
    else:
        kernel = np.full(period + 1, 1.0 / period)
        kernel[0] = kernel[-1] = 0.5 / period
    half = kernel.size // 2
    out = np.full(n, np.nan)
    conv = np.convolve(y, kernel, mode="valid")
    out[half : half + conv.size] = conv
    return out


def seasonal_decompose(y: ArrayLike, period: int, model: Model = "additive") -> Decomposition:
    """Classical decomposition of an evenly spaced series.

    Parameters
    ----------
    y:
        Observations without gaps or NaNs.
    period:
        Seasonal period in observations (e.g. 12 for monthly data with a yearly cycle).
    model:
        ``"additive"`` or ``"multiplicative"`` (requires strictly positive data).
    """
    period = require_positive_int(period, "period", minimum=2)
    arr = as_float_array(y, "y")
    n = arr.size
    if np.isnan(arr).any():
        raise ValueError("seasonal_decompose does not accept NaN values")
    if n < 2 * period:
        raise ValueError(f"Need at least two full periods ({2 * period} observations), got {n}")
    if model not in {"additive", "multiplicative"}:
        raise ValueError("model must be 'additive' or 'multiplicative'")
    if model == "multiplicative" and (arr <= 0).any():
        raise ValueError("multiplicative model requires strictly positive data")

    trend = _centered_ma(arr, period)
    detrended = arr - trend if model == "additive" else arr / trend
    seasonal_means = np.array([np.nanmean(detrended[i::period]) for i in range(period)])
    seasonal_means = (
        seasonal_means - seasonal_means.mean() if model == "additive" else seasonal_means / seasonal_means.mean()
    )
    seasonal = np.resize(seasonal_means, n)
    residual = arr - trend - seasonal if model == "additive" else arr / (trend * seasonal)
    return Decomposition(arr, trend, seasonal, residual, period, model)


def autocorrelation(y: ArrayLike, max_lag: int = 40) -> tuple[FloatArray, float]:
    """Sample autocorrelation function up to ``max_lag`` and the +/- 1.96/sqrt(n) bound."""
    max_lag = require_positive_int(max_lag, "max_lag")
    arr = as_float_array(y, "y")
    arr = arr[~np.isnan(arr)]
    n = arr.size
    if n < 3:
        raise ValueError("Need at least three finite observations")
    max_lag = min(max_lag, n - 1)
    x = arr - arr.mean()
    denom = float(x @ x)
    acf = np.array([1.0] + [float(x[:-k] @ x[k:]) / denom for k in range(1, max_lag + 1)])
    return acf, 1.96 / np.sqrt(n)
