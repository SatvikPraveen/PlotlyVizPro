"""
Quick Start: Basic Bar Chart

Create a simple bar chart for categorical data.
Perfect for: Comparing categories, showing rankings
"""
import pandas as pd
import plotly.express as px

# Sample categorical data
df = pd.DataFrame({
    'Category': ['Electronics', 'Furniture', 'Clothing', 'Books', 'Toys'],
    'Revenue': [45000, 32000, 28000, 15000, 12000]
})

# Create bar chart
fig = px.bar(df, x='Category', y='Revenue', 
             title='Revenue by Category',
             color='Revenue',
             color_continuous_scale='Blues')

fig.show()
