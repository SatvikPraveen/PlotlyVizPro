"""
Recipe: Top N Analysis

Identify and visualize top performers (products, regions, categories).
Use Case: Sales leaders, best customers, top performers
"""
import pandas as pd
import plotly.express as px
from pathlib import Path

# Load data
data_path = Path(__file__).parent.parent.parent / 'datasets' / 'superstore.csv'
df = pd.read_csv(data_path)

# Calculate profit by subcategory
profit_by_subcat = df.groupby('SubCategory')['Profit'].sum().reset_index()

# Get top 10 and bottom 5
top_10 = profit_by_subcat.nlargest(10, 'Profit')
bottom_5 = profit_by_subcat.nsmallest(5, 'Profit')

# Combine and create category
combined = pd.concat([top_10, bottom_5])
combined['Performance'] = combined['Profit'].apply(
    lambda x: 'Top 10' if x > 0 else 'Bottom 5'
)

# Create horizontal bar chart (easier to read labels)
fig = px.bar(
    combined.sort_values('Profit'),
    y='SubCategory',
    x='Profit',
    color='Performance',
    title='Top 10 Most Profitable vs Bottom 5 Least Profitable Subcategories',
    labels={'Profit': 'Total Profit ($)', 'SubCategory': ''},
    color_discrete_map={'Top 10': 'green', 'Bottom 5': 'red'},
    orientation='h'
)

# Add vertical line at zero
fig.add_vline(x=0, line_dash="dash", line_color="gray")

# Customize
fig.update_layout(
    xaxis_title='Profit ($)',
    yaxis={'categoryorder': 'total ascending'},
    height=600,
    showlegend=True
)

print("🏆 Displaying top/bottom performers...")
print(f"Top performer: {top_10.iloc[0]['SubCategory']} (${top_10.iloc[0]['Profit']:,.0f})")
print(f"Needs attention: {bottom_5.iloc[0]['SubCategory']} (${bottom_5.iloc[0]['Profit']:,.0f})")
fig.show()
