"""Downsampling: shape preservation, invariants and property tests."""

from __future__ import annotations

import numpy as np
import pytest
from hypothesis import given, settings
from hypothesis import strategies as st
from hypothesis.extra import numpy as hnp

from plotlyvizpro.downsample import downsample, lttb, m4, max_error, minmax


@pytest.fixture(scope="module")
def series():
    rng = np.random.default_rng(0)
    x = np.arange(10_000, dtype=float)
    y = np.cumsum(rng.normal(size=x.size))
    y[5000] += 50  # a spike that a good downsampler must keep
    return x, y


class TestLTTB:
    def test_exact_size_and_endpoints(self, series):
        x, y = series
        keep = lttb(x, y, 500)
        assert keep.size == 500
        assert keep[0] == 0
        assert keep[-1] == x.size - 1
        assert np.all(np.diff(keep) > 0)

    def test_keeps_spike(self, series):
        x, y = series
        keep = lttb(x, y, 300)
        assert 5000 in keep

    def test_noop_when_threshold_large(self, series):
        x, y = series
        np.testing.assert_array_equal(lttb(x[:10], y[:10], 50), np.arange(10))

    def test_reference_small_case(self):
        # Hand-checked: the middle bucket should choose the point farthest from the chord.
        x = np.arange(7, dtype=float)
        y = np.array([0, 0, 5, 0, 0, 0, 0.0])
        keep = lttb(x, y, 3)
        np.testing.assert_array_equal(keep, [0, 2, 6])

    def test_errors(self):
        with pytest.raises(ValueError, match="threshold"):
            lttb([0, 1, 2], [0, 1, 2], 2)
        with pytest.raises(ValueError, match="sorted"):
            lttb([2, 1, 0], [0, 1, 2], 3)
        with pytest.raises(ValueError, match="same length"):
            lttb([0, 1, 2], [0, 1], 3)

    @settings(max_examples=40, deadline=None)
    @given(
        y=hnp.arrays(np.float64, st.integers(3, 300), elements=st.floats(-1e3, 1e3)),
        threshold=st.integers(3, 50),
    )
    def test_property_invariants(self, y, threshold):
        x = np.arange(y.size, dtype=float)
        keep = lttb(x, y, threshold)
        assert keep[0] == 0
        assert keep[-1] == y.size - 1
        assert keep.size == min(threshold, y.size)
        assert np.all(np.diff(keep) > 0)


class TestMinMax:
    def test_envelope_exact(self, series):
        x, y = series
        keep = minmax(x, y, 400)
        assert keep.size <= 400
        assert y[keep].max() == y.max()
        assert y[keep].min() == y.min()
        assert np.all(np.diff(keep) > 0)

    def test_noop(self):
        np.testing.assert_array_equal(minmax(np.arange(5.0), np.arange(5.0), 10), np.arange(5))


class TestM4:
    def test_pixel_columns(self, series):
        x, y = series
        keep = m4(x, y, 100)
        assert keep.size <= 400
        assert keep[0] == 0
        assert keep[-1] == x.size - 1
        assert y[keep].max() == y.max()

    def test_noop_and_degenerate(self):
        np.testing.assert_array_equal(m4(np.arange(8.0), np.arange(8.0), 2), np.arange(8))
        np.testing.assert_array_equal(m4(np.zeros(10), np.arange(10.0), 1), [0, 9])

    def test_respects_gaps_in_x(self):
        x = np.concatenate([np.arange(100.0), np.arange(900.0, 1000.0)])
        y = np.sin(x)
        keep = m4(x, y, 10)
        # No column should be created in the empty middle; all kept points are real.
        assert np.all((x[keep] < 100) | (x[keep] >= 900))


def test_dispatcher_and_error_metric(series):
    x, y = series
    for method in ("lttb", "minmax", "m4"):
        keep = downsample(x, y, 800, method=method)  # type: ignore[arg-type]
        assert keep.size <= 800
        assert max_error(x, y, keep) < max_error(x, y, np.array([0, x.size - 1]))
    with pytest.raises(ValueError, match="Unknown method"):
        downsample(x, y, 10, method="random")  # type: ignore[arg-type]
    assert downsample(x[:5], y[:5], 100).size == 5


def test_lttb_error_decreases_with_threshold(series):
    x, y = series
    errs = [max_error(x, y, lttb(x, y, t)) for t in (50, 200, 1000, 5000)]
    assert errs == sorted(errs, reverse=True)
