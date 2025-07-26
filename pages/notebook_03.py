# 📄 pages/notebook_03.py
import streamlit as st
import pandas as pd
from utils.plot_utils import (
    histogram_plot,
    density_heatmap,
    density_contour,
    apply_theme,
    save_fig_as_html,
    save_fig_as_png
)

# 🎨 Apply global theme
apply_theme("plotly_white")

# ⚙️ Page Config
st.set_page_config(page_title="Notebook 03 – Histogram & Heatmap", layout="wide")
st.title("📈 Notebook 03: Histogram, KDE, Heatmap")

# 📂 Load Data
df = pd.read_csv("datasets/superstore.csv")

# 🎛️ Sidebar Controls
st.sidebar.header("Filter Controls")
selected_category = st.sidebar.selectbox("Select Product Category", df["Category"].unique())
selected_measure = st.sidebar.radio("Select Numerical Measure", ["Profit", "Sales"])  # 🔧 Removed 'Quantity'

filtered_df = df[df["Category"] == selected_category]

# 📊 Histogram – Selected Measure
st.subheader(f"1️⃣ Histogram of {selected_measure} – {selected_category}")
fig1 = histogram_plot(filtered_df, x=selected_measure, nbins=50, title=f"{selected_measure} Distribution")
st.plotly_chart(fig1, use_container_width=True)

# 📘 Histogram – By Category (Overlayed)
st.subheader("2️⃣ Profit Distribution by Category (Overlayed)")
fig2 = histogram_plot(df, x="Profit", color="Category", nbins=50, barmode="overlay", title="Profit by Category (Overlay)")
st.plotly_chart(fig2, use_container_width=True)

# 🌈 Density Heatmap – Sales vs Profit
st.subheader("3️⃣ Density Heatmap – Sales vs Profit")
fig3 = density_heatmap(df, x="Sales", y="Profit", title="Sales vs Profit Density Heatmap")
st.plotly_chart(fig3, use_container_width=True)

# 📈 Density Contour Plot
st.subheader("4️⃣ KDE-style Density Contour – Sales vs Profit")
fig4 = density_contour(df, x="Sales", y="Profit", title="Sales vs Profit Density Contour")
st.plotly_chart(fig4, use_container_width=True)

# 💾 Save Plots
if st.sidebar.checkbox("💾 Save All Plots"):
    save_fig_as_html(fig1, "histogram_selected_measure.html", notebook_name="notebook_03")
    save_fig_as_png(fig1, "histogram_selected_measure.png", notebook_name="notebook_03")

    save_fig_as_html(fig2, "profit_hist_by_category.html", notebook_name="notebook_03")
    save_fig_as_png(fig2, "profit_hist_by_category.png", notebook_name="notebook_03")

    save_fig_as_html(fig3, "sales_profit_density_heatmap.html", notebook_name="notebook_03")
    save_fig_as_png(fig3, "sales_profit_density_heatmap.png", notebook_name="notebook_03")

    save_fig_as_html(fig4, "sales_profit_density_contour.html", notebook_name="notebook_03")
    save_fig_as_png(fig4, "sales_profit_density_contour.png", notebook_name="notebook_03")

    st.success("✅ All plots saved to `exports/` folders")

# ✅ Footer
st.success("✅ Notebook 03 Visualizations Rendered")
