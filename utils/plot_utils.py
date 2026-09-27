"""Backward-compatible facade over :mod:`plotlyvizpro`.

The notebooks and Streamlit pages historically imported from ``utils.plot_utils``.
That module grew duplicate definitions (``add_trendline``, ``add_moving_average``,
``add_zscore_band`` and ``scatter_mapbox`` were each defined twice with different
signatures) and a PNG exporter that broke on Plotly >= 6. Everything here now
delegates to the typed, tested package; new code should import from
:mod:`plotlyvizpro` directly.
"""

from __future__ import annotations

import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

from plotlyvizpro import export as _export
from plotlyvizpro import theme as _theme
from plotlyvizpro.charts import (  # noqa: F401  (re-exported)
    animated_plot,
    bar_plot,
    box_plot,
    bubble_plot,
    choropleth_map,
    density_contour,
    density_heatmap,
    histogram_plot,
    line_plot,
    pie_chart,
    scatter_geo,
    scatter_map,
    scatter_plot,
    violin_plot,
)
from plotlyvizpro.layout import (  # noqa: F401  (re-exported)
    add_annotation,
    add_dropdown,
    add_shape,
    add_slider,
    add_trace,
    create_figure,
    create_subplots,
    set_margins,
    update_layout,
)
from plotlyvizpro.theme import apply_dark_theme  # noqa: F401  (re-exported)

# --- legacy aliases ------------------------------------------------------------

apply_custom_layout = update_layout
update_go_layout = update_layout
create_go_figure = create_figure
add_trace_go = add_trace
add_trace_to_subplot = add_trace
add_annotation_go = add_annotation
add_shape_go = add_shape
apply_dashboard_margins = set_margins


def apply_theme(template: str = "plotly_white", font_family: str = "Arial", font_size: int = 14) -> None:
    """Legacy signature: set the global default template with a font override."""
    _theme.apply_theme(template, font_family=font_family, font_size=font_size)


def update_subplot_layout(
    fig: go.Figure, title: str = "", height: int = 600, width: int = 1000, showlegend: bool = True
) -> go.Figure:
    """Legacy helper: set title, size and legend visibility on a subplot figure."""
    fig.update_layout(title=title, height=height, width=width, showlegend=showlegend)
    return fig


def scatter_mapbox(
    df: pd.DataFrame,
    lat: str,
    lon: str,
    color: str | None = None,
    size: str | None = None,
    hover_name: str | None = None,
    title: str = "",
    zoom: int = 1,
    center: dict[str, float] | None = None,
    mapbox_style: str = "carto-positron",
    token: str | None = None,
) -> go.Figure:
    """Deprecated: use :func:`plotlyvizpro.charts.scatter_map` (MapLibre, token-free)."""
    warnings.warn("scatter_mapbox is deprecated; use plotlyvizpro.charts.scatter_map", DeprecationWarning, stacklevel=2)
    if token:
        pio.mapbox.default_access_token = token  # type: ignore[attr-defined]
    style = {
        "carto-positron": "carto-positron",
        "open-street-map": "open-street-map",
        "carto-darkmatter": "carto-darkmatter",
    }.get(mapbox_style, "carto-positron")
    return scatter_map(
        df,
        lat,
        lon,
        color=color,
        size=size,
        hover_name=hover_name,
        title=title,
        zoom=zoom,
        center=center,
        map_style=style,
    )


def _project_root() -> Path:
    here = Path(__file__).resolve().parent.parent
    return here


def save_fig_as_html(fig: go.Figure, filename: str, notebook_name: str = "general") -> Path:
    """Save to ``<project>/exports/html/<notebook_name>/<filename>`` and return the path."""
    return _export.save_html(fig, _project_root() / "exports" / "html" / notebook_name / filename)


def save_fig_as_png(fig: go.Figure, filename: str, notebook_name: str = "general") -> Path:
    """Save to ``<project>/exports/images/<notebook_name>/<filename>`` and return the path."""
    return _export.save_image(fig, _project_root() / "exports" / "images" / notebook_name / filename)


def quick_preview(df: pd.DataFrame, chart_type: str = "line", **kwargs: object) -> go.Figure:
    """Build (and ``show``) a quick line/scatter/bubble chart."""
    builders = {"line": line_plot, "scatter": scatter_plot, "bubble": bubble_plot}
    if chart_type not in builders:
        raise ValueError(f"Unknown chart type {chart_type!r}; choose from {sorted(builders)}")
    fig = builders[chart_type](df, **kwargs)  # type: ignore[operator]
    fig.show()
    return fig


# --- legacy statistical overlays (trace-returning forms used by notebook 10) ---


def add_trendline(x: pd.Series, y: pd.Series, name: str = "Trendline", color: str = "crimson") -> go.Scatter:
    """Return an OLS trendline trace for ``x``/``y`` (datetime ``x`` supported)."""
    from plotlyvizpro.stats.regression import ols_fit

    fit = ols_fit(x, y)
    return go.Scatter(x=fit.x, y=fit.y_hat, mode="lines", name=name, line={"color": color, "dash": "dash"})


def add_moving_average(
    x: pd.Series, y: pd.Series, window: int = 5, name: str = "Moving Avg", color: str = "royalblue"
) -> go.Scatter:
    """Return a rolling-mean trace."""
    y_series = pd.Series(np.asarray(y, dtype=float)).rolling(window=window).mean()
    return go.Scatter(x=x, y=y_series, mode="lines", name=name, line={"color": color, "dash": "dot"})


def add_zscore_band(x: pd.Series, y: pd.Series, z: float = 2) -> tuple[np.ndarray, np.ndarray]:
    """Return constant ``(upper, lower)`` arrays at mean +/- z standard deviations."""
    arr = np.asarray(y, dtype=float)
    mean, std = arr.mean(), arr.std()
    return np.full_like(arr, mean + z * std), np.full_like(arr, mean - z * std)
