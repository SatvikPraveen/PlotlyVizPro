# Examples

Runnable scripts, grouped by intent. Run any of them from the repository root
after `pip install -e ".[all]"`; outputs go to `exports/` (override with
`PLOTLYVIZPRO_EXPORT_DIR`).

| Folder | Contents |
|---|---|
| `01_quick_starts/` | one chart each: line, bar, scatter, bubble, dark theme, saving |
| `02_recipes/` | category comparison, correlation heatmap, multi-metric dashboard, time-series trend, top-N |
| `03_integrations/` | animated geo, branding/theming, dashboard layout, interactive explorer |
| `04_advanced/` | custom interactions, parametric plotting, performance, real-time simulation, statistical overlays |
| `05_research/` | **the research toolkit**: uncertainty overlays (OLS bands, LOWESS, BCa bootstrap), anomaly detection, palette audit and CVD simulation, million-point downsampling, journal-preset export with provenance, seasonal decomposition |

```bash
python examples/05_research/uncertainty_overlays.py
python examples/05_research/palette_audit.py
python examples/05_research/downsample_million.py
```

Scripts in 01-04 use the legacy `utils.plot_utils` facade or raw Plotly and
still run; new code should follow `05_research/` and import from
`plotlyvizpro` directly.
