"""
Advanced: Performance Optimization Techniques

Demonstrate strategies for handling large datasets efficiently.
Demonstrates: Data aggregation + sampling + WebGL + plotly_resampler concepts
"""
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
from pathlib import Path

# Generate large dataset for testing
print("Generating large test dataset...")
np.random.seed(42)
n_points = 100_000

large_df = pd.DataFrame({
    'x': np.random.randn(n_points).cumsum(),
    'y': np.random.randn(n_points).cumsum(),
    'category': np.random.choice(['A', 'B', 'C', 'D'], n_points),
    'value': np.random.rand(n_points) * 100
})

print(f"Created dataset with {n_points:,} points")

# ===== TECHNIQUE 1: Smart Sampling =====
print("\n1️⃣ Applying smart sampling (reduce to 1% for similar visual)...")
sampled_df = large_df.sample(n=1000, random_state=42)

fig1 = go.Figure()
fig1.add_trace(go.Scattergl(  # Note: Scattergl instead of Scatter
    x=sampled_df['x'],
    y=sampled_df['y'],
    mode='markers',
    marker=dict(size=4, color=sampled_df['value'], colorscale='Viridis'),
    name='Sampled (1,000 pts)'
))

fig1.update_layout(
    title='Technique 1: Smart Sampling (1,000 from 100,000 points)',
    xaxis_title='X', yaxis_title='Y',
    template='plotly_white'
)

# ===== TECHNIQUE 2: Aggregation/Binning =====
print("\n2️⃣ Applying 2D histogram binning for density visualization...")

fig2 = go.Figure(data=[
    go.Histogram2d(
        x=large_df['x'],
        y=large_df['y'],
        colorscale='Blues',
        nbinsx=100,
        nbinsy=100,
        colorbar=dict(title='Count')
    )
])

fig2.update_layout(
    title='Technique 2: 2D Histogram Binning (handles 100K points efficiently)',
    xaxis_title='X', yaxis_title='Y'
)

# ===== TECHNIQUE 3: WebGL for Large Scatter Plots =====
print("\n3️⃣ Using WebGL rendering (Scattergl) for performance...")

# Time comparison
start = time.time()
fig3_slow = go.Figure(data=[
    go.Scatter(x=sampled_df['x'], y=sampled_df['y'], mode='markers')
])
time_svg = time.time() - start

start = time.time()
fig3_fast = go.Figure(data=[
    go.Scattergl(x=sampled_df['x'], y=sampled_df['y'], mode='markers')
])
time_webgl = time.time() - start

print(f"   SVG rendering: {time_svg*1000:.2f}ms")
print(f"   WebGL rendering: {time_webgl*1000:.2f}ms")
print(f"   Speedup: {time_svg/time_webgl:.1f}x faster")

# ===== TECHNIQUE 4: Aggregated Time Series =====
print("\n4️⃣ Time series aggregation...")

# Simulate time series
dates = pd.date_range('2020-01-01', periods=n_points, freq='1min')
ts_df = pd.DataFrame({
    'timestamp': dates,
    'value': np.random.randn(n_points).cumsum()
})

# Aggregate to hourly instead of per-minute
ts_hourly = ts_df.set_index('timestamp').resample('1H').mean().reset_index()

fig4 = go.Figure()
fig4.add_trace(go.Scatter(
    x=ts_hourly['timestamp'],
    y=ts_hourly['value'],
    mode='lines',
    name=f'Hourly Aggregated ({len(ts_hourly)} points)',
    line=dict(width=2)
))

fig4.update_layout(
    title=f'Technique 4: Time Aggregation ({n_points:,} → {len(ts_hourly)} points)',
    xaxis_title='Time', yaxis_title='Value'
)

print(f"   Reduced from {n_points:,} to {len(ts_hourly)} points")

# ===== Display all techniques =====
print("\n📊 Displaying performance optimization examples...")

# Show technique 2 (most impressive)
fig2.show()

print("\n" + "="*60)
print("PERFORMANCE OPTIMIZATION SUMMARY")
print("="*60)
print("\n✅ Key Techniques:")
print("  1. Smart Sampling: Random/stratified sampling for large datasets")
print("  2. Aggregation: Binning/grouping to reduce data points")
print("  3. WebGL: Use Scattergl for >10K points (renders on GPU)")
print("  4. Time Resampling: Aggregate high-frequency data")
print("  5. Data Types: Use appropriate dtypes (int32 vs int64)")
print("  6. Incremental Loading: Load data in chunks for streaming")
print("\n📚 Advanced Libraries:")
print("  - plotly-resampler: Automatic downsampling for time series")
print("  - datashader: Pre-render large datasets to images")
print("  - vaex: Out-of-core dataframe processing")
print("\n💡 Rule of Thumb:")
print("  - < 10K points: Regular Scatter is fine")
print("  - 10K - 100K: Use Scattergl (WebGL)")
print("  - > 100K: Aggregate or use specialized tools")
print("  - > 1M: Consider datashader or server-side rendering")
