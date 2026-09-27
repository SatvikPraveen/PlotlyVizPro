"""Input validation helpers shared across modules.

These helpers turn silent Plotly / pandas failures into early, explicit
``ValueError`` / ``TypeError`` exceptions with actionable messages.
"""

from __future__ import annotations

from collections.abc import Iterable

import numpy as np
import pandas as pd

from plotlyvizpro._typing import ArrayLike, FloatArray


def require_columns(df: pd.DataFrame, *columns: str | None) -> None:
    """Raise ``KeyError`` if any non-``None`` column name is missing from ``df``.

    Parameters
    ----------
    df:
        The data frame to check.
    *columns:
        Column names. ``None`` entries are ignored so optional encodings can be
        passed straight through.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"Expected a pandas DataFrame, got {type(df).__name__}")
    missing = [c for c in columns if c is not None and c not in df.columns]
    if missing:
        raise KeyError(f"Column(s) {missing} not found. Available: {list(df.columns)}")


def as_float_array(values: ArrayLike, name: str = "values") -> FloatArray:
    """Coerce a sequence into a contiguous 1-D ``float64`` array.

    Datetime input is converted to nanoseconds since the epoch so the result can
    be used directly in numerical routines.
    """
    if isinstance(values, pd.Series):
        if pd.api.types.is_datetime64_any_dtype(values):
            return values.to_numpy(dtype="datetime64[ns]").astype("int64").astype(np.float64)
        values = values.to_numpy()
    arr = np.asarray(values)
    if np.issubdtype(arr.dtype, np.datetime64):
        arr = arr.astype("datetime64[ns]").astype("int64")
    try:
        out = np.asarray(arr, dtype=np.float64).ravel()
    except (TypeError, ValueError) as exc:
        raise TypeError(f"{name} must be numeric or datetime-like") from exc
    return np.ascontiguousarray(out)


def require_same_length(*arrays: Iterable[object], names: tuple[str, ...] | None = None) -> None:
    """Raise ``ValueError`` when the provided arrays differ in length."""
    lengths = [len(list(a)) if not hasattr(a, "__len__") else len(a) for a in arrays]  # type: ignore[arg-type]
    if len(set(lengths)) > 1:
        labels = names or tuple(f"array{i}" for i in range(len(lengths)))
        detail = ", ".join(f"{n}={ln}" for n, ln in zip(labels, lengths, strict=True))
        raise ValueError(f"Inputs must have the same length ({detail})")


def require_positive_int(value: int, name: str, minimum: int = 1) -> int:
    """Validate that ``value`` is an integer at least ``minimum``."""
    if isinstance(value, bool) or not isinstance(value, (int, np.integer)):
        raise TypeError(f"{name} must be an integer, got {type(value).__name__}")
    if value < minimum:
        raise ValueError(f"{name} must be >= {minimum}, got {value}")
    return int(value)


def require_in_unit_interval(value: float, name: str, *, inclusive: bool = False) -> float:
    """Validate that ``value`` lies in (0, 1) (or [0, 1] when ``inclusive``)."""
    v = float(value)
    ok = 0.0 <= v <= 1.0 if inclusive else 0.0 < v < 1.0
    if not ok:
        bounds = "[0, 1]" if inclusive else "(0, 1)"
        raise ValueError(f"{name} must lie in {bounds}, got {value}")
    return v
