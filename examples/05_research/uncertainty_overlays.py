"""Research: OLS with confidence/prediction bands, LOWESS and per-group bootstrap CIs.

Run:  python examples/05_research/uncertainty_overlays.py
Writes HTML (and PNG if kaleido is installed) into the export directory.
"""

from functools import partial

import plotlyvizpro as pvp
from plotlyvizpro.data import load
from plotlyvizpro.export import save_figure
from plotlyvizpro.overlays import add_bootstrap_errorbars, add_lowess, add_trendline
from plotlyvizpro.stats import ols_fit

df = load("superstore")
daily = df.groupby("OrderDate")["Sales"].sum().reset_index()
x, y = daily["OrderDate"], daily["Sales"]

fit = ols_fit(x, y)
print(f"{fit.equation()}   slope p = {fit.p_values[1]:.3g}   R² = {fit.r_squared:.3f}   n = {fit.dof + 2}")

fig = pvp.pipe(
    pvp.scatter_plot(daily, "OrderDate", "Sales", opacity=0.5, title="Daily sales with OLS 95 % CI / PI and LOWESS"),
    partial(add_trendline, x=x, y=y, show_ci=True, show_pi=True),
    partial(add_lowess, x=x, y=y, frac=0.2),
)
print(save_figure(fig, "research_uncertainty_daily", formats=("html", "png")))

groups = add_bootstrap_errorbars(
    pvp.create_figure(title="Mean profit by category, BCa 95 % bootstrap CI"), df["Profit"], df["Category"], seed=0
)
print(save_figure(groups, "research_bootstrap_groups", formats=("html", "png")))
