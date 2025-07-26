# 📄 pages/notebook_06.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.plot_utils import (
    apply_theme,
    create_subplots,
    add_trace_to_subplot,
    update_subplot_layout,
    apply_dashboard_margins,
    save_fig_as_html,
    save_fig_as_png
)

# 🎨 Apply Theme
apply_theme("plotly_white")

# 🧭 Page Config
st.set_page_config(page_title="Notebook 06 – Subplots & Dashboards", layout="wide")
st.title("🧩 Notebook 06: Subplots and Dashboards")

# 📂 Load Data
store_df = pd.read_csv("datasets/superstore.csv")
world_df = pd.read_csv("datasets/world_population.csv")

# 📊 Dashboard 1 – 2x2 Layout
st.subheader("📊 2x2 Subplot Dashboard: Sales, Profit & Global Metrics")

fig1 = create_subplots(
    rows=2,
    cols=2,
    subplot_titles=[
        "Sales by Category",
        "Profit Distribution (Box)",
        "GDP per Capita by Country",
        "Life Expectancy Distribution"
    ]
)

# Top-left: Sales by Category
bar_data = store_df.groupby("Category")["Sales"].sum().reset_index()
trace1 = go.Bar(x=bar_data["Category"], y=bar_data["Sales"], name="Sales")
add_trace_to_subplot(fig1, trace1, row=1, col=1)

# Top-right: Profit Box
trace2 = go.Box(x=store_df["Category"], y=store_df["Profit"], name="Profit")
add_trace_to_subplot(fig1, trace2, row=1, col=2)

# Bottom-left: GDP Histogram
trace3 = go.Histogram(x=world_df["GDP_per_capita"], nbinsx=20, name="GDP")
add_trace_to_subplot(fig1, trace3, row=2, col=1)

# Bottom-right: Life Expectancy Violin Plot
trace4 = go.Violin(y=world_df["Life_Expectancy"], box_visible=True, meanline_visible=True, name="Life Exp")
add_trace_to_subplot(fig1, trace4, row=2, col=2)

fig1 = update_subplot_layout(fig1, title="📊 Dashboard: Sales, Profit, and Global Metrics", height=800)
fig1 = apply_dashboard_margins(fig1)
st.plotly_chart(fig1, use_container_width=True)

# 📘 Dashboard 2 – Shared X-Axis
st.subheader("📘 1×2 Subplot: Sales & Profit by SubCategory")

fig2 = create_subplots(
    rows=1,
    cols=2,
    subplot_titles=["Sales by SubCategory", "Profit by SubCategory"],
    shared_x=True,
    vertical_spacing=0.05,
    horizontal_spacing=0.15
)

bar_data2 = store_df.groupby("SubCategory")[["Sales", "Profit"]].sum().reset_index()

trace1 = go.Bar(x=bar_data2["SubCategory"], y=bar_data2["Sales"], name="Sales")
trace2 = go.Bar(x=bar_data2["SubCategory"], y=bar_data2["Profit"], name="Profit", marker_color="green")

add_trace_to_subplot(fig2, trace1, row=1, col=1)
add_trace_to_subplot(fig2, trace2, row=1, col=2)

fig2 = update_subplot_layout(fig2, title="📈 SubCategory KPIs – Shared X & Custom Spacing", width=1000)
fig2 = apply_dashboard_margins(fig2, l=30, r=30, t=60, b=40)
st.plotly_chart(fig2, use_container_width=True)

# 💾 Save Option
if st.sidebar.checkbox("💾 Save Dashboards"):
    save_fig_as_html(fig1, "dashboard_sales_global.html", notebook_name="notebook_06")
    save_fig_as_png(fig1, "dashboard_sales_global.png", notebook_name="notebook_06")
    save_fig_as_html(fig2, "subcategory_kpis_sharedx.html", notebook_name="notebook_06")
    save_fig_as_png(fig2, "subcategory_kpis_sharedx.png", notebook_name="notebook_06")
    st.success("✅ Dashboards saved to exports/ folders")

# ✅ Completion
st.success("✅ Notebook 06 Visualizations Rendered")
