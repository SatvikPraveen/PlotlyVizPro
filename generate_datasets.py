"""Regenerate the bundled synthetic datasets (thin wrapper around plotlyvizpro.datasets).

Usage::

    python generate_datasets.py [--seed 42] [--out datasets]
"""

from __future__ import annotations

import argparse

from plotlyvizpro.datasets import DEFAULT_SEED, generate_all


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--out", default=None, help="target directory (default: <project>/datasets)")
    args = parser.parse_args()
    written = generate_all(args.out, seed=args.seed)
    for name, path in written.items():
        print(f"wrote {name:24s} -> {path}")


if __name__ == "__main__":
    main()
