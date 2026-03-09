"""
Quick Start: Bubble Plot

Create a bubble plot with size representing a third dimension.
Perfect for: 3D relationships, weighted comparisons
"""
import pandas as pd
from utils.plot_utils import bubble_plot

# Create data with three dimensions
df = pd.DataFrame({
    'Product': ['Laptop', 'Phone', 'Tablet', 'Watch', 'Headphones'],
    'Price': [1200, 800, 500, 400, 150],
    'Units_Sold': [150, 500, 300, 800, 1200],
    'Profit_Margin': [25, 35, 20, 40, 30]
})

# Create bubble plot (size = Profit_Margin)
fig = bubble_plot(df, x='Price', y='Units_Sold', size='Profit_Margin',
                  title='Product Performance Analysis')

# Add hover information
fig.update_traces(text=df['Product'], hovertemplate='<b>%{text}</b><br>Price: $%{x}<br>Units: %{y}<extra></extra>')

fig.show()
