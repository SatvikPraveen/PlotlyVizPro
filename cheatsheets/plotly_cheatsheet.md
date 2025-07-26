# 📊 PlotlyVizPro Cheatsheet — Master-Level Utility Reference

A categorized, ready-to-copy reference of all utility functions built in `plot_utils.py` to supercharge your Plotly productivity.

---

## 📦 Basic Chart Utilities (Plotly Express)

### ▶️ Line Plot

```python
line_plot(df, x="Date", y="Sales", color="Region", title="Sales Trend")
```

### 🔵 Scatter Plot

```python
scatter_plot(df, x="Sales", y="Profit", color="SubCategory", hover_name="SubCategory")
```

### 🫧 Bubble Plot

```python
bubble_plot(df, x="Sales", y="Profit", size="Orders", color="SubCategory")
```

### 📊 Bar Plot

```python
bar_plot(df, x="Category", y="Sales", color="Region", barmode="group", orientation="v")
```

### 🥧 Pie Chart

```python
pie_chart(df, names="Region", values="Sales", title="Sales Distribution")
```

### 📦 Box Plot

```python
box_plot(df, x="Category", y="Profit", color="Category", points="outliers")
```

---

## 🧮 Distribution Charts

### 📘 Histogram

```python
histogram_plot(df, x="Profit", nbins=40, color="Category", barmode="overlay")
```

### 🌡️ Density Heatmap

```python
density_heatmap(df, x="Sales", y="Profit", color_continuous_scale="Viridis")
```

### 📈 Density Contour (KDE-style)

```python
density_contour(df, x="Sales", y="Profit", color="Category")
```

---

## 🗺️ Geo and Map Utilities

### 🗺️ Choropleth Map (Country-wise)

```python
choropleth_map(df, locations="Country", color="GDP_per_capita", locationmode="country names")
```

### 🌍 Scatter Geo

```python
scatter_geo(df, lat="Latitude", lon="Longitude", color="Score", hover_name="City")
```

### 🧭 Scatter Mapbox (Optional token)

```python
scatter_mapbox(df, lat="Latitude", lon="Longitude", mapbox_style="open-street-map", zoom=2)
```

> 🔐 Add `token=MAPBOX_TOKEN` for satellite tiles or premium styling.

---

## 🎞️ Animation & Interactivity

### 🎬 Animated Plot

```python
animated_plot(df, x="Category", y="Sales", animation_frame="Month", color="Category", plot_type="bar")
```

### 🔽 Dropdown Menu to Toggle Traces

```python
label_map = {"Region A": [0], "Region B": [1], "Region C": [2]}
add_dropdown(fig, label_trace_map=label_map, title="Toggle Region")
```

### 🎚️ Slider to Toggle Traces

```python
steps_titles = ["Jan", "Feb", "Mar"]
add_slider(fig, steps_titles=steps_titles, title="Monthly Sales")
```

---

## 📊 Subplots & Dashboards

### 🧱 Create Subplots

```python
fig = create_subplots(
    rows=2, cols=2,
    subplot_titles=["Chart 1", "Chart 2", "Chart 3", "Chart 4"],
    shared_x=True, vertical_spacing=0.1, horizontal_spacing=0.1
)
```

### ➕ Add Trace to Subplot

```python
add_trace_to_subplot(fig, go.Bar(...), row=1, col=1)
```

### 🧾 Update Subplot Layout

```python
update_subplot_layout(fig, title="Dashboard", height=800, width=1000)
```

### 📐 Apply Dashboard Margins

```python
apply_dashboard_margins(fig, l=40, r=40, t=60, b=40)
```

---

## ⚙️ Graph Objects Helpers

### 📘 Create Blank `go.Figure`

```python
fig = create_go_figure(title="Empty Figure")
```

### ➕ Add Trace to `go.Figure`

```python
add_trace_go(fig, go.Scatter(x=x, y=y, mode="lines"))
```

### 🎯 Update Axes and Legend

```python
update_go_layout(fig, xaxis_title="Sales", yaxis_title="Profit", legend_title="Region")
```

### 🏷️ Add Annotation

```python
add_annotation_go(fig, text="Peak", x=1000, y=200)
```

### ➖ Add Shape (e.g., threshold line)

```python
shape = dict(type="line", x0=0, x1=1, y0=100, y1=100, xref="paper", yref="y")
add_shape_go(fig, shape)
```

---

## 📈 Statistical Overlays

### 📐 Add Linear Trendline

```python
add_trendline(fig, x=df["Sales"], y=df["Profit"], name="OLS Fit")
```

### 📊 Add Z-Score Band (±1 std)

```python
add_zscore_band(fig, x=df["Sales"], y=df["Profit"], band=1)
```

### 📉 Add Moving Average Line

```python
add_moving_average(fig, x=df["Date"], y=df["Sales"], window=7, name="7-day Avg")
```

---

## 💾 Export Helpers

### 💾 Save as HTML

```python
save_fig_as_html(fig, "sales_trend.html", notebook_name="01_line_scatter")
```

### 🖼️ Save as PNG

```python
save_fig_as_png(fig, "sales_trend.png", notebook_name="01_line_scatter")
```

> 📁 Automatically saved to `exports/html/{notebook}` and `exports/images/{notebook}`

---

## 🧠 Tips for Mastery

- 🔁 Use `.pipe()` to chain multiple utility enhancements in advanced workflows
- 🧼 Use expressive subplot titles and shared axes to simplify storytelling
- 💡 Use `animated_plot()` sparingly for time-varying dashboards and presentations
- 🛰️ Mapbox styles like `"carto-positron"` and `"satellite-streets"` offer clean base layers for location plots

---
