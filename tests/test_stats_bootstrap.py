"""Bootstrap intervals: reproducibility, ordering and empirical coverage."""

from __future__ import annotations

import numpy as np
import pytest

from plotlyvizpro.stats import bootstrap_ci, bootstrap_groups


@pytest.mark.parametrize("method", ["percentile", "basic", "bca"])
def test_interval_contains_estimate_and_is_reproducible(method):
    rs = np.random.default_rng(11)
    x = rs.exponential(2.0, 80)
    a = bootstrap_ci(x, np.mean, method=method, seed=1, n_resamples=500)
    b = bootstrap_ci(x, np.mean, method=method, seed=1, n_resamples=500)
    assert a.lower <= a.estimate <= a.upper
    assert (a.lower, a.upper) == (b.lower, b.upper)
    assert a.distribution.shape == (500,)
    assert a.half_width > 0


def test_bca_is_asymmetric_for_skewed_statistic():
    rs = np.random.default_rng(4)
    x = rs.lognormal(0, 1, 60)
    res = bootstrap_ci(x, np.mean, method="bca", seed=0, n_resamples=1000)
    assert (res.upper - res.estimate) > (res.estimate - res.lower)


@pytest.mark.slow
def test_empirical_coverage_close_to_nominal():
    """95% percentile CI for the mean of N(0,1), n=30: coverage should be ~0.93-0.97."""
    rs = np.random.default_rng(99)
    hits = 0
    trials = 200
    for _ in range(trials):
        x = rs.normal(size=30)
        res = bootstrap_ci(x, np.mean, method="percentile", seed=rs.integers(1 << 31), n_resamples=400)
        hits += res.lower <= 0 <= res.upper
    assert 0.90 <= hits / trials <= 0.99


def test_degenerate_data_falls_back():
    res = bootstrap_ci(np.ones(20), np.mean, method="bca", seed=0, n_resamples=200)
    assert res.lower == res.upper == 1.0


def test_errors():
    with pytest.raises(ValueError, match="two finite"):
        bootstrap_ci([1.0], np.mean)
    with pytest.raises(ValueError, match="Unknown method"):
        bootstrap_ci([1, 2, 3], np.mean, method="magic")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="n_resamples"):
        bootstrap_ci([1, 2, 3], np.mean, n_resamples=10)


def test_groups_preserve_first_appearance_order():
    values = np.array([1, 2, 3, 10, 11, 12, 5, 6, 7.0])
    groups = np.array(["b", "b", "b", "a", "a", "a", "c", "c", "c"])
    out = bootstrap_groups(values, groups, np.mean, seed=0, n_resamples=200)
    assert list(out) == ["b", "a", "c"]
    assert out["a"].estimate == pytest.approx(11.0)
    with pytest.raises(ValueError, match="same length"):
        bootstrap_groups(values, groups[:-1])
