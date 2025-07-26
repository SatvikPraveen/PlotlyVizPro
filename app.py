# app.py

import streamlit as st
from pathlib import Path
from utils.streamlit_utils import load_html_plot

# 🧭 Configure Streamlit page
st.set_page_config(page_title="📊 PlotlyVizPro – Visual Gallery", layout="wide")

# 💠 Enhanced Header Block with Styling
st.markdown("""
    <div style="background-color: #0E1117; padding: 30px; border-radius: 10px;">
        <h1 style='color: #56B4E9; font-size: 3em; margin-bottom: 0;'>📊 PlotlyVizPro</h1>
        <h3 style='color: white; margin-top: 0;'>Interactive Visual Gallery</h3>
        <p style='color: #CCCCCC; font-size: 1.1em;'>
            Welcome to <b>PlotlyVizPro</b> – a curated collection of interactive dashboards built with Plotly and Python.
        </p>
        <ul style='color: #DDDDDD; font-size: 1.05em;'>
            <li>👉 Use the <b>sidebar</b> to browse each notebook’s dashboard</li>
            <li>💾 Click on <b>Save Plot</b> in each page to export visuals as <code>HTML</code> or <code>PNG</code></li>
            <li>🧰 Reuse the visual templates and utility code for your own data projects</li>
        </ul>
    </div>
""", unsafe_allow_html=True)

# 🔍 Optional sample plot preview
st.markdown("### 📌 Sample Preview from Notebook 01")

html_preview = Path("exports/html/01_line_scatter/line_plot.html")
if html_preview.exists():
    load_html_plot(html_preview)
else:
    st.warning("⚠️ Sample preview not available. Please run `notebook_01.py` to generate it.")
