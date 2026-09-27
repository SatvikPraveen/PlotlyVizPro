"""PlotlyVizPro gallery: landing page."""

from __future__ import annotations

from functools import partial

import streamlit as st

import plotlyvizpro as pvp
from plotlyvizpro.colors import audit_palette
from plotlyvizpro.overlays import add_anomalies, add_lowess, add_trendline
from plotlyvizpro.provenance import package_versions
from utils.streamlit_utils import load_dataset

st.set_page_config(page_title="PlotlyVizPro", page_icon="📊", layout="wide")

st.title("PlotlyVizPro")
st.caption(
    f"v{pvp.__version__} · research-grade Plotly toolkit: "
    "statistical overlays, CVD-safe palettes, downsampling, provenance"
)

left, right = st.columns([3, 2])
with left:
    st.markdown(
        """
        **What is in the box**

        - `plotlyvizpro.stats` – OLS with confidence/prediction bands, robust LOWESS, bootstrap (BCa),
          anomaly detectors (z-score, IQR, Hampel, generalized ESD), KDE/ECDF/Q-Q, seasonal decomposition.
        - `plotlyvizpro.overlays` – draw any of the above on a figure with one call.
        - `plotlyvizpro.colors` – OKLab/OKLCH, Machado-2009 colour-vision-deficiency simulation, palette audit.
        - `plotlyvizpro.downsample` – LTTB, MinMax and M4 for million-point series.
        - `plotlyvizpro.export` – HTML/PNG/SVG/PDF/JSON with a provenance sidecar; journal size presets.

        Use the **sidebar** to open the notebook galleries (01-10) and the interactive research pages.
        """
    )
with right:
    st.markdown("**Environment**")
    st.json({"plotlyvizpro": pvp.__version__, **package_versions()}, expanded=False)
    report = audit_palette(pvp.theme.CATEGORICAL_LIGHT)
    st.markdown(
        f"Default palette audit: **{'PASS' if report.ok else 'FAIL'}** · worst CVD ΔE {report.worst_cvd_delta_e:.1f}"
    )

st.subheader("Live demo: daily sales with OLS band, LOWESS and Hampel anomalies")
df = load_dataset("superstore")
daily = df.groupby("OrderDate")["Sales"].sum().reset_index()
fig = pvp.pipe(
    pvp.scatter_plot(daily, "OrderDate", "Sales", opacity=0.55, title=""),
    partial(add_trendline, x=daily["OrderDate"], y=daily["Sales"], show_ci=True),
    partial(add_lowess, x=daily["OrderDate"], y=daily["Sales"], frac=0.2),
    partial(add_anomalies, x=daily["OrderDate"], y=daily["Sales"], method="hampel", window=10),
)
fig.update_layout(height=480)
st.plotly_chart(fig, use_container_width=True)
ols = fig.layout.meta["ols"]
st.caption(
    f"OLS slope {ols['coef'][1]:.3g} per day (p = {ols['p_values'][1]:.2g}), R² = {ols['r_squared']:.3f}; "
    f"{len(fig.layout.meta['anomalies']['indices'])} Hampel anomalies flagged."
)
