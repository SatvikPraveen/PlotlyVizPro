# 📄 pages/notebook_05.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.plot_utils import (
    animated_plot,
    add_dropdown,
    add_slider,
    apply_theme,
    save_fig_as_html,
    save_fig_as_png
)

# 🎨 Apply Theme
apply_theme("plotly_white")

# 🧭 Page Config
st.set_page_config(page_title="Notebook 05 – Animations & Interactivity", layout="wide")
st.title("🎞️ Notebook 05: Animations and Interactive Controls")

# 📂 Load Data
df = pd.read_csv("datasets/animated_sales.csv")
categories = df["Category"].unique()

# 🎞️ Animated Plot
st.subheader("📊 Animated Bar Chart: Monthly Sales by Category")
fig1 = animated_plot(
    df,
    x="Category",
    y="Sales",
    animation_frame="Month",
    color="Category",
    title="Monthly Sales by Category (Animated)",
    plot_type="bar"
)
st.plotly_chart(fig1, use_container_width=True)

# 🔽 Dropdown Interactivity
st.subheader("🔽 Dropdown Interactivity: View Sales by Category Over Time")

# Prepare trace-per-category
fig2 = go.Figure()
frames = []
for i, cat in enumerate(categories):
    cat_df = df[df["Category"] == cat]
    fig2.add_trace(go.Scatter(
        x=cat_df["Month"],
        y=cat_df["Sales"],
        name=cat,
        visible=(i == 0)
    ))

label_map = {cat: [i] for i, cat in enumerate(categories)}
fig2 = add_dropdown(fig2, label_map, title="Toggle Category Sales Over Time")
fig2.update_layout(height=500)
st.plotly_chart(fig2, use_container_width=True)

# 🎚️ Slider Interactivity
st.subheader("🎚️ Slider Interactivity: Total Sales by Category")

fig3 = go.Figure()
step_titles = []
for i, cat in enumerate(categories):
    cat_df = df[df["Category"] == cat]
    fig3.add_trace(go.Bar(
        x=[cat],
        y=[cat_df["Sales"].sum()],
        name=cat,
        visible=(i == 0)
    ))
    step_titles.append(cat)

fig3 = add_slider(fig3, step_titles, title="Slider: Sales by Category")
fig3.update_layout(height=500)
st.plotly_chart(fig3, use_container_width=True)

# 💾 Save
if st.sidebar.checkbox("💾 Save All Plots"):
    save_fig_as_html(fig1, "monthly_sales_animated.html", notebook_name="notebook_05")
    save_fig_as_png(fig1, "monthly_sales_animated.png", notebook_name="notebook_05")
    save_fig_as_html(fig2, "category_toggle_dropdown.html", notebook_name="notebook_05")
    save_fig_as_png(fig2, "category_toggle_dropdown.png", notebook_name="notebook_05")
    save_fig_as_html(fig3, "category_slider.html", notebook_name="notebook_05")
    save_fig_as_png(fig3, "category_slider.png", notebook_name="notebook_05")
    st.success("✅ Plots saved to exports folders")

# ✅ Done
st.success("✅ Notebook 05 Visualizations Rendered")
