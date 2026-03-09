"""
Advanced: Real-time Data Simulation

Simulate real-time streaming data visualization.
Demonstrates: Dynamic updates + time-windowed display + performance optimization
"""
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

# Simulate streaming sensor data
def generate_sensor_stream(n_points=100):
    """Generate simulated time-series sensor data"""
    timestamps = pd.date_range(
        start=datetime.now() - timedelta(seconds=n_points),
        end=datetime.now(),
        periods=n_points
    )
    
    # Simulate multiple sensors with noise and trends
    np.random.seed(42)
    sensor_1 = 20 + np.cumsum(np.random.randn(n_points) * 0.5)  # Temperature
    sensor_2 = 50 + np.random.randn(n_points) * 5  # Humidity
    sensor_3 = np.sin(np.linspace(0, 4*np.pi, n_points)) * 10 + 60  # Pressure (cyclic)
    
    return timestamps, sensor_1, sensor_2, sensor_3

# Generate initial data
times, temp, humidity, pressure = generate_sensor_stream(200)

# Create figure with secondary y-axis
fig = go.Figure()

# Temperature trace
fig.add_trace(go.Scatter(
    x=times,
    y=temp,
    name='Temperature (°C)',
    mode='lines',
    line=dict(color='red', width=2),
    yaxis='y1'
))

# Humidity trace
fig.add_trace(go.Scatter(
    x=times,
    y=humidity,
    name='Humidity (%)',
    mode='lines',
    line=dict(color='blue', width=2),
    yaxis='y2'
))

# Pressure trace
fig.add_trace(go.Scatter(
    x=times,
    y=pressure,
    name='Pressure (kPa)',
    mode='lines',
    line=dict(color='green', width=2),
    yaxis='y1'
))

# Add threshold lines
fig.add_hline(y=25, line_dash='dash', line_color='orange',
              annotation_text='Temp Warning', annotation_position='left')

# Configure layout with dual y-axes
fig.update_layout(
    title={
        'text': '<b>Real-Time Sensor Dashboard</b><br><sub>Live monitoring simulation</sub>',
        'x': 0.5,
        'xanchor': 'center'
    },
    xaxis=dict(
        title='Time',
        rangeslider=dict(visible=True),  # Add range slider for zooming
        type='date'
    ),
    yaxis=dict(
        title='Temperature (°C) / Pressure (kPa)',
        titlefont=dict(color='red'),
        tickfont=dict(color='red')
    ),
    yaxis2=dict(
        title='Humidity (%)',
        titlefont=dict(color='blue'),
        tickfont=dict(color='blue'),
        overlaying='y',
        side='right'
    ),
    hovermode='x unified',
    template='plotly_dark',
    height=600,
    showlegend=True
)

# Add current value annotations
latest_idx = -1
fig.add_annotation(
    x=times[latest_idx], y=temp[latest_idx],
    text=f'{temp[latest_idx]:.1f}°C',
    showarrow=True,
    arrowhead=2,
    bgcolor='red',
    font=dict(color='white')
)

print("📡 Displaying real-time sensor simulation...")
print(f"Monitoring {len(times)} data points across 3 sensors")
print(f"Temperature: {temp[-1]:.1f}°C | Humidity: {humidity[-1]:.1f}% | Pressure: {pressure[-1]:.1f} kPa")
fig.show()

# Performance tip: For actual real-time updates in Dash/Streamlit:
# - Use dcc.Interval or st.rerun() for updates
# - Implement circular buffer to limit data points
# - Use plotly_resampler for large datasets
# - Consider WebGL with scattergl for >100k points
