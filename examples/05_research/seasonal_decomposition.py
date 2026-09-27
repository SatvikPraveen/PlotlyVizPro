"""Research: classical seasonal decomposition, strength measures and residual ACF."""

import numpy as np
import pandas as pd

from plotlyvizpro.export import save_figure
from plotlyvizpro.overlays import acf_figure, decomposition_figure
from plotlyvizpro.stats import seasonal_decompose

rng = np.random.default_rng(1)
t = np.arange(120)
y = 100 + 0.4 * t + 12 * np.sin(2 * np.pi * t / 12) + rng.normal(0, 3, t.size)
dates = pd.date_range("2016-01-01", periods=t.size, freq="MS")

dec = seasonal_decompose(y, period=12)
print(f"seasonal strength F_S = {dec.seasonal_strength:.3f}, trend strength F_T = {dec.trend_strength:.3f}")
print(save_figure(decomposition_figure(dates, y, period=12), "research_decomposition", formats=("html", "png")))
resid = dec.residual[~np.isnan(dec.residual)]
print(save_figure(acf_figure(resid, max_lag=24, title="Residual ACF"), "research_residual_acf", formats=("html",)))
