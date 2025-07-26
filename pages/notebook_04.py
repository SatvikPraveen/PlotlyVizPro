# 📄 pages/notebook_04.py
import streamlit as st
import pandas as pd
from utils.plot_utils import (
    choropleth_map,
    scatter_geo,
    apply_theme,
    save_fig_as_html,
    save_fig_as_png
)

# 🎨 Apply Plotly theme
apply_theme("plotly_white")

# ⚙️ Page Config
st.set_page_config(page_title="Notebook 04 – Choropleth & Geo Maps", layout="wide")
st.title("🗺️ Notebook 04: Choropleth and Geographic Visualizations")

# 📂 Load Data
world_df = pd.read_csv("datasets/world_population.csv")
city_df = pd.read_csv("datasets/map_data.csv")

# 🎛️ Sidebar Interactivity
st.sidebar.header("Controls")
selected_metric = st.sidebar.selectbox("Choropleth Color Metric", ["GDP_per_capita", "Life_Expectancy"])
metric_title = {
    "GDP_per_capita": "World GDP per Capita (Synthetic Data)",
    "Life_Expectancy": "Life Expectancy by Country"
}[selected_metric]

# 🌍 Choropleth Map – Selected Metric
st.subheader(f"1️⃣ Choropleth Map – {selected_metric.replace('_', ' ').title()}")
fig1 = choropleth_map(
    world_df,
    locations="Country",
    color=selected_metric,
    locationmode="country names",
    title=metric_title
)
st.plotly_chart(fig1, use_container_width=True)

# 🌐 Scatter Geo – City Score
st.subheader("2️⃣ City-wise Score Map (Synthetic Data)")
fig2 = scatter_geo(
    city_df,
    lat="Latitude",
    lon="Longitude",
    color="Score",
    hover_name="City",
    size="Score",
    title="City-wise Synthetic Score (100 cities)"
)
st.plotly_chart(fig2, use_container_width=True)

# 💾 Save
if st.sidebar.checkbox("💾 Save All Plots"):
    save_fig_as_html(fig1, f"{selected_metric}_choropleth.html", notebook_name="notebook_04")
    save_fig_as_png(fig1, f"{selected_metric}_choropleth.png", notebook_name="notebook_04")
    save_fig_as_html(fig2, "city_scores_scatter_geo.html", notebook_name="notebook_04")
    save_fig_as_png(fig2, "city_scores_scatter_geo.png", notebook_name="notebook_04")
    st.success("✅ All plots saved to `exports/` folders")

# ✅ Done
st.success("✅ Notebook 04 Visualizations Rendered")
