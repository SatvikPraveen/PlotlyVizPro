# 📄 pages/notebook_09.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.plot_utils import (
    apply_theme,
    add_trendline,
    add_moving_average,
    add_zscore_band,
    create_subplots,
    add_trace_to_subplot,
    update_subplot_layout,
    save_fig_as_html,
    save_fig_as_png,
)

# 🎨 Apply global Plotly theme
apply_theme("plotly_white")

# 🧭 Page Config
st.set_page_config(page_title="Notebook 09 – Capstone Dashboard", layout="wide")
st.title("🧪 Notebook 09: Capstone – Sales & COVID Dashboard")

# 📂 Load Datasets
store_df = pd.read_csv("datasets/superstore.csv", parse_dates=["OrderDate"])
covid_df = pd.read_csv("datasets/covid_data.csv")

# --------------------------------
# 📈 Case 1: USA COVID Trend Line
# --------------------------------
usa_df = covid_df[covid_df["Country"] == "USA"].copy()
usa_df["Date"] = pd.to_datetime(usa_df["Date"])

fig_covid = go.Figure()
fig_covid.add_trace(go.Scatter(
    x=usa_df["Date"],
    y=usa_df["Cases"],
    name="Daily Cases",
    mode="lines",
    line=dict(color="orange")
))

ma_trace = add_moving_average(usa_df["Date"], usa_df["Cases"], window=7, name="7-Day Avg")
fig_covid.add_trace(ma_trace)
upper_band, lower_band = add_zscore_band(usa_df["Date"], usa_df["Cases"], z=1)

fig_covid.add_trace(go.Scatter(
    x=usa_df["Date"],
    y=upper_band,
    mode="lines",
    name="+1σ Band",
    line=dict(color="lightgray", dash="dash")
))

fig_covid.add_trace(go.Scatter(
    x=usa_df["Date"],
    y=lower_band,
    mode="lines",
    name="−1σ Band",
    line=dict(color="lightgray", dash="dash")
))

trend_trace = add_trendline(usa_df["Date"].map(pd.Timestamp.toordinal), usa_df["Cases"], name="Trend")
fig_covid.add_trace(trend_trace)


fig_covid.update_layout(
    title="🦠 COVID-19 Case Trends – USA",
    xaxis_title="Date",
    yaxis_title="Daily Cases"
)

# --------------------------------
# 📦 Case 2: Superstore KPI Dashboard
# --------------------------------
fig_kpi = create_subplots(rows=1, cols=2, subplot_titles=["Sales by Region", "Profit Distribution"])

# 📊 Region-wise Sales
sales_by_region = store_df.groupby("Region")["Sales"].sum().reset_index()
trace_sales = go.Bar(x=sales_by_region["Region"], y=sales_by_region["Sales"], name="Sales")
add_trace_to_subplot(fig_kpi, trace_sales, row=1, col=1)

# 📊 Profit Boxplot
trace_profit = go.Box(y=store_df["Profit"], name="Profit")
add_trace_to_subplot(fig_kpi, trace_profit, row=1, col=2)

update_subplot_layout(fig_kpi, title="📦 Superstore KPIs")

# --------------------------------
# 🖼️ Display All
# --------------------------------
st.subheader("1️⃣ COVID Trend – USA")
st.plotly_chart(fig_covid, use_container_width=True)

st.subheader("2️⃣ Superstore KPIs")
st.plotly_chart(fig_kpi, use_container_width=True)

# 💾 Save Option
if st.sidebar.checkbox("Save All Plots"):
    save_fig_as_html(fig_covid, "covid_usa_trends.html", notebook_name="notebook_09")
    save_fig_as_png(fig_covid, "covid_usa_trends.png", notebook_name="notebook_09")

    save_fig_as_html(fig_kpi, "superstore_kpi_dashboard.html", notebook_name="notebook_09")
    save_fig_as_png(fig_kpi, "superstore_kpi_dashboard.png", notebook_name="notebook_09")

st.success("✅ Notebook 09 – Capstone Dashboard Rendered")
