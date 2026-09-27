"""Statistical estimators with no plotting dependency.

Each function returns a small dataclass holding arrays and fitted quantities;
:mod:`plotlyvizpro.overlays` turns those into traces. Keeping the estimators
separate makes them unit-testable against closed-form results and reference
implementations (SciPy, statsmodels).
"""

from __future__ import annotations

from plotlyvizpro.stats.anomaly import (
    AnomalyResult,
    generalized_esd,
    hampel_filter,
    iqr_outliers,
    zscore_outliers,
)
from plotlyvizpro.stats.bootstrap import BootstrapResult, bootstrap_ci, bootstrap_groups
from plotlyvizpro.stats.decomposition import Decomposition, autocorrelation, seasonal_decompose
from plotlyvizpro.stats.distributions import (
    ECDFResult,
    KDEResult,
    QQResult,
    describe,
    ecdf,
    histogram_bins,
    kde,
    qq_points,
)
from plotlyvizpro.stats.regression import LowessFit, OLSFit, lowess, ols_fit
from plotlyvizpro.stats.smoothing import (
    Bands,
    bollinger_bands,
    ewma,
    rolling,
    savitzky_golay,
    zscore_bands,
)

__all__ = [
    "AnomalyResult",
    "Bands",
    "BootstrapResult",
    "Decomposition",
    "ECDFResult",
    "KDEResult",
    "LowessFit",
    "OLSFit",
    "QQResult",
    "autocorrelation",
    "bollinger_bands",
    "bootstrap_ci",
    "bootstrap_groups",
    "describe",
    "ecdf",
    "ewma",
    "generalized_esd",
    "hampel_filter",
    "histogram_bins",
    "iqr_outliers",
    "kde",
    "lowess",
    "ols_fit",
    "qq_points",
    "rolling",
    "savitzky_golay",
    "seasonal_decompose",
    "zscore_bands",
    "zscore_outliers",
]
