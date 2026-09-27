# Architecture

```
plotlyvizpro/
├── charts.py        Plotly Express builders (validated inputs, project template)
├── layout.py        subplots, controls, annotations, shapes, pipe()
├── theme.py         pvp_light / pvp_dark templates, journal presets
├── colors.py        OKLab, CVD simulation, contrast, palette audit + ordering
├── stats/           plotting-free estimators returning dataclasses
│   ├── regression.py    OLS (QR, t-bands, p-values), LOWESS
│   ├── smoothing.py     rolling, EWMA, Bollinger, z-bands, Savitzky-Golay
│   ├── bootstrap.py     percentile / basic / BCa, per-group
│   ├── anomaly.py       z-score, IQR, Hampel, generalized ESD
│   ├── distributions.py KDE, ECDF+DKW, Q-Q, bin rules, describe
│   └── decomposition.py classical seasonal decomposition, ACF
├── overlays.py      draw stats results on figures
├── downsample.py    LTTB, MinMax, M4, max_error
├── export.py        HTML/PNG/SVG/PDF/JSON, save_figure with provenance
├── provenance.py    versions, git commit, SHA-256, attach/read on figure.meta
├── data.py          named datasets, schema, manifest verification
├── datasets.py      seeded generators
└── cli.py           console entry point
utils/plot_utils.py  backward-compatible facade for the notebooks
```

## Design rules

**Estimators are separate from drawing.** `plotlyvizpro.stats` has no Plotly
import. That is what lets the OLS bands be cross-checked against statsmodels to
1e-6, the ESD test against the NIST worked example, and LOWESS against
statsmodels' implementation, all without a browser or renderer.

**Every result is a dataclass.** `OLSFit`, `BootstrapResult`, `AnomalyResult`
and friends carry the arrays and the fitted quantities; overlays read them,
tests assert on them, and the Streamlit pages tabulate them.

**Overlays add, never mutate.** An overlay appends labelled traces (bands as
filled polygons with `hoverinfo="skip"`, lines, hollow markers) and stores
machine-readable results in `fig.layout.meta` (`"ols"`, `"anomalies"`,
`"provenance"`, `"journal_preset"`), so downstream code can inspect a figure
without re-fitting.

**Inputs are validated at the boundary.** `_validation.py` turns silent
pandas/Plotly failures into `KeyError`/`ValueError`/`TypeError` with the
offending names in the message. Datetime x is accepted everywhere and converted
to days (regression) or nanoseconds (generic) as appropriate.

**Colour is computed, not eyeballed.** The two registered templates use
palettes that pass `audit_palette` in their mode; the audit thresholds are the
same as the reference JavaScript validator the palettes were designed against
(numbers agree to the printed precision).

**Indices, not copies, for downsampling.** All three algorithms return index
arrays so companion columns can be aligned with one fancy-index.

**Reproducibility is default-on.** `save_figure` attaches provenance unless
told otherwise; datasets are generated from one seeded `Generator` and
verified by SHA-256 on load.

## Quality gates

| Gate | Tool | Threshold |
|---|---|---|
| Lint + format | ruff (E, W, F, I, B, UP, N, D, SIM, RUF, NPY, PD, PT) | zero findings |
| Types | mypy `--strict` on the package | zero errors |
| Tests | pytest + Hypothesis, matrix py3.10-3.13 × Linux/macOS/Windows | 85 % branch coverage floor (currently ≈98 %) |
| Notebooks | nbclient executes all ten | no error cells |
| App | Streamlit `AppTest` runs every page | no exceptions |
| Images | kaleido job renders PNG/SVG/PDF at preset DPI | pixel width matches preset |
| Build | `python -m build` + `twine check` | passes |
