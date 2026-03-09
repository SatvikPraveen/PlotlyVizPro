"""
Advanced: Custom Interactive Callbacks

Implement custom interactivity patterns beyond standard Plotly features.
Demonstrates: Custom hover behavior + click events + coordinated views
"""
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path

# Load data
data_path = Path(__file__).parent.parent.parent / 'datasets' / 'superstore.csv'
df = pd.read_csv(data_path)

# Prepare aggregated views
region_data = df.groupby('Region').agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Quantity': 'sum'
}).reset_index()

# Create linked views (scatter + bar)
fig = make_subplots(
    rows=1, cols=2,
    subplot_titles=('Sales vs Profit by Region (Click to filter) →',
                    'Top Products in Selected Region'),
    column_widths=[0.5, 0.5],
    specs=[[{'type': 'scatter'}, {'type': 'bar'}]]
)

# Main scatter plot
fig.add_trace(
    go.Scatter(
        x=region_data['Sales'],
        y=region_data['Profit'],
        mode='markers+text',
        text=region_data['Region'],
        textposition='top center',
        marker=dict(
            size=region_data['Quantity'] / 50,
            color=region_data['Profit'],
            colorscale='RdYlGn',
            showscale=True,
            line=dict(width=2, color='white'),
            colorbar=dict(title='Profit', x=0.45)
        ),
        name='Regions',
        customdata=region_data['Region'],  # Store region names for clicks
        hovertemplate='<b>%{text}</b><br>' +
                      'Sales: $%{x:,.0f}<br>' +
                      'Profit: $%{y:,.0f}<br>' +
                      '<extra></extra>'
    ),
    row=1, col=1
)

# Detail view - initially show all regions
top_products = df.groupby('SubCategory')['Sales'].sum().nlargest(10).reset_index()
fig.add_trace(
    go.Bar(
        x=top_products['Sales'],
        y=top_products['SubCategory'],
        orientation='h',
        marker_color='lightblue',
        name='Products',
        hovertemplate='%{y}<br>Sales: $%{x:,.0f}<extra></extra>'
    ),
    row=1, col=2
)

# Add click instruction annotation
fig.add_annotation(
    text='💡 Click on a region bubble to see its top products',
    xref='paper', yref='paper',
    x=0.5, y=1.1,
    showarrow=False,
    font=dict(size=13, color='blue'),
    bgcolor='lightyellow',
    bordercolor='orange',
    borderwidth=2
)

# Configure layout
fig.update_xaxes(title_text='Total Sales ($)', row=1, col=1)
fig.update_yaxes(title_text='Total Profit ($)', row=1, col=1)
fig.update_xaxes(title_text='Sales ($)', row=1, col=2)
fig.update_yaxes(title_text='', showticklabels=True, row=1, col=2)

fig.update_layout(
    title='Interactive Regional Analysis - Click to Drill Down',
    height=600,
    width=1400,
    showlegend=False,
    hovermode='closest',
    template='plotly_white'
)

print("🖱️  Displaying interactive coordinated views...")
print("Features:")
print("  - Bubble size represents quantity sold")
print("  - Color represents profit (green=high, red=low)")
print("  - Click bubbles to filter detailed view")
print("\nNote: For full click interactivity, integrate with Dash using:")
print("  @app.callback(Output('detail-chart', 'figure'), Input('scatter', 'clickData'))")
fig.show()

# Example Dash callback implementation:
"""
from dash import Dash, dcc, html, Input, Output

app = Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='scatter', figure=fig),
    dcc.Graph(id='detail')
])

@app.callback(
    Output('detail', 'figure'),
    Input('scatter', 'clickData')
)
def update_detail(clickData):
    if clickData is None:
        region = None  # Show all
    else:
        region = clickData['points'][0]['customdata']
    
    # Filter data by selected region
    filtered = df if region is None else df[df['Region'] == region]
    top_products = filtered.groupby('SubCategory')['Sales'].sum().nlargest(10)
    
    # Return updated figure
    return px.bar(top_products, orientation='h', 
                  title=f'Top Products in {region or "All Regions"}')

if __name__ == '__main__':
    app.run_server(debug=True)
"""
