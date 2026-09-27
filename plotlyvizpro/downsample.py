"""Downsampling for large ordered series.

Plotly renders every point it is given; beyond a few tens of thousands of
points interaction becomes sluggish and file sizes balloon. These algorithms
reduce a series to a target number of points while preserving its visual
shape:

- :func:`lttb` -- Largest-Triangle-Three-Buckets (Steinarsson 2013), the
  standard for line charts: keeps the points that maximise the area of the
  triangle formed with neighbouring buckets, so peaks and troughs survive.
- :func:`minmax` -- keeps the minimum and maximum of each bucket, guaranteeing
  that the envelope of the series is exact.
- :func:`m4` -- Jugel et al. (2014): the first, last, min and max of each
  bucket, which yields pixel-perfect line rendering at a given plot width.
- :func:`downsample` -- convenience dispatcher that is a no-op when the series
  already fits.

All functions return **indices** into the original arrays so any companion
columns (hover text, colour) can be aligned with a single fancy-index.
"""

from __future__ import annotations

import itertools
from typing import Literal

import numpy as np

from plotlyvizpro._typing import ArrayLike
from plotlyvizpro._validation import as_float_array, require_positive_int, require_same_length

Method = Literal["lttb", "minmax", "m4"]


def _prepare(x: ArrayLike, y: ArrayLike, threshold: int, minimum: int) -> tuple[np.ndarray, np.ndarray, int]:
    threshold = require_positive_int(threshold, "threshold", minimum=minimum)
    require_same_length(x, y, names=("x", "y"))
    xf = as_float_array(x, "x")
    yf = as_float_array(y, "y")
    if np.any(np.diff(xf) < 0):
        raise ValueError("x must be sorted in non-decreasing order")
    return xf, yf, threshold


def lttb(x: ArrayLike, y: ArrayLike, threshold: int) -> np.ndarray:
    """Largest-Triangle-Three-Buckets: indices of ``threshold`` representative points.

    The first and last points are always kept. When ``threshold >= len(x)``
    all indices are returned.

    Complexity is O(n) with a fully vectorised inner loop per bucket.
    """
    xf, yf, threshold = _prepare(x, y, threshold, minimum=3)
    n = xf.size
    if threshold >= n:
        return np.arange(n)
    # Bucket boundaries for the n-2 interior points.
    edges = np.linspace(1, n - 1, threshold - 1).astype(np.int64)
    edges[-1] = n - 1
    out = np.empty(threshold, dtype=np.int64)
    out[0] = 0
    a = 0
    for i in range(threshold - 2):
        lo, hi = edges[i], edges[i + 1]
        nlo, nhi = edges[i + 1], edges[i + 2] if i + 2 < edges.size else n
        # Average point of the *next* bucket.
        avg_x = xf[nlo:nhi].mean()
        avg_y = yf[nlo:nhi].mean()
        xs = xf[lo:hi]
        ys = yf[lo:hi]
        area = np.abs((xf[a] - avg_x) * (ys - yf[a]) - (xf[a] - xs) * (avg_y - yf[a]))
        a = lo + int(np.argmax(area))
        out[i + 1] = a
    out[-1] = n - 1
    return out


def _buckets(n: int, n_buckets: int) -> np.ndarray:
    return np.linspace(0, n, n_buckets + 1).astype(np.int64)


def minmax(x: ArrayLike, y: ArrayLike, threshold: int) -> np.ndarray:
    """Per-bucket minimum and maximum: at most ``threshold`` indices, sorted.

    ``threshold`` is rounded down to an even number of points (two per bucket).
    """
    xf, yf, threshold = _prepare(x, y, threshold, minimum=2)
    n = xf.size
    if threshold >= n:
        return np.arange(n)
    edges = _buckets(n, threshold // 2)
    idx: list[int] = []
    for lo, hi in itertools.pairwise(edges):
        if hi <= lo:
            continue
        seg = yf[lo:hi]
        idx.append(lo + int(np.nanargmin(seg)))
        idx.append(lo + int(np.nanargmax(seg)))
    return np.unique(np.array(idx, dtype=np.int64))


def m4(x: ArrayLike, y: ArrayLike, width_px: int) -> np.ndarray:
    """M4 aggregation: first, last, min and max of each of ``width_px`` pixel columns.

    Rendering the returned points with a line trace reproduces the same pixels as
    rendering the full series at that width (Jugel, Fischer, Thomsen & Wallace 2014).
    """
    xf, yf, width_px = _prepare(x, y, width_px, minimum=1)
    n = xf.size
    if 4 * width_px >= n:
        return np.arange(n)
    # Columns by x range (not by count) so gaps in x are respected.
    span = xf[-1] - xf[0]
    if span <= 0:
        return np.array([0, n - 1])
    col = np.minimum(((xf - xf[0]) / span * width_px).astype(np.int64), width_px - 1)
    idx: list[int] = []
    starts = np.flatnonzero(np.diff(col, prepend=-1))
    ends = np.append(starts[1:], n)
    for lo, hi in zip(starts, ends, strict=True):
        seg = yf[lo:hi]
        idx.extend([int(lo), int(hi) - 1, int(lo) + int(np.nanargmin(seg)), int(lo) + int(np.nanargmax(seg))])
    return np.unique(np.array(idx, dtype=np.int64))


def downsample(x: ArrayLike, y: ArrayLike, threshold: int = 5000, method: Method = "lttb") -> np.ndarray:
    """Return indices that reduce ``(x, y)`` to about ``threshold`` points.

    A no-op (all indices) when the series already has at most ``threshold``
    points. For ``"m4"`` the threshold is interpreted as ``4 * width_px``.
    """
    if method == "lttb":
        return lttb(x, y, threshold)
    if method == "minmax":
        return minmax(x, y, threshold)
    if method == "m4":
        return m4(x, y, max(1, threshold // 4))
    raise ValueError(f"Unknown method {method!r}; choose from ('lttb', 'minmax', 'm4')")


def max_error(x: ArrayLike, y: ArrayLike, keep: np.ndarray) -> float:
    """Largest absolute vertical gap between the series and its downsampled linear interpolant.

    Useful for reporting how much shape a given threshold sacrificed.
    """
    xf = as_float_array(x, "x")
    yf = as_float_array(y, "y")
    keep = np.asarray(keep, dtype=np.int64)
    interp = np.interp(xf, xf[keep], yf[keep])
    return float(np.nanmax(np.abs(yf - interp)))
