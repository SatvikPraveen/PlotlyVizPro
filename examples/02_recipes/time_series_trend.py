"""
Recipe: Time Series with Trend

Visualize time series data with moving average overlay.
Use Case: Stock prices, website traffic, sales trends, KPI tracking
"""
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

# Load time-based data
data_path = Path(__file__).parent.parent.parent / 'datasets' / 'superstore.csv'
df = pd.read_csv(data_path, parse_dates=['OrderDate'])

# Aggregate daily sales
daily_sales = df.groupby('OrderDate')['Sales'].sum().reset_index()
daily_sales = daily_sales.sort_values('OrderDate')

# Calculate 7-day moving average
daily_sales['MA_7'] = daily_sales['Sales'].rolling(window=7).mean()

# Create figure with both actual and trend
fig = go.Figure()

# Add actual sales
fig.add_trace(go.Scatter(
    x=daily_sales['OrderDate'],
    y=daily_sales['Sales'],
    mode='lines',
    name='Daily Sales',
    line=dict(color='lightblue', width=1),
    opacity=0.6
))

# Add moving average (trend)
fig.add_trace(go.Scatter(
    x=daily_sales['OrderDate'],
    y=daily_sales['MA_7'],
    mode='lines',
    name='7-Day Trend',
    line=dict(color='red', width=3)
))

# Customize
fig.update_layout(
    title='Sales Trend with 7-Day Moving Average',
    xaxis_title='Date',
    yaxis_title='Sales ($)',
    hovermode='x unified',
    template='plotly_white'
)

print("📈 Displaying time series with trend analysis...")
fig.show()
