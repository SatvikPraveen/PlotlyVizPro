"""Run the Streamlit landing page and every gallery page headlessly with AppTest."""

from __future__ import annotations

from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
PAGES = sorted(p.name for p in (ROOT / "pages").glob("*.py"))
EXPECTED_PAGES = [f"notebook_{i:02d}.py" for i in range(1, 11)] + [
    "11_statistical_lab.py",
    "12_palette_audit.py",
    "13_downsampling.py",
]


def test_all_expected_pages_present():
    assert sorted(EXPECTED_PAGES) == PAGES


def _run(script: Path, timeout: int = 120):
    at = pytest.importorskip("streamlit.testing.v1").AppTest.from_file(str(script), default_timeout=timeout)
    at.run()
    errors = [e.value for e in at.exception]
    assert not errors, f"{script.name} raised: {errors}"
    return at


@pytest.mark.slow
def test_landing_page_runs(monkeypatch):
    monkeypatch.chdir(ROOT)
    at = _run(ROOT / "app.py")
    assert at.title[0].value == "PlotlyVizPro"


@pytest.mark.slow
@pytest.mark.parametrize("page", EXPECTED_PAGES)
def test_each_page_runs(page, monkeypatch, tmp_path):
    monkeypatch.chdir(ROOT)
    monkeypatch.setenv("PLOTLYVIZPRO_EXPORT_DIR", str(tmp_path))
    _run(ROOT / "pages" / page)


@pytest.mark.slow
def test_palette_audit_page_reacts_to_input(monkeypatch):
    monkeypatch.chdir(ROOT)
    at = _run(ROOT / "pages" / "12_palette_audit.py")
    at.sidebar.text_area[0].set_value("#000000,#010101").run()
    assert any("FAIL" in m.value for m in at.markdown)
