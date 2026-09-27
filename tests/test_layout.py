"""Tests for plotlyvizpro.layout."""

from __future__ import annotations

import plotly.graph_objects as go
import pytest

from plotlyvizpro import layout


def _fig(n: int = 3) -> go.Figure:
    fig = layout.create_figure(title="x")
    for i in range(n):
        layout.add_trace(fig, go.Scatter(x=[0, 1], y=[i, i + 1], name=str(i)))
    return fig


def test_create_figure_template_and_title():
    fig = layout.create_figure(title="Hello", showlegend=False)
    assert fig.layout.title.text == "Hello"
    assert fig.layout.showlegend is False
    assert fig.layout.template.layout.paper_bgcolor == "#fcfcfb"


def test_add_trace_requires_row_and_col_together():
    fig = layout.create_subplots(1, 2)
    with pytest.raises(ValueError, match="row and col"):
        layout.add_trace(fig, go.Scatter(x=[1], y=[1]), row=1)
    layout.add_trace(fig, go.Scatter(x=[1], y=[1]), row=1, col=2)
    assert fig.data[0].xaxis == "x2"


def test_update_layout_skips_none():
    fig = _fig(1)
    layout.update_layout(fig, xaxis_title="X", legend_title="L")
    assert fig.layout.xaxis.title.text == "X"
    assert fig.layout.legend.title.text == "L"
    assert fig.layout.title.text == "x"


def test_set_margins():
    fig = layout.set_margins(_fig(1), left=1, right=2, top=3, bottom=4)
    assert (fig.layout.margin.l, fig.layout.margin.r, fig.layout.margin.t, fig.layout.margin.b) == (1, 2, 3, 4)


def test_create_subplots_shared_axes():
    fig = layout.create_subplots(2, 1, shared_x=True, subplot_titles=("a", "b"))
    assert fig.layout.xaxis2.matches == "x" or fig.layout.xaxis.matches in (None, "x2")
    assert [a.text for a in fig.layout.annotations] == ["a", "b"]


def test_dropdown_visibility_masks():
    fig = layout.add_dropdown(_fig(3), {"first": [0], "rest": [1, 2]}, title="T")
    buttons = fig.layout.updatemenus[0].buttons
    assert list(buttons[0].args[0]["visible"]) == [True, False, False]
    assert list(buttons[1].args[0]["visible"]) == [False, True, True]
    assert buttons[0].args[1]["title"] == "T"


def test_dropdown_rejects_bad_index():
    with pytest.raises(IndexError):
        layout.add_dropdown(_fig(2), {"bad": [5]})


def test_slider_one_step_per_trace():
    fig = layout.add_slider(_fig(3), ["a", "b", "c"], prefix="Step ")
    steps = fig.layout.sliders[0].steps
    assert len(steps) == 3
    assert steps[1].args[1]["title"] == "Step b"
    assert [t.visible for t in fig.data] == [True, False, False]


def test_slider_label_count_mismatch():
    with pytest.raises(ValueError, match="Expected 3 labels"):
        layout.add_slider(_fig(3), ["a"])


def test_annotation_and_shape():
    fig = layout.add_annotation(_fig(1), "hi", x=0.5, y=0.5)
    fig = layout.add_shape(fig, {"type": "rect", "x0": 0, "x1": 1, "y0": 0, "y1": 1})
    assert fig.layout.annotations[0].text == "hi"
    assert fig.layout.shapes[0].type == "rect"


@pytest.mark.parametrize("axis", ["x", "y"])
def test_reference_line(axis):
    fig = layout.add_reference_line(_fig(1), 0.5, axis=axis, label="ref")
    assert len(fig.layout.shapes) == 1


def test_reference_line_bad_axis():
    with pytest.raises(ValueError, match="axis"):
        layout.add_reference_line(_fig(1), 0.5, axis="z")
