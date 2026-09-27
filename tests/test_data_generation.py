"""The committed datasets must be loadable and match their manifest (see test_data.py)."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from plotlyvizpro import data

DATASETS_DIR = Path(__file__).parent.parent / "datasets"


@pytest.mark.parametrize("spec", list(data.SPECS.values()), ids=[s.filename for s in data.SPECS.values()])
def test_committed_dataset_has_headers_and_rows(spec):
    df = pd.read_csv(DATASETS_DIR / spec.filename)
    assert len(df) > 0
    assert not df.columns[0].startswith("Unnamed")
    assert set(spec.columns) <= set(df.columns)


def test_manifest_present_and_valid():
    assert (DATASETS_DIR / data.MANIFEST_NAME).exists()
    assert all(data.verify_manifest().values())
