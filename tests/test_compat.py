"""The legacy utils.plot_utils facade must keep notebook code working."""

from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import pytest


def test_legacy_names_importable():
    from utils.plot_utils import (  # noqa: F401
        add_annotation_go,
        add_moving_average,
        add_trendline,
        add_zscore_band,
        apply_custom_layout,
        apply_dark_theme,
        apply_theme,
        bar_plot,
        create_go_figure,
        line_plot,
        save_fig_as_html,
        save_fig_as_png,
        scatter_mapbox,
        update_subplot_layout,
    )


def test_legacy_overlays_return_traces(sample_df):
    from utils.plot_utils import add_moving_average, add_trendline, add_zscore_band

    trend = add_trendline(sample_df["Date"], sample_df["Sales"])
    assert isinstance(trend, go.Scatter)
    assert len(trend.y) == len(sample_df)
    ma = add_moving_average(sample_df["Date"], sample_df["Sales"], window=5)
    assert np.isnan(ma.y[:4]).all()
    upper, lower = add_zscore_band(sample_df["Date"], sample_df["Sales"], z=2)
    assert (upper > lower).all()


def test_scatter_mapbox_deprecated(sample_df):
    from utils.plot_utils import scatter_mapbox

    with pytest.warns(DeprecationWarning, match="scatter_map"):
        fig = scatter_mapbox(sample_df, "Lat", "Lon")
    assert fig.data[0].type == "scattermap"


def test_save_fig_as_html_targets_project_exports(tmp_path, monkeypatch):
    import utils.plot_utils as pu

    monkeypatch.setattr(pu, "_project_root", lambda: tmp_path)
    p = pu.save_fig_as_html(go.Figure(), "x.html", notebook_name="nb")
    assert p == tmp_path / "exports" / "html" / "nb" / "x.html"
    assert p.exists()
