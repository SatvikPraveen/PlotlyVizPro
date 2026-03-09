"""
Integration: Custom Theme with Branding

Apply consistent custom theme across multiple chart types.
Demonstrates: Custom templates + color schemes + annotations + logos
"""
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path

# Define custom corporate theme
CUSTOM_THEME = {
    'layout': go.Layout(
        font=dict(family='Helvetica, Arial, sans-serif', size=12, color='#2c3e50'),
        title_font=dict(size=20, color='#34495e', family='Helvetica Bold'),
        plot_bgcolor='#ecf0f1',
        paper_bgcolor='white',
        colorway=['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c'],
        xaxis=dict(
            gridcolor='white',
            linecolor='#95a5a6',
            title_font=dict(size=14, color='#34495e')
        ),
        yaxis=dict(
            gridcolor='white',
            linecolor='#95a5a6',
            title_font=dict(size=14, color='#34495e')
        ),
        hoverlabel=dict(
            bgcolor='white',
            font_size=12,
            font_family='Helvetica'
        )
    )
}

# Load data
data_path = Path(__file__).parent.parent.parent / 'datasets' / 'superstore.csv'
df = pd.read_csv(data_path)

# Create dashboard with custom theme
fig = make_subplots(
    rows=1, cols=3,
    subplot_titles=('Sales by Category', 'Regional Performance', 'Profit Distribution'),
    specs=[[{'type': 'bar'}, {'type': 'bar'}, {'type': 'box'}]]
)

# Chart 1: Category sales
category_sales = df.groupby('Category')['Sales'].sum().reset_index()
fig.add_trace(
    go.Bar(x=category_sales['Category'], y=category_sales['Sales'],
           name='Sales', marker_color='#3498db'),
    row=1, col=1
)

# Chart 2: Regional performance
region_profit = df.groupby('Region')['Profit'].sum().sort_values(ascending=True).reset_index()
fig.add_trace(
    go.Bar(x=region_profit['Profit'], y=region_profit['Region'],
           name='Profit', marker_color='#2ecc71', orientation='h'),
    row=1, col=2
)

# Chart 3: Profit distribution by category
for category in df['Category'].unique():
    fig.add_trace(
        go.Box(y=df[df['Category'] == category]['Profit'],
               name=category),
        row=1, col=3
    )

# Apply custom theme
fig.update_layout(CUSTOM_THEME['layout'])

# Add branding - watermark and title
fig.update_layout(
    title={
        'text': '<b>PlotlyVizPro Analytics</b><br><sub>Business Performance Report</sub>',
        'x': 0.5,
        'xanchor': 'center'
    },
    showlegend=True,
    height=500,
    width=1400,
    annotations=[
        # Company watermark
        dict(
            text='PlotlyVizPro',
            xref='paper', yref='paper',
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=60, color='rgba(149, 165, 166, 0.1)'),
            textangle=-30
        ),
        # Footer
        dict(
            text='Generated with PlotlyVizPro | Confidential',
            xref='paper', yref='paper',
            x=1, y=-0.1,
            xanchor='right',
            showarrow=False,
            font=dict(size=9, color='#95a5a6')
        )
    ]
)

# Update axes with custom styling
fig.update_xaxes(title_text='Category', row=1, col=1)
fig.update_yaxes(title_text='Total Sales ($)', row=1, col=1)
fig.update_xaxes(title_text='Profit ($)', row=1, col=2)
fig.update_yaxes(title_text='', row=1, col=2)
fig.update_yaxes(title_text='Profit ($)', row=1, col=3)

print("🎨 Displaying custom branded dashboard...")
print("Theme includes: Custom colors, fonts, grid styling, and branding")
fig.show()
