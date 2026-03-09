"""
Quick Start: Basic Line Plot

The simplest possible line plot - 10 lines to visualization.
Perfect for: Getting started, testing setup, quick prototypes
"""
import pandas as pd
from utils.plot_utils import line_plot

# Create simple time series data
df = pd.DataFrame({
    'Date': pd.date_range('2024-01-01', periods=30),
    'Sales': range(100, 130)
})

# Create and display plot
fig = line_plot(df, x='Date', y='Sales', title='Daily Sales')
fig.show()
