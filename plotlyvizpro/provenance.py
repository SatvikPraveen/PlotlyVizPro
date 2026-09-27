"""Reproducibility metadata for figures.

A :class:`Provenance` record captures *what produced a figure*: package
versions, the Git commit of the working tree, the platform, a UTC timestamp,
and SHA-256 digests of the input data. :func:`attach` stores it in
``fig.layout.meta["provenance"]`` so it survives ``to_json``/``from_json`` and
is written as a sidecar file by :func:`plotlyvizpro.export.save_figure`.
"""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from importlib import metadata
from pathlib import Path
from typing import Any

import pandas as pd
import plotly.graph_objects as go

from plotlyvizpro._typing import StrPath
from plotlyvizpro._version import __version__

TRACKED_PACKAGES = ("plotly", "pandas", "numpy", "scipy", "scikit-learn", "kaleido", "streamlit")


def sha256_of_file(path: StrPath, chunk_size: int = 1 << 20) -> str:
    """Hex SHA-256 digest of a file, streamed in chunks."""
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(chunk_size), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_of_dataframe(df: pd.DataFrame) -> str:
    """Content digest of a DataFrame that is stable across process runs.

    Uses :func:`pandas.util.hash_pandas_object` on values plus a digest of the
    column names and dtypes so a renamed column changes the hash.
    """
    h = hashlib.sha256()
    h.update(pd.util.hash_pandas_object(df, index=True).to_numpy().tobytes())
    h.update(json.dumps([[str(c), str(t)] for c, t in df.dtypes.items()]).encode())
    return h.hexdigest()


def git_commit(cwd: StrPath | None = None) -> str | None:
    """Short SHA of ``HEAD`` (with ``-dirty`` when the tree has changes), or ``None``."""
    try:
        sha = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"], cwd=cwd, capture_output=True, text=True, check=True, timeout=5
        ).stdout.strip()
        dirty = subprocess.run(
            ["git", "status", "--porcelain"], cwd=cwd, capture_output=True, text=True, check=True, timeout=5
        ).stdout.strip()
        return f"{sha}-dirty" if dirty else sha
    except (OSError, subprocess.SubprocessError):
        return None


def package_versions(names: tuple[str, ...] = TRACKED_PACKAGES) -> dict[str, str]:
    """Installed versions of the given distributions (missing ones are omitted)."""
    out: dict[str, str] = {}
    for name in names:
        try:
            out[name] = metadata.version(name)
        except metadata.PackageNotFoundError:
            continue
    return out


@dataclass
class Provenance:
    """Everything needed to say where a figure came from."""

    created_utc: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat(timespec="seconds"))
    plotlyvizpro: str = __version__
    python: str = field(default_factory=lambda: sys.version.split()[0])
    platform: str = field(default_factory=platform.platform)
    packages: dict[str, str] = field(default_factory=package_versions)
    git_commit: str | None = field(default_factory=git_commit)
    inputs: dict[str, str] = field(default_factory=dict)
    parameters: dict[str, Any] = field(default_factory=dict)
    random_seed: int | None = None

    def add_input(self, name: str, source: StrPath | pd.DataFrame) -> Provenance:
        """Record a SHA-256 digest of a file path or DataFrame under ``name``."""
        self.inputs[name] = sha256_of_dataframe(source) if isinstance(source, pd.DataFrame) else sha256_of_file(source)
        return self

    def to_dict(self) -> dict[str, Any]:
        """Plain-dict form suitable for JSON."""
        return asdict(self)

    def write(self, path: StrPath) -> Path:
        """Write the record as indented JSON and return the path."""
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(self.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
        return p


def attach(fig: go.Figure, provenance: Provenance | None = None) -> go.Figure:
    """Store a provenance record in ``fig.layout.meta["provenance"]``."""
    record = provenance or Provenance()
    meta = dict(fig.layout.meta or {})
    meta["provenance"] = record.to_dict()
    fig.update_layout(meta=meta)
    return fig


def read(fig: go.Figure) -> dict[str, Any] | None:
    """Return the provenance stored on a figure, if any."""
    meta = fig.layout.meta
    if not meta or "provenance" not in meta:
        return None
    return dict(meta["provenance"])
