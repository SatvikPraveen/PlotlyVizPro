"""Rolling/EWMA/Bollinger/Savitzky-Golay."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from plotlyvizpro.stats import bollinger_bands, ewma, rolling, savitzky_golay, zscore_bands


def test_rolling_mean_matches_pandas():
    y = np.arange(10, dtype=float)
    out = rolling(y, 3)
    assert np.isnan(out[:2]).all()
    np.testing.assert_allclose(out[2:], pd.Series(y).rolling(3).mean().to_numpy()[2:])


@pytest.mark.parametrize("stat", ["mean", "median", "std", "min", "max", "sum"])
def test_rolling_stats_shape(stat):
    out = rolling(np.random.default_rng(0).normal(size=50), 5, stat, center=True, min_periods=1)
    assert out.shape == (50,)
    assert not np.isnan(out).any()


def test_rolling_bad_args():
    with pytest.raises(ValueError, match="window"):
        rolling([1, 2, 3], 0)
    with pytest.raises(ValueError, match="Unknown stat"):
        rolling([1, 2, 3], 2, "mode")  # type: ignore[arg-type]


def test_ewma_requires_exactly_one_parameter():
    with pytest.raises(ValueError, match="exactly one"):
        ewma([1, 2, 3])
    with pytest.raises(ValueError, match="exactly one"):
        ewma([1, 2, 3], span=2, alpha=0.5)
    out = ewma([1.0, 2.0, 3.0], alpha=0.5)
    np.testing.assert_allclose(out, pd.Series([1.0, 2.0, 3.0]).ewm(alpha=0.5).mean())


def test_bollinger_band_geometry():
    rs = np.random.default_rng(2)
    y = rs.normal(size=200)
    bands = bollinger_bands(y, window=20, n_std=2)
    ok = ~np.isnan(bands.centre)
    assert np.all(bands.upper[ok] >= bands.centre[ok])
    assert np.all(bands.lower[ok] <= bands.centre[ok])
    assert "Bollinger" in bands.label
    with pytest.raises(ValueError, match="n_std"):
        bollinger_bands(y, n_std=0)


def test_zscore_bands_plain_and_robust():
    y = np.array([1, 2, 3, 4, 100.0])
    plain = zscore_bands(y, z=1)
    robust = zscore_bands(y, z=1, robust=True)
    assert plain.centre[0] == pytest.approx(22.0)
    assert robust.centre[0] == pytest.approx(3.0)
    assert robust.upper[0] - robust.lower[0] < plain.upper[0] - plain.lower[0]
    with pytest.raises(ValueError, match="z must"):
        zscore_bands(y, z=-1)
    with pytest.raises(ValueError, match="two finite"):
        zscore_bands([1.0])


def test_savitzky_golay_preserves_polynomial():
    x = np.linspace(0, 1, 51)
    y = 3 * x**2 - x + 0.5
    np.testing.assert_allclose(savitzky_golay(y, window=7, polyorder=2), y, atol=1e-10)
    with pytest.raises(ValueError, match="odd"):
        savitzky_golay(y, window=6)
    with pytest.raises(ValueError, match="polyorder"):
        savitzky_golay(y, window=5, polyorder=5)
    with pytest.raises(ValueError, match="NaN"):
        savitzky_golay(np.array([1, np.nan, 3, 4, 5.0]), window=3, polyorder=1)
