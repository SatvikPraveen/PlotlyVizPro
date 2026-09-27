"""Streamlit helpers shared by the gallery pages."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from plotlyvizpro import data as _data


def load_html_plot(html_path: Path, height: int = 600) -> None:
    """Embed a standalone Plotly HTML export inside the app."""
    if not html_path.exists():
        st.error(f"HTML file not found: {html_path}")
        return
    try:
        st.components.v1.html(html_path.read_text(encoding="utf-8"), height=height)
    except OSError as exc:
        st.error(f"Failed to load HTML: {exc}")


@st.cache_data(show_spinner=False)
def load_dataset(name: str) -> pd.DataFrame:
    """Cached, manifest-verified dataset load."""
    return _data.load(name)


def numeric_columns(df: pd.DataFrame) -> list[str]:
    """Names of numeric columns."""
    return [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]


def datetime_or_numeric_columns(df: pd.DataFrame) -> list[str]:
    """Columns usable as an ordered x axis."""
    return [
        c for c in df.columns if pd.api.types.is_numeric_dtype(df[c]) or pd.api.types.is_datetime64_any_dtype(df[c])
    ]


def categorical_columns(df: pd.DataFrame, max_levels: int = 30) -> list[str]:
    """Object/category columns with a manageable number of levels."""
    return [c for c in df.columns if not pd.api.types.is_numeric_dtype(df[c]) and df[c].nunique() <= max_levels]
