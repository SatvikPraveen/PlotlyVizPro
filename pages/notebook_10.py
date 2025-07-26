# 📄 pages/notebook_10.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.plot_utils import (
    apply_theme,
    add_trendline,
    add_moving_average,
    add_zscore_band,
    save_fig_as_html,
    save_fig_as_png
)

# 🎨 Apply global Plotly theme
apply_theme("plotly_white")

# 🧭 Page Config
st.set_page_config(page_title="Notebook 10 – Advanced Plotting Patterns", layout="wide")
st.title("🔬 Notebook 10: Advanced Plotting Patterns & Best Practices")

# 📂 Load Data
df = pd.read_csv("datasets/superstore.csv", parse_dates=["OrderDate"])
df = df.sort_values("OrderDate")
df["Sales"] = df["Sales"].fillna(0)

x = df["OrderDate"]
y = df["Sales"]

# ----------------------------
# 📈 Trendline + Moving Average
# ----------------------------
scatter = go.Scatter(x=x, y=y, mode="markers", name="Sales", marker=dict(size=4, color="gray"))
trend = add_trendline(x, y)
ma = add_moving_average(x, y, window=30)

fig1 = go.Figure([scatter, trend, ma])
fig1.update_layout(
    title="📈 Sales Over Time with Trendline & Moving Average",
    xaxis_title="Order Date",
    yaxis_title="Sales",
    height=500
)

# ----------------------------
# 📊 Z-Score Band Overlay
# ----------------------------
upper, lower = add_zscore_band(x, y, z=2)
band_upper = go.Scatter(x=x, y=upper, name="+2σ", mode="lines", line=dict(color="red", dash="dash"))
band_lower = go.Scatter(x=x, y=lower, name="-2σ", mode="lines", line=dict(color="red", dash="dash"))

fig2 = go.Figure([scatter, band_upper, band_lower])
fig2.update_layout(
    title="📊 Z-Score Confidence Bands (±2σ) on Sales",
    xaxis_title="Order Date",
    yaxis_title="Sales",
    height=500
)

# ----------------------------
# 🧩 Modular Chart (.pipe()-style)
# ----------------------------
def base_scatter(x, y, label="Sales"):
    return go.Scatter(x=x, y=y, mode="markers", name=label, marker=dict(size=4, color="navy"))

chart = go.Figure()
chart.add_trace(base_scatter(x, y))
chart.add_trace(add_moving_average(x, y, window=30))
chart.add_trace(add_trendline(x, y))

chart.update_layout(
    title="🧩 Modular Workflow: .pipe()-style Assembly",
    xaxis_title="Order Date",
    yaxis_title="Sales",
    height=500
)

# ----------------------------
# 🖼️ Display All
# ----------------------------
st.subheader("1️⃣ Trendline & Moving Average")
st.plotly_chart(fig1, use_container_width=True)

st.subheader("2️⃣ Z-Score Bands on Sales")
st.plotly_chart(fig2, use_container_width=True)

st.subheader("3️⃣ Modular Workflow Example")
st.plotly_chart(chart, use_container_width=True)

# 💾 Save Option
if st.sidebar.checkbox("Save All Plots"):
    save_fig_as_html(fig1, "sales_trend_ma.html", notebook_name="notebook_10")
    save_fig_as_png(fig1, "sales_trend_ma.png", notebook_name="notebook_10")

    save_fig_as_html(fig2, "sales_zscore_band.html", notebook_name="notebook_10")
    save_fig_as_png(fig2, "sales_zscore_band.png", notebook_name="notebook_10")

    save_fig_as_html(chart, "modular_workflow.html", notebook_name="notebook_10")
    save_fig_as_png(chart, "modular_workflow.png", notebook_name="notebook_10")

st.success("✅ Notebook 10 – Advanced Patterns Rendered")
