"""Figure-level statistical overlays.

Each ``add_*`` function takes a :class:`plotly.graph_objects.Figure`, computes
an estimator from :mod:`plotlyvizpro.stats`, adds the corresponding traces or
shapes, and returns the figure so calls can be chained with
:func:`plotlyvizpro.layout.pipe`::

    from functools import partial

    fig = pipe(
        scatter_plot(df, "date", "sales"),
        partial(add_trendline, x=df["date"], y=df["sales"], show_ci=True),
        partial(add_moving_average, x=df["date"], y=df["sales"], window=30),
    )

The overlays never change the colour of existing traces; they add clearly
labelled series so the legend stays truthful.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import numpy as np
import plotly.graph_objects as go

from plotlyvizpro._typing import ArrayLike
from plotlyvizpro.stats import (
    anomaly as _anomaly,
)
from plotlyvizpro.stats import (
    bootstrap as _bootstrap,
)
from plotlyvizpro.stats import (
    decomposition as _decomp,
)
from plotlyvizpro.stats import (
    distributions as _dist,
)
from plotlyvizpro.stats import (
    regression as _reg,
)
from plotlyvizpro.stats import (
    smoothing as _smooth,
)

INK = "#1f1f1e"
MUTED = "#6b6b68"


def _rgba(hex_color: str, alpha: float) -> str:
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i : i + 2], 16) for i in (0, 2, 4))
    return f"rgba({r},{g},{b},{alpha})"


def _band(
    fig: go.Figure,
    x: ArrayLike,
    lower: ArrayLike,
    upper: ArrayLike,
    color: str,
    name: str,
    alpha: float = 0.15,
    **trace_kwargs: Any,
) -> go.Figure:
    xs = np.asarray(x)
    lo = np.asarray(lower, dtype=float)
    hi = np.asarray(upper, dtype=float)
    ok = ~(np.isnan(lo) | np.isnan(hi))
    fig.add_trace(
        go.Scatter(
            x=np.concatenate([xs[ok], xs[ok][::-1]]),
            y=np.concatenate([hi[ok], lo[ok][::-1]]),
            fill="toself",
            fillcolor=_rgba(color, alpha),
            line={"width": 0},
            hoverinfo="skip",
            name=name,
            legendgroup=name,
            showlegend=True,
            **trace_kwargs,
        )
    )
    return fig


def add_trendline(
    fig: go.Figure,
    x: ArrayLike,
    y: ArrayLike,
    *,
    degree: int = 1,
    confidence: float = 0.95,
    show_ci: bool = True,
    show_pi: bool = False,
    name: str | None = None,
    color: str = "#e34948",
    annotate: bool = True,
    **trace_kwargs: Any,
) -> go.Figure:
    """Add an OLS polynomial fit with optional confidence / prediction bands.

    The fitted equation and R² are written as an annotation when ``annotate``
    is ``True``.
    """
    fit = _reg.ols_fit(x, y, degree=degree, confidence=confidence)
    order = np.argsort(
        np.asarray(fit.x).astype("int64") if np.issubdtype(np.asarray(fit.x).dtype, np.datetime64) else fit.x
    )
    label = name or ("OLS fit" if degree == 1 else f"OLS degree-{degree} fit")
    if show_pi:
        _band(fig, fit.x[order], fit.pi_lower[order], fit.pi_upper[order], color, f"{label} {confidence:.0%} PI", 0.08)
    if show_ci:
        _band(fig, fit.x[order], fit.ci_lower[order], fit.ci_upper[order], color, f"{label} {confidence:.0%} CI", 0.18)
    fig.add_trace(
        go.Scatter(
            x=fit.x[order],
            y=fit.y_hat[order],
            mode="lines",
            name=label,
            line={"color": color, "width": 2, "dash": "dash"},
            **trace_kwargs,
        )
    )
    if annotate:
        fig.add_annotation(
            xref="paper",
            yref="paper",
            x=0.01,
            y=0.99,
            xanchor="left",
            yanchor="top",
            showarrow=False,
            align="left",
            font={"size": 11, "color": MUTED},
            text=f"{fit.equation()}<br>R² = {fit.r_squared:.3f}, n = {fit.dof + degree + 1}",
        )
    fig.layout.meta = {
        **(fig.layout.meta or {}),
        "ols": {"coef": fit.coef.tolist(), "r_squared": fit.r_squared, "p_values": fit.p_values.tolist()},
    }
    return fig


def add_lowess(
    fig: go.Figure,
    x: ArrayLike,
    y: ArrayLike,
    *,
    frac: float = 0.3,
    iterations: int = 3,
    name: str = "LOWESS",
    color: str = "#4a3aa7",
    **trace_kwargs: Any,
) -> go.Figure:
    """Add a robust LOWESS smoother."""
    fit = _reg.lowess(x, y, frac=frac, iterations=iterations)
    fig.add_trace(
        go.Scatter(
            x=fit.x,
            y=fit.y_hat,
            mode="lines",
            name=f"{name} (f={frac:g})",
            line={"color": color, "width": 2},
            **trace_kwargs,
        )
    )
    return fig


def add_moving_average(
    fig: go.Figure,
    x: ArrayLike,
    y: ArrayLike,
    *,
    window: int = 7,
    stat: _smooth.RollingStat = "mean",
    center: bool = False,
    name: str | None = None,
    color: str = "#1baf7a",
    **trace_kwargs: Any,
) -> go.Figure:
    """Add a rolling statistic (mean by default) line."""
    values = _smooth.rolling(y, window, stat, center=center)
    label = name or f"Rolling {stat} ({window})"
    fig.add_trace(
        go.Scatter(
            x=np.asarray(x),
            y=values,
            mode="lines",
            name=label,
            line={"color": color, "width": 2, "dash": "dot"},
            **trace_kwargs,
        )
    )
    return fig


def add_ewma(
    fig: go.Figure,
    x: ArrayLike,
    y: ArrayLike,
    *,
    span: float = 10,
    name: str | None = None,
    color: str = "#eda100",
    **trace_kwargs: Any,
) -> go.Figure:
    """Add an exponentially weighted moving average line."""
    values = _smooth.ewma(y, span=span)
    fig.add_trace(
        go.Scatter(
            x=np.asarray(x),
            y=values,
            mode="lines",
            name=name or f"EWMA (span={span:g})",
            line={"color": color, "width": 2},
            **trace_kwargs,
        )
    )
    return fig


def add_bollinger_bands(
    fig: go.Figure, x: ArrayLike, y: ArrayLike, *, window: int = 20, n_std: float = 2.0, color: str = "#2a78d6"
) -> go.Figure:
    """Add Bollinger bands (rolling mean ± n·SD) as a shaded band plus centre line."""
    bands = _smooth.bollinger_bands(y, window=window, n_std=n_std)
    xs = np.asarray(x)
    _band(fig, xs, bands.lower, bands.upper, color, bands.label)
    fig.add_trace(
        go.Scatter(
            x=xs, y=bands.centre, mode="lines", name=f"Rolling mean ({window})", line={"color": color, "width": 1.5}
        )
    )
    return fig


def add_zscore_band(
    fig: go.Figure, x: ArrayLike, y: ArrayLike, *, z: float = 2.0, robust: bool = False, color: str = "#2a78d6"
) -> go.Figure:
    """Shade the global mean ± z·SD (or median ± z·MAD) region and draw the centre line."""
    bands = _smooth.zscore_bands(y, z=z, robust=robust)
    xs = np.asarray(x)
    _band(fig, xs, bands.lower, bands.upper, color, bands.label, 0.12)
    fig.add_hline(y=float(bands.centre[0]), line={"color": color, "width": 1, "dash": "dot"})
    return fig


def add_anomalies(
    fig: go.Figure,
    x: ArrayLike,
    y: ArrayLike,
    *,
    method: str = "hampel",
    name: str | None = None,
    color: str = "#e34948",
    show_bounds: bool = False,
    **params: Any,
) -> go.Figure:
    """Mark anomalous points with hollow markers.

    ``method`` is one of ``"zscore"``, ``"iqr"``, ``"hampel"`` or ``"esd"``;
    extra keyword arguments are forwarded to the detector.
    """
    detectors: dict[str, Callable[..., _anomaly.AnomalyResult]] = {
        "zscore": _anomaly.zscore_outliers,
        "iqr": _anomaly.iqr_outliers,
        "hampel": _anomaly.hampel_filter,
        "esd": _anomaly.generalized_esd,
    }
    if method not in detectors:
        raise ValueError(f"Unknown method {method!r}; choose from {sorted(detectors)}")
    result = detectors[method](y, **params)
    xs = np.asarray(x)
    ys = np.asarray(y, dtype=float)
    if show_bounds and not np.isnan(result.lower).all():
        _band(fig, xs, result.lower, result.upper, color, f"{result.method} bounds", 0.08)
    fig.add_trace(
        go.Scatter(
            x=xs[result.mask],
            y=ys[result.mask],
            mode="markers",
            name=name or f"Anomaly ({result.method})",
            marker={"size": 12, "color": "rgba(0,0,0,0)", "line": {"color": color, "width": 2}, "symbol": "circle"},
            hovertemplate="%{x}<br>%{y}<br>score=%{customdata:.2f}<extra></extra>",
            customdata=result.score[result.mask],
        )
    )
    fig.layout.meta = {
        **(fig.layout.meta or {}),
        "anomalies": {"method": result.method, "indices": result.indices.tolist()},
    }
    return fig


def add_bootstrap_errorbars(
    fig: go.Figure,
    values: ArrayLike,
    groups: ArrayLike,
    *,
    statistic: Any = np.mean,
    confidence: float = 0.95,
    n_resamples: int = 2000,
    method: _bootstrap.Method = "bca",
    seed: int | None = 0,
    name: str | None = None,
    color: str = INK,
) -> go.Figure:
    """Add per-group point estimates with bootstrap confidence intervals as error bars."""
    results = _bootstrap.bootstrap_groups(
        values, groups, statistic, confidence=confidence, n_resamples=n_resamples, method=method, seed=seed
    )
    labels = list(results)
    est = [r.estimate for r in results.values()]
    plus = [r.upper - r.estimate for r in results.values()]
    minus = [r.estimate - r.lower for r in results.values()]
    fig.add_trace(
        go.Scatter(
            x=labels,
            y=est,
            mode="markers",
            name=name or f"{statistic.__name__} ± {confidence:.0%} {method.upper()} CI",
            marker={"size": 10, "color": color},
            error_y={
                "type": "data",
                "symmetric": False,
                "array": plus,
                "arrayminus": minus,
                "color": color,
                "thickness": 1.5,
                "width": 6,
            },
        )
    )
    return fig


def add_kde(
    fig: go.Figure,
    y: ArrayLike,
    *,
    bandwidth: _dist.Bandwidth = "scott",
    name: str = "KDE",
    color: str = "#2a78d6",
    fill: bool = True,
) -> go.Figure:
    """Add a kernel density curve (x = value, y = density)."""
    est = _dist.kde(y, bandwidth=bandwidth)
    fig.add_trace(
        go.Scatter(
            x=est.x,
            y=est.density,
            mode="lines",
            name=f"{name} (bw={est.bandwidth:.3g})",
            line={"color": color, "width": 2},
            fill="tozeroy" if fill else None,
            fillcolor=_rgba(color, 0.15),
        )
    )
    return fig


def add_ecdf(
    fig: go.Figure, y: ArrayLike, *, confidence: float | None = 0.95, name: str = "ECDF", color: str = "#2a78d6"
) -> go.Figure:
    """Add an empirical CDF step plot with an optional DKW confidence band."""
    res = _dist.ecdf(y, confidence=confidence)
    if res.lower is not None and res.upper is not None:
        _band(fig, res.x, res.lower, res.upper, color, f"{name} {confidence:.0%} DKW band", 0.12, line_shape="hv")
    fig.add_trace(
        go.Scatter(x=res.x, y=res.cdf, mode="lines", name=name, line={"color": color, "width": 2, "shape": "hv"})
    )
    fig.update_yaxes(range=[0, 1.02], title_text="F(x)")
    return fig


def add_qq(
    fig: go.Figure, y: ArrayLike, *, dist: str = "norm", name: str = "Sample", color: str = "#2a78d6"
) -> go.Figure:
    """Add Q-Q points against a theoretical distribution and the fitted reference line."""
    res = _dist.qq_points(y, dist=dist)
    fig.add_trace(
        go.Scatter(x=res.theoretical, y=res.sample, mode="markers", name=name, marker={"color": color, "size": 7})
    )
    xs = np.array([res.theoretical.min(), res.theoretical.max()])
    fig.add_trace(
        go.Scatter(
            x=xs,
            y=res.intercept + res.slope * xs,
            mode="lines",
            name=f"{dist} fit (R²={res.r_squared:.3f})",
            line={"color": MUTED, "dash": "dash"},
        )
    )
    fig.update_layout(xaxis_title=f"Theoretical quantiles ({dist})", yaxis_title="Sample quantiles")
    return fig


def decomposition_figure(
    x: ArrayLike,
    y: ArrayLike,
    period: int,
    *,
    model: _decomp.Model = "additive",
    title: str = "Seasonal decomposition",
    template: str = "pvp_light",
) -> go.Figure:
    """Build a four-panel observed / trend / seasonal / residual figure."""
    from plotly.subplots import make_subplots

    res = _decomp.seasonal_decompose(y, period=period, model=model)
    xs = np.asarray(x)
    fig = make_subplots(
        rows=4,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.04,
        subplot_titles=("Observed", "Trend", "Seasonal", "Residual"),
    )
    fig.add_trace(
        go.Scatter(x=xs, y=res.observed, mode="lines", name="Observed", line={"color": INK, "width": 1.5}), row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=xs, y=res.trend, mode="lines", name="Trend", line={"color": "#2a78d6", "width": 2}), row=2, col=1
    )
    fig.add_trace(
        go.Scatter(x=xs, y=res.seasonal, mode="lines", name="Seasonal", line={"color": "#1baf7a", "width": 1.5}),
        row=3,
        col=1,
    )
    fig.add_trace(
        go.Scatter(x=xs, y=res.residual, mode="markers", name="Residual", marker={"color": MUTED, "size": 5}),
        row=4,
        col=1,
    )
    fig.update_layout(
        title=f"{title} (period={period}, {model}; F_S={res.seasonal_strength:.2f}, F_T={res.trend_strength:.2f})",
        template=template,
        height=760,
        showlegend=False,
    )
    return fig


def acf_figure(
    y: ArrayLike, max_lag: int = 40, *, title: str = "Autocorrelation", template: str = "pvp_light"
) -> go.Figure:
    """Build a stem plot of the sample autocorrelation function with ±1.96/√n bounds."""
    acf, bound = _decomp.autocorrelation(y, max_lag=max_lag)
    lags = np.arange(acf.size)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=lags, y=acf, width=0.3, name="ACF", marker={"color": "#2a78d6"}))
    fig.add_hline(y=bound, line={"color": MUTED, "dash": "dot", "width": 1})
    fig.add_hline(y=-bound, line={"color": MUTED, "dash": "dot", "width": 1})
    fig.update_layout(title=title, xaxis_title="Lag", yaxis_title="ACF", template=template, bargap=0.6)
    return fig
