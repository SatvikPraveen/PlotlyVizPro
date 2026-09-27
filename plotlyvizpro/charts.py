"""Typed chart builders on top of Plotly Express.

Every builder validates its column arguments up front, uses the project
template by default, and returns a :class:`plotly.graph_objects.Figure` so the
result can be piped through :mod:`plotlyvizpro.overlays` and
:mod:`plotlyvizpro.layout` helpers.
"""

from __future__ import annotations

from typing import Any, Literal

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from plotlyvizpro._validation import require_columns

DEFAULT_TEMPLATE = "pvp_light"


def _finish(fig: go.Figure, legend_title: str | None) -> go.Figure:
    fig.update_layout(legend_title_text=legend_title or "")
    return fig


def line_plot(
    df: pd.DataFrame,
    x: str,
    y: str | list[str],
    color: str | None = None,
    title: str = "",
    markers: bool = False,
    template: str = DEFAULT_TEMPLATE,
    line_dash: str | None = None,
    facet_col: str | None = None,
    facet_row: str | None = None,
    **kwargs: object,
) -> go.Figure:
    """Line chart for change over time or ordered categories."""
    require_columns(df, x, *(y if isinstance(y, list) else [y]), color, line_dash, facet_col, facet_row)
    fig = px.line(
        df,
        x=x,
        y=y,
        color=color,
        line_dash=line_dash,
        facet_col=facet_col,
        facet_row=facet_row,
        title=title,
        markers=markers,
        template=template,
        **kwargs,
    )
    return _finish(fig, color)


def scatter_plot(
    df: pd.DataFrame,
    x: str,
    y: str,
    color: str | None = None,
    size: str | None = None,
    symbol: str | None = None,
    hover_name: str | None = None,
    title: str = "",
    template: str = DEFAULT_TEMPLATE,
    trendline: Literal["ols", "lowess"] | None = None,
    opacity: float = 0.85,
    **kwargs: object,
) -> go.Figure:
    """Scatter chart with optional colour, size and symbol encodings."""
    require_columns(df, x, y, color, size, symbol, hover_name)
    fig = px.scatter(
        df,
        x=x,
        y=y,
        color=color,
        size=size,
        symbol=symbol,
        hover_name=hover_name,
        title=title,
        template=template,
        trendline=trendline,
        opacity=opacity,
        **kwargs,
    )
    return _finish(fig, color)


def bubble_plot(
    df: pd.DataFrame,
    x: str,
    y: str,
    size: str,
    color: str | None = None,
    hover_name: str | None = None,
    title: str = "",
    template: str = DEFAULT_TEMPLATE,
    size_max: int = 40,
    **kwargs: Any,
) -> go.Figure:
    """Scatter chart where a third quantity is encoded as marker area."""
    return scatter_plot(
        df,
        x,
        y,
        color=color,
        size=size,
        hover_name=hover_name,
        title=title,
        template=template,
        size_max=size_max,
        **kwargs,
    )


def bar_plot(
    df: pd.DataFrame,
    x: str,
    y: str,
    color: str | None = None,
    barmode: Literal["group", "stack", "relative", "overlay"] = "group",
    title: str = "",
    template: str = DEFAULT_TEMPLATE,
    orientation: Literal["v", "h"] = "v",
    text_auto: bool | str = False,
    **kwargs: object,
) -> go.Figure:
    """Bar chart for comparing magnitudes across categories."""
    require_columns(df, x, y, color)
    fig = px.bar(
        df,
        x=x,
        y=y,
        color=color,
        barmode=barmode,
        orientation=orientation,
        title=title,
        template=template,
        text_auto=text_auto,
        **kwargs,
    )
    return _finish(fig, color)


def pie_chart(
    df: pd.DataFrame,
    names: str,
    values: str,
    title: str = "",
    hole: float = 0.0,
    template: str = DEFAULT_TEMPLATE,
    **kwargs: object,
) -> go.Figure:
    """Pie (or donut when ``hole > 0``) chart of part-to-whole shares.

    Prefer :func:`bar_plot` when there are more than five categories or when
    the shares are close: angle is read less accurately than length.
    """
    require_columns(df, names, values)
    fig = px.pie(df, names=names, values=values, title=title, hole=hole, template=template, **kwargs)
    fig.update_traces(textposition="inside", textinfo="percent+label", sort=False)
    return fig


def box_plot(
    df: pd.DataFrame,
    x: str | None,
    y: str,
    color: str | None = None,
    title: str = "",
    template: str = DEFAULT_TEMPLATE,
    points: Literal["all", "outliers", "suspectedoutliers", False] = "outliers",
    notched: bool = False,
    **kwargs: object,
) -> go.Figure:
    """Box plot of a distribution per category.

    ``notched=True`` draws median confidence notches (McGill, Tukey & Larsen 1978),
    which lets two medians be compared visually at roughly the 95% level.
    """
    require_columns(df, x, y, color)
    fig = px.box(df, x=x, y=y, color=color, points=points, notched=notched, title=title, template=template, **kwargs)
    return _finish(fig, color)


def violin_plot(
    df: pd.DataFrame,
    x: str | None,
    y: str,
    color: str | None = None,
    title: str = "",
    template: str = DEFAULT_TEMPLATE,
    box: bool = True,
    points: Literal["all", "outliers", "suspectedoutliers", False] = "outliers",
    **kwargs: object,
) -> go.Figure:
    """Violin plot: kernel density per category, optionally with an inner box."""
    require_columns(df, x, y, color)
    fig = px.violin(df, x=x, y=y, color=color, box=box, points=points, title=title, template=template, **kwargs)
    return _finish(fig, color)


def histogram_plot(
    df: pd.DataFrame,
    x: str,
    color: str | None = None,
    nbins: int | None = None,
    title: str = "",
    template: str = DEFAULT_TEMPLATE,
    barmode: Literal["overlay", "stack", "group", "relative"] = "overlay",
    histnorm: Literal["", "percent", "probability", "density", "probability density"] = "",
    marginal: Literal["rug", "box", "violin"] | None = None,
    **kwargs: object,
) -> go.Figure:
    """Histogram with optional grouping, normalisation and marginal plot."""
    require_columns(df, x, color)
    fig = px.histogram(
        df,
        x=x,
        color=color,
        nbins=nbins,
        title=title,
        template=template,
        barmode=barmode,
        histnorm=histnorm,
        marginal=marginal,
        **kwargs,
    )
    if barmode == "overlay" and color:
        fig.update_traces(opacity=0.75, selector={"type": "histogram"})
    return _finish(fig, color)


def density_heatmap(
    df: pd.DataFrame,
    x: str,
    y: str,
    color_continuous_scale: str = "Blues",
    title: str = "",
    template: str = DEFAULT_TEMPLATE,
    nbinsx: int | None = None,
    nbinsy: int | None = None,
    **kwargs: object,
) -> go.Figure:
    """2-D binned density as a heatmap (one sequential hue by default)."""
    require_columns(df, x, y)
    fig = px.density_heatmap(
        df,
        x=x,
        y=y,
        color_continuous_scale=color_continuous_scale,
        title=title,
        template=template,
        nbinsx=nbinsx,
        nbinsy=nbinsy,
        **kwargs,
    )
    return fig


def density_contour(
    df: pd.DataFrame,
    x: str,
    y: str,
    color: str | None = None,
    title: str = "",
    template: str = DEFAULT_TEMPLATE,
    **kwargs: object,
) -> go.Figure:
    """2-D density contours (kernel-density style)."""
    require_columns(df, x, y, color)
    fig = px.density_contour(df, x=x, y=y, color=color, title=title, template=template, **kwargs)
    return _finish(fig, color)


def scatter_geo(
    df: pd.DataFrame,
    lat: str,
    lon: str,
    color: str | None = None,
    size: str | None = None,
    hover_name: str | None = None,
    title: str = "",
    template: str = DEFAULT_TEMPLATE,
    projection: str = "natural earth",
    **kwargs: object,
) -> go.Figure:
    """Point map on a geographic projection (no tile server required)."""
    require_columns(df, lat, lon, color, size, hover_name)
    fig = px.scatter_geo(
        df, lat=lat, lon=lon, color=color, size=size, hover_name=hover_name, title=title, template=template, **kwargs
    )
    fig.update_geos(projection_type=projection, showcountries=True, countrycolor="#c9c9c5")
    return _finish(fig, color)


def choropleth_map(
    df: pd.DataFrame,
    locations: str,
    color: str,
    locationmode: Literal["ISO-3", "USA-states", "country names", "geojson-id"] = "country names",
    title: str = "",
    template: str = DEFAULT_TEMPLATE,
    color_continuous_scale: str = "Blues",
    **kwargs: object,
) -> go.Figure:
    """Choropleth map coloured by a sequential scale."""
    require_columns(df, locations, color)
    fig = px.choropleth(
        df,
        locations=locations,
        color=color,
        locationmode=locationmode,
        color_continuous_scale=color_continuous_scale,
        title=title,
        template=template,
        **kwargs,
    )
    return fig


def scatter_map(
    df: pd.DataFrame,
    lat: str,
    lon: str,
    color: str | None = None,
    size: str | None = None,
    hover_name: str | None = None,
    title: str = "",
    zoom: int = 1,
    center: dict[str, float] | None = None,
    map_style: str = "carto-positron",
    **kwargs: object,
) -> go.Figure:
    """Tile-based point map using MapLibre (``px.scatter_map``).

    This replaces the deprecated Mapbox-token based ``scatter_mapbox``; the
    default ``carto-positron`` style needs no access token.
    """
    require_columns(df, lat, lon, color, size, hover_name)
    fig = px.scatter_map(
        df,
        lat=lat,
        lon=lon,
        color=color,
        size=size,
        hover_name=hover_name,
        zoom=zoom,
        center=center,
        map_style=map_style,
        title=title,
        **kwargs,
    )
    return _finish(fig, color)


def animated_plot(
    df: pd.DataFrame,
    x: str,
    y: str,
    animation_frame: str,
    color: str | None = None,
    title: str = "",
    template: str = DEFAULT_TEMPLATE,
    plot_type: Literal["line", "bar", "scatter"] = "line",
    frame_duration_ms: int = 300,
    **kwargs: object,
) -> go.Figure:
    """Animated line, bar or scatter chart driven by ``animation_frame``."""
    require_columns(df, x, y, animation_frame, color)
    builders = {"line": px.line, "bar": px.bar, "scatter": px.scatter}
    if plot_type not in builders:
        raise ValueError(f"Unsupported plot_type {plot_type!r}. Use one of {sorted(builders)}.")
    fig = builders[plot_type](
        df, x=x, y=y, color=color, animation_frame=animation_frame, title=title, template=template, **kwargs
    )
    fig.update_layout(transition={"duration": frame_duration_ms})
    if fig.layout.updatemenus:
        fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = frame_duration_ms
    return _finish(fig, color)
