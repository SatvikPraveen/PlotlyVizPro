"""Export figures to HTML, raster/vector images and JSON.

All writers create parent directories, return the written :class:`~pathlib.Path`,
and never print. :func:`save_figure` writes several formats plus a provenance
sidecar in one call, which is the recommended entry point for figures headed
into a paper or report.
"""

from __future__ import annotations

import json
import os
from collections.abc import Iterable
from pathlib import Path
from typing import Literal

import plotly.graph_objects as go
import plotly.io as pio

from plotlyvizpro import provenance as _prov
from plotlyvizpro._typing import StrPath

ImageFormat = Literal["png", "svg", "pdf", "jpeg", "webp"]
IMAGE_FORMATS: tuple[str, ...] = ("png", "svg", "pdf", "jpeg", "webp")


def default_export_dir() -> Path:
    """Root export directory.

    Resolution order: ``PLOTLYVIZPRO_EXPORT_DIR`` environment variable, then
    ``<project root>/exports`` where the project root is the nearest ancestor of
    the current directory containing ``pyproject.toml``, then ``./exports``.
    """
    env = os.environ.get("PLOTLYVIZPRO_EXPORT_DIR")
    if env:
        return Path(env)
    for candidate in (Path.cwd(), *Path.cwd().parents):
        if (candidate / "pyproject.toml").exists():
            return candidate / "exports"
    return Path.cwd() / "exports"


def _prepare(path: StrPath) -> Path:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def save_html(
    fig: go.Figure,
    path: StrPath,
    *,
    include_plotlyjs: bool | str = "cdn",
    full_html: bool = True,
    config: dict[str, object] | None = None,
) -> Path:
    """Write an interactive HTML file.

    ``include_plotlyjs="cdn"`` (default) keeps files small; pass ``True`` to
    embed the library for fully offline archives.
    """
    p = _prepare(path)
    cfg = {"displaylogo": False, "responsive": True, **(config or {})}
    fig.write_html(str(p), include_plotlyjs=include_plotlyjs, full_html=full_html, config=cfg)
    return p


def image_export_available() -> bool:
    """Whether a static-image engine (kaleido) is importable."""
    try:
        import kaleido  # noqa: F401
    except ImportError:
        return False
    return True


def save_image(
    fig: go.Figure,
    path: StrPath,
    *,
    format: ImageFormat | None = None,
    width: int | None = None,
    height: int | None = None,
    scale: float | None = None,
) -> Path:
    """Write a static image (PNG, SVG, PDF, JPEG or WebP).

    The format is inferred from the suffix when not given. If the figure was
    sized with :func:`plotlyvizpro.theme.apply_journal_preset`, the preset's
    raster ``scale`` is used unless ``scale`` is passed explicitly.

    Raises
    ------
    RuntimeError
        If no static-image engine is installed.
    """
    p = _prepare(path)
    fmt = (format or p.suffix.lstrip(".")).lower()
    if fmt == "jpg":
        fmt = "jpeg"
    if fmt not in IMAGE_FORMATS:
        raise ValueError(f"Unsupported image format {fmt!r}. Choose from {IMAGE_FORMATS}.")
    if not image_export_available():
        raise RuntimeError("Static image export requires the 'kaleido' package: pip install kaleido")
    if scale is None:
        meta = fig.layout.meta or {}
        scale = float(meta.get("journal_preset", {}).get("scale", 2.0)) if isinstance(meta, dict) else 2.0
    fig.write_image(str(p), format=fmt, width=width, height=height, scale=scale)
    return p


def save_json(fig: go.Figure, path: StrPath, *, pretty: bool = True) -> Path:
    """Write the figure as Plotly JSON (round-trippable with :func:`plotly.io.from_json`)."""
    p = _prepare(path)
    text = pio.to_json(fig, pretty=pretty)
    p.write_text(text, encoding="utf-8")
    return p


def load_json(path: StrPath) -> go.Figure:
    """Read a figure previously written by :func:`save_json`."""
    return pio.from_json(Path(path).read_text(encoding="utf-8"))


def save_figure(
    fig: go.Figure,
    stem: str,
    directory: StrPath | None = None,
    formats: Iterable[str] = ("html", "png"),
    *,
    provenance: bool | _prov.Provenance = True,
    include_plotlyjs: bool | str = "cdn",
) -> dict[str, Path]:
    """Write a figure in several formats and a provenance sidecar.

    Parameters
    ----------
    fig:
        The figure.
    stem:
        Base file name without extension.
    directory:
        Target directory; defaults to :func:`default_export_dir`.
    formats:
        Any of ``"html"``, ``"json"`` and the image formats. Image formats are
        skipped with a ``"skipped"`` marker when kaleido is unavailable, so a
        headless CI run still produces the HTML and JSON.
    provenance:
        ``True`` to attach a fresh record, a :class:`~plotlyvizpro.provenance.Provenance`
        to attach that one, or ``False`` to skip.

    Returns
    -------
    dict
        Mapping ``format -> path`` for everything written (plus ``"provenance"``).
    """
    out_dir = Path(directory) if directory is not None else default_export_dir()
    written: dict[str, Path] = {}
    if provenance:
        record = provenance if isinstance(provenance, _prov.Provenance) else _prov.Provenance()
        _prov.attach(fig, record)
        written["provenance"] = record.write(out_dir / f"{stem}.provenance.json")
    for fmt in formats:
        fmt = fmt.lower()
        target = out_dir / f"{stem}.{fmt}"
        if fmt == "html":
            written[fmt] = save_html(fig, target, include_plotlyjs=include_plotlyjs)
        elif fmt == "json":
            written[fmt] = save_json(fig, target)
        elif fmt in IMAGE_FORMATS:
            if not image_export_available():
                continue
            written[fmt] = save_image(fig, target)
        else:
            raise ValueError(f"Unknown format {fmt!r}")
    return written


def figure_summary(fig: go.Figure) -> dict[str, object]:
    """Compact, JSON-serialisable description of a figure for logs and tests."""
    return {
        "n_traces": len(fig.data),
        "trace_types": sorted({t.type for t in fig.data}),
        "title": (fig.layout.title.text if fig.layout.title else None),
        "template": getattr(fig.layout.template.layout, "colorway", None) is not None,
        "size_bytes": len(json.dumps(fig.to_plotly_json(), default=str)),
    }
