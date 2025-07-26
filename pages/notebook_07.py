# 📄 pages/notebook_07.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.plot_utils import (
    apply_theme,
    save_fig_as_html,
    save_fig_as_png,
)

# 🎨 Apply global theme
apply_theme("plotly_white")

# 🧭 Page Config
st.set_page_config(page_title="Notebook 07 – Graph Objects Deep Dive", layout="wide")
st.title("🧮 Notebook 07: Graph Objects Deep Dive")

# 📂 Load Data
df = pd.read_csv("datasets/superstore.csv")
df["OrderDate"] = pd.to_datetime(df["OrderDate"])
df["Month"] = df["OrderDate"].dt.to_period("M").astype(str)

# 📊 Aggregate Monthly Sales
monthly_sales = df.groupby("Month")["Sales"].sum().sort_index()

# 📘 Graph Object with Annotation
st.subheader("📈 Monthly Sales with Annotation")

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=monthly_sales.index,
        y=monthly_sales.values,
        mode="lines+markers",
        name="Sales",
        line=dict(color="royalblue"),
        marker=dict(size=6),
    )
)

# 📌 Add annotation for peak sales
max_idx = monthly_sales.idxmax()
max_val = monthly_sales.max()

fig.add_annotation(
    x=max_idx,
    y=max_val,
    text=f"📌 Peak: {max_val:.0f}",
    showarrow=True,
    arrowhead=2,
    ax=0,
    ay=-40,
    font=dict(color="darkred", size=12)
)

# 🎯 Layout + Line Shape
fig.update_layout(
    title="📈 Monthly Sales with Annotation",
    xaxis_title="Month",
    yaxis_title="Total Sales",
    shapes=[
        dict(
            type="line",
            x0=max_idx,
            y0=0,
            x1=max_idx,
            y1=max_val,
            line=dict(color="red", dash="dot"),
        )
    ],
    height=500,
)

# 🔍 Show Chart
st.plotly_chart(fig, use_container_width=True)

# 💾 Save Option
if st.sidebar.checkbox("Save Plot"):
    save_fig_as_html(fig, "graph_objects_annotations.html", notebook_name="notebook_07")
    save_fig_as_png(fig, "graph_objects_annotations.png", notebook_name="notebook_07")

st.success("✅ Notebook 07 Visualizations Rendered")
