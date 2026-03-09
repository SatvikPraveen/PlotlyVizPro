"""
Quick Start: Dark Theme Plot

Apply dark theme for modern, eye-friendly visualizations.
Perfect for: Presentations, dashboards, modern UI
"""
import pandas as pd
from utils.plot_utils import line_plot, apply_dark_theme

# Create data
df = pd.DataFrame({
    'Month': pd.date_range('2024-01-01', periods=12, freq='M'),
    'Revenue': [45, 52, 48, 61, 58, 67, 71, 69, 78, 82, 85, 90]
})

# Create plot and apply dark theme
fig = line_plot(df, x='Month', y='Revenue', title='Monthly Revenue Growth')
fig = apply_dark_theme(fig)

fig.show()
