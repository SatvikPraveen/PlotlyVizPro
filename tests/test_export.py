"""Tests for plotlyvizpro.export and plotlyvizpro.provenance."""

from __future__ import annotations

import json

import pandas as pd
import plotly.graph_objects as go
import pytest

from plotlyvizpro import export, provenance
from plotlyvizpro.theme import apply_journal_preset
from tests.conftest import requires_kaleido


@pytest.fixture
def fig() -> go.Figure:
    return go.Figure(go.Scatter(x=[1, 2, 3], y=[3, 1, 2]), layout={"title": "t"})


def test_save_html_creates_dirs_and_cdn(fig, tmp_path):
    p = export.save_html(fig, tmp_path / "a" / "b" / "fig.html")
    assert p.exists()
    text = p.read_text()
    assert "cdn.plot.ly" in text or "plotly-latest" in text
    assert '"displaylogo": false' in text or "displaylogo" in text


def test_save_json_roundtrip(fig, tmp_path):
    p = export.save_json(fig, tmp_path / "fig.json")
    loaded = export.load_json(p)
    assert loaded.layout.title.text == "t"
    assert list(loaded.data[0].y) == [3, 1, 2]


def test_save_image_rejects_bad_format(fig, tmp_path):
    with pytest.raises(ValueError, match="Unsupported image format"):
        export.save_image(fig, tmp_path / "fig.bmp")


def test_save_image_without_engine(fig, tmp_path, monkeypatch):
    monkeypatch.setattr(export, "image_export_available", lambda: False)
    with pytest.raises(RuntimeError, match="kaleido"):
        export.save_image(fig, tmp_path / "fig.png")


@requires_kaleido
@pytest.mark.kaleido
@pytest.mark.parametrize("ext", ["png", "svg", "pdf"])
def test_save_image_formats(fig, tmp_path, ext):
    p = export.save_image(fig, tmp_path / f"fig.{ext}")
    assert p.stat().st_size > 500


@requires_kaleido
@pytest.mark.kaleido
def test_journal_preset_scale_applied(fig, tmp_path):
    apply_journal_preset(fig, "ieee_single")
    p = export.save_image(fig, tmp_path / "fig.png")
    from PIL import Image

    with Image.open(p) as im:
        # 3.5 in * 300 dpi = 1050 px wide
        assert im.width == pytest.approx(1050, abs=3)


def test_save_figure_writes_requested_formats_and_provenance(fig, tmp_path, monkeypatch):
    monkeypatch.setattr(export, "image_export_available", lambda: False)
    written = export.save_figure(fig, "fig", tmp_path, formats=("html", "json", "png"))
    assert set(written) == {"html", "json", "provenance"}
    record = json.loads(written["provenance"].read_text())
    assert record["plotlyvizpro"] == provenance.__version__
    assert provenance.read(fig)["python"] == record["python"]


def test_save_figure_unknown_format(fig, tmp_path):
    with pytest.raises(ValueError, match="Unknown format"):
        export.save_figure(fig, "fig", tmp_path, formats=("docx",))


def test_default_export_dir_env(monkeypatch, tmp_path):
    monkeypatch.setenv("PLOTLYVIZPRO_EXPORT_DIR", str(tmp_path))
    assert export.default_export_dir() == tmp_path


def test_default_export_dir_project_root(monkeypatch, tmp_path):
    monkeypatch.delenv("PLOTLYVIZPRO_EXPORT_DIR", raising=False)
    (tmp_path / "pyproject.toml").write_text("")
    sub = tmp_path / "notebooks"
    sub.mkdir()
    monkeypatch.chdir(sub)
    assert export.default_export_dir() == tmp_path / "exports"


def test_figure_summary(fig):
    s = export.figure_summary(fig)
    assert s["n_traces"] == 1
    assert s["trace_types"] == ["scatter"]
    assert s["title"] == "t"


class TestProvenance:
    def test_dataframe_hash_sensitive_to_values_and_names(self):
        a = pd.DataFrame({"x": [1, 2, 3]})
        b = pd.DataFrame({"x": [1, 2, 4]})
        c = pd.DataFrame({"y": [1, 2, 3]})
        assert provenance.sha256_of_dataframe(a) == provenance.sha256_of_dataframe(a.copy())
        assert provenance.sha256_of_dataframe(a) != provenance.sha256_of_dataframe(b)
        assert provenance.sha256_of_dataframe(a) != provenance.sha256_of_dataframe(c)

    def test_file_hash(self, tmp_path):
        p = tmp_path / "d.csv"
        p.write_bytes(b"a,b\n1,2\n")
        import hashlib

        assert provenance.sha256_of_file(p) == hashlib.sha256(b"a,b\n1,2\n").hexdigest()

    def test_record_add_input_and_attach(self, tmp_path):
        rec = provenance.Provenance(random_seed=42, parameters={"window": 7})
        rec.add_input("frame", pd.DataFrame({"x": [1]}))
        p = tmp_path / "d.csv"
        p.write_text("x\n1\n")
        rec.add_input("file", p)
        fig = provenance.attach(go.Figure(), rec)
        stored = provenance.read(fig)
        assert stored["random_seed"] == 42
        assert set(stored["inputs"]) == {"frame", "file"}
        assert "plotly" in stored["packages"]

    def test_read_none(self):
        assert provenance.read(go.Figure()) is None

    def test_git_commit_handles_missing_repo(self, tmp_path):
        assert provenance.git_commit(cwd=tmp_path) is None or isinstance(provenance.git_commit(cwd=tmp_path), str)
