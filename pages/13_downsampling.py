"""Compare LTTB, MinMax and M4 on a large synthetic series."""

from __future__ import annotations

import time

import numpy as np
import plotly.graph_objects as go
import streamlit as st

import plotlyvizpro as pvp
from plotlyvizpro.downsample import lttb, m4, max_error, minmax

st.set_page_config(page_title="Downsampling", layout="wide")
st.title("Downsampling large series")
st.caption("All three algorithms return *indices*, so hover text and colour columns stay aligned with the kept points.")

with st.sidebar:
    n = st.select_slider("points", [10_000, 50_000, 200_000, 1_000_000], value=200_000)
    threshold = st.slider("target points", 200, 10_000, 2_000, 100)
    seed = st.number_input("seed", 0, 10_000, 0)

rng = np.random.default_rng(int(seed))
x = np.arange(n, dtype=float)
y = np.cumsum(rng.normal(size=n)) + 20 * np.sin(x / (n / 12))
y[n // 3] += 60  # a spike every method should keep


@st.cache_data(show_spinner=False)
def _run(n: int, threshold: int, seed: int) -> dict[str, tuple[np.ndarray, float]]:
    out = {}
    for name, fn, arg in (("LTTB", lttb, threshold), ("MinMax", minmax, threshold), ("M4", m4, max(1, threshold // 4))):
        t0 = time.perf_counter()
        keep = fn(x, y, arg)
        out[name] = (keep, time.perf_counter() - t0)
    return out


results = _run(n, threshold, int(seed))

st.dataframe(
    [
        {
            "method": k,
            "kept": int(v[0].size),
            "reduction": f"{n / v[0].size:.0f}×",
            "seconds": round(v[1], 4),
            "max |error|": round(max_error(x, y, v[0]), 3),
        }
        for k, v in results.items()
    ],
    use_container_width=True,
)

fig = pvp.create_figure(title=f"{n:,} points → ≈{threshold:,}")
for name, (keep, _) in results.items():
    fig.add_trace(go.Scatter(x=x[keep], y=y[keep], mode="lines", name=f"{name} ({keep.size})", line={"width": 1.5}))
fig.update_layout(height=520, hovermode="x")
st.plotly_chart(fig, use_container_width=True)
st.caption(
    "Zoom into the spike near x = n/3: LTTB keeps its shape with the fewest points; "
    "MinMax guarantees the envelope; M4 reproduces pixel columns exactly."
)
