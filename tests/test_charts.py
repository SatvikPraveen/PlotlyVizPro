"""Tests for plotlyvizpro.charts."""

from __future__ import annotations

import plotly.graph_objects as go
import pytest

from plotlyvizpro import charts


class TestLine:
    def test_returns_figure_with_title(self, sample_df):
        fig = charts.line_plot(sample_df, "Date", "Sales", title="T")
        assert isinstance(fig, go.Figure)
        assert fig.layout.title.text == "T"
        assert len(fig.data) == 1

    def test_color_creates_one_trace_per_group(self, sample_df):
        fig = charts.line_plot(sample_df, "Date", "Sales", color="Region")
        assert len(fig.data) == 2
        assert fig.layout.legend.title.text == "Region"

    def test_multiple_y_columns(self, sample_df):
        fig = charts.line_plot(sample_df, "Date", ["Sales", "Profit"])
        assert len(fig.data) == 2

    def test_missing_column_raises(self, sample_df):
        with pytest.raises(KeyError, match="Nope"):
            charts.line_plot(sample_df, "Date", "Nope")

    def test_non_dataframe_raises(self):
        with pytest.raises(TypeError):
            charts.line_plot([1, 2, 3], "a", "b")  # type: ignore[arg-type]

    def test_uses_project_template(self, sample_df):
        fig = charts.line_plot(sample_df, "Date", "Sales")
        assert fig.layout.template.layout.paper_bgcolor == "#fcfcfb"


class TestScatterAndBubble:
    def test_scatter_encodings(self, sample_df):
        fig = charts.scatter_plot(sample_df, "Sales", "Profit", color="Category", size="Orders", symbol="Region")
        assert len(fig.data) >= 4

    def test_scatter_trendline_ols(self, sample_df):
        fig = charts.scatter_plot(sample_df, "Sales", "Profit", trendline="ols")
        assert any(t.mode == "lines" for t in fig.data)

    def test_bubble_is_scatter_with_size(self, sample_df):
        fig = charts.bubble_plot(sample_df, "Sales", "Profit", size="Orders")
        assert fig.data[0].marker.size is not None


class TestBarPieBox:
    @pytest.mark.parametrize("barmode", ["group", "stack", "relative", "overlay"])
    def test_bar_modes(self, sample_df, barmode):
        fig = charts.bar_plot(sample_df, "Category", "Sales", color="Region", barmode=barmode)
        assert fig.layout.barmode == barmode

    def test_horizontal_bar(self, sample_df):
        fig = charts.bar_plot(sample_df, "Sales", "Category", orientation="h")
        assert fig.data[0].orientation == "h"

    def test_pie_and_donut(self, sample_df):
        agg = sample_df.groupby("Category", as_index=False)["Sales"].sum()
        fig = charts.pie_chart(agg, "Category", "Sales", hole=0.4)
        assert fig.data[0].type == "pie"
        assert fig.data[0].hole == 0.4

    def test_box_notched(self, sample_df):
        fig = charts.box_plot(sample_df, "Category", "Sales", notched=True)
        assert fig.data[0].notched is True

    def test_violin(self, sample_df):
        fig = charts.violin_plot(sample_df, "Category", "Sales", color="Region")
        assert all(t.type == "violin" for t in fig.data)


class TestDistributions:
    def test_histogram_overlay_sets_opacity(self, sample_df):
        fig = charts.histogram_plot(sample_df, "Sales", color="Region", nbins=10)
        assert fig.layout.barmode == "overlay"
        assert fig.data[0].opacity == 0.75

    def test_histogram_marginal(self, sample_df):
        fig = charts.histogram_plot(sample_df, "Sales", marginal="box")
        assert any(t.type == "box" for t in fig.data)

    def test_density_heatmap_and_contour(self, sample_df):
        assert charts.density_heatmap(sample_df, "Sales", "Profit").data[0].type == "histogram2d"
        assert charts.density_contour(sample_df, "Sales", "Profit").data[0].type == "histogram2dcontour"


class TestGeo:
    def test_scatter_geo_projection(self, sample_df):
        fig = charts.scatter_geo(sample_df, "Lat", "Lon", color="Region", projection="orthographic")
        assert fig.layout.geo.projection.type == "orthographic"

    def test_choropleth(self):
        import pandas as pd

        df = pd.DataFrame({"country": ["France", "Brazil"], "value": [1.0, 2.0]})
        fig = charts.choropleth_map(df, "country", "value")
        assert fig.data[0].type == "choropleth"

    def test_scatter_map_token_free(self, sample_df):
        fig = charts.scatter_map(sample_df, "Lat", "Lon", zoom=2)
        assert fig.data[0].type == "scattermap"
        assert fig.layout.map.style == "carto-positron"


class TestAnimated:
    @pytest.mark.parametrize("plot_type", ["line", "bar", "scatter"])
    def test_animation_frames(self, sample_df, plot_type):
        fig = charts.animated_plot(sample_df, "Category", "Sales", animation_frame="Region", plot_type=plot_type)
        assert len(fig.frames) == 2
        assert fig.layout.transition.duration == 300

    def test_bad_plot_type(self, sample_df):
        with pytest.raises(ValueError, match="Unsupported plot_type"):
            charts.animated_plot(sample_df, "Category", "Sales", animation_frame="Region", plot_type="pie")  # type: ignore[arg-type]
