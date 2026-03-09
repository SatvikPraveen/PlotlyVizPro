"""
Integration: Interactive Data Explorer

Combine dropdowns + sliders + multiple chart updates.
Demonstrates: Callbacks via updatemenus + dynamic filtering + responsive design
"""
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

# Load data
data_path = Path(__file__).parent.parent.parent / 'datasets' / 'superstore.csv'
df = pd.read_csv(data_path, parse_dates=['OrderDate'])

# Create traces for each region
regions = df['Region'].unique()
categories = df['Category'].unique()

# Initialize figure
fig = go.Figure()

# Create a trace for each region-category combination
for region in regions:
    for category in categories:
        filtered_df = df[(df['Region'] == region) & (df['Category'] == category)]
        monthly = filtered_df.groupby(filtered_df['OrderDate'].dt.to_period('M'))['Sales'].sum()
        
        fig.add_trace(go.Scatter(
            x=[str(x) for x in monthly.index],
            y=monthly.values,
            name=f'{region} - {category}',
            mode='lines+markers',
            visible=(region == regions[0] and category == categories[0])  # Only first visible
        ))

# Create dropdown menus for region and category
region_buttons = []
for i, region in enumerate(regions):
    visible = [False] * len(fig.data)
    # Show all categories for this region
    for j, category in enumerate(categories):
        trace_idx = i * len(categories) + j
        visible[trace_idx] = True
    
    region_buttons.append(
        dict(label=region,
             method='update',
             args=[{'visible': visible},
                   {'title': f'Sales Trend - {region} (All Categories)'}])
    )

category_buttons = []
for j, category in enumerate(categories):
    visible = [False] * len(fig.data)
    # Show this category for all regions
    for i in range(len(regions)):
        trace_idx = i * len(categories) + j
        visible[trace_idx] = True
    
    category_buttons.append(
        dict(label=category,
             method='update',
             args=[{'visible': visible},
                   {'title': f'Sales Trend - {category} (All Regions)'}])
    )

# Add dropdown menus
fig.update_layout(
    updatemenus=[
        dict(
            buttons=region_buttons,
            direction='down',
            pad={'r': 10, 't': 10},
            showactive=True,
            x=0.1,
            xanchor='left',
            y=1.15,
            yanchor='top',
            bgcolor='lightblue',
            bordercolor='gray',
            font=dict(size=11)
        ),
        dict(
            buttons=category_buttons,
            direction='down',
            pad={'r': 10, 't': 10},
            showactive=True,
            x=0.35,
            xanchor='left',
            y=1.15,
            yanchor='top',
            bgcolor='lightgreen',
            bordercolor='gray',
            font=dict(size=11)
        )
    ],
    annotations=[
        dict(text='<b>Filter by Region:</b>', x=0.05, y=1.12, xref='paper', yref='paper',
             showarrow=False, font=dict(size=12)),
        dict(text='<b>Filter by Category:</b>', x=0.28, y=1.12, xref='paper', yref='paper',
             showarrow=False, font=dict(size=12))
    ],
    title='Interactive Sales Explorer - Use Dropdowns to Filter',
    xaxis_title='Month',
    yaxis_title='Sales ($)',
    height=600,
    template='plotly_white',
    hovermode='x unified'
)

print("🔍 Displaying interactive data explorer...")
print("Use the dropdown menus to filter by Region or Category")
fig.show()
