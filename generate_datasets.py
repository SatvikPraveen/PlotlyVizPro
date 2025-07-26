import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import os
import random

# ========== CONFIG ==========
faker = Faker()
np.random.seed(42)
random.seed(42)
os.makedirs("datasets", exist_ok=True)

# Toggle this to True if you want to visualize a quick sanity-check using Plotly
ENABLE_SANITY_PLOTS = False

if ENABLE_SANITY_PLOTS:
    import plotly.express as px

# ========== 1. Superstore Sales Dataset ==========
def generate_superstore():
    categories = ['Furniture', 'Office Supplies', 'Technology']
    subcategories = {
        'Furniture': ['Chairs', 'Tables', 'Bookcases'],
        'Office Supplies': ['Binders', 'Paper', 'Pens'],
        'Technology': ['Phones', 'Laptops', 'Accessories']
    }
    regions = ['East', 'West', 'Central', 'South']
    rows = []

    for _ in range(1000):
        cat = random.choice(categories)
        sub = random.choice(subcategories[cat])
        region = random.choice(regions)
        date = faker.date_between(start_date='-1y', end_date='today')
        sales = round(random.uniform(10, 1000), 2)
        profit = round(random.uniform(-100, 300), 2)
        rows.append([faker.uuid4(), date, cat, sub, region, sales, profit])

    df = pd.DataFrame(rows, columns=[
        'OrderID', 'OrderDate', 'Category', 'SubCategory', 'Region', 'Sales', 'Profit'
    ])
    df.to_csv("datasets/superstore.csv", index=False)

# ========== 2. COVID Time Series ==========
def generate_covid_data():
    countries = ['USA', 'India', 'Brazil', 'UK', 'Germany']
    base_date = datetime(2020, 1, 1)
    data = []

    for country in countries:
        cases = 100
        deaths = 1
        for i in range(365):
            date = base_date + timedelta(days=i)
            cases += int(np.random.normal(300, 100))
            deaths += int(np.random.normal(5, 2))
            data.append([country, date.date(), max(cases, 0), max(deaths, 0)])

    df = pd.DataFrame(data, columns=['Country', 'Date', 'Cases', 'Deaths'])
    df.to_csv("datasets/covid_data.csv", index=False)

# ========== 3. Stock Price Data ==========
def generate_stock_data():
    companies = ['AlphaCorp', 'BetaTech', 'GammaHealth']
    base_date = datetime.today() - timedelta(days=180)
    data = []

    for company in companies:
        price = round(random.uniform(20, 100), 2)
        for i in range(180):
            date = base_date + timedelta(days=i)
            open_price = round(price + np.random.normal(0, 2), 2)
            close = round(open_price + np.random.normal(0, 2), 2)
            high = max(open_price, close) + round(random.uniform(0, 2), 2)
            low = min(open_price, close) - round(random.uniform(0, 2), 2)
            volume = random.randint(1000, 5000)
            data.append([company, date.date(), open_price, close, high, low, volume])
            price = close

    df = pd.DataFrame(data, columns=['Company', 'Date', 'Open', 'Close', 'High', 'Low', 'Volume'])
    df.to_csv("datasets/stock_data.csv", index=False)

# ========== 4. World Population ==========
def generate_world_population():
    countries = [faker.country() for _ in range(60)]
    data = []

    for country in countries:
        population = random.randint(1_000_000, 1_500_000_000)
        gdp = round(random.uniform(1000, 60000), 2)
        life_expectancy = round(random.uniform(50, 85), 2)
        continent = random.choice(['Asia', 'Europe', 'Africa', 'Americas', 'Oceania'])
        data.append([country, population, gdp, life_expectancy, continent])

    df = pd.DataFrame(data, columns=[
        'Country', 'Population', 'GDP_per_capita', 'Life_Expectancy', 'Continent'
    ])
    df.to_csv("datasets/world_population.csv", index=False)

# ========== 5. Customer Segments ==========
def generate_customer_segments():
    data = []

    for _ in range(500):
        gender = random.choice(['Male', 'Female', 'Other'])
        age = random.randint(18, 70)
        income = random.randint(20_000, 150_000)
        segment = random.choice(['Budget', 'Mid-range', 'Premium'])
        region = faker.state()
        data.append([faker.uuid4(), gender, age, income, segment, region])

    df = pd.DataFrame(data, columns=[
        'CustomerID', 'Gender', 'Age', 'Income', 'Segment', 'Region'
    ])
    df.to_csv("datasets/customer_segments.csv", index=False)

# ========== 6. Product Launch Lifecycle ==========
def generate_product_launch():
    stages = ['Pre-Launch', 'Launch', 'Growth', 'Maturity', 'Decline']
    products = ['ProdX', 'ProdY', 'ProdZ']
    data = []

    for product in products:
        for stage in stages:
            for week in range(1, 5):
                sales = round(random.uniform(1000, 10000), 2)
                marketing_spend = round(random.uniform(500, 5000), 2)
                data.append([product, stage, week, sales, marketing_spend])

    df = pd.DataFrame(data, columns=['Product', 'Stage', 'Week', 'Sales', 'MarketingSpend'])
    df.to_csv("datasets/product_launch.csv", index=False)

# ========== 7. Geo Location Data ==========
def generate_map_data():
    cities = [faker.city() for _ in range(100)]
    data = []

    for city in cities:
        lat = faker.latitude()
        lon = faker.longitude()
        score = round(random.uniform(0, 100), 2)
        data.append([city, lat, lon, score])

    df = pd.DataFrame(data, columns=['City', 'Latitude', 'Longitude', 'Score'])
    df.to_csv("datasets/map_data.csv", index=False)

# ========== 8. Animated Sales Data ==========
def generate_animated_sales():
    categories = ['Electronics', 'Apparel', 'Books', 'Home']
    months = pd.date_range(start="2022-01-01", periods=12, freq="ME").strftime('%Y-%m')
    data = []

    for cat in categories:
        for month in months:
            sales = round(random.uniform(5000, 25000), 2)
            data.append([month, cat, sales])

    df = pd.DataFrame(data, columns=['Month', 'Category', 'Sales'])
    df.to_csv("datasets/animated_sales.csv", index=False)

# ========== Main Execution ==========
if __name__ == "__main__":
    generate_superstore()
    generate_covid_data()
    generate_stock_data()
    generate_world_population()
    generate_customer_segments()
    generate_product_launch()
    generate_map_data()
    generate_animated_sales()

    print("✅ All datasets generated successfully in ./datasets/")

    if ENABLE_SANITY_PLOTS:
        import plotly.express as px
        df = pd.read_csv("datasets/superstore.csv")
        fig = px.bar(df, x="SubCategory", y="Sales", color="Region")
        fig.show()
