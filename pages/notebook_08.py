# 📄 pages/notebook_08.py

import pandas as pd
import streamlit as st

from utils.plot_utils import (
    apply_theme,
    save_fig_as_html,
    save_fig_as_png,
    scatter_mapbox,
)

# 🎨 Apply theme
apply_theme("plotly_white")

# 🧭 Page Config
st.set_page_config(page_title="Notebook 08 – Mapbox & Projection Styling", layout="wide")
st.title("🗺️ Notebook 08: Mapbox & Geo Projections")

# 📂 Load Dataset
df = pd.read_csv("datasets/map_data.csv")

# ✅ Column Check
required_cols = ["City", "Latitude", "Longitude", "Score"]
if not all(col in df.columns for col in required_cols):
    st.error(f"Dataset must contain columns: {', '.join(required_cols)}")
    st.stop()

# 🎛️ Sidebar Styling Options
st.sidebar.header("Map Style Options")
map_style = st.sidebar.selectbox("Select Mapbox Style", ["open-street-map", "carto-positron", "carto-darkmatter"])
zoom_level = st.sidebar.slider("Zoom Level", min_value=1, max_value=10, value=2)

# 🌍 Mapbox Plot
fig = scatter_mapbox(
    df,
    lat="Latitude",
    lon="Longitude",
    color="Score",
    size="Score",
    hover_name="City",
    zoom=zoom_level,
    title=f"City Scores – {map_style.replace('-', ' ').title()}",
    mapbox_style=map_style,
)

# 📊 Display
st.plotly_chart(fig, use_container_width=True)

# 💾 Save Option
if st.sidebar.checkbox("💾 Save Plot"):
    save_fig_as_html(fig, f"city_scores_{map_style}.html", notebook_name="notebook_08")
    save_fig_as_png(fig, f"city_scores_{map_style}.png", notebook_name="notebook_08")
    st.success("✅ Plot saved in `exports/` folders")

# ✅ Footer
st.success("✅ Notebook 08 Visualizations Rendered")
