"""
Recipe: Compare Categories

Compare metrics across different categories with grouped bar charts.
Use Case: Sales by region, performance by department, revenue by product line
"""
import pandas as pd
import plotly.express as px
from pathlib import Path

# Load real data from the project's datasets
data_path = Path(__file__).parent.parent.parent / 'datasets' / 'superstore.csv'
df = pd.read_csv(data_path)

# Aggregate sales by category and region
comparison = df.groupby(['Category', 'Region'])['Sales'].sum().reset_index()

# Create grouped bar chart
fig = px.bar(
    comparison,
    x='Category',
    y='Sales',
    color='Region',
    barmode='group',
    title='Sales Comparison: Categories by Region',
    labels={'Sales': 'Total Sales ($)'},
    color_discrete_sequence=px.colors.qualitative.Set2
)

# Customize layout
fig.update_layout(
    xaxis_title='Product Category',
    yaxis_title='Sales ($)',
    legend_title='Region',
    hovermode='x unified',
    font=dict(size=12)
)

print("📊 Displaying sales comparison across categories and regions...")
fig.show()
