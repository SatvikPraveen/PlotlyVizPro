# 🎓 PlotlyVizPro Tutorials

Step-by-step tutorials to help you master interactive visualizations.

---

## Table of Contents

1. [Getting Started](#tutorial-1-getting-started)
2. [Creating Your First Interactive Plot](#tutorial-2-creating-your-first-interactive-plot)
3. [Customizing Plot Themes](#tutorial-3-customizing-plot-themes)
4. [Building a Dashboard](#tutorial-4-building-a-dashboard)
5. [Adding Statistical Overlays](#tutorial-5-adding-statistical-overlays)
6. [Creating Animated Visualizations](#tutorial-6-creating-animated-visualizations)
7. [Geographic Visualizations](#tutorial-7-geographic-visualizations)
8. [Exporting for Reports](#tutorial-8-exporting-for-reports)

---

## Tutorial 1: Getting Started

### Step 1: Set Up Your Environment

```bash
# Clone the repository
git clone https://github.com/SatvikPraveen/PlotlyVizPro.git
cd PlotlyVizPro

# Create virtual environment
make install

# Or manually:
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Launch JupyterLab

```bash
# Using Makefile
make run-jupyter

# Or directly
jupyter lab
```

### Step 3: Open Your First Notebook

Navigate to `notebooks/01_line_scatter.ipynb` and run the first few cells.

---

## Tutorial 2: Creating Your First Interactive Plot

### Basic Line Plot

```python
import pandas as pd
from utils.plot_utils import line_plot

# Create sample data
df = pd.DataFrame({
    'Date': pd.date_range('2024-01-01', periods=30),
    'Sales': [100 + i*5 + (i%7)*10 for i in range(30)]
})

# Create and display plot
fig = line_plot(
    df,
    x='Date',
    y='Sales',
    title='Daily Sales Trend',
    markers=True
)

fig.show()
```

### Interactive Features

Your plot now has:
- ✅ **Zoom**: Click and drag to zoom into areas
- ✅ **Pan**: Shift + drag to move around
- ✅ **Hover**: Mouse over points to see values
- ✅ **Legend**: Click items to toggle visibility
- ✅ **Export**: Download as PNG using camera icon

---

## Tutorial 3: Customizing Plot Themes

### Applying Dark Theme

```python
from utils.plot_utils import line_plot, apply_dark_theme

# Create plot
fig = line_plot(df, x='Date', y='Sales', title='Sales Trend')

# Apply dark theme
fig = apply_dark_theme(fig)

fig.show()
```

### Custom Styling

```python
from utils.plot_utils import apply_custom_layout

fig = line_plot(df, x='Date', y='Sales')

# Customize layout
fig = apply_custom_layout(
    fig,
    title='📊 Monthly Sales Report',
    xaxis_title='Time Period',
    yaxis_title='Revenue (USD)',
    legend_title='Metrics'
)

# Additional customization
fig.update_layout(
    font=dict(family="Arial, sans-serif", size=14),
    hovermode='x unified',
    height=500
)

fig.show()
```

---

## Tutorial 4: Building a Dashboard

### Creating Subplots

```python
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Create subplot grid
fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=('Sales Trend', 'Profit Analysis', 
                    'Category Breakdown', 'Regional Performance')
)

# Add traces
fig.add_trace(
    go.Scatter(x=df['Date'], y=df['Sales'], mode='lines', name='Sales'),
    row=1, col=1
)

fig.add_trace(
    go.Bar(x=df['Category'], y=df['Sales'], name='By Category'),
    row=1, col=2
)

# Update layout
fig.update_layout(
    title_text='Sales Dashboard',
    showlegend=True,
    height=800
)

fig.show()
```

### Using Streamlit for Interactive Dashboards

```python
# In a new file: my_dashboard.py
import streamlit as st
import pandas as pd
from utils.plot_utils import line_plot, scatter_plot

st.title('📊 Sales Analysis Dashboard')

# Sidebar filters
region = st.sidebar.selectbox('Region', ['All', 'East', 'West', 'Central'])
date_range = st.sidebar.date_input('Date Range', [])

# Load data
df = pd.read_csv('datasets/superstore.csv')

# Filter data based on selections
if region != 'All':
    df = df[df['Region'] == region]

# Display plots
col1, col2 = st.columns(2)

with col1:
    fig1 = line_plot(df, x='OrderDate', y='Sales', title='Sales Over Time')
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = scatter_plot(df, x='Sales', y='Profit', color='Category')
    st.plotly_chart(fig2, use_container_width=True)

# Run with: streamlit run my_dashboard.py
```

---

## Tutorial 5: Adding Statistical Overlays

### Adding a Trendline

```python
from utils.plot_utils import line_plot, add_trendline

# Create base plot
fig = line_plot(df, x='Date', y='Sales', title='Sales with Trendline')

# Add linear trendline
fig = add_trendline(fig, df, x='Date', y='Sales', order=1)

fig.show()
```

### Moving Average

```python
from utils.plot_utils import add_moving_average

fig = line_plot(df, x='Date', y='Sales')

# Add 7-day moving average
fig = add_moving_average(fig, df, y='Sales', window=7, color='red')

fig.show()
```

### Confidence Bands

```python
from utils.plot_utils import add_zscore_band

fig = line_plot(df, x='Date', y='Sales')

# Add ±2 sigma bands (95% confidence)
fig = add_zscore_band(fig, df, y='Sales', z=2)

fig.show()
```

---

## Tutorial 6: Creating Animated Visualizations

### Time-Based Animation

```python
import plotly.express as px

# Load dataset with time component
df = pd.read_csv('datasets/animated_sales.csv')

# Create animated plot
fig = px.bar(
    df,
    x='Category',
    y='Sales',
    color='Region',
    animation_frame='Month',  # This creates the animation
    animation_group='Category',
    range_y=[0, df['Sales'].max() * 1.1],
    title='Sales by Category Over Time'
)

# Customize animation
fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 1000
fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 500

fig.show()
```

### Adding Sliders

```python
# The animation_frame automatically creates a slider
# You can customize it:
fig.update_layout(
    sliders=[{
        'active': 0,
        'yanchor': 'top',
        'y': 0,
        'xanchor': 'left',
        'currentvalue': {
            'prefix': 'Month: ',
            'visible': True,
            'xanchor': 'right'
        }
    }]
)
```

---

## Tutorial 7: Geographic Visualizations

### Creating a Choropleth Map

```python
import plotly.express as px

# Load world population data
df = pd.read_csv('datasets/world_population.csv')

# Create choropleth
fig = px.choropleth(
    df,
    locations='Country',
    locationmode='country names',
    color='Population',
    hover_name='Country',
    color_continuous_scale='Viridis',
    title='World Population by Country'
)

fig.update_layout(geo=dict(showframe=False, projection_type='natural earth'))
fig.show()
```

### Scatter Map with Coordinates

```python
# Load location data
df = pd.read_csv('datasets/map_data.csv')

# Create scatter geo map
fig = px.scatter_geo(
    df,
    lat='Latitude',
    lon='Longitude',
    color='Score',
    hover_name='City',
    size='Population',
    projection='natural earth',
    title='Cities by Score'
)

fig.show()
```

---

## Tutorial 8: Exporting for Reports

### Saving as HTML (Interactive)

```python
from utils.plot_utils import save_fig_as_html

fig = line_plot(df, x='Date', y='Sales', title='Q1 Sales Report')

# Save for sharing
save_fig_as_html(
    fig,
    filename='q1_sales_report.html',
    notebook_name='reports'
)

# File saved to: exports/html/reports/q1_sales_report.html
```

### Saving as PNG (Static)

```python
from utils.plot_utils import save_fig_as_png

fig = scatter_plot(df, x='Sales', y='Profit', color='Category')

# Save for presentations
save_fig_as_png(
    fig,
    filename='sales_profit_analysis.png',
    notebook_name='reports'
)

# File saved to: exports/images/reports/sales_profit_analysis.png
```

### Batch Export

```python
# Export multiple plots at once
plots = {
    'sales_trend': line_plot(df, x='Date', y='Sales'),
    'profit_analysis': scatter_plot(df, x='Sales', y='Profit'),
    'category_breakdown': bar_plot(df, x='Category', y='Sales')
}

for name, fig in plots.items():
    save_fig_as_html(fig, f'{name}.html', notebook_name='batch_export')
    save_fig_as_png(fig, f'{name}.png', notebook_name='batch_export')

print('✅ All plots exported successfully!')
```

---

## Next Steps

1. **Explore the Notebooks**: Work through all 10 notebooks in order
2. **Modify Examples**: Change parameters and data to see effects
3. **Build Your Own**: Create visualizations with your own datasets
4. **Share Your Work**: Use Streamlit to create interactive apps
5. **Contribute**: Submit your improvements via Pull Requests

---

## Common Patterns

### The `.pipe()` Method

Chain operations elegantly:

```python
fig = (df
    .pipe(lambda d: line_plot(d, x='Date', y='Sales'))
    .pipe(apply_dark_theme)
    .pipe(add_moving_average, df=df, y='Sales', window=7))
```

### Reusable Templates

Create your own plotting functions:

```python
def my_standard_plot(df, x, y, theme='dark'):
    fig = line_plot(df, x, y, title=f'{y} Analysis')
    
    if theme == 'dark':
        fig = apply_dark_theme(fig)
    
    fig = add_moving_average(fig, df, y, window=7)
    return fig

# Use it
fig = my_standard_plot(df, 'Date', 'Sales')
```

---

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues and solutions.

For more help, check the [API Reference](API.md) or open an issue on GitHub.
