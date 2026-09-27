"""Shared fixtures."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from plotlyvizpro.export import image_export_available


@pytest.fixture(scope="session")
def rng() -> np.random.Generator:
    return np.random.default_rng(20240926)


@pytest.fixture
def sample_df() -> pd.DataFrame:
    dates = pd.date_range("2024-01-01", periods=40, freq="D")
    rs = np.random.default_rng(7)
    return pd.DataFrame(
        {
            "Date": dates,
            "Sales": np.linspace(100, 300, 40) + rs.normal(0, 10, 40),
            "Profit": np.linspace(20, 60, 40) + rs.normal(0, 3, 40),
            "Orders": rs.integers(1, 50, 40),
            "Region": np.where(np.arange(40) % 2 == 0, "East", "West"),
            "Category": np.tile(["A", "B", "C", "D"], 10),
            "Lat": rs.uniform(-60, 60, 40),
            "Lon": rs.uniform(-150, 150, 40),
        }
    )


@pytest.fixture
def linear_xy() -> tuple[np.ndarray, np.ndarray]:
    rs = np.random.default_rng(123)
    x = np.linspace(0, 10, 200)
    y = 3.0 + 2.0 * x + rs.normal(0, 1.0, x.size)
    return x, y


requires_kaleido = pytest.mark.skipif(not image_export_available(), reason="kaleido not installed")


def has_statsmodels() -> bool:
    try:
        import statsmodels  # noqa: F401
    except ImportError:
        return False
    return True


requires_statsmodels = pytest.mark.skipif(not has_statsmodels(), reason="statsmodels not installed")
