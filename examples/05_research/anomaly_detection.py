"""Research: compare four anomaly detectors on a drifting stock series."""

import plotlyvizpro as pvp
from plotlyvizpro.data import load
from plotlyvizpro.export import save_figure
from plotlyvizpro.overlays import add_anomalies
from plotlyvizpro.stats import generalized_esd, hampel_filter, iqr_outliers, zscore_outliers

stocks = load("stocks")
s = stocks[stocks["Company"] == "AlphaCorp"].reset_index(drop=True)
x, y = s["Date"], s["Close"]

for name, res in {
    "z-score": zscore_outliers(y, 3),
    "IQR": iqr_outliers(y, 1.5),
    "Hampel": hampel_filter(y, window=7),
    "ESD": generalized_esd(y, max_outliers=5),
}.items():
    print(f"{name:8s} flagged {res.n_anomalies:2d}: {res.indices.tolist()}")

fig = pvp.line_plot(s, "Date", "Close", title="AlphaCorp close: Hampel (red) vs generalized ESD (violet)")
add_anomalies(fig, x, y, method="hampel", window=7, show_bounds=True)
add_anomalies(fig, x, y, method="esd", max_outliers=5, color="#4a3aa7", name="ESD anomaly")
print(save_figure(fig, "research_anomalies", formats=("html", "png")))
