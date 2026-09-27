# Contributing to PlotlyVizPro

Thanks for your interest. This document explains how the project is organised,
what the quality gates are, and how to get a change merged.

## Set up

```bash
git clone https://github.com/<you>/PlotlyVizPro.git
cd PlotlyVizPro
make install-dev        # .venv with dev/docs/notebook extras, pre-commit hooks
make check              # ruff + mypy --strict + pytest with coverage gate
```

`make help` lists every target.

## Where things live

| Path | Purpose |
|---|---|
| `plotlyvizpro/` | the library. `stats/` holds estimators (no Plotly imports); `overlays.py` draws them; `charts.py`/`layout.py`/`theme.py` build figures; `colors.py`, `downsample.py`, `export.py`, `provenance.py`, `data.py`, `datasets.py`, `cli.py` |
| `tests/` | pytest suite; property tests with Hypothesis; cross-checks against statsmodels/SciPy; Streamlit `AppTest` |
| `benchmarks/` | pytest-benchmark suite |
| `notebooks/`, `pages/`, `app.py` | tutorial notebooks and the Streamlit gallery |
| `examples/` | runnable scripts (`05_research/` uses the package API) |
| `docs/` + `mkdocs.yml` | documentation site; `docs/methods.md` is the mathematical spec |
| `utils/plot_utils.py` | backward-compatible facade for the notebooks; do not add new features here |

See [docs/architecture.md](docs/architecture.md) for the design rules.

## Quality gates (all enforced in CI)

- **ruff** lint and format (`make lint` / `make format`), including numpy-style docstrings on public functions.
- **mypy --strict** on `plotlyvizpro/` (`make typecheck`).
- **pytest** on Python 3.10-3.13 with an 85 % branch-coverage floor (`make coverage`). New estimators need:
  - a closed-form or reference-implementation check (statsmodels/SciPy are available via the `dev` extra, skip-marked when absent),
  - error-path tests for bad inputs,
  - a property test when the function has an invariant (Hypothesis).
- **Notebook execution** (`make test-notebooks`) and **AppTest** for any page you touch.
- **Docs build** with `mkdocs build --strict`; new public modules get an entry under `docs/api/`.

## Adding an estimator + overlay

1. Implement it in the right `plotlyvizpro/stats/*.py` module, returning a dataclass; validate inputs with helpers from `_validation.py`; accept datetime `x` where sensible.
2. Export it from `plotlyvizpro/stats/__init__.py`.
3. Add `overlays.add_<name>` that appends labelled traces and stores results in `fig.layout.meta` when useful.
4. Tests as above; document the method and its reference in `docs/methods.md`; add a line to `docs/CHANGELOG.md` under *Unreleased*.

## Commit and PR conventions

- Conventional prefixes: `feat:`, `fix:`, `docs:`, `ci:`, `refactor:`, `test:`, `perf:`.
- One logical change per commit; keep exports/notebook output changes in their own commit.
- PRs run the full matrix; please make `make check` pass locally first.
- Regenerating datasets (`plotlyvizpro generate-data`) changes the manifest and every derived export; call it out in the PR.

## Reporting issues

Open an issue with the version (`plotlyvizpro info`), a minimal snippet, and the traceback. For numerical questions, include the reference you compared against.

## Code of conduct

This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md).
