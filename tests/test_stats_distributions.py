"""KDE, ECDF, Q-Q, bin rules, describe."""

from __future__ import annotations

import numpy as np
import pytest
from scipy import stats as sps

from plotlyvizpro.stats import describe, ecdf, histogram_bins, kde, qq_points


def test_kde_integrates_to_one_and_matches_scipy():
    rs = np.random.default_rng(5)
    x = rs.normal(size=500)
    res = kde(x, grid_size=512)
    area = np.trapezoid(res.density, res.x)
    assert area == pytest.approx(1.0, abs=0.01)
    ref = sps.gaussian_kde(x)(res.x)
    np.testing.assert_allclose(res.density, ref)
    assert res.n == 500
    with pytest.raises(ValueError, match="constant"):
        kde(np.ones(10))
    assert kde(x, bandwidth=0.5).bandwidth > res.bandwidth


def test_ecdf_values_and_dkw_band():
    x = np.array([3, 1, 2.0])
    res = ecdf(x)
    np.testing.assert_array_equal(res.x, [1, 2, 3])
    np.testing.assert_allclose(res.cdf, [1 / 3, 2 / 3, 1])
    banded = ecdf(x, confidence=0.95)
    eps = np.sqrt(np.log(2 / 0.05) / 6)
    assert banded.upper is not None
    assert banded.lower is not None
    np.testing.assert_allclose(banded.upper, np.clip(banded.cdf + eps, 0, 1))
    assert banded.lower.min() >= 0
    with pytest.raises(ValueError, match="confidence"):
        ecdf(x, confidence=1.5)


def test_qq_normal_sample_is_linear():
    rs = np.random.default_rng(1)
    res = qq_points(rs.normal(5, 2, 400))
    assert res.r_squared > 0.99
    assert res.slope == pytest.approx(2, abs=0.3)
    assert res.intercept == pytest.approx(5, abs=0.3)
    assert res.dist == "norm"


@pytest.mark.parametrize("rule", ["sturges", "scott", "fd", "rice", "sqrt", "auto"])
def test_histogram_bins_rules(rule):
    n = histogram_bins(np.random.default_rng(0).normal(size=200), rule)
    assert 3 <= n <= 60


def test_histogram_bins_bad_rule():
    with pytest.raises(ValueError, match="Unknown rule"):
        histogram_bins([1, 2, 3], "guess")  # type: ignore[arg-type]


def test_describe_keys_and_values():
    d = describe([1, 2, 3, 4, 100])
    assert d["n"] == 5
    assert d["median"] == 3
    assert d["max"] == 100
    assert d["skew"] > 1
    small = describe([1.0])
    assert np.isnan(small["std"])
