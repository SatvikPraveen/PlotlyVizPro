"""
Integration: Comprehensive Dashboard Layout

Combine multiple chart types in a professional multi-panel layout.
Demonstrates: Subplots + mixed chart types + unified theme + annotations
"""
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path

# Load data
data_path = Path(__file__).parent.parent.parent / 'datasets' / 'superstore.csv'
df = pd.read_csv(data_path, parse_dates=['OrderDate'])

# Prepare data for different panels
# Panel 1: Time series
monthly_sales = df.groupby(df['OrderDate'].dt.to_period('M'))['Sales'].sum()

# Panel 2: Category comparison
category_metrics = df.groupby('Category').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()

# Panel 3: Regional distribution
region_sales = df.groupby('Region')['Sales'].sum()

# Panel 4: Scatter - Sales vs Profit
segment_data = df.groupby('Segment').agg({'Sales': 'sum', 'Profit': 'sum', 'Quantity': 'sum'}).reset_index()

# Create 2x2 subplot grid
fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=('Monthly Sales Trend', 'Category Performance',
                    'Regional Distribution', 'Sales vs Profit by Segment'),
    specs=[[{'type': 'scatter'}, {'type': 'bar'}],
           [{'type': 'pie'}, {'type': 'scatter'}]],
    vertical_spacing=0.12,
    horizontal_spacing=0.1
)

# Panel 1: Time series line
fig.add_trace(
    go.Scatter(
        x=[str(x) for x in monthly_sales.index],
        y=monthly_sales.values,
        mode='lines+markers',
        name='Sales',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=6)
    ),
    row=1, col=1
)

# Panel 2: Grouped bar (Sales and Profit)
fig.add_trace(
    go.Bar(name='Sales', x=category_metrics['Category'], y=category_metrics['Sales'],
           marker_color='lightblue'),
    row=1, col=2
)
fig.add_trace(
    go.Bar(name='Profit', x=category_metrics['Category'], y=category_metrics['Profit'],
           marker_color='lightcoral'),
    row=1, col=2
)

# Panel 3: Pie chart
fig.add_trace(
    go.Pie(labels=region_sales.index, values=region_sales.values,
           hole=0.3, marker=dict(colors=px.colors.qualitative.Set2)),
    row=2, col=1
)

# Panel 4: Bubble scatter
fig.add_trace(
    go.Scatter(
        x=segment_data['Sales'],
        y=segment_data['Profit'],
        mode='markers+text',
        text=segment_data['Segment'],
        textposition='top center',
        marker=dict(
            size=segment_data['Quantity']/10,
            color=segment_data['Profit'],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title='Profit', x=1.15)
        ),
        name='Segments'
    ),
    row=2, col=2
)

# Update axes
fig.update_xaxes(title_text='Month', row=1, col=1)
fig.update_yaxes(title_text='Sales ($)', row=1, col=1)
fig.update_xaxes(title_text='Category', row=1, col=2)
fig.update_yaxes(title_text='Amount ($)', row=1, col=2)
fig.update_xaxes(title_text='Sales ($)', row=2, col=2)
fig.update_yaxes(title_text='Profit ($)', row=2, col=2)

# Global layout
fig.update_layout(
    title_text='<b>Executive Sales Dashboard</b><br><sub>Comprehensive Business Performance Analysis</sub>',
    showlegend=True,
    height=800,
    width=1200,
    template='plotly_white',
    font=dict(family='Arial, sans-serif', size=11)
)

print("📊 Displaying comprehensive dashboard with 4 integrated panels...")
fig.show()

# Calculate key metrics
import plotly.express as px
