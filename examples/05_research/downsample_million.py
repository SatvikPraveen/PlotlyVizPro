"""Research: downsample a million-point series three ways and compare error and timing."""

import time

import numpy as np
import plotly.graph_objects as go

import plotlyvizpro as pvp
from plotlyvizpro.downsample import lttb, m4, max_error, minmax
from plotlyvizpro.export import save_figure

rng = np.random.default_rng(0)
n = 1_000_000
x = np.arange(n, dtype=float)
y = np.cumsum(rng.normal(size=n)) + 30 * np.sin(x / 80_000)

fig = pvp.create_figure(title=f"{n:,} points reduced to ≈4 000")
for name, fn, arg in (("LTTB", lttb, 4000), ("MinMax", minmax, 4000), ("M4", m4, 1000)):
    t0 = time.perf_counter()
    keep = fn(x, y, arg)
    dt = time.perf_counter() - t0
    err = max_error(x, y, keep)
    print(f"{name:7s} kept {keep.size:5d}  {dt * 1000:7.1f} ms  max|err| {err:6.2f}")
    fig.add_trace(go.Scatter(x=x[keep], y=y[keep], mode="lines", name=f"{name} ({keep.size})", line={"width": 1.2}))
print(save_figure(fig, "research_downsample", formats=("html",)))
