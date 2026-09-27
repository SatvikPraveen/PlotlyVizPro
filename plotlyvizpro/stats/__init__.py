"""Statistical estimators with no plotting dependency.

Each function returns a small dataclass holding arrays and fitted quantities;
:mod:`plotlyvizpro.overlays` turns those into traces. Keeping the estimators
separate makes them unit-testable against closed-form results and reference
implementations (SciPy, statsmodels).
"""

from __future__ import annotations

from plotlyvizpro.stats.regression import (
    LowessFit,
    OLSFit,
    lowess,
    ols_fit,
)

__all__ = ["LowessFit", "OLSFit", "lowess", "ols_fit"]
