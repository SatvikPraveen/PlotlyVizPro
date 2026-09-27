# Benchmarks

Micro-benchmarks for the numerically heavy paths, using
[pytest-benchmark](https://pytest-benchmark.readthedocs.io/).

```bash
pip install -e ".[dev]"
pytest benchmarks/ --benchmark-only --benchmark-sort=mean
```

The CLI has a quick end-to-end timing for the downsamplers:

```bash
plotlyvizpro benchmark --n 1000000 --threshold 4000
```

Results are machine-dependent; the CI job publishes them as an artifact but
does not gate on them. Reference numbers from a 2023 laptop (Apple M2) are
recorded in `docs/benchmarks.md`.
