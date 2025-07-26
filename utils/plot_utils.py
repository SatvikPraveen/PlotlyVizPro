import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import plotly.io as pio

# ============================
# 📊 EXPRESS HELPERS
# ============================

def line_plot(df, x, y, color=None, title="", markers=True, template="plotly_white"):
    fig = px.line(
        df, x=x, y=y, color=color,
        title=title,
        markers=markers,
        template=template
    )
    fig.update_layout(legend_title_text=color if color else "")
    return fig

def scatter_plot(df, x, y, color=None, size=None, hover_name=None, title="", template="plotly_white"):
    fig = px.scatter(
        df, x=x, y=y, color=color, size=size,
        hover_name=hover_name,
        title=title,
        template=template
    )
    fig.update_layout(legend_title_text=color if color else "")
    return fig

def bubble_plot(df, x, y, size, color=None, title="", template="plotly_white"):
    return scatter_plot(df, x, y, color=color, size=size, title=title, template=template)

# ============================
# 🎨 THEMING & LAYOUT
# ============================

def apply_dark_theme(fig, paper_bgcolor="#111", plot_bgcolor="#222", font_color="white"):
    fig.update_layout(
        paper_bgcolor=paper_bgcolor,
        plot_bgcolor=plot_bgcolor,
        font=dict(color=font_color)
    )
    return fig

def apply_custom_layout(fig, title=None, xaxis_title=None, yaxis_title=None, legend_title=None):
    fig.update_layout(
        title=title,
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        legend_title_text=legend_title
    )
    return fig

# ============================
# 💾 EXPORT UTILITIES
# ============================

from pathlib import Path

# ============================
# 💾 EXPORT UTILITIES
# ============================

def save_fig_as_html(fig, filename, notebook_name="general"):
    """
    Saves the figure as HTML in exports/html/{notebook_name}/
    """
    export_dir = Path.cwd().parent / "exports/html" / notebook_name
    export_dir.mkdir(parents=True, exist_ok=True)
    full_path = export_dir / filename
    fig.write_html(full_path)
    print(f"✅ HTML saved to: {full_path}")

def save_fig_as_png(fig, filename, notebook_name="general"):
    """
    Saves the figure as PNG in exports/images/{notebook_name}/
    Requires `kaleido` installed.
    """
    export_dir = Path.cwd().parent / "exports/images" / notebook_name
    export_dir.mkdir(parents=True, exist_ok=True)
    full_path = export_dir / filename
    fig.write_image(full_path, engine="kaleido")
    print(f"✅ PNG saved to: {full_path}")

# ============================
# ✅ QUICK SANITY PREVIEW
# ============================

def quick_preview(df, chart_type="line", **kwargs):
    if chart_type == "line":
        return line_plot(df, **kwargs).show()
    elif chart_type == "scatter":
        return scatter_plot(df, **kwargs).show()
    elif chart_type == "bubble":
        return bubble_plot(df, **kwargs).show()
    else:
        print(f"[!] Unknown chart type: {chart_type}")


# 📊 Bar Plot Utility

def bar_plot(df, x, y, color=None, barmode="group", title="", template="plotly_white", orientation="v"):
    fig = px.bar(
        df,
        x=x,
        y=y,
        color=color,
        barmode=barmode,
        orientation=orientation,
        title=title,
        template=template
    )
    return fig


# 🥧 Pie Chart Utility

def pie_chart(df, names, values, title=""):
    fig = px.pie(
        df,
        names=names,
        values=values,
        title=title,
        hole=0  # Set to 0.4 for donut chart
    )
    return fig


# 📦 Box Plot Utility

def box_plot(df, x, y, color=None, title="", template="plotly_white", points="outliers"):
    fig = px.box(
        df,
        x=x,
        y=y,
        color=color,
        points=points,
        title=title,
        template=template
    )
    return fig

# 📊 Histogram Utility

def histogram_plot(df, x, color=None, nbins=None, title="", template="plotly_white", barmode="overlay"):
    fig = px.histogram(
        df,
        x=x,
        color=color,
        nbins=nbins,
        title=title,
        template=template,
        barmode=barmode
    )
    return fig


# 🌡️ Density Heatmap Utility

def density_heatmap(df, x, y, color_continuous_scale="Viridis", title="", template="plotly_white"):
    fig = px.density_heatmap(
        df,
        x=x,
        y=y,
        color_continuous_scale=color_continuous_scale,
        title=title,
        template=template
    )
    return fig

# 📈 Density Contour (KDE-style) Utility

def density_contour(df, x, y, color=None, title="", template="plotly_white"):
    fig = px.density_contour(
        df,
        x=x,
        y=y,
        color=color,
        title=title,
        template=template
    )
    return fig


# 🌍 Scatter Geo Utility

def scatter_geo(df, lat, lon, color=None, size=None, hover_name=None, title="", template="plotly_white"):
    fig = px.scatter_geo(
        df,
        lat=lat,
        lon=lon,
        color=color,
        size=size,
        hover_name=hover_name,
        title=title,
        template=template
    )
    fig.update_geos(projection_type="natural earth")
    return fig


# 🗺️ Choropleth Utility (By Country)

def choropleth_map(df, locations, color, locationmode="country names", title="", template="plotly_white", color_continuous_scale="Viridis"):
    fig = px.choropleth(
        df,
        locations=locations,
        color=color,
        locationmode=locationmode,
        color_continuous_scale=color_continuous_scale,
        title=title,
        template=template
    )
    return fig


# 🧭 Scatter Mapbox Utility (Optional if using Mapbox token)

def scatter_mapbox(df, lat, lon, color=None, size=None, hover_name=None, title="", zoom=1, mapbox_style="carto-positron", token=None):
    if token:
        import plotly
        plotly.io.mapbox.default_access_token = token

    fig = px.scatter_mapbox(
        df,
        lat=lat,
        lon=lon,
        color=color,
        size=size,
        hover_name=hover_name,
        zoom=zoom,
        mapbox_style=mapbox_style,
        title=title
    )
    return fig

# 🎞️ Animated Bar/Line Plot Utility (using animation_frame)

def animated_plot(df, x, y, animation_frame, color=None, title="", template="plotly_white", plot_type="line"):
    if plot_type == "line":
        fig = px.line(
            df,
            x=x,
            y=y,
            color=color,
            animation_frame=animation_frame,
            title=title,
            template=template
        )
    elif plot_type == "bar":
        fig = px.bar(
            df,
            x=x,
            y=y,
            color=color,
            animation_frame=animation_frame,
            title=title,
            template=template
        )
    else:
        raise ValueError("Unsupported plot_type. Use 'line' or 'bar'.")
    
    fig.update_layout(transition={"duration": 300})
    return fig


# 🎛️ Interactive Dropdown with Traces

def add_dropdown(fig, label_trace_map, title=""):
    buttons = []
    for label, trace_idxs in label_trace_map.items():
        visible = [False] * len(fig.data)
        for i in trace_idxs:
            visible[i] = True
        buttons.append(dict(label=label, method="update", args=[{"visible": visible}, {"title": title}]))

    fig.update_layout(
        updatemenus=[
            dict(
                type="dropdown",
                direction="down",
                showactive=True,
                x=1.15,
                xanchor="left",
                buttons=buttons
            )
        ]
    )
    return fig


# 🎚️ Slider Utility (Trace-based Time Slider for go.Figure)


def add_slider(fig, steps_titles, title=""):
    steps = []
    for i, step_title in enumerate(steps_titles):
        step = dict(
            method="update",
            args=[{"visible": [j == i for j in range(len(fig.data))]},
                  {"title": step_title}],
            label=step_title
        )
        steps.append(step)

    sliders = [dict(
        active=0,
        pad={"t": 50},
        steps=steps
    )]

    fig.update_layout(sliders=sliders, title=title)
    return fig


# 🧱 Subplot Creator Utility

def create_subplots(rows, cols, specs=None, subplot_titles=None, shared_x=False, shared_y=False, vertical_spacing=0.1, horizontal_spacing=0.1):
    fig = make_subplots(
        rows=rows,
        cols=cols,
        specs=specs,
        subplot_titles=subplot_titles,
        shared_xaxes=shared_x,
        shared_yaxes=shared_y,
        vertical_spacing=vertical_spacing,
        horizontal_spacing=horizontal_spacing
    )
    return fig


# ➕ Add Trace to Subplot Utility

def add_trace_to_subplot(fig, trace, row, col):
    fig.add_trace(trace, row=row, col=col)
    return fig


# 🎯 Update Layout for Subplots

def update_subplot_layout(fig, title="", height=600, width=1000, showlegend=True):
    fig.update_layout(
        title=title,
        height=height,
        width=width,
        showlegend=showlegend
    )
    return fig


# Custom Margins for Dashboards
def apply_dashboard_margins(fig, l=40, r=40, t=60, b=40):
    fig.update_layout(margin=dict(l=l, r=r, t=t, b=b))
    return fig


# 📐 create_go_figure()

def create_go_figure(title="", showlegend=True):
    fig = go.Figure()
    fig.update_layout(title=title, showlegend=showlegend)
    return fig


# ➕ add_trace_go()

def add_trace_go(fig, trace):
    fig.add_trace(trace)
    return fig


# 🛠️ update_go_layout()

def update_go_layout(fig, title=None, xaxis_title=None, yaxis_title=None, legend_title=None):
    fig.update_layout(
        title=title,
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        legend_title_text=legend_title
    )
    return fig


# 🧾 add_annotation_go()

def add_annotation_go(fig, text, x, y, xref="x", yref="y", showarrow=True):
    fig.add_annotation(
        text=text,
        x=x,
        y=y,
        xref=xref,
        yref=yref,
        showarrow=showarrow
    )
    return fig

# 🧭 add_shape_go() (e.g., vertical/horizontal line)

def add_shape_go(fig, shape_dict):
    fig.add_shape(shape_dict)
    return fig

# 🧭 Mapbox-Based Scatter Utility

def scatter_mapbox(df, lat, lon, color=None, size=None, hover_name=None, title="", zoom=1, center=None,
                   mapbox_style="carto-positron", token=None):
    """
    Create a scatter mapbox plot. Optionally inject your Mapbox access token for custom styling.
    """
    if token:
        import plotly
        plotly.io.mapbox.default_access_token = token

    fig = px.scatter_mapbox(
        df,
        lat=lat,
        lon=lon,
        color=color,
        size=size,
        hover_name=hover_name,
        zoom=zoom,
        center=center,
        mapbox_style=mapbox_style,
        title=title
    )
    return fig


# 📈 Linear Trendline (OLS)

def add_trendline(fig, x, y, name="Trendline", color="red", dash="dash"):
    """
    Adds a linear trendline to an existing figure using numpy polyfit.
    """
    coeffs = np.polyfit(x, y, 1)
    trend_y = coeffs[0] * np.array(x) + coeffs[1]

    trend_trace = go.Scatter(
        x=x,
        y=trend_y,
        mode="lines",
        name=name,
        line=dict(color=color, dash=dash)
    )
    fig.add_trace(trend_trace)
    return fig


# 🟦 Z-Score Band Utility

def add_zscore_band(fig, x, y, band=1, color='rgba(0,100,255,0.1)', name=None):
    """
    Adds a shaded band of ±Z standard deviations around the mean.
    """
    y = np.array(y)
    mean = np.mean(y)
    std = np.std(y)

    upper = mean + band * std
    lower = mean - band * std

    fig.add_shape(
        type="rect",
        xref="x",
        yref="y",
        x0=min(x),
        x1=max(x),
        y0=lower,
        y1=upper,
        fillcolor=color,
        opacity=0.3,
        layer="below",
        line_width=0
    )
    return fig


# 🔁 Moving Average Line

def add_moving_average(fig, x, y, window=7, name="Moving Avg", color="green", dash="dot"):
    """
    Adds a rolling average line to a go.Figure.
    """
    y_smooth = pd.Series(y).rolling(window=window, min_periods=1).mean()

    ma_trace = go.Scatter(
        x=x,
        y=y_smooth,
        mode="lines",
        name=name,
        line=dict(color=color, dash=dash)
    )
    fig.add_trace(ma_trace)
    return fig


#📈 add_trendline(): Linear Regression Overlay

def add_trendline(x, y, name="Trendline", color="crimson"):
    # Convert datetime to numeric if needed
    if pd.api.types.is_datetime64_any_dtype(x):
        x_numeric = (pd.to_datetime(x) - pd.to_datetime(x).min()).dt.days.values.reshape(-1, 1)
        x_display = pd.to_datetime(x)
    else:
        x_numeric = np.array(x).reshape(-1, 1)
        x_display = x

    y_np = np.array(y)

    model = LinearRegression().fit(x_numeric, y_np)
    y_pred = model.predict(x_numeric)

    return go.Scatter(
        x=x_display,
        y=y_pred,
        mode="lines",
        name=name,
        line=dict(color=color, dash="dash")
    )


# 📊 add_moving_average(): Rolling Mean Overlay

def add_moving_average(x, y, window=5, name="Moving Avg", color="royalblue"):
    y_series = pd.Series(y).rolling(window=window).mean()
    
    return go.Scatter(
        x=x,
        y=y_series,
        mode="lines",
        name=name,
        line=dict(color=color, dash="dot")
    )


# 🔵 add_zscore_band(): Highlight ±Z Score Range

def add_zscore_band(x, y, z=2):
    """
    Returns upper and lower z-score bands for overlaying on time series.
    """
    mean = np.mean(y)
    std = np.std(y)
    upper = mean + z * std
    lower = mean - z * std
    upper_band = np.full_like(y, upper)
    lower_band = np.full_like(y, lower)
    return upper_band, lower_band



# ============================
# 🎨 GLOBAL PROJECT THEME
# ============================

def apply_theme(template="plotly_white", font_family="Arial", font_size=14):
    """
    Sets a global Plotly theme.
    """
    pio.templates.default = template
    pio.templates[template].layout.font.family = font_family
    pio.templates[template].layout.font.size = font_size

