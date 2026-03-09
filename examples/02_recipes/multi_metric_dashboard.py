"""
Recipe: Multi-Metric Dashboard

Display multiple related metrics in a single view.
Use Case: Business KPIs, health monitoring, project status
"""
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path

# Load data
data_path = Path(__file__).parent.parent.parent / 'datasets' / 'superstore.csv'
df = pd.read_csv(data_path)

# Prepare metrics
metrics = {
    'Total Sales': df['Sales'].sum(),
    'Total Profit': df['Profit'].sum(),
    'Avg Order': df['Sales'].mean(),
    'Profit Margin': (df['Profit'].sum() / df['Sales'].sum() * 100)
}

# Category breakdown
category_sales = df.groupby('Category')['Sales'].sum()
region_profit = df.groupby('Region')['Profit'].sum()

# Create dashboard with 4 panels
fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=('Key Metrics', 'Sales by Category', 
                    'Profit by Region', 'Sales Trend'),
    specs=[[{'type': 'indicator'}, {'type': 'bar'}],
           [{'type': 'pie'}, {'type': 'scatter'}]]
)

# Panel 1: KPI Indicators  
fig.add_trace(go.Indicator(
    mode='number',
    value=metrics['Total Sales'],
    title={'text': f"Total Sales<br><sub>Profit Margin: {metrics['Profit Margin']:.1f}%</sub>"},
    number={'prefix': '$', 'valueformat': ',.0f'},
), row=1, col=1)

# Panel 2: Category Bar Chart
fig.add_trace(go.Bar(
    x=category_sales.index,
    y=category_sales.values,
    name='Sales',
    marker_color='lightblue'
), row=1, col=2)

# Panel 3: Region Pie Chart
fig.add_trace(go.Pie(
    labels=region_profit.index,
    values=region_profit.values,
    name='Profit'
), row=2, col=1)

# Panel 4: Monthly Trend
df['OrderDate'] = pd.to_datetime(df['OrderDate'])
monthly = df.groupby(df['OrderDate'].dt.to_period('M'))['Sales'].sum()
fig.add_trace(go.Scatter(
    x=[str(x) for x in monthly.index],
    y=monthly.values,
    mode='lines+markers',
    name='Monthly Sales',
    line=dict(color='green')
), row=2, col=2)

# Update layout
fig.update_layout(
    title_text='Business Performance Dashboard',
    showlegend=False,
    height=700
)

print("📊 Displaying multi-metric dashboard...")
fig.show()
