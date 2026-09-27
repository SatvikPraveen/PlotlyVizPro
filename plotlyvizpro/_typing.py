"""Shared type aliases used across the package."""

from __future__ import annotations

from collections.abc import Sequence
from os import PathLike
from typing import Union

import numpy as np
import numpy.typing as npt
import pandas as pd

#: Anything that can be coerced to a 1-D float array (list, tuple, Series, ndarray).
ArrayLike = Union[Sequence[float], npt.NDArray[np.floating], "pd.Series[float]"]

#: A file-system path.
StrPath = str | PathLike[str]

FloatArray = npt.NDArray[np.float64]
