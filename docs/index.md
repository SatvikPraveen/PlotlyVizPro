# PlotlyVizPro

**A research-grade toolkit for interactive, publication-ready Plotly figures.**

PlotlyVizPro adds to Plotly the pieces a quantitative analyst needs and Plotly
leaves to the user: statistical overlays with honest uncertainty, palettes
that survive colour-vision deficiency, shape-preserving downsampling for
million-point series, and exports that carry their own provenance.

![Overlays demo](https://raw.githubusercontent.com/SatvikPraveen/PlotlyVizPro/main/exports/images/readme/overlays.png)

## Highlights

| Module | What it gives you |
|---|---|
| `plotlyvizpro.stats` | OLS with *t*-based confidence and prediction bands and coefficient p-values; robust LOWESS; percentile/basic/BCa bootstrap; z-score, IQR, Hampel and generalized-ESD anomaly detectors; KDE, ECDF with DKW band, Q-Q; classical seasonal decomposition; ACF |
| `plotlyvizpro.overlays` | One call to draw any of the above on an existing figure, chainable with `pipe` |
| `plotlyvizpro.colors` | OKLab/OKLCH conversions, Machado-2009 CVD simulation, WCAG contrast, a five-check palette audit, CVD-optimal ordering, one-hue sequential ramps |
| `plotlyvizpro.downsample` | LTTB, MinMax and M4 returning indices, plus a max-error metric |
| `plotlyvizpro.export` / `provenance` | HTML, PNG, SVG, PDF and JSON writers; journal size presets (Nature, IEEE, Elsevier, PLOS, ACM); SHA-256 of inputs, package versions and git commit stored on the figure and in a sidecar |
| `plotlyvizpro.data` / `datasets` | Seeded synthetic datasets with a checksum manifest |
| `plotlyvizpro` CLI | `info`, `generate-data`, `verify-data`, `audit-palette`, `demo`, `benchmark` |

## Install

```bash
pip install "plotlyvizpro[all] @ git+https://github.com/SatvikPraveen/PlotlyVizPro"
# or, from a clone
pip install -e ".[all]"
```

The core package depends only on NumPy, pandas, SciPy and Plotly. Extras:
`export` (kaleido), `app` (Streamlit), `data` (Faker, optional), `notebooks`,
`ml` (scikit-learn, statsmodels for cross-validation), `dev`, `docs`.

## Thirty-second tour

```python
from functools import partial
import plotlyvizpro as pvp
from plotlyvizpro.overlays import add_trendline, add_lowess, add_anomalies
from plotlyvizpro.data import load

df = load("superstore")  # schema + SHA-256 verified
daily = df.groupby("OrderDate")["Sales"].sum().reset_index()

fig = pvp.pipe(
    pvp.scatter_plot(daily, "OrderDate", "Sales", opacity=0.5),
    partial(add_trendline, x=daily["OrderDate"], y=daily["Sales"], show_ci=True),
    partial(add_lowess, x=daily["OrderDate"], y=daily["Sales"], frac=0.2),
    partial(add_anomalies, x=daily["OrderDate"], y=daily["Sales"], method="hampel"),
)
pvp.apply_journal_preset(fig, "ieee_single")
pvp.save_figure(fig, "daily_sales", formats=("html", "png", "svg"))  # + provenance sidecar
```

Continue with [Getting started](getting-started.md), the [Methods](methods.md)
write-up, or the API reference.
