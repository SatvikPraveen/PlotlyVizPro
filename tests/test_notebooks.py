"""Structural checks on the tutorial notebooks, plus an opt-in execution test."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

NOTEBOOKS_DIR = Path(__file__).parent.parent / "notebooks"
EXPECTED = [
    "01_line_scatter.ipynb",
    "02_bar_pie_box.ipynb",
    "03_histogram_density.ipynb",
    "04_heatmaps_choropeth.ipynb",
    "05_animations_interactive.ipynb",
    "06_subplots_dashboards.ipynb",
    "07_graph_objects.ipynb",
    "08_mapbox_geo.ipynb",
    "09_real_world_cases.ipynb",
    "10_statistical_overlays.ipynb",
]


def _load(path: Path) -> dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


@pytest.mark.parametrize("name", EXPECTED)
def test_notebook_exists_and_is_valid(name):
    path = NOTEBOOKS_DIR / name
    assert path.exists(), f"Missing notebook: {name}"
    nb = _load(path)
    assert "cells" in nb
    assert nb["cells"], "notebook has no cells"
    assert any(c["cell_type"] == "markdown" for c in nb["cells"]), "notebook has no documentation"
    assert any(c["cell_type"] == "code" for c in nb["cells"]), "notebook has no code"


def test_no_unexpected_notebooks():
    found = sorted(p.name for p in NOTEBOOKS_DIR.glob("*.ipynb"))
    assert found == sorted(EXPECTED)


@pytest.mark.slow
@pytest.mark.notebook
@pytest.mark.parametrize("name", EXPECTED)
def test_notebook_executes(name, tmp_path, monkeypatch):
    """Execute each notebook end-to-end (run with ``-m notebook``)."""
    nbformat = pytest.importorskip("nbformat")
    nbclient = pytest.importorskip("nbclient")
    monkeypatch.setenv("PLOTLYVIZPRO_EXPORT_DIR", str(tmp_path))
    nb = nbformat.read(NOTEBOOKS_DIR / name, as_version=4)
    client = nbclient.NotebookClient(
        nb, timeout=600, kernel_name="python3", resources={"metadata": {"path": str(NOTEBOOKS_DIR)}}
    )
    client.execute()
