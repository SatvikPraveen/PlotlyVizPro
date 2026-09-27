"""PlotlyVizPro: a research-grade toolkit for interactive, publication-ready Plotly figures.

The package is organised by concern:

- :mod:`plotlyvizpro.charts` -- typed builders for common chart forms (Plotly Express based).
- :mod:`plotlyvizpro.layout` -- subplots, dropdowns, sliders, annotations, graph-object helpers.
- :mod:`plotlyvizpro.theme` -- registered project templates, journal presets, font handling.
- :mod:`plotlyvizpro.colors` -- colour-vision-deficiency simulation and palette auditing.
- :mod:`plotlyvizpro.stats` -- statistical estimators (regression, LOWESS, bootstrap,
  anomaly detection, distributions, seasonal decomposition) with no plotting dependency.
- :mod:`plotlyvizpro.overlays` -- figure-level overlays that draw the estimators above.
- :mod:`plotlyvizpro.downsample` -- LTTB / MinMax / M4 downsampling for large series.
- :mod:`plotlyvizpro.export` -- HTML / PNG / SVG / PDF / JSON export with provenance.
- :mod:`plotlyvizpro.provenance` -- reproducibility metadata capture.
- :mod:`plotlyvizpro.data` -- dataset loading, schema validation and checksum manifest.

Every public function is typed, documented and unit-tested.
"""

from __future__ import annotations

from plotlyvizpro._version import __version__
from plotlyvizpro.charts import (
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
from plotlyvizpro.export import (
    save_figure,
    save_html,
    save_image,
    save_json,
)
from plotlyvizpro.layout import (
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
from plotlyvizpro.theme import (
    JOURNAL_PRESETS,
    apply_dark_theme,
    apply_journal_preset,
    apply_theme,
    register_templates,
)

__all__ = [
    "JOURNAL_PRESETS",
    "__version__",
    "add_annotation",
    "add_dropdown",
    "add_shape",
    "add_slider",
    "add_trace",
    "animated_plot",
    "apply_dark_theme",
    "apply_journal_preset",
    "apply_theme",
    "bar_plot",
    "box_plot",
    "bubble_plot",
    "choropleth_map",
    "create_figure",
    "create_subplots",
    "density_contour",
    "density_heatmap",
    "histogram_plot",
    "line_plot",
    "pie_chart",
    "register_templates",
    "save_figure",
    "save_html",
    "save_image",
    "save_json",
    "scatter_geo",
    "scatter_map",
    "scatter_plot",
    "set_margins",
    "update_layout",
    "violin_plot",
]

register_templates()
