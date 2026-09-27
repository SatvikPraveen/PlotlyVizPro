# Benchmarks

Reference numbers from the `pytest-benchmark` suite in `benchmarks/` and the
`plotlyvizpro benchmark` command. Machine: Apple M-series laptop, Python 3.13,
NumPy 2.5. Run `make bench` to reproduce on your hardware; CI uploads
`benchmark.json` as an artifact on every push.

## Downsampling, 1,000,000 points → 4,000

| method | kept | seconds | max abs error |
|---|---:|---:|---:|
| LTTB | 4000 | 0.042 | 33.1 |
| MinMax | 4000 | 0.022 | 36.6 |
| M4 (1000 px) | 3940 | 0.017 | 47.9 |

(random walk plus sinusoid; error is the largest vertical gap between the
original series and the interpolant through kept points)

## Micro-benchmarks (200,000-point series unless noted)

| benchmark | mean (ms) |
|---|---:|
| `minmax`, threshold 1000 | 6.2 |
| `ols_fit`, n = 50,000 | 6.5 |
| `lttb`, threshold 1000 | 8.2 |
| `m4`, 800 px | 12.8 |
| `m4`, 1920 px | 20.9 |
| `minmax`, threshold 5000 | 25.1 |
| `lttb`, threshold 5000 | 36.1 |
| `lowess`, n = 5000, frac 0.1, 1 iteration, delta 25 | 62.0 |

LOWESS without `delta` is O(n²) in the number of local fits; use `delta` (or
downsample first) above a few thousand points.
