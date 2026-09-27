"""Rolling and smoothing estimators for ordered series.

All functions accept any 1-D array-like ``y`` and return arrays aligned to
the input (leading positions that cannot be estimated are ``NaN``).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np
import pandas as pd
from scipy.signal import savgol_filter

from plotlyvizpro._typing import ArrayLike, FloatArray
from plotlyvizpro._validation import as_float_array, require_positive_int

RollingStat = Literal["mean", "median", "std", "min", "max", "sum"]


def rolling(
    y: ArrayLike, window: int, stat: RollingStat = "mean", *, center: bool = False, min_periods: int | None = None
) -> FloatArray:
    """Compute a rolling statistic over a fixed window.

    Parameters
    ----------
    y:
        Ordered observations.
    window:
        Window length in observations.
    stat:
        One of ``mean``, ``median``, ``std`` (ddof=1), ``min``, ``max``, ``sum``.
    center:
        Whether the window is centred on each point (introduces look-ahead).
    min_periods:
        Minimum observations required to emit a value; defaults to ``window``.
    """
    window = require_positive_int(window, "window")
    series = pd.Series(as_float_array(y, "y"))
    roll = series.rolling(window=window, center=center, min_periods=min_periods)
    if stat not in {"mean", "median", "std", "min", "max", "sum"}:
        raise ValueError(f"Unknown stat {stat!r}")
    return getattr(roll, stat)().to_numpy(dtype=np.float64)


def ewma(
    y: ArrayLike, span: float | None = None, *, halflife: float | None = None, alpha: float | None = None
) -> FloatArray:
    """Exponentially weighted moving average.

    Exactly one of ``span``, ``halflife`` or ``alpha`` must be given.
    """
    given = [v is not None for v in (span, halflife, alpha)]
    if sum(given) != 1:
        raise ValueError("Specify exactly one of span, halflife or alpha")
    series = pd.Series(as_float_array(y, "y"))
    return series.ewm(span=span, halflife=halflife, alpha=alpha, adjust=True).mean().to_numpy(dtype=np.float64)


@dataclass
class Bands:
    """A centre line with symmetric (or asymmetric) bands around it."""

    centre: FloatArray
    lower: FloatArray
    upper: FloatArray
    label: str


def bollinger_bands(y: ArrayLike, window: int = 20, n_std: float = 2.0) -> Bands:
    """Bollinger bands: rolling mean +/- ``n_std`` rolling standard deviations."""
    if n_std <= 0:
        raise ValueError("n_std must be positive")
    centre = rolling(y, window, "mean")
    sd = rolling(y, window, "std")
    return Bands(
        centre=centre, lower=centre - n_std * sd, upper=centre + n_std * sd, label=f"Bollinger ({window}, {n_std:g}σ)"
    )


def zscore_bands(y: ArrayLike, z: float = 2.0, *, robust: bool = False) -> Bands:
    """Global bands at mean +/- ``z`` standard deviations.

    With ``robust=True`` the centre is the median and the scale is
    ``1.4826 * MAD`` (consistent with the standard deviation under normality).
    """
    if z <= 0:
        raise ValueError("z must be positive")
    arr = as_float_array(y, "y")
    arr = arr[~np.isnan(arr)]
    if arr.size < 2:
        raise ValueError("Need at least two finite observations")
    if robust:
        centre = float(np.median(arr))
        scale = 1.4826 * float(np.median(np.abs(arr - centre)))
    else:
        centre = float(arr.mean())
        scale = float(arr.std(ddof=1))
    n = len(as_float_array(y, "y"))
    return Bands(
        centre=np.full(n, centre),
        lower=np.full(n, centre - z * scale),
        upper=np.full(n, centre + z * scale),
        label=f"{'median' if robust else 'mean'} ± {z:g}{'·MAD' if robust else 'σ'}",
    )


def savitzky_golay(y: ArrayLike, window: int = 11, polyorder: int = 3) -> FloatArray:
    """Savitzky-Golay smoothing (least-squares polynomial over a sliding window).

    ``window`` must be odd and larger than ``polyorder``.
    """
    window = require_positive_int(window, "window", minimum=3)
    if window % 2 == 0:
        raise ValueError("window must be odd")
    if polyorder >= window:
        raise ValueError("polyorder must be smaller than window")
    arr = as_float_array(y, "y")
    if np.isnan(arr).any():
        raise ValueError("savitzky_golay does not accept NaN values; interpolate first")
    return np.asarray(savgol_filter(arr, window, polyorder), dtype=np.float64)
