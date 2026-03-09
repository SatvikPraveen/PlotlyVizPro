# 📚 API Reference

Complete reference for PlotlyVizPro utility functions.

---

## Table of Contents

- [Plot Utilities](#plot-utilities)
- [Streamlit Utilities](#streamlit-utilities)
- [Statistical Overlays](#statistical-overlays)
- [Export Functions](#export-functions)
- [Theming Functions](#theming-functions)

---

## Plot Utilities

Located in `utils/plot_utils.py`

### Basic Charts

#### `line_plot(df, x, y, color=None, title="", markers=True, template="plotly_white")`

Create an interactive line plot using Plotly Express.

**Parameters:**
- `df` (DataFrame): Input data
- `x` (str): Column name for x-axis
- `y` (str): Column name for y-axis
- `color` (str, optional): Column for color grouping
- `title` (str, optional): Plot title
- `markers` (bool): Show markers on line (default: True)
- `template` (str): Plotly template (default: "plotly_white")

**Returns:**
- `plotly.graph_objects.Figure`: Interactive figure object

**Example:**
```python
import pandas as pd
from utils.plot_utils import line_plot

df = pd.DataFrame({
    'Date': pd.date_range('2024-01-01', periods=10),
    'Sales': [100, 150, 120, 180, 200, 210, 190, 220, 240, 250]
})

fig = line_plot(df, x='Date', y='Sales', title='Sales Trend')
fig.show()
```

---

#### `scatter_plot(df, x, y, color=None, size=None, hover_name=None, title="", template="plotly_white")`

Create an interactive scatter plot.

**Parameters:**
- `df` (DataFrame): Input data
- `x` (str): Column name for x-axis
- `y` (str): Column name for y-axis
- `color` (str, optional): Column for color grouping
- `size` (str, optional): Column for marker size
- `hover_name` (str, optional): Column for hover labels
- `title` (str, optional): Plot title
- `template` (str): Plotly template

**Returns:**
- `plotly.graph_objects.Figure`: Interactive figure object

**Example:**
```python
fig = scatter_plot(
    df,
    x='Sales',
    y='Profit',
    color='Category',
    hover_name='Product',
    title='Sales vs Profit'
)
```

---

#### `bubble_plot(df, x, y, size, color=None, title="", template="plotly_white")`

Create a bubble plot (scatter with size parameter).

**Parameters:**
- `df` (DataFrame): Input data
- `x` (str): Column name for x-axis
- `y` (str): Column name for y-axis
- `size` (str): Column for bubble size
- `color` (str, optional): Column for color grouping
- `title` (str, optional): Plot title
- `template` (str): Plotly template

**Returns:**
- `plotly.graph_objects.Figure`: Interactive figure object

---

## Theming Functions

#### `apply_dark_theme(fig, paper_bgcolor="#111", plot_bgcolor="#222", font_color="white")`

Apply a dark theme to any Plotly figure.

**Parameters:**
- `fig` (Figure): Plotly figure object
- `paper_bgcolor` (str): Background color for entire figure
- `plot_bgcolor` (str): Background color for plot area
- `font_color` (str): Font color

**Returns:**
- `plotly.graph_objects.Figure`: Modified figure with dark theme

**Example:**
```python
fig = line_plot(df, x='Date', y='Sales')
fig = apply_dark_theme(fig)
fig.show()
```

---

#### `apply_custom_layout(fig, title=None, xaxis_title=None, yaxis_title=None, legend_title=None)`

Apply custom layout settings to a figure.

**Parameters:**
- `fig` (Figure): Plotly figure object
- `title` (str, optional): Custom title
- `xaxis_title` (str, optional): X-axis label
- `yaxis_title` (str, optional): Y-axis label
- `legend_title` (str, optional): Legend title

**Returns:**
- `plotly.graph_objects.Figure`: Modified figure

---

## Export Functions

#### `save_fig_as_html(fig, filename, notebook_name="general")`

Save a Plotly figure as an interactive HTML file.

**Parameters:**
- `fig` (Figure): Plotly figure to save
- `filename` (str): Output filename (e.g., "my_plot.html")
- `notebook_name` (str): Subfolder name in exports/html/

**Output Location:**
- `exports/html/{notebook_name}/{filename}`

**Example:**
```python
fig = line_plot(df, x='Date', y='Sales')
save_fig_as_html(fig, 'sales_trend.html', notebook_name='01_line_scatter')
```

---

#### `save_fig_as_png(fig, filename, notebook_name="general")`

Save a Plotly figure as a static PNG image.

**Requirements:** Requires `kaleido` package

**Parameters:**
- `fig` (Figure): Plotly figure to save
- `filename` (str): Output filename (e.g., "my_plot.png")
- `notebook_name` (str): Subfolder name in exports/images/

**Output Location:**
- `exports/images/{notebook_name}/{filename}`

**Example:**
```python
fig = scatter_plot(df, x='Sales', y='Profit')
save_fig_as_png(fig, 'sales_vs_profit.png', notebook_name='01_line_scatter')
```

---

## Streamlit Utilities

Located in `utils/streamlit_utils.py`

### `load_html_plot(file_path)`

Load and display a saved HTML plot in Streamlit.

**Parameters:**
- `file_path` (Path or str): Path to HTML file

**Example:**
```python
import streamlit as st
from pathlib import Path
from utils.streamlit_utils import load_html_plot

html_file = Path("exports/html/01_line_scatter/sales_trend.html")
load_html_plot(html_file)
```

---

## Statistical Overlays

Advanced functions for adding statistical elements to plots.

### `add_trendline(fig, df, x, y, order=1)`

Add a polynomial trendline to an existing figure.

**Parameters:**
- `fig` (Figure): Existing Plotly figure
- `df` (DataFrame): Source data
- `x` (str): X column name
- `y` (str): Y column name
- `order` (int): Polynomial order (1=linear, 2=quadratic, etc.)

**Returns:**
- `plotly.graph_objects.Figure`: Figure with trendline added

---

### `add_moving_average(fig, df, y, window=7, color='red')`

Add a moving average line to a time series plot.

**Parameters:**
- `fig` (Figure): Existing Plotly figure
- `df` (DataFrame): Source data
- `y` (str): Column to calculate MA for
- `window` (int): Rolling window size
- `color` (str): Line color

**Returns:**
- `plotly.graph_objects.Figure`: Figure with MA line added

---

### `add_zscore_band(fig, df, y, z=2, color='rgba(255,0,0,0.2)')`

Add confidence bands based on z-score.

**Parameters:**
- `fig` (Figure): Existing Plotly figure
- `df` (DataFrame): Source data
- `y` (str): Column to calculate bands for
- `z` (float): Z-score multiplier (default: 2 for ~95% CI)
- `color` (str): Fill color for band

**Returns:**
- `plotly.graph_objects.Figure`: Figure with confidence bands

---

## Usage Patterns

### Chaining Functions

Many utility functions return Figure objects, allowing for method chaining:

```python
fig = (line_plot(df, x='Date', y='Sales', title='Sales Trend')
       .pipe(apply_dark_theme)
       .pipe(add_moving_average, df=df, y='Sales', window=7))

save_fig_as_html(fig, 'sales_with_ma.html')
```

### Quick Preview

```python
from utils.plot_utils import quick_preview

quick_preview(df, chart_type='scatter', x='Sales', y='Profit', color='Category')
```

---

## Type Hints

For better IDE support, functions use type hints:

```python
from typing import Optional
import pandas as pd
import plotly.graph_objects as go

def line_plot(
    df: pd.DataFrame,
    x: str,
    y: str,
    color: Optional[str] = None,
    title: str = "",
    markers: bool = True,
    template: str = "plotly_white"
) -> go.Figure:
    ...
```

---

## Error Handling

All utility functions include basic error handling:

- **Missing columns**: Raises `KeyError` with helpful message
- **Invalid data types**: Raises `TypeError`
- **Empty DataFrames**: Raises `ValueError`

**Example:**
```python
try:
    fig = line_plot(df, x='NonExistentColumn', y='Sales')
except KeyError as e:
    print(f"Column not found: {e}")
```

---

For more examples, see the Jupyter notebooks in the `notebooks/` directory.
