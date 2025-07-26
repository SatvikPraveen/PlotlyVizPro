# utils/streamlit_utils.py

import streamlit as st
from pathlib import Path

def load_html_plot(html_path: Path, height: int = 600):
    """
    Embed a standalone Plotly HTML file inside a Streamlit app.
    
    Parameters:
    - html_path (Path): Path to the exported HTML file.
    - height (int): Height of the embedded iframe (default: 600px).
    """
    if not html_path.exists():
        st.error(f"❌ HTML file not found: {html_path}")
        return

    try:
        with open(html_path, "r", encoding="utf-8") as f:
            html = f.read()
        st.components.v1.html(html, height=height)
    except Exception as e:
        st.error(f"🚨 Failed to load HTML: {e}")
