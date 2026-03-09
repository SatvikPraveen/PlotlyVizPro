"""
Recipe: Correlation Heatmap

Create a correlation matrix to identify relationships between variables.
Use Case: Feature selection, data exploration, multivariate analysis
"""
import pandas as pd
import plotly.express as px
from pathlib import Path

# Load data
data_path = Path(__file__).parent.parent.parent / 'datasets' / 'customer_segments.csv'
df = pd.read_csv(data_path)

# Select numeric columns for correlation
numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
correlation_matrix = df[numeric_cols].corr()

# Create heatmap
fig = px.imshow(
    correlation_matrix,
    labels=dict(color="Correlation"),
    x=correlation_matrix.columns,
    y=correlation_matrix.columns,
    color_continuous_scale='RdBu_r',  # Red-Blue diverging
    zmin=-1,
    zmax=1,
    text_auto='.2f',  # Show correlation values
    title='Feature Correlation Matrix'
)

# Customize
fig.update_layout(
    width=700,
    height=700,
    font=dict(size=10)
)

print("🔥 Displaying correlation heatmap...")
print(f"Analyzing {len(numeric_cols)} numeric features")
fig.show()
