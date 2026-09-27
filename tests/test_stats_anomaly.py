"""Anomaly detectors."""

from __future__ import annotations

import numpy as np
import pytest

from plotlyvizpro.stats import generalized_esd, hampel_filter, iqr_outliers, zscore_outliers


@pytest.fixture
def spiked():
    rs = np.random.default_rng(8)
    y = rs.normal(0, 1, 300)
    y[[50, 150, 250]] = [12, -11, 13]
    return y


def test_zscore_flags_spikes(spiked):
    res = zscore_outliers(spiked, threshold=3)
    assert set(res.indices) == {50, 150, 250}
    assert res.n_anomalies == 3
    assert "z-score" in res.method


def test_robust_zscore_resists_masking():
    y = np.array([0.0] * 20 + [100.0] * 5)
    plain = zscore_outliers(y, threshold=2)
    robust = zscore_outliers(y, threshold=2, robust=True)
    assert plain.n_anomalies <= robust.n_anomalies
    assert robust.n_anomalies == 5


def test_iqr_fences(spiked):
    res = iqr_outliers(spiked, k=3)
    assert {50, 150, 250} <= set(res.indices)
    assert np.all(res.score[res.mask] > 0)
    with pytest.raises(ValueError, match="k must"):
        iqr_outliers(spiked, k=0)


def test_hampel_local_detection_on_trend():
    x = np.linspace(0, 50, 200)
    y = x.copy()  # strong trend: global z-score would miss local spikes
    y[100] += 4
    hampel = hampel_filter(y, window=5, n_sigmas=3)
    assert 100 in hampel.indices
    assert zscore_outliers(y, 3).n_anomalies == 0


def test_hampel_nan_handling():
    y = np.array([1, 2, np.nan, 100, 2, 1, 2.0])
    res = hampel_filter(y, window=2, n_sigmas=2)
    assert 3 in res.indices
    assert not res.mask[2]


def test_generalized_esd_matches_nist_example():
    # NIST/SEMATECH e-Handbook 1.3.5.17.3: 3 outliers at alpha=0.05.
    y = np.array(
        [
            -0.25,
            0.68,
            0.94,
            1.15,
            1.20,
            1.26,
            1.26,
            1.34,
            1.38,
            1.43,
            1.49,
            1.49,
            1.55,
            1.56,
            1.58,
            1.65,
            1.69,
            1.70,
            1.76,
            1.77,
            1.81,
            1.91,
            1.94,
            1.96,
            1.99,
            2.06,
            2.09,
            2.10,
            2.14,
            2.15,
            2.23,
            2.24,
            2.26,
            2.35,
            2.37,
            2.40,
            2.47,
            2.54,
            2.62,
            2.64,
            2.90,
            2.92,
            2.92,
            2.93,
            3.21,
            3.26,
            3.30,
            3.59,
            3.68,
            4.30,
            4.64,
            5.34,
            5.42,
            6.01,
        ]
    )
    res = generalized_esd(y, max_outliers=10, alpha=0.05)
    assert res.n_anomalies == 3
    assert set(y[res.mask]) == {6.01, 5.42, 5.34}


def test_esd_no_outliers_in_clean_data():
    rs = np.random.default_rng(0)
    res = generalized_esd(rs.normal(size=100), max_outliers=5, alpha=0.01)
    assert res.n_anomalies <= 1


def test_esd_errors():
    with pytest.raises(ValueError, match="at least"):
        generalized_esd([1, 2, 3], max_outliers=5)
    with pytest.raises(ValueError, match="alpha"):
        generalized_esd(np.arange(20.0), alpha=1.5)


def test_common_errors():
    with pytest.raises(ValueError, match="threshold"):
        zscore_outliers([1, 2, 3], threshold=0)
    with pytest.raises(ValueError, match="four finite"):
        iqr_outliers([1, 2, 3])
    with pytest.raises(ValueError, match="n_sigmas"):
        hampel_filter([1, 2, 3], n_sigmas=0)
