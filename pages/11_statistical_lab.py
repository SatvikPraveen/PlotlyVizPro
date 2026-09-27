"""Interactive statistical overlays on any bundled dataset."""

from __future__ import annotations

from functools import partial

import pandas as pd
import streamlit as st

import plotlyvizpro as pvp
from plotlyvizpro import overlays
from plotlyvizpro.data import list_datasets
from plotlyvizpro.stats import bootstrap_ci, describe, ols_fit
from utils.streamlit_utils import categorical_columns, datetime_or_numeric_columns, load_dataset, numeric_columns

st.set_page_config(page_title="Statistical lab", layout="wide")
st.title("Statistical lab")
st.caption(
    "Pick a dataset and columns; every overlay below is computed by `plotlyvizpro.stats` "
    "and drawn by `plotlyvizpro.overlays`."
)

with st.sidebar:
    name = st.selectbox("Dataset", list_datasets(), index=list_datasets().index("superstore"))
    df = load_dataset(name)
    x_col = st.selectbox("x (ordered)", datetime_or_numeric_columns(df))
    y_col = st.selectbox("y (numeric)", [c for c in numeric_columns(df) if c != x_col])
    group_cols = categorical_columns(df)
    aggregate = st.checkbox("Aggregate y by x (sum)", value=name == "superstore")
    st.divider()
    st.markdown("**Overlays**")
    show_ols = st.checkbox("OLS trendline", True)
    degree = st.slider("polynomial degree", 1, 4, 1, disabled=not show_ols)
    show_pi = st.checkbox("prediction band", False, disabled=not show_ols)
    show_lowess = st.checkbox("LOWESS", True)
    frac = st.slider("LOWESS span", 0.05, 0.9, 0.3, 0.05, disabled=not show_lowess)
    show_ma = st.checkbox("Rolling mean", False)
    window = st.slider("window", 2, 60, 7, disabled=not show_ma)
    show_anom = st.checkbox("Anomalies", True)
    method = st.selectbox("detector", ["hampel", "zscore", "iqr", "esd"], disabled=not show_anom)

series = df.groupby(x_col, as_index=False)[y_col].sum() if aggregate else df[[x_col, y_col]].dropna().sort_values(x_col)
x, y = series[x_col], series[y_col]

steps = []
if show_ols:
    steps.append(partial(overlays.add_trendline, x=x, y=y, degree=degree, show_ci=True, show_pi=show_pi))
if show_lowess:
    steps.append(partial(overlays.add_lowess, x=x, y=y, frac=frac))
if show_ma:
    steps.append(partial(overlays.add_moving_average, x=x, y=y, window=window))
if show_anom:
    params = {"window": max(2, window // 2)} if method == "hampel" else {"max_outliers": 5} if method == "esd" else {}
    steps.append(partial(overlays.add_anomalies, x=x, y=y, method=method, show_bounds=method != "esd", **params))

fig = pvp.pipe(pvp.scatter_plot(series, x_col, y_col, opacity=0.6, title=f"{y_col} vs {x_col} ({name})"), *steps)
fig.update_layout(height=520)
st.plotly_chart(fig, use_container_width=True)

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("**Summary of y**")
    st.dataframe(pd.Series(describe(y)).rename("value").to_frame().style.format("{:.4g}"), use_container_width=True)
with c2:
    st.markdown("**OLS fit**")
    fit = ols_fit(x, y, degree=degree if show_ols else 1)
    st.code(fit.equation(), language=None)
    st.dataframe(
        pd.DataFrame(
            {"coef": fit.coef, "std err": fit.stderr, "p-value": fit.p_values},
            index=[f"β{i}" for i in range(fit.coef.size)],
        ).style.format("{:.4g}"),
        use_container_width=True,
    )
    st.caption(
        f"R² = {fit.r_squared:.4f}, adjusted R² = {fit.adj_r_squared:.4f}, "
        f"residual SE = {fit.residual_std:.4g}, dof = {fit.dof}"
    )
with c3:
    st.markdown("**Bootstrap 95% CI for the mean (BCa)**")
    boot = bootstrap_ci(y, n_resamples=2000, seed=0)
    st.metric("mean", f"{boot.estimate:.4g}", f"[{boot.lower:.4g}, {boot.upper:.4g}]", delta_color="off")
    if group_cols:
        gcol = st.selectbox("per-group error bars", group_cols)
        gfig = overlays.add_bootstrap_errorbars(
            pvp.create_figure(title=f"Mean {y_col} by {gcol}"), df[y_col], df[gcol], n_resamples=1000, seed=0
        )
        gfig.update_layout(height=300)
        st.plotly_chart(gfig, use_container_width=True)

st.subheader("Distribution diagnostics")
d1, d2, d3 = st.columns(3)
with d1:
    st.plotly_chart(
        overlays.add_kde(pvp.create_figure(title="Kernel density"), y).update_layout(height=320),
        use_container_width=True,
    )
with d2:
    st.plotly_chart(
        overlays.add_ecdf(pvp.create_figure(title="ECDF with 95% DKW band"), y).update_layout(height=320),
        use_container_width=True,
    )
with d3:
    st.plotly_chart(
        overlays.add_qq(pvp.create_figure(title="Normal Q-Q"), y).update_layout(height=320), use_container_width=True
    )
