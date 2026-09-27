"""Project templates, journal presets and theme helpers.

Two Plotly templates are registered on import of :mod:`plotlyvizpro`:

``pvp_light``
    A restrained light template: recessive grid, thin marks, an accessible
    categorical palette (see :mod:`plotlyvizpro.colors`), sans-serif text.
``pvp_dark``
    The dark counterpart, with its own validated colour steps rather than an
    automatic inversion of the light palette.

Journal presets encode physical figure sizes (in inches at a given DPI) and
font sizes that common publishers require, so a figure can be exported with
``apply_journal_preset(fig, "nature_single")`` and land at the right size.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import plotly.graph_objects as go
import plotly.io as pio

from plotlyvizpro.colors import CATEGORICAL_DARK, CATEGORICAL_LIGHT

TemplateName = Literal["pvp_light", "pvp_dark", "plotly", "plotly_white", "plotly_dark", "simple_white"]

FONT_STACK = 'Inter, "Helvetica Neue", Helvetica, Arial, sans-serif'


@dataclass(frozen=True)
class JournalPreset:
    """Physical figure specification for a publisher.

    Attributes
    ----------
    width_in, height_in:
        Figure size in inches.
    dpi:
        Raster resolution used when exporting to PNG.
    font_size_pt:
        Base font size in points. Axis titles use this size; tick labels one point smaller.
    description:
        Human-readable provenance of the numbers.
    """

    width_in: float
    height_in: float
    dpi: int
    font_size_pt: float
    description: str

    @property
    def width_px(self) -> int:
        """Width in CSS pixels at 96 px/in (Plotly's layout unit)."""
        return round(self.width_in * 96)

    @property
    def height_px(self) -> int:
        """Height in CSS pixels at 96 px/in."""
        return round(self.height_in * 96)

    @property
    def scale(self) -> float:
        """Raster scale factor that turns 96 px/in layout pixels into ``dpi``."""
        return self.dpi / 96


JOURNAL_PRESETS: dict[str, JournalPreset] = {
    "nature_single": JournalPreset(3.5, 2.6, 300, 7, "Nature single column: 89 mm wide, 5-7 pt text"),
    "nature_double": JournalPreset(7.2, 4.5, 300, 7, "Nature double column: 183 mm wide"),
    "ieee_single": JournalPreset(3.5, 2.5, 300, 8, "IEEE single column: 3.5 in wide, 8 pt text"),
    "ieee_double": JournalPreset(7.16, 4.0, 300, 8, "IEEE double column: 7.16 in wide"),
    "elsevier_single": JournalPreset(3.54, 2.7, 300, 8, "Elsevier single column: 90 mm wide"),
    "elsevier_double": JournalPreset(7.48, 4.5, 300, 8, "Elsevier double column: 190 mm wide"),
    "plos": JournalPreset(5.2, 3.9, 300, 8, "PLOS: 13.2 cm max width, 8-12 pt text"),
    "acm_single": JournalPreset(3.33, 2.5, 300, 8, "ACM single column: 3.33 in wide"),
    "poster": JournalPreset(10.0, 7.5, 200, 18, "Conference poster panel"),
    "slide_16_9": JournalPreset(13.33, 7.5, 150, 16, "16:9 slide at 150 dpi"),
}


def _base_layout(paper: str, plot: str, ink: str, grid: str, colorway: tuple[str, ...]) -> go.Layout:
    return go.Layout(
        font={"family": FONT_STACK, "size": 13, "color": ink},
        title={"x": 0.0, "xanchor": "left", "font": {"size": 16}},
        paper_bgcolor=paper,
        plot_bgcolor=plot,
        colorway=list(colorway),
        hovermode="x unified",
        hoverlabel={"font": {"family": FONT_STACK, "size": 12}},
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "left", "x": 0, "title": {"text": ""}},
        margin={"l": 56, "r": 24, "t": 64, "b": 48},
        xaxis={
            "showgrid": False,
            "zeroline": False,
            "showline": True,
            "linecolor": grid,
            "ticks": "outside",
            "tickcolor": grid,
        },
        yaxis={"showgrid": True, "gridcolor": grid, "gridwidth": 1, "zeroline": False, "showline": False, "ticks": ""},
    )


def build_templates() -> dict[str, go.layout.Template]:
    """Return the project templates keyed by name (without registering them)."""
    light = go.layout.Template(layout=_base_layout("#fcfcfb", "#fcfcfb", "#1f1f1e", "#e4e4e1", CATEGORICAL_LIGHT))
    light.data.scatter = [go.Scatter(line={"width": 2}, marker={"size": 8})]
    light.data.bar = [go.Bar(marker={"line": {"width": 1, "color": "#fcfcfb"}})]

    dark = go.layout.Template(layout=_base_layout("#1a1a19", "#1a1a19", "#f2f2f0", "#333331", CATEGORICAL_DARK))
    dark.data.scatter = [go.Scatter(line={"width": 2}, marker={"size": 8})]
    dark.data.bar = [go.Bar(marker={"line": {"width": 1, "color": "#1a1a19"}})]
    return {"pvp_light": light, "pvp_dark": dark}


def register_templates(*, set_default: bool = False) -> None:
    """Register ``pvp_light`` and ``pvp_dark`` with :mod:`plotly.io`.

    Parameters
    ----------
    set_default:
        When ``True``, ``pvp_light`` becomes ``pio.templates.default``.
    """
    for name, template in build_templates().items():
        pio.templates[name] = template
    if set_default:
        pio.templates.default = "pvp_light"


def apply_theme(template: str = "pvp_light", font_family: str | None = None, font_size: int | None = None) -> str:
    """Set the global Plotly default template and optionally override fonts.

    Unlike the historical implementation this does **not** mutate the built-in
    Plotly templates in place: overrides are written to a derived template named
    ``"<template>_pvp_font"`` so repeated calls are idempotent.

    Returns
    -------
    str
        The name of the template that is now the default.
    """
    if template not in pio.templates:
        raise ValueError(f"Unknown template {template!r}. Registered: {list(pio.templates)}")
    if font_family is None and font_size is None:
        pio.templates.default = template
        return template

    derived_name = f"{template}_pvp_font"
    derived = go.layout.Template(pio.templates[template].to_plotly_json())
    if font_family is not None:
        derived.layout.font.family = font_family
    if font_size is not None:
        derived.layout.font.size = font_size
    pio.templates[derived_name] = derived
    pio.templates.default = derived_name
    return derived_name


def apply_dark_theme(
    fig: go.Figure,
    paper_bgcolor: str = "#1a1a19",
    plot_bgcolor: str = "#1a1a19",
    font_color: str = "#f2f2f0",
) -> go.Figure:
    """Switch an existing figure to the dark template and surface colours."""
    fig.update_layout(
        template="pvp_dark", paper_bgcolor=paper_bgcolor, plot_bgcolor=plot_bgcolor, font={"color": font_color}
    )
    fig.update_xaxes(linecolor="#333331", tickcolor="#333331")
    fig.update_yaxes(gridcolor="#333331")
    return fig


def apply_journal_preset(fig: go.Figure, preset: str | JournalPreset, *, font_family: str | None = None) -> go.Figure:
    """Resize and re-font a figure for a publisher's physical column width.

    The figure's ``layout.width``/``layout.height`` are set in CSS pixels at
    96 px/in; :func:`plotlyvizpro.export.save_image` reads the preset's
    ``scale`` back from ``fig.layout.meta`` so the raster lands at the right DPI.
    """
    spec = JOURNAL_PRESETS[preset] if isinstance(preset, str) else preset
    fig.update_layout(
        width=spec.width_px,
        height=spec.height_px,
        font={"size": spec.font_size_pt * 96 / 72, **({"family": font_family} if font_family else {})},
        margin={"l": 48, "r": 12, "t": 32, "b": 40},
        title={"font": {"size": (spec.font_size_pt + 1) * 96 / 72}},
    )
    meta = dict(fig.layout.meta or {})
    meta["journal_preset"] = {
        "name": preset if isinstance(preset, str) else "custom",
        "dpi": spec.dpi,
        "scale": spec.scale,
        "width_in": spec.width_in,
        "height_in": spec.height_in,
    }
    fig.update_layout(meta=meta)
    return fig
