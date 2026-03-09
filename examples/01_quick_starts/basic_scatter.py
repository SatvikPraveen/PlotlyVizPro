"""
Quick Start: Basic Scatter Plot

Simple scatter plot showing relationship between two variables.
Perfect for: Correlation analysis, data exploration
"""
import pandas as pd
from utils.plot_utils import scatter_plot

# Create sample data
df = pd.DataFrame({
    'Sales': [100, 150, 120, 200, 180, 220, 190, 250],
    'Profit': [20, 35, 25, 45, 40, 50, 42, 60],
    'Product': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
})

# Create scatter plot with color by product
fig = scatter_plot(df, x='Sales', y='Profit', hover_name='Product', 
                   title='Sales vs Profit Analysis')
fig.show()
