"""pytest-benchmark suite for the downsampling algorithms.

Run with::

    pytest benchmarks/ --benchmark-only --benchmark-sort=mean
"""

from __future__ import annotations

import numpy as np
import pytest

from plotlyvizpro.downsample import lttb, m4, minmax
from plotlyvizpro.stats import lowess, ols_fit

N = 200_000
rng = np.random.default_rng(0)
X = np.arange(N, dtype=float)
Y = np.cumsum(rng.normal(size=N))


@pytest.mark.parametrize("threshold", [1000, 5000])
def test_bench_lttb(benchmark, threshold):
    keep = benchmark(lttb, X, Y, threshold)
    assert keep.size == threshold


@pytest.mark.parametrize("threshold", [1000, 5000])
def test_bench_minmax(benchmark, threshold):
    keep = benchmark(minmax, X, Y, threshold)
    assert keep.size <= threshold


@pytest.mark.parametrize("width", [800, 1920])
def test_bench_m4(benchmark, width):
    keep = benchmark(m4, X, Y, width)
    assert keep.size <= 4 * width


def test_bench_ols(benchmark):
    fit = benchmark(ols_fit, X[:50_000], Y[:50_000])
    assert fit.dof == 50_000 - 2


def test_bench_lowess_delta(benchmark):
    fit = benchmark(lowess, X[:5000], Y[:5000], 0.1, 1, 25.0)
    assert fit.y_hat.size == 5000
