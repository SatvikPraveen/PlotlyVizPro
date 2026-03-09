"""
Advanced: Statistical Analysis Overlays

Advanced statistical visualizations with confidence intervals and distributions.
Demonstrates: Multiple statistical layers + uncertainty visualization + annotations
"""
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy import stats
from pathlib import Path

# Load data
data_path = Path(__file__).parent.parent.parent / 'datasets' / 'superstore.csv'
df = pd.read_csv(data_path, parse_dates=['OrderDate'])

# Analyze sales by category with statistical metrics
category_sales = df.groupby('Category')['Sales'].apply(list).to_dict()

# Calculate statistics for each category
stats_data = []
for category, sales in category_sales.items():
    stats_data.append({
        'category': category,
        'mean': np.mean(sales),
        'median': np.median(sales),
        'std': np.std(sales),
        'n': len(sales),
        'sales': sales
    })

stats_df = pd.DataFrame(stats_data)

# Calculate 95% confidence intervals
confidence_level = 0.95
stats_df['ci_lower'] = stats_df.apply(
    lambda row: stats.t.interval(confidence_level, row['n']-1, 
                                  loc=row['mean'], 
                                  scale=stats.sem(row['sales']))[0],
    axis=1
)
stats_df['ci_upper'] = stats_df.apply(
    lambda row: stats.t.interval(confidence_level, row['n']-1,
                                  loc=row['mean'],
                                  scale=stats.sem(row['sales']))[1],
    axis=1
)

# Create advanced statistical visualization
fig = go.Figure()

# Layer 1: Confidence interval bands
for _, row in stats_df.iterrows():
    fig.add_trace(go.Scatter(
        x=[row['category'], row['category']],
        y=[row['ci_lower'], row['ci_upper']],
        mode='lines',
        line=dict(color='lightgray', width=15),
        showlegend=False,
        hoverinfo='skip'
    ))

# Layer 2: Box plots for distribution
for category in stats_df['category']:
    sales = category_sales[category]
    fig.add_trace(go.Box(
        y=sales,
        name=category,
        x=[category] * len(sales),
        boxmean='sd',  # Show mean and standard deviation
        marker_color='lightblue',
        line=dict(color='blue'),
        showlegend=False
    ))

# Layer 3: Mean with error bars
fig.add_trace(go.Scatter(
    x=stats_df['category'],
    y=stats_df['mean'],
    mode='markers',
    marker=dict(size=15, color='red', symbol='diamond', line=dict(width=2, color='white')),
    error_y=dict(
        type='data',
        symmetric=False,
        array=stats_df['ci_upper'] - stats_df['mean'],
        arrayminus=stats_df['mean'] - stats_df['ci_lower'],
        color='red',
        thickness=2,
        width=6
    ),
    name='Mean ± 95% CI',
    hovertemplate='<b>%{x}</b><br>' +
                  'Mean: $%{y:,.0f}<br>' +
                  '<extra></extra>'
))

# Layer 4: Sample size annotations
for _, row in stats_df.iterrows():
    fig.add_annotation(
        x=row['category'],
        y=row['ci_upper'],
        text=f"n={row['n']}",
        showarrow=False,
        yshift=10,
        font=dict(size=10, color='gray')
    )

# Add statistical summary annotation
summary_text = (
    "<b>Statistical Summary</b><br>"
    f"Confidence Level: {confidence_level*100}%<br>"
    f"Total Samples: {len(df):,}<br>"
    "Red diamonds: Mean<br>"
    "Error bars: 95% CI<br>"
    "Blue boxes: Distribution"
)

fig.add_annotation(
    text=summary_text,
    xref='paper', yref='paper',
    x=1.02, y=0.98,
    xanchor='left', yanchor='top',
    showarrow=False,
    bgcolor='lightyellow',
    bordercolor='orange',
    borderwidth=2,
    font=dict(size=10)
)

# Update layout
fig.update_layout(
    title='Advanced Statistical Analysis - Sales by Category<br>' +
          '<sub>Box plots with confidence intervals and distribution metrics</sub>',
    xaxis_title='Product Category',
    yaxis_title='Sales per Transaction ($)',
    template='plotly_white',
    height=700,
    showlegend=True,
    hovermode='closest'
)

# Add reference lines for overall mean
overall_mean = df['Sales'].mean()
fig.add_hline(
    y=overall_mean,
    line_dash='dash',
    line_color='green',
    annotation_text=f'Overall Mean: ${overall_mean:.0f}',
    annotation_position='right'
)

print("📊 Displaying advanced statistical analysis...")
print("\nStatistical Summary by Category:")
print("="*70)
for _, row in stats_df.iterrows():
    print(f"{row['category']:20s} | Mean: ${row['mean']:8,.0f} | "
          f"95% CI: [${row['ci_lower']:,.0f}, ${row['ci_upper']:,.0f}] | "
          f"n={row['n']}")
print("="*70)

fig.show()

# Bonus: Regression analysis
print("\n📈 Bonus: Regression analysis...")

# Sales vs Profit regression
fig2 = go.Figure()

# Scatter plot
fig2.add_trace(go.Scatter(
    x=df['Sales'],
    y=df['Profit'],
    mode='markers',
    marker=dict(size=3, color='lightblue', opacity=0.5),
    name='Data Points'
))

# Calculate regression
slope, intercept, r_value, p_value, std_err = stats.linregress(df['Sales'], df['Profit'])
x_range = np.array([df['Sales'].min(), df['Sales'].max()])
y_pred = slope * x_range + intercept

# Add regression line
fig2.add_trace(go.Scatter(
    x=x_range,
    y=y_pred,
    mode='lines',
    line=dict(color='red', width=3),
    name=f'Regression (R²={r_value**2:.3f})'
))

# Add confidence band (simplified)
margin = 1.96 * std_err * x_range  # 95% CI approximation
fig2.add_trace(go.Scatter(
    x=np.concatenate([x_range, x_range[::-1]]),
    y=np.concatenate([y_pred + margin, (y_pred - margin)[::-1]]),
    fill='toself',
    fillcolor='rgba(255,0,0,0.1)',
    line=dict(color='rgba(255,0,0,0)'),
    name='95% Confidence',
    showlegend=True
))

fig2.update_layout(
    title=f'Linear Regression: Sales vs Profit<br><sub>y = {slope:.2f}x + {intercept:.2f} (p={p_value:.2e})</sub>',
    xaxis_title='Sales ($)',
    yaxis_title='Profit ($)',
    template='plotly_white'
)

print(f"Regression equation: Profit = {slope:.3f} × Sales + {intercept:.2f}")
print(f"R² = {r_value**2:.3f} (explains {r_value**2*100:.1f}% of variance)")
print(f"p-value = {p_value:.2e} ({'significant' if p_value < 0.05 else 'not significant'})")

fig2.show()
