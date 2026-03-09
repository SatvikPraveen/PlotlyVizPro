"""
Quick Start: Save Plot to Files

Create a plot and export as both HTML (interactive) and PNG (static).
Perfect for: Reports, sharing, documentation
"""
import pandas as pd
from utils.plot_utils import line_plot, save_fig_as_html, save_fig_as_png

# Create data
df = pd.DataFrame({
    'Quarter': ['Q1', 'Q2', 'Q3', 'Q4'],
    'Target': [100, 110, 120, 130],
    'Actual': [95, 115, 118, 135]
})

# Create plot
import plotly.express as px
fig = px.line(df, x='Quarter', y=['Target', 'Actual'], 
              title='Quarterly Performance', markers=True)

# Save in both formats
save_fig_as_html(fig, 'quarterly_performance.html', notebook_name='examples')
save_fig_as_png(fig, 'quarterly_performance.png', notebook_name='examples')

print("✅ Plot saved as HTML and PNG in exports/")
fig.show()
