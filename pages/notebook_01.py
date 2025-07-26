# 📄 pages/notebook_01.py
import streamlit as st
import pandas as pd
from utils.plot_utils import (
    line_plot,
    scatter_plot,
    bubble_plot,
    apply_custom_layout,
    apply_dark_theme,
    apply_theme,
    save_fig_as_html,
    save_fig_as_png,
)

# 🎨 Apply default theme
apply_theme("plotly_white")

# ⚙️ Page config
st.set_page_config(page_title="Notebook 01 – Line, Scatter, Bubble", layout="wide")
st.title("📈 Notebook 01: Line, Scatter & Bubble Visualizations")

# 📊 Load Dataset
df = pd.read_csv("datasets/superstore.csv", parse_dates=["OrderDate"])
df.sort_values("OrderDate", inplace=True)

# 📌 Aggregated for Line Plot
line_df = df.groupby("OrderDate")["Sales"].sum().reset_index()
region_df = df.groupby(["OrderDate", "Region"])["Sales"].sum().reset_index()

# 📈 Line Plot – Total Sales
fig1 = line_plot(line_df, x="OrderDate", y="Sales", title="Total Sales Over Time")
st.subheader("1️⃣ Total Sales Over Time")
st.plotly_chart(fig1, use_container_width=True)

# 📈 Line Plot – Region Breakdown
fig2 = line_plot(region_df, x="OrderDate", y="Sales", color="Region", title="Regional Sales Trends")
st.subheader("2️⃣ Regional Sales Trends")
st.plotly_chart(fig2, use_container_width=True)

# 📍 Scatter Plot – Profit vs Sales by SubCategory
agg_df = df.groupby("SubCategory")[["Sales", "Profit"]].sum().reset_index()
fig3 = scatter_plot(
    agg_df, x="Sales", y="Profit",
    hover_name="SubCategory",
    title="Profit vs Sales by SubCategory"
)
st.subheader("3️⃣ Profit vs Sales (Scatter)")
st.plotly_chart(fig3, use_container_width=True)

# 🔵 Bubble Plot
df_count = df.groupby("SubCategory").agg({
    "Sales": "sum", "Profit": "sum", "OrderID": "count"
}).reset_index().rename(columns={"OrderID": "Orders"})

fig4 = bubble_plot(
    df_count,
    x="Sales", y="Profit",
    size="Orders", color="SubCategory",
    title="Sales vs Profit by SubCategory with Order Volume"
)
st.subheader("4️⃣ Bubble Plot with Order Volume")
st.plotly_chart(fig4, use_container_width=True)

# 🌒 Dark Theme Plot
fig5 = line_plot(region_df, x="OrderDate", y="Sales", color="Region")
fig5 = apply_custom_layout(
    fig5,
    title="💰 Regional Sales Trend Over Time (Dark)",
    xaxis_title="Date", yaxis_title="Sales in USD",
    legend_title="Region"
)
fig5 = apply_dark_theme(fig5)
st.subheader("5️⃣ Dark Theme Regional Sales")
st.plotly_chart(fig5, use_container_width=True)

# 💾 Save all plots
if st.sidebar.checkbox("💾 Save All Plots"):
    save_fig_as_html(fig1, "total_sales_over_time.html", notebook_name="notebook_01")
    save_fig_as_png(fig1, "total_sales_over_time.png", notebook_name="notebook_01")

    save_fig_as_html(fig2, "regional_sales_trend.html", notebook_name="notebook_01")
    save_fig_as_png(fig2, "regional_sales_trend.png", notebook_name="notebook_01")

    save_fig_as_html(fig3, "profit_vs_sales_scatter.html", notebook_name="notebook_01")
    save_fig_as_png(fig3, "profit_vs_sales_scatter.png", notebook_name="notebook_01")

    save_fig_as_html(fig4, "bubble_sales_profit_orders.html", notebook_name="notebook_01")
    save_fig_as_png(fig4, "bubble_sales_profit_orders.png", notebook_name="notebook_01")

    save_fig_as_html(fig5, "regional_sales_dark.html", notebook_name="notebook_01")
    save_fig_as_png(fig5, "regional_sales_dark.png", notebook_name="notebook_01")

    st.success("✅ All plots saved to exports/")

st.success("✅ Notebook 01 Visualizations Rendered")
