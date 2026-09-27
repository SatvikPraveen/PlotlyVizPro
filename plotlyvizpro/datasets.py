"""Deterministic synthetic dataset generation.

Every generator draws from a single :class:`numpy.random.Generator` seeded
once, so ``generate_all(seed=42)`` reproduces byte-identical CSVs on any
platform. Faker is optional: when it is not installed, names are drawn from
small built-in vocabularies so the core package has no hard dependency on it.
"""

from __future__ import annotations

import uuid
from collections.abc import Callable
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

from plotlyvizpro._typing import StrPath
from plotlyvizpro.data import datasets_dir, write_manifest

DEFAULT_SEED = 42

_COUNTRIES = [
    "Argentina",
    "Australia",
    "Austria",
    "Belgium",
    "Brazil",
    "Canada",
    "Chile",
    "China",
    "Colombia",
    "Czechia",
    "Denmark",
    "Egypt",
    "Ethiopia",
    "Finland",
    "France",
    "Germany",
    "Ghana",
    "Greece",
    "Hungary",
    "India",
    "Indonesia",
    "Ireland",
    "Israel",
    "Italy",
    "Japan",
    "Kenya",
    "Malaysia",
    "Mexico",
    "Morocco",
    "Netherlands",
    "New Zealand",
    "Nigeria",
    "Norway",
    "Pakistan",
    "Peru",
    "Philippines",
    "Poland",
    "Portugal",
    "Romania",
    "Saudi Arabia",
    "Singapore",
    "South Africa",
    "South Korea",
    "Spain",
    "Sweden",
    "Switzerland",
    "Thailand",
    "Turkey",
    "Ukraine",
    "United Arab Emirates",
    "United Kingdom",
    "United States",
    "Uruguay",
    "Vietnam",
    "Bangladesh",
    "Sri Lanka",
    "Nepal",
    "Iceland",
    "Estonia",
    "Latvia",
]
_CITIES = [
    "Springfield",
    "Riverside",
    "Franklin",
    "Greenville",
    "Bristol",
    "Clinton",
    "Fairview",
    "Salem",
    "Madison",
    "Georgetown",
    "Arlington",
    "Ashland",
    "Burlington",
    "Dover",
    "Hudson",
    "Kingston",
    "Lexington",
    "Milton",
    "Newport",
    "Oxford",
]
_STATES = [
    "Alabama",
    "Alaska",
    "Arizona",
    "Arkansas",
    "California",
    "Colorado",
    "Connecticut",
    "Delaware",
    "Florida",
    "Georgia",
    "Hawaii",
    "Idaho",
    "Illinois",
    "Indiana",
    "Iowa",
    "Kansas",
    "Kentucky",
    "Louisiana",
    "Maine",
    "Maryland",
    "Massachusetts",
    "Michigan",
    "Minnesota",
    "Mississippi",
    "Missouri",
    "Montana",
    "Nebraska",
    "Nevada",
    "New Hampshire",
    "New Jersey",
    "New Mexico",
    "New York",
    "North Carolina",
    "North Dakota",
    "Ohio",
    "Oklahoma",
    "Oregon",
    "Pennsylvania",
    "Rhode Island",
    "South Carolina",
    "South Dakota",
    "Tennessee",
    "Texas",
    "Utah",
    "Vermont",
    "Virginia",
    "Washington",
    "West Virginia",
    "Wisconsin",
    "Wyoming",
]


def _uuid(rng: np.random.Generator) -> str:
    return str(uuid.UUID(bytes=rng.bytes(16), version=4))


def superstore(rng: np.random.Generator, n: int = 1000, end: date = date(2025, 12, 31)) -> pd.DataFrame:
    """Retail orders with category/sub-category/region and sales/profit."""
    subcats = {
        "Furniture": ["Chairs", "Tables", "Bookcases"],
        "Office Supplies": ["Binders", "Paper", "Pens"],
        "Technology": ["Phones", "Laptops", "Accessories"],
    }
    cats = rng.choice(list(subcats), n)
    rows = []
    for cat in cats:
        sub = rng.choice(subcats[cat])
        region = rng.choice(["East", "West", "Central", "South"])
        day = end - timedelta(days=int(rng.integers(0, 365)))
        sales = round(float(rng.uniform(10, 1000)), 2)
        profit = round(float(rng.uniform(-100, 300)), 2)
        rows.append([_uuid(rng), day, cat, sub, region, sales, profit])
    return pd.DataFrame(rows, columns=["OrderID", "OrderDate", "Category", "SubCategory", "Region", "Sales", "Profit"])


def covid(rng: np.random.Generator, days: int = 365) -> pd.DataFrame:
    """Cumulative cases/deaths as a clipped random walk per country."""
    base = date(2020, 1, 1)
    rows = []
    for country in ["USA", "India", "Brazil", "UK", "Germany"]:
        cases, deaths = 100, 1
        for i in range(days):
            cases = max(cases + int(rng.normal(300, 100)), 0)
            deaths = max(deaths + int(rng.normal(5, 2)), 0)
            rows.append([country, base + timedelta(days=i), cases, deaths])
    return pd.DataFrame(rows, columns=["Country", "Date", "Cases", "Deaths"])


def stocks(rng: np.random.Generator, days: int = 180, end: date = date(2025, 12, 31)) -> pd.DataFrame:
    """Daily OHLCV for three tickers, Gaussian increments."""
    base = end - timedelta(days=days)
    rows = []
    for company in ["AlphaCorp", "BetaTech", "GammaHealth"]:
        price = round(float(rng.uniform(20, 100)), 2)
        for i in range(days):
            open_p = round(price + float(rng.normal(0, 2)), 2)
            close = round(open_p + float(rng.normal(0, 2)), 2)
            high = round(max(open_p, close) + float(rng.uniform(0, 2)), 2)
            low = round(min(open_p, close) - float(rng.uniform(0, 2)), 2)
            volume = int(rng.integers(1000, 5001))
            rows.append([company, base + timedelta(days=i), open_p, close, high, low, volume])
            price = close
    return pd.DataFrame(rows, columns=["Company", "Date", "Open", "Close", "High", "Low", "Volume"])


def world_population(rng: np.random.Generator, n: int = 60) -> pd.DataFrame:
    """Country indicators drawn independently."""
    countries = rng.choice(_COUNTRIES, size=n, replace=False)
    return pd.DataFrame(
        {
            "Country": countries,
            "Population": rng.integers(1_000_000, 1_500_000_000, n),
            "GDP_per_capita": np.round(rng.uniform(1000, 60000, n), 2),
            "Life_Expectancy": np.round(rng.uniform(50, 85, n), 2),
            "Continent": rng.choice(["Asia", "Europe", "Africa", "Americas", "Oceania"], n),
        }
    )


def customer_segments(rng: np.random.Generator, n: int = 500) -> pd.DataFrame:
    """Generate customer demographics."""
    return pd.DataFrame(
        {
            "CustomerID": [_uuid(rng) for _ in range(n)],
            "Gender": rng.choice(["Male", "Female", "Other"], n),
            "Age": rng.integers(18, 71, n),
            "Income": rng.integers(20_000, 150_001, n),
            "Segment": rng.choice(["Budget", "Mid-range", "Premium"], n),
            "Region": rng.choice(_STATES, n),
        }
    )


def product_launch(rng: np.random.Generator) -> pd.DataFrame:
    """Weekly sales and marketing spend across lifecycle stages."""
    rows = []
    for product in ["ProdX", "ProdY", "ProdZ"]:
        for stage in ["Pre-Launch", "Launch", "Growth", "Maturity", "Decline"]:
            for week in range(1, 5):
                rows.append(
                    [
                        product,
                        stage,
                        week,
                        round(float(rng.uniform(1000, 10000)), 2),
                        round(float(rng.uniform(500, 5000)), 2),
                    ]
                )
    return pd.DataFrame(rows, columns=["Product", "Stage", "Week", "Sales", "MarketingSpend"])


def map_points(rng: np.random.Generator, n: int = 100) -> pd.DataFrame:
    """City points with random coordinates and a score."""
    return pd.DataFrame(
        {
            "City": [f"{rng.choice(_CITIES)} {i + 1}" for i in range(n)],
            "Latitude": np.round(rng.uniform(-90, 90, n), 6),
            "Longitude": np.round(rng.uniform(-180, 180, n), 6),
            "Score": np.round(rng.uniform(0, 100, n), 2),
        }
    )


def animated_sales(rng: np.random.Generator) -> pd.DataFrame:
    """Monthly category sales for a single year."""
    months = pd.date_range("2022-01-01", periods=12, freq="MS").strftime("%Y-%m")
    rows = [
        [m, c, round(float(rng.uniform(5000, 25000)), 2)]
        for c in ["Electronics", "Apparel", "Books", "Home"]
        for m in months
    ]
    return pd.DataFrame(rows, columns=["Month", "Category", "Sales"])


GENERATORS: dict[str, Callable[[np.random.Generator], pd.DataFrame]] = {
    "superstore.csv": superstore,
    "covid_data.csv": covid,
    "stock_data.csv": stocks,
    "world_population.csv": world_population,
    "customer_segments.csv": customer_segments,
    "product_launch.csv": product_launch,
    "map_data.csv": map_points,
    "animated_sales.csv": animated_sales,
}


def generate_all(
    directory: StrPath | None = None, seed: int = DEFAULT_SEED, *, manifest: bool = True
) -> dict[str, Path]:
    """Generate every dataset into ``directory`` and (optionally) write the manifest.

    Returns a mapping ``filename -> path``.
    """
    base = Path(directory) if directory is not None else datasets_dir()
    base.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)
    written: dict[str, Path] = {}
    for filename, gen in GENERATORS.items():
        df = gen(rng)
        path = base / filename
        df.to_csv(path, index=False, lineterminator="\n")
        written[filename] = path
    if manifest:
        written["manifest.json"] = write_manifest(
            base, seed=seed, extra={"generator": "plotlyvizpro.datasets.generate_all"}
        )
    return written
