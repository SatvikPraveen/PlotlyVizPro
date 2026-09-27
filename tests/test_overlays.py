"""Overlays add correctly labelled traces without touching existing ones."""

from __future__ import annotations

from functools import partial

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import pytest

from plotlyvizpro import overlays
from plotlyvizpro.charts import scatter_plot
from plotlyvizpro.layout import pipe


@pytest.fixture
def base(sample_df):
    return scatter_plot(sample_df, "Date", "Sales", title="base")


def _names(fig):
    return [t.name for t in fig.data]


def test_trendline_adds_band_and_line_and_annotation(base, sample_df):
    n0 = len(base.data)
    fig = pipe(
        base, partial(overlays.add_trendline, x=sample_df["Date"], y=sample_df["Sales"], show_ci=True, show_pi=True)
    )
    assert len(fig.data) == n0 + 3
    assert any("95% CI" in n for n in _names(fig))
    assert any("95% PI" in n for n in _names(fig))
    assert fig.layout.annotations[0].text.startswith("y = ")
    assert "ols" in fig.layout.meta
    assert fig.data[0].name == base.data[0].name  # existing trace untouched


def test_trendline_polynomial_label(base, sample_df):
    fig = overlays.add_trendline(base, sample_df["Sales"], sample_df["Profit"], degree=2, show_ci=False, annotate=False)
    assert "degree-2" in fig.data[-1].name
    assert not fig.layout.annotations


def test_lowess_and_moving_average_and_ewma(base, sample_df):
    x, y = sample_df["Date"], sample_df["Sales"]
    fig = pipe(
        base,
        partial(overlays.add_lowess, x=x, y=y, frac=0.4),
        (overlays.add_moving_average, {"x": x, "y": y, "window": 5}),
        partial(overlays.add_ewma, x=x, y=y, span=5),
    )
    names = _names(fig)
    assert any(n.startswith("LOWESS") for n in names)
    assert "Rolling mean (5)" in names
    assert any(n.startswith("EWMA") for n in names)


def test_bollinger_and_zscore_bands(base, sample_df):
    x, y = sample_df["Date"], sample_df["Sales"]
    fig = pipe(
        base,
        partial(overlays.add_bollinger_bands, x=x, y=y, window=5),
        partial(overlays.add_zscore_band, x=x, y=y, z=2, robust=True),
    )
    assert any(t.fill == "toself" for t in fig.data)
    assert len(fig.layout.shapes) == 1  # centre hline from zscore band
    assert any("MAD" in n for n in _names(fig))


@pytest.mark.parametrize("method", ["zscore", "iqr", "hampel", "esd"])
def test_anomalies_marks_spike(method):
    x = np.arange(60)
    y = np.sin(x / 5)
    y[30] = 10
    fig = go.Figure(go.Scatter(x=x, y=y))
    kwargs = {"max_outliers": 3} if method == "esd" else {}
    fig = overlays.add_anomalies(fig, x, y, method=method, show_bounds=True, **kwargs)
    assert 30 in fig.layout.meta["anomalies"]["indices"]
    marker_trace = fig.data[-1]
    assert marker_trace.mode == "markers"
    assert 30 in list(marker_trace.x)


def test_pipe_rejects_non_figure_result():
    with pytest.raises(TypeError, match="did not return a Figure"):
        pipe(go.Figure(), lambda fig: None)  # type: ignore[arg-type,return-value]


def test_anomalies_bad_method():
    with pytest.raises(ValueError, match="Unknown method"):
        overlays.add_anomalies(go.Figure(), [1, 2], [1, 2], method="oracle")


def test_bootstrap_errorbars(sample_df):
    fig = overlays.add_bootstrap_errorbars(
        go.Figure(), sample_df["Sales"], sample_df["Category"], n_resamples=200, seed=1
    )
    tr = fig.data[0]
    assert list(tr.x) == ["A", "B", "C", "D"]
    assert tr.error_y.symmetric is False
    assert all(v >= 0 for v in tr.error_y.array)


def test_kde_ecdf_qq(sample_df):
    y = sample_df["Sales"]
    fig = overlays.add_kde(go.Figure(), y)
    assert fig.data[0].fill == "tozeroy"
    fig2 = overlays.add_ecdf(go.Figure(), y, confidence=0.9)
    assert fig2.data[-1].line.shape == "hv"
    assert "90% DKW" in fig2.data[0].name
    assert fig2.layout.yaxis.range[1] == pytest.approx(1.02)
    fig3 = overlays.add_qq(go.Figure(), y)
    assert len(fig3.data) == 2
    assert "R²" in fig3.data[1].name


def test_decomposition_and_acf_figures():
    t = np.arange(96)
    y = 10 + 0.1 * t + 2 * np.sin(2 * np.pi * t / 12)
    dates = pd.date_range("2020-01-01", periods=96, freq="MS")
    fig = overlays.decomposition_figure(dates, y, period=12)
    assert len(fig.data) == 4
    assert "F_S=" in fig.layout.title.text
    acf = overlays.acf_figure(y, max_lag=20)
    assert acf.data[0].type == "bar"
    assert len(acf.layout.shapes) == 2
