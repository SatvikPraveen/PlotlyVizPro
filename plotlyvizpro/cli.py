"""Command-line interface: ``plotlyvizpro <command>``.

Commands
--------
``info``            Print versions, export directory and export-engine status.
``generate-data``   Regenerate the synthetic datasets with a fixed seed.
``verify-data``     Check dataset digests against the manifest.
``audit-palette``   Run the CVD/contrast checks on a comma-separated hex list.
``demo``            Render a showcase figure with overlays to the export directory.
``benchmark``       Time the downsampling algorithms on a synthetic series.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from collections.abc import Sequence

import numpy as np

from plotlyvizpro._version import __version__


def _cmd_info(_: argparse.Namespace) -> int:
    from plotlyvizpro.export import default_export_dir, image_export_available
    from plotlyvizpro.provenance import package_versions

    print(f"plotlyvizpro {__version__}")
    for k, v in package_versions().items():
        print(f"  {k:14s} {v}")
    print(f"export dir     {default_export_dir()}")
    print(
        f"image export   {'available (kaleido)' if image_export_available() else 'unavailable - pip install kaleido'}"
    )
    return 0


def _cmd_generate(args: argparse.Namespace) -> int:
    from plotlyvizpro.datasets import generate_all

    for name, path in generate_all(args.out, seed=args.seed).items():
        print(f"wrote {name:24s} -> {path}")
    return 0


def _cmd_verify(args: argparse.Namespace) -> int:
    from plotlyvizpro.data import verify_manifest

    results = verify_manifest(args.directory)
    for name, ok in results.items():
        print(f"{'OK  ' if ok else 'FAIL'} {name}")
    return 0 if all(results.values()) else 1


def _cmd_audit(args: argparse.Namespace) -> int:
    from plotlyvizpro.colors import PALETTES, audit_palette

    colors = PALETTES[args.palette] if args.palette in PALETTES else tuple(c.strip() for c in args.palette.split(","))
    report = audit_palette(colors, mode=args.mode, surface=args.surface, pairs=args.pairs)
    if args.json:
        print(json.dumps({"ok": report.ok, "checks": [c.__dict__ for c in report.checks]}, indent=2))
    else:
        print(report.to_text())
    return 0 if report.ok else 1


def _cmd_demo(args: argparse.Namespace) -> int:
    from functools import partial

    from plotlyvizpro.charts import scatter_plot
    from plotlyvizpro.data import load
    from plotlyvizpro.export import save_figure
    from plotlyvizpro.layout import pipe
    from plotlyvizpro.overlays import add_anomalies, add_lowess, add_moving_average, add_trendline

    df = load("superstore")
    daily = df.groupby("OrderDate")["Sales"].sum().reset_index()
    fig = pipe(
        scatter_plot(
            daily,
            "OrderDate",
            "Sales",
            title="Daily sales with OLS, LOWESS, rolling mean and Hampel anomalies",
            opacity=0.5,
        ),
        partial(add_trendline, x=daily["OrderDate"], y=daily["Sales"], show_ci=True),
        partial(add_lowess, x=daily["OrderDate"], y=daily["Sales"], frac=0.2),
        partial(add_moving_average, x=daily["OrderDate"], y=daily["Sales"], window=14),
        partial(add_anomalies, x=daily["OrderDate"], y=daily["Sales"], method="hampel", window=10),
    )
    written = save_figure(fig, "demo_overlays", args.out, formats=args.formats.split(","))
    for fmt, path in written.items():
        print(f"{fmt:12s} {path}")
    return 0


def _cmd_benchmark(args: argparse.Namespace) -> int:
    from plotlyvizpro.downsample import lttb, m4, max_error, minmax

    rng = np.random.default_rng(0)
    n = args.n
    x = np.arange(n, dtype=float)
    y = np.cumsum(rng.normal(size=n)) + 5 * np.sin(x / 500)
    print(f"n={n:,} points, threshold={args.threshold:,}")
    print(f"{'method':8s} {'kept':>8s} {'seconds':>9s} {'max_err':>9s}")
    for name, fn, arg in (
        ("lttb", lttb, args.threshold),
        ("minmax", minmax, args.threshold),
        ("m4", m4, args.threshold // 4),
    ):
        t0 = time.perf_counter()
        keep = fn(x, y, arg)
        dt = time.perf_counter() - t0
        print(f"{name:8s} {keep.size:8d} {dt:9.4f} {max_error(x, y, keep):9.3f}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    """Construct the CLI parser."""
    p = argparse.ArgumentParser(prog="plotlyvizpro", description="Research-grade Plotly toolkit")
    p.add_argument("--version", action="version", version=f"plotlyvizpro {__version__}")
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("info", help="print environment information").set_defaults(func=_cmd_info)

    g = sub.add_parser("generate-data", help="regenerate synthetic datasets")
    g.add_argument("--seed", type=int, default=42)
    g.add_argument("--out", default=None)
    g.set_defaults(func=_cmd_generate)

    v = sub.add_parser("verify-data", help="verify dataset digests against manifest.json")
    v.add_argument("--directory", default=None)
    v.set_defaults(func=_cmd_verify)

    a = sub.add_parser("audit-palette", help="check a palette for CVD safety and contrast")
    a.add_argument(
        "palette", help="comma-separated hex colours or a named palette (pvp_light, pvp_dark, okabe_ito, ...)"
    )
    a.add_argument("--mode", choices=["light", "dark"], default="light")
    a.add_argument("--surface", default=None)
    a.add_argument("--pairs", choices=["adjacent", "all"], default="adjacent")
    a.add_argument("--json", action="store_true")
    a.set_defaults(func=_cmd_audit)

    d = sub.add_parser("demo", help="render a showcase figure")
    d.add_argument("--out", default=None)
    d.add_argument("--formats", default="html,json")
    d.set_defaults(func=_cmd_demo)

    b = sub.add_parser("benchmark", help="time the downsampling algorithms")
    b.add_argument("--n", type=int, default=1_000_000)
    b.add_argument("--threshold", type=int, default=4000)
    b.set_defaults(func=_cmd_benchmark)
    return p


def main(argv: Sequence[str] | None = None) -> int:
    """Entry point."""
    args = build_parser().parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
