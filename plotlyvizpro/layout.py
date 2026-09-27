"""Figure-composition helpers: subplots, controls, annotations, shapes."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

import plotly.graph_objects as go
from plotly.basedatatypes import BaseTraceType
from plotly.subplots import make_subplots


def create_figure(title: str = "", showlegend: bool = True, template: str = "pvp_light") -> go.Figure:
    """Create an empty graph-objects figure with the project template."""
    fig = go.Figure()
    fig.update_layout(title=title, showlegend=showlegend, template=template)
    return fig


def add_trace(fig: go.Figure, trace: BaseTraceType, row: int | None = None, col: int | None = None) -> go.Figure:
    """Add a trace, optionally targeting a subplot cell, and return the figure."""
    if (row is None) != (col is None):
        raise ValueError("row and col must be given together")
    if row is None:
        fig.add_trace(trace)
    else:
        fig.add_trace(trace, row=row, col=col)
    return fig


def update_layout(
    fig: go.Figure,
    title: str | None = None,
    xaxis_title: str | None = None,
    yaxis_title: str | None = None,
    legend_title: str | None = None,
    **kwargs: Any,
) -> go.Figure:
    """Update common layout fields, ignoring any that are ``None``."""
    updates: dict[str, Any] = {
        k: v
        for k, v in {
            "title": title,
            "xaxis_title": xaxis_title,
            "yaxis_title": yaxis_title,
            "legend_title_text": legend_title,
        }.items()
        if v is not None
    }
    updates.update(kwargs)
    fig.update_layout(**updates)
    return fig


def set_margins(fig: go.Figure, left: int = 40, right: int = 40, top: int = 60, bottom: int = 40) -> go.Figure:
    """Set figure margins in pixels."""
    fig.update_layout(margin={"l": left, "r": right, "t": top, "b": bottom})
    return fig


def create_subplots(
    rows: int,
    cols: int,
    specs: Sequence[Sequence[Mapping[str, Any] | None]] | None = None,
    subplot_titles: Sequence[str] | None = None,
    shared_x: bool = False,
    shared_y: bool = False,
    vertical_spacing: float = 0.1,
    horizontal_spacing: float = 0.1,
    template: str = "pvp_light",
    **kwargs: Any,
) -> go.Figure:
    """Create a ``rows x cols`` subplot grid using the project template."""
    fig = make_subplots(
        rows=rows,
        cols=cols,
        specs=specs,
        subplot_titles=subplot_titles,
        shared_xaxes=shared_x,
        shared_yaxes=shared_y,
        vertical_spacing=vertical_spacing,
        horizontal_spacing=horizontal_spacing,
        **kwargs,
    )
    fig.update_layout(template=template)
    return fig


def add_dropdown(
    fig: go.Figure,
    label_trace_map: Mapping[str, Sequence[int]],
    title: str | None = None,
    x: float = 1.0,
    y: float = 1.15,
) -> go.Figure:
    """Add a dropdown that toggles trace visibility.

    Parameters
    ----------
    label_trace_map:
        Mapping from button label to the indices of traces visible for that option.
    """
    n = len(fig.data)
    buttons = []
    for label, idxs in label_trace_map.items():
        bad = [i for i in idxs if i < 0 or i >= n]
        if bad:
            raise IndexError(f"Trace indices {bad} out of range for figure with {n} traces")
        visible = [i in set(idxs) for i in range(n)]
        layout_args: dict[str, Any] = {"title": title} if title is not None else {}
        buttons.append({"label": label, "method": "update", "args": [{"visible": visible}, layout_args]})
    fig.update_layout(
        updatemenus=[
            {
                "type": "dropdown",
                "direction": "down",
                "showactive": True,
                "x": x,
                "xanchor": "right",
                "y": y,
                "yanchor": "top",
                "buttons": buttons,
            }
        ]
    )
    return fig


def add_slider(fig: go.Figure, step_labels: Sequence[str], title: str | None = None, prefix: str = "") -> go.Figure:
    """Add a slider where step ``i`` shows only trace ``i``.

    The number of labels must equal the number of traces.
    """
    if len(step_labels) != len(fig.data):
        raise ValueError(f"Expected {len(fig.data)} labels (one per trace), got {len(step_labels)}")
    steps = [
        {
            "method": "update",
            "label": str(label),
            "args": [{"visible": [j == i for j in range(len(fig.data))]}, {"title": f"{prefix}{label}"}],
        }
        for i, label in enumerate(step_labels)
    ]
    for i, trace in enumerate(fig.data):
        trace.visible = i == 0
    fig.update_layout(sliders=[{"active": 0, "pad": {"t": 40}, "steps": steps}])
    if title is not None:
        fig.update_layout(title=title)
    return fig


def add_annotation(
    fig: go.Figure,
    text: str,
    x: float | str,
    y: float,
    xref: str = "x",
    yref: str = "y",
    showarrow: bool = True,
    **kwargs: Any,
) -> go.Figure:
    """Add a text annotation at a data or paper coordinate."""
    fig.add_annotation(text=text, x=x, y=y, xref=xref, yref=yref, showarrow=showarrow, **kwargs)
    return fig


def add_shape(fig: go.Figure, shape: Mapping[str, Any]) -> go.Figure:
    """Add a shape (line, rect, circle, path) from a plain mapping."""
    fig.add_shape(dict(shape))
    return fig


def add_reference_line(
    fig: go.Figure,
    value: float,
    axis: str = "y",
    label: str | None = None,
    color: str = "#6b6b68",
    dash: str = "dot",
) -> go.Figure:
    """Draw a horizontal (``axis="y"``) or vertical (``axis="x"``) reference line."""
    if axis == "y":
        fig.add_hline(y=value, line={"color": color, "dash": dash, "width": 1}, annotation_text=label)
    elif axis == "x":
        fig.add_vline(x=value, line={"color": color, "dash": dash, "width": 1}, annotation_text=label)
    else:
        raise ValueError("axis must be 'x' or 'y'")
    return fig
