# Tutorials

Worked, copy-pasteable walkthroughs. Each assumes `pip install -e ".[all]"` and
runs from the repository root. The notebooks in `notebooks/` cover chart forms
(01-10); these tutorials cover the research features.

## 1. A trend you can defend

```python
from functools import partial
import plotlyvizpro as pvp
from plotlyvizpro.data import load
from plotlyvizpro.overlays import add_trendline, add_lowess
from plotlyvizpro.stats import ols_fit

covid = load("covid")
usa = covid[covid["Country"] == "USA"]
x, y = usa["Date"], usa["Cases"]

fit = ols_fit(x, y)
print(fit.equation(), f"slope p = {fit.p_values[1]:.3g}", f"R² = {fit.r_squared:.3f}")

fig = pvp.pipe(
    pvp.line_plot(usa, "Date", "Cases", title="USA cumulative cases"),
    partial(add_trendline, x=x, y=y, show_ci=True, show_pi=True),
    partial(add_lowess, x=x, y=y, frac=0.15),
)
fig.show()
```

The confidence band is for the *mean* response; the prediction band is for a
*new* observation. Both use the *t* distribution with `fit.dof` degrees of freedom.

## 2. Group means with bootstrap error bars

```python
from plotlyvizpro.overlays import add_bootstrap_errorbars
from plotlyvizpro.stats import bootstrap_groups

store = load("superstore")
cis = bootstrap_groups(store["Profit"], store["Category"], method="bca", seed=0)
for k, r in cis.items():
    print(f"{k:16s} {r.estimate:8.2f}  [{r.lower:8.2f}, {r.upper:8.2f}]")

fig = add_bootstrap_errorbars(
    pvp.create_figure(title="Mean profit by category (BCa 95 %)"), store["Profit"], store["Category"], seed=0
)
fig.show()
```

## 3. Finding anomalies in a drifting series

```python
from plotlyvizpro.overlays import add_anomalies

stocks = load("stocks")
alpha = stocks[stocks["Company"] == "AlphaCorp"]
fig = pvp.line_plot(alpha, "Date", "Close", title="AlphaCorp close")
add_anomalies(fig, alpha["Date"], alpha["Close"], method="hampel", window=7, n_sigmas=3, show_bounds=True)
add_anomalies(fig, alpha["Date"], alpha["Close"], method="esd", max_outliers=5, color="#4a3aa7", name="ESD")
fig.show()
print(fig.layout.meta["anomalies"])
```

Hampel compares each point with its local median; ESD is global with a
controlled false-positive rate. Disagreement between them is informative.

## 4. Seasonality

```python
import numpy as np, pandas as pd
from plotlyvizpro.overlays import decomposition_figure, acf_figure
from plotlyvizpro.stats import seasonal_decompose

t = np.arange(96)
y = 100 + 0.5 * t + 12 * np.sin(2 * np.pi * t / 12) + np.random.default_rng(1).normal(0, 3, 96)
dates = pd.date_range("2018-01-01", periods=96, freq="MS")

dec = seasonal_decompose(y, period=12)
print(f"seasonal strength {dec.seasonal_strength:.2f}, trend strength {dec.trend_strength:.2f}")
decomposition_figure(dates, y, period=12).show()
acf_figure(dec.residual[~np.isnan(dec.residual)], max_lag=24).show()
```

## 5. Auditing your brand palette

```python
from plotlyvizpro.colors import audit_palette, order_palette, sequential_scale

brand = ["#0b5fff", "#ff6b00", "#00a878", "#ffc400", "#d62864"]
print(audit_palette(brand, mode="light").to_text())
print("better order:", order_palette(brand))
print("blue ramp:", sequential_scale("#0b5fff", steps=6))
```

Fix a FAIL by nudging one colour's OKLCH lightness (hold the hue) and re-run;
a WARN on contrast is acceptable only with direct labels or a table view.

## 6. Two million points

```python
import numpy as np, plotly.graph_objects as go
from plotlyvizpro.downsample import lttb, max_error

n = 2_000_000
x = np.arange(n, dtype=float)
y = np.cumsum(np.random.default_rng(0).normal(size=n))
keep = lttb(x, y, 5000)
print(f"kept {keep.size}, max error {max_error(x, y, keep):.2f}")
fig = pvp.create_figure(title="2 M points, LTTB → 5 000")
fig.add_trace(go.Scatter(x=x[keep], y=y[keep], mode="lines"))
fig.show()
```

## 7. Figure for a paper, with provenance

```python
from plotlyvizpro.provenance import Provenance

fig = pvp.box_plot(store, "Category", "Sales", notched=True, title="Sales by category")
pvp.apply_journal_preset(fig, "elsevier_single")
rec = Provenance(parameters={"notched": True}).add_input("superstore", store)
paths = pvp.save_figure(fig, "fig_sales_by_category", formats=("pdf", "svg", "png", "json"), provenance=rec)
print(paths)
```

## 8. Migrating from `utils.plot_utils`

Old notebook code keeps working, but new code should import from the package:

| old | new |
|---|---|
| `from utils.plot_utils import line_plot` | `from plotlyvizpro import line_plot` |
| `apply_custom_layout(fig, ...)` | `update_layout(fig, ...)` |
| `create_go_figure()` | `create_figure()` |
| `add_trace_go`, `add_trace_to_subplot` | `add_trace(fig, trace, row=, col=)` |
| `add_trendline(x, y)` (trace) | `overlays.add_trendline(fig, x, y)` |
| `add_zscore_band(x, y, z)` (arrays) | `overlays.add_zscore_band(fig, x, y, z=)` |
| `scatter_mapbox(..., token=)` | `scatter_map(...)` (no token) |
| `save_fig_as_html(fig, name, nb)` | `save_figure(fig, stem, formats=("html",))` |
