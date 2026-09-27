"""Seasonal decomposition and autocorrelation."""

from __future__ import annotations

import numpy as np
import pytest

from plotlyvizpro.stats import autocorrelation, seasonal_decompose
from tests.conftest import requires_statsmodels


def _seasonal_series(n=120, period=12, model="additive"):
    t = np.arange(n)
    season = 3 * np.sin(2 * np.pi * t / period)
    trend = 0.1 * t + 10
    if model == "additive":
        return trend + season
    return trend * (1 + 0.2 * np.sin(2 * np.pi * t / period))


def test_additive_components_recover_signal():
    y = _seasonal_series()
    res = seasonal_decompose(y, period=12)
    ok = ~np.isnan(res.trend)
    np.testing.assert_allclose(res.trend[ok], 0.1 * np.arange(120)[ok] + 10, atol=1e-6)
    assert res.seasonal[:12].sum() == pytest.approx(0.0, abs=1e-9)
    assert np.nanmax(np.abs(res.residual)) < 1e-6
    assert res.seasonal_strength > 0.99
    assert res.trend_strength > 0.99


def test_multiplicative_components():
    y = _seasonal_series(model="multiplicative")
    res = seasonal_decompose(y, period=12, model="multiplicative")
    assert res.seasonal[:12].mean() == pytest.approx(1.0)
    assert np.nanmax(np.abs(res.residual - 1)) < 0.05


@requires_statsmodels
@pytest.mark.statsmodels
@pytest.mark.parametrize(("period", "model"), [(12, "additive"), (7, "additive"), (12, "multiplicative")])
def test_matches_statsmodels(period, model):
    from statsmodels.tsa.seasonal import seasonal_decompose as sm_decompose

    rs = np.random.default_rng(0)
    y = _seasonal_series(150, period, model) + rs.normal(0, 0.1, 150) * (1 if model == "additive" else 0)
    if model == "multiplicative":
        y = np.abs(y) + 1
    ours = seasonal_decompose(y, period=period, model=model)
    ref = sm_decompose(y, model=model, period=period)
    np.testing.assert_allclose(ours.trend, ref.trend, rtol=1e-8, equal_nan=True)
    np.testing.assert_allclose(ours.seasonal, ref.seasonal, rtol=1e-6, atol=1e-8)
    np.testing.assert_allclose(ours.residual, ref.resid, rtol=1e-6, atol=1e-8, equal_nan=True)


def test_odd_period_centred_ma():
    y = np.arange(30, dtype=float)
    res = seasonal_decompose(y, period=5)
    assert np.isnan(res.trend[:2]).all()
    assert np.isnan(res.trend[-2:]).all()
    np.testing.assert_allclose(res.trend[2:-2], y[2:-2])


def test_errors():
    with pytest.raises(ValueError, match="two full periods"):
        seasonal_decompose(np.arange(10.0), period=12)
    with pytest.raises(ValueError, match="NaN"):
        seasonal_decompose(np.array([1, np.nan] * 20), period=4)
    with pytest.raises(ValueError, match="strictly positive"):
        seasonal_decompose(np.arange(-5, 35, dtype=float), period=4, model="multiplicative")
    with pytest.raises(ValueError, match="model"):
        seasonal_decompose(np.arange(40.0), period=4, model="hybrid")  # type: ignore[arg-type]


def test_autocorrelation_of_white_noise_and_ar1():
    rs = np.random.default_rng(3)
    acf, bound = autocorrelation(rs.normal(size=2000), max_lag=10)
    assert acf[0] == 1.0
    assert np.all(np.abs(acf[1:]) < 3 * bound)
    ar = np.zeros(3000)
    for i in range(1, ar.size):
        ar[i] = 0.8 * ar[i - 1] + rs.normal()
    acf_ar, _ = autocorrelation(ar, 5)
    assert acf_ar[1] == pytest.approx(0.8, abs=0.05)
    with pytest.raises(ValueError, match="three finite"):
        autocorrelation([1, 2])
