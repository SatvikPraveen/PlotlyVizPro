"""CLI smoke tests (each subcommand runs end-to-end)."""

from __future__ import annotations

import json

import pytest

from plotlyvizpro import cli


def test_info(capsys):
    assert cli.main(["info"]) == 0
    out = capsys.readouterr().out
    assert "plotlyvizpro" in out
    assert "export dir" in out


def test_generate_and_verify(tmp_path, capsys):
    assert cli.main(["generate-data", "--out", str(tmp_path), "--seed", "3"]) == 0
    assert cli.main(["verify-data", "--directory", str(tmp_path)]) == 0
    (tmp_path / "map_data.csv").write_text("City,Latitude,Longitude,Score\n")
    assert cli.main(["verify-data", "--directory", str(tmp_path)]) == 1
    assert "FAIL map_data.csv" in capsys.readouterr().out


def test_audit_named_and_custom(capsys):
    assert cli.main(["audit-palette", "pvp_dark", "--mode", "dark"]) == 0
    assert cli.main(["audit-palette", "#000000,#111111", "--json"]) == 1
    assert '"ok": false' in capsys.readouterr().out


def test_audit_json_shape(capsys):
    cli.main(["audit-palette", "pvp_light", "--json"])
    payload = json.loads(capsys.readouterr().out)
    assert payload["ok"] is True
    assert {c["name"] for c in payload["checks"]} >= {"CVD separation", "Contrast vs surface"}


def test_demo_writes_files(tmp_path, monkeypatch):
    from plotlyvizpro import export

    monkeypatch.setattr(export, "image_export_available", lambda: False)
    assert cli.main(["demo", "--out", str(tmp_path), "--formats", "html,json"]) == 0
    assert (tmp_path / "demo_overlays.html").exists()
    assert (tmp_path / "demo_overlays.provenance.json").exists()


def test_benchmark_small(capsys):
    assert cli.main(["benchmark", "--n", "5000", "--threshold", "200"]) == 0
    out = capsys.readouterr().out
    assert "lttb" in out
    assert "m4" in out


def test_version(capsys):
    with pytest.raises(SystemExit):
        cli.main(["--version"])
    assert "plotlyvizpro" in capsys.readouterr().out
