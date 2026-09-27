# Getting started

## Installation

```bash
git clone https://github.com/SatvikPraveen/PlotlyVizPro.git
cd PlotlyVizPro
make install-dev          # .venv with dev, docs and notebook extras + pre-commit
make check                # ruff, mypy --strict, pytest with coverage gate
```

Static image export (PNG/SVG/PDF) needs `kaleido` and a Chrome binary. On a
fresh machine run `kaleido_get_chrome` once, or `pip install "plotlyvizpro[export]"`
and let kaleido download it.

## Three entry points

1. **Library** – `import plotlyvizpro as pvp` in scripts and notebooks.
2. **Streamlit gallery** – `make run-app`. Pages 01-10 mirror the tutorial
   notebooks; pages 11-13 are interactive research tools (statistical lab,
   palette audit, downsampling comparison).
3. **CLI** – `plotlyvizpro --help`.

## Building a figure

Chart builders are thin, validated wrappers around Plotly Express that use the
project template `pvp_light` (or `pvp_dark`):

```python
fig = pvp.bar_plot(df, "Category", "Sales", color="Region", barmode="group", title="Sales by category")
```

A missing column raises `KeyError` with the available columns listed instead
of a cryptic Plotly error.

## Adding statistics

Every estimator in `plotlyvizpro.stats` is independent of plotting and returns
a dataclass you can inspect:

```python
from plotlyvizpro.stats import ols_fit, bootstrap_ci, hampel_filter

fit = ols_fit(daily["OrderDate"], daily["Sales"])
fit.slope, fit.p_values[1], fit.r_squared  # per-day slope for datetime x
ci = bootstrap_ci(daily["Sales"], method="bca", seed=0)
ci.lower, ci.upper
flags = hampel_filter(daily["Sales"], window=10)
flags.indices
```

The corresponding `overlays.add_*` function draws each result. Overlays add
new, labelled traces and never recolour what is already on the figure.

## Choosing colours

```python
from plotlyvizpro.colors import audit_palette, order_palette, simulate_cvd

report = audit_palette(["#2a78d6", "#eb6834", "#1baf7a"], mode="light", pairs="all")
print(report.to_text())
```

`pairs="all"` is the right check for scatter, bubble and map charts, where any
two marks can be neighbours; the default `adjacent` check is for bars, stacks
and lines.

## Exporting for a paper

```python
pvp.apply_journal_preset(fig, "nature_single")  # 89 mm wide, 7 pt text, 300 dpi
paths = pvp.save_figure(fig, "figure_2", formats=("pdf", "svg", "png", "json"))
```

`save_figure` writes a `figure_2.provenance.json` next to the images with the
package versions, git commit, platform and SHA-256 of any inputs you registered
via `Provenance.add_input`.

## Large series

```python
from plotlyvizpro.downsample import downsample

keep = downsample(x, y, threshold=4000, method="lttb")
fig = pvp.line_plot(df.iloc[keep], "x", "y")
```

The functions return indices so hover text and colour columns stay aligned.
