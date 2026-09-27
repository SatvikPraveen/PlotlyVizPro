"""Backward-compatible facade over :mod:`plotlyvizpro`.

The notebooks and Streamlit pages historically imported from ``utils.plot_utils``.
That module grew duplicate definitions (``add_trendline``, ``add_moving_average``,
``add_zscore_band`` and ``scatter_mapbox`` were each defined twice with different
signatures) and a PNG exporter that broke on Plotly >= 6. Everything here now
delegates to the typed, tested package; new code should import from
:mod:`plotlyvizpro` directly.
"""

from __future__ import annotations

import os
import warnings
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

try:
    import plotlyvizpro  # noqa: F401
except ImportError:  # notebooks put utils/ on sys.path without installing the package
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

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


def apply_theme(template: str = "plotly_white", font_family: str = "Arial", font_size: int = 14) -> None:
    """Legacy signature: set the global default template with a font override."""
    _theme.apply_theme(template, font_family=font_family, font_size=font_size)


def apply_dashboard_margins(fig: go.Figure, l: int = 40, r: int = 40, t: int = 60, b: int = 40) -> go.Figure:
    """Legacy margin helper with single-letter keywords."""
    return set_margins(fig, left=l, right=r, top=t, bottom=b)


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


def _export_root() -> Path:
    """Export root: ``PLOTLYVIZPRO_EXPORT_DIR`` if set, else ``<project>/exports``."""
    env = os.environ.get("PLOTLYVIZPRO_EXPORT_DIR")
    return Path(env) if env else Path(__file__).resolve().parent.parent / "exports"


def save_fig_as_html(fig: go.Figure, filename: str, notebook_name: str = "general") -> Path:
    """Save to ``<project>/exports/html/<notebook_name>/<filename>`` and return the path."""
    return _export.save_html(fig, _export_root() / "html" / notebook_name / filename)


def save_fig_as_png(fig: go.Figure, filename: str, notebook_name: str = "general") -> Path:
    """Save to ``<project>/exports/images/<notebook_name>/<filename>`` and return the path."""
    return _export.save_image(fig, _export_root() / "images" / notebook_name / filename)


def quick_preview(df: pd.DataFrame, chart_type: str = "line", **kwargs: object) -> go.Figure:
    """Build (and ``show``) a quick line/scatter/bubble chart."""
    builders = {"line": line_plot, "scatter": scatter_plot, "bubble": bubble_plot}
    if chart_type not in builders:
        raise ValueError(f"Unknown chart type {chart_type!r}; choose from {sorted(builders)}")
    fig = builders[chart_type](df, **kwargs)  # type: ignore[operator]
    fig.show()
    return fig


# --- legacy statistical overlays ---------------------------------------------
#
# The original module defined each of these twice: a figure-first form that
# added a trace in place (used by notebook 09) and a trace-returning form (used
# by notebook 10). Both call styles are supported here by dispatching on the
# first argument.


def add_trendline(*args: Any, name: str = "Trendline", color: str = "crimson", **kwargs: Any) -> go.Scatter | go.Figure:
    """OLS trendline.

    ``add_trendline(x, y)`` returns a trace; ``add_trendline(fig, x, y)`` adds the
    fit (via :func:`plotlyvizpro.overlays.add_trendline`) and returns the figure.
    """
    from plotlyvizpro.overlays import add_trendline as _overlay
    from plotlyvizpro.stats.regression import ols_fit

    if args and isinstance(args[0], go.Figure):
        fig, x, y = args[0], args[1], args[2]
        return _overlay(fig, x, y, name=name, color=color, show_ci=False, annotate=False, **kwargs)
    x, y = args[0], args[1]
    fit = ols_fit(x, y)
    return go.Scatter(x=fit.x, y=fit.y_hat, mode="lines", name=name, line={"color": color, "dash": "dash"})


def add_moving_average(
    *args: Any, window: int = 5, name: str = "Moving Avg", color: str = "royalblue", **kwargs: Any
) -> go.Scatter | go.Figure:
    """Rolling-mean line; trace-returning or figure-first (see :func:`add_trendline`)."""
    from plotlyvizpro.overlays import add_moving_average as _overlay

    if args and isinstance(args[0], go.Figure):
        fig, x, y = args[0], args[1], args[2]
        return _overlay(fig, x, y, window=window, name=name, color=color, **kwargs)
    x, y = args[0], args[1]
    y_series = pd.Series(np.asarray(y, dtype=float)).rolling(window=window).mean()
    return go.Scatter(x=x, y=y_series, mode="lines", name=name, line={"color": color, "dash": "dot"})


def add_zscore_band(
    *args: Any, z: float = 2, band: float | None = None, **kwargs: Any
) -> tuple[np.ndarray, np.ndarray] | go.Figure:
    """Mean +/- z*SD band.

    ``add_zscore_band(x, y, z=2)`` returns ``(upper, lower)`` arrays;
    ``add_zscore_band(fig, x, y, band=1)`` shades the band on the figure.
    """
    from plotlyvizpro.overlays import add_zscore_band as _overlay

    z = band if band is not None else z
    if args and isinstance(args[0], go.Figure):
        fig, x, y = args[0], args[1], args[2]
        kwargs.pop("name", None)
        return _overlay(fig, x, y, z=z, **kwargs)
    x, y = args[0], args[1]
    arr = np.asarray(y, dtype=float)
    mean, std = arr.mean(), arr.std()
    return np.full_like(arr, mean + z * std), np.full_like(arr, mean - z * std)
