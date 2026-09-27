"""
Integration: Animated Geographic Visualization

Combine animation + geographic mapping + time series.
Demonstrates: Animation frames + choropleth + time-based transitions
"""

import plotly.express as px

# Plotly's bundled Gapminder panel has the country/year/ISO structure an animated
# choropleth needs (the project's synthetic world_population.csv has no time axis).
df = px.data.gapminder()

# Create animated choropleth map
fig = px.choropleth(
    df,
    locations="iso_alpha",
    color="lifeExp",
    hover_name="country",
    hover_data={"pop": ":,", "gdpPercap": "$:,.0f", "lifeExp": ":.1f", "iso_alpha": False},
    animation_frame="year",
    color_continuous_scale="Viridis",
    range_color=[40, 85],
    title="World Life Expectancy Evolution (1952-2007)",
    labels={"lifeExp": "Life Expectancy (years)"},
)

# Update map layout
fig.update_geos(
    showcountries=True,
    countrycolor="lightgray",
    showcoastlines=True,
    coastlinecolor="darkgray",
    projection_type="natural earth",
)

# Customize animation
fig.update_layout(
    height=600,
    width=1000,
    font=dict(size=12),
    geo=dict(bgcolor="rgba(0,0,0,0)"),
    sliders=[{"currentvalue": {"prefix": "Year: ", "font": {"size": 16, "color": "black"}}}],
)

# Slow down animation speed
fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 500
fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 300

print("🌍 Displaying animated geographic visualization...")
print("Click ▶ to watch life expectancy change over time")
fig.show()
