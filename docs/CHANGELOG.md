# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses
[Semantic Versioning](https://semver.org/).

## [2.0.0] - 2026-09-27

### Added
- Installable, typed package `plotlyvizpro` (`py.typed`, mypy `--strict` clean).
- `stats`: OLS with *t* confidence/prediction bands and p-values; robust
  LOWESS; percentile/basic/BCa bootstrap; z-score, IQR, Hampel and generalized
  ESD anomaly detectors; KDE, ECDF with DKW band, Q-Q, bin rules; classical
  seasonal decomposition with strength measures; ACF.
- `overlays`: trendline (CI/PI bands, equation annotation), LOWESS, rolling and
  EWMA lines, Bollinger and z-score bands, anomaly markers, bootstrap error
  bars, KDE/ECDF/Q-Q, decomposition and ACF figures; `layout.pipe` for chaining.
- `colors`: OKLab/OKLCH, Machado-2009 CVD simulation, WCAG contrast, five-check
  palette audit, CVD-optimal ordering, sequential ramps; Okabe-Ito and Tol palettes.
- `theme`: `pvp_light`/`pvp_dark` templates with audited palettes; journal
  presets (Nature, IEEE, Elsevier, PLOS, ACM, poster, slide) with DPI-aware export.
- `downsample`: LTTB, MinMax, M4 and `max_error`.
- `export`/`provenance`: HTML/PNG/SVG/PDF/JSON, `save_figure` with provenance
  sidecar; SHA-256 of inputs, package versions, git commit.
- `data`/`datasets`: seeded generators, checksum manifest, verified loader.
- CLI: `info`, `generate-data`, `verify-data`, `audit-palette`, `demo`, `benchmark`.
- Streamlit pages: statistical lab, palette audit, downsampling comparison;
  every page runs under `AppTest` in CI.
- CI: ruff + mypy gate, py3.10-3.13 × 3 OS matrix with coverage floor,
  kaleido export job, notebook execution job, benchmarks artifact, build check;
  docs deploy; release workflow with trusted publishing.
- MkDocs site with methods write-up, architecture, reproducibility and benchmarks.
- `CITATION.cff`, `docker-compose.yml`, multi-stage non-root Dockerfile.

### Changed
- `utils/plot_utils.py` is now a facade over the package (notebooks unchanged).
- `scatter_mapbox` deprecated in favour of token-free `scatter_map` (MapLibre).
- `apply_theme` no longer mutates built-in templates in place.
- Datasets regenerated deterministically (seed 42); exports regenerated.
- Tooling: ruff replaces black/flake8/isort; `requirements*.txt` defer to extras.

### Fixed
- Duplicate definitions of `add_trendline`, `add_moving_average`,
  `add_zscore_band` and `scatter_mapbox` shadowing each other.
- PNG export passing the `engine` argument removed in Plotly 6.
- Undefined `px` in `examples/03_integrations/dashboard_layout.py`.
- Landing page referencing a non-existent sample export.

## [1.0.0] - 2026-03-09

Initial release: ten tutorial notebooks, Streamlit gallery, `plot_utils.py`,
synthetic datasets, Docker environment.

[2.0.0]: https://github.com/SatvikPraveen/PlotlyVizPro/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/SatvikPraveen/PlotlyVizPro/releases/tag/v1.0.0
