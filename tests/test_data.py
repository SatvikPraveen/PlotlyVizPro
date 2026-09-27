"""Dataset generation, loading, schema and manifest integrity."""

from __future__ import annotations

import json

import pandas as pd
import pytest

from plotlyvizpro import data, datasets


@pytest.fixture(scope="module")
def generated(tmp_path_factory):
    out = tmp_path_factory.mktemp("datasets")
    written = datasets.generate_all(out, seed=123)
    return out, written


def test_generate_all_writes_every_dataset_and_manifest(generated):
    out, written = generated
    assert set(written) == set(datasets.GENERATORS) | {"manifest.json"}
    manifest = json.loads((out / "manifest.json").read_text())
    assert manifest["seed"] == 123
    assert set(manifest["files"]) == set(datasets.GENERATORS)
    assert all(v["rows"] > 0 for v in manifest["files"].values())


def test_generation_is_deterministic(tmp_path):
    a = datasets.generate_all(tmp_path / "a", seed=7)
    b = datasets.generate_all(tmp_path / "b", seed=7)
    for name in datasets.GENERATORS:
        assert a[name].read_bytes() == b[name].read_bytes()
    c = datasets.generate_all(tmp_path / "c", seed=8)
    assert a["superstore.csv"].read_bytes() != c["superstore.csv"].read_bytes()


@pytest.mark.parametrize("name", data.list_datasets())
def test_load_each_dataset_matches_spec(generated, name):
    out, _ = generated
    df = data.load(name, directory=out)
    spec = data.SPECS[name]
    assert list(spec.columns) == [c for c in df.columns if c in spec.columns]
    for col in spec.date_columns:
        assert pd.api.types.is_datetime64_any_dtype(df[col])
    if spec.sort_by:
        assert df[list(spec.sort_by)].apply(tuple, axis=1).is_monotonic_increasing


def test_load_bundled_datasets_verify_against_manifest():
    for name in data.list_datasets():
        df = data.load(name)
        assert len(df) > 0
    assert all(data.verify_manifest().values())


def test_load_errors(generated, tmp_path):
    _out, _ = generated
    with pytest.raises(KeyError, match="Unknown dataset"):
        data.load("nope")
    with pytest.raises(FileNotFoundError, match="generate-data"):
        data.load("superstore", directory=tmp_path)


def test_integrity_and_schema_errors(tmp_path):
    datasets.generate_all(tmp_path, seed=1)
    path = tmp_path / "superstore.csv"
    path.write_text(path.read_text().replace("Sales", "Revenue"))
    with pytest.raises(data.IntegrityError, match="sha256"):
        data.load("superstore", directory=tmp_path)
    with pytest.raises(data.SchemaError, match="Sales"):
        data.load("superstore", directory=tmp_path, verify=False)
    assert data.verify_manifest(tmp_path)["superstore.csv"] is False


def test_manifest_skips_missing_files(tmp_path):
    datasets.generate_all(tmp_path, seed=1, manifest=False)
    (tmp_path / "covid_data.csv").unlink()
    manifest = json.loads(data.write_manifest(tmp_path).read_text())
    assert "covid_data.csv" not in manifest["files"]
