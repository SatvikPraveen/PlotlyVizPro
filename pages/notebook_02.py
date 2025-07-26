# 📄 pages/notebook_02.py
import streamlit as st
import pandas as pd
from utils.plot_utils import (
    bar_plot,
    pie_chart,
    box_plot,
    apply_theme,
    save_fig_as_html,
    save_fig_as_png
)

# 🎨 Theme Setup
apply_theme("plotly_white")

# ⚙️ Page Settings
st.set_page_config(page_title="Notebook 02 – Bar, Pie, Box", layout="wide")
st.title("📊 Notebook 02: Bar, Pie & Box Plots")

# 📊 Load Dataset
df = pd.read_csv("datasets/superstore.csv")

# 📘 Bar Plot – Total Sales by Category
bar_df = df.groupby("Category")["Sales"].sum().reset_index()
fig1 = bar_plot(bar_df, x="Category", y="Sales", title="Total Sales by Category")
st.subheader("1️⃣ Sales by Category")
st.plotly_chart(fig1, use_container_width=True)

# 📘 Grouped Bar – SubCategory vs Region (Grouped)
group_df = df.groupby(["SubCategory", "Region"])["Sales"].sum().reset_index()
fig2 = bar_plot(group_df, x="SubCategory", y="Sales", color="Region", barmode="group", title="SubCategory Sales by Region (Grouped)")
st.subheader("2️⃣ Grouped Sales by SubCategory & Region")
st.plotly_chart(fig2, use_container_width=True)

# 📘 Stacked Bar – SubCategory vs Region (Stacked)
fig3 = bar_plot(group_df, x="SubCategory", y="Sales", color="Region", barmode="stack", title="SubCategory Sales by Region (Stacked)")
st.subheader("3️⃣ Stacked Sales by SubCategory & Region")
st.plotly_chart(fig3, use_container_width=True)

# 🥧 Pie Chart – Region Sales Share
pie_df = df.groupby("Region")["Sales"].sum().reset_index()
fig4 = pie_chart(pie_df, names="Region", values="Sales", title="Sales Share by Region")
st.subheader("4️⃣ Sales Distribution by Region (Pie)")
st.plotly_chart(fig4, use_container_width=True)

# 📦 Box Plot – Profit Distribution by Category
fig5 = box_plot(df, x="Category", y="Profit", color="Category", title="Profit Distribution by Category")
st.subheader("5️⃣ Profit Distribution per Category")
st.plotly_chart(fig5, use_container_width=True)

# 💾 Save All
if st.sidebar.checkbox("💾 Save All Plots"):
    save_fig_as_html(fig1, "sales_by_category.html", notebook_name="notebook_02")
    save_fig_as_png(fig1, "sales_by_category.png", notebook_name="notebook_02")

    save_fig_as_html(fig2, "subcat_sales_by_region_grouped.html", notebook_name="notebook_02")
    save_fig_as_png(fig2, "subcat_sales_by_region_grouped.png", notebook_name="notebook_02")

    save_fig_as_html(fig3, "subcat_sales_by_region_stacked.html", notebook_name="notebook_02")
    save_fig_as_png(fig3, "subcat_sales_by_region_stacked.png", notebook_name="notebook_02")

    save_fig_as_html(fig4, "sales_share_pie_region.html", notebook_name="notebook_02")
    save_fig_as_png(fig4, "sales_share_pie_region.png", notebook_name="notebook_02")

    save_fig_as_html(fig5, "profit_boxplot_by_category.html", notebook_name="notebook_02")
    save_fig_as_png(fig5, "profit_boxplot_by_category.png", notebook_name="notebook_02")

    st.success("✅ All plots saved to `exports/`")

st.success("✅ Notebook 02 Visualizations Rendered")
