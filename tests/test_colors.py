"""Tests for plotlyvizpro.colors (values cross-checked against the reference JS validator)."""

from __future__ import annotations

import numpy as np
import pytest
from hypothesis import given
from hypothesis import strategies as st

from plotlyvizpro import colors


def test_hex_roundtrip():
    for h in ("#000000", "#ffffff", "#2a78d6", "#abc"):
        rgb = colors.hex_to_rgb(h)
        assert colors.hex_to_rgb(colors.rgb_to_hex(rgb)) == pytest.approx(rgb, abs=1 / 255)


@pytest.mark.parametrize("bad", ["#12", "zzzzzz", "#12345g", ""])
def test_invalid_hex(bad):
    with pytest.raises(ValueError, match="Invalid hex"):
        colors.hex_to_rgb(bad)


def test_oklab_reference_values():
    # White should be L=1, a=b=0; black L=0.
    assert colors.hex_to_oklab("#ffffff") == pytest.approx([1.0, 0.0, 0.0], abs=1e-4)
    assert colors.hex_to_oklab("#000000") == pytest.approx([0.0, 0.0, 0.0], abs=1e-6)
    L, C, h = colors.hex_to_oklch("#2a78d6")
    assert (L, C, h) == pytest.approx((0.5753, 0.1626, 255.532), abs=2e-3)


def test_contrast_ratio_extremes_and_symmetry():
    assert colors.contrast_ratio("#000000", "#ffffff") == pytest.approx(21.0, abs=1e-6)
    assert colors.contrast_ratio("#2a78d6", "#fcfcfb") == pytest.approx(4.30, abs=0.01)
    assert colors.contrast_ratio("#2a78d6", "#fcfcfb") == colors.contrast_ratio("#fcfcfb", "#2a78d6")


def test_cvd_simulation_matches_reference():
    assert colors.simulate_cvd("#2a78d6", "protan") == "#4780da"
    assert colors.simulate_cvd("#eb6834", "deutan") == "#ad9b30"
    assert colors.simulate_cvd("#2a78d6", "deutan", severity=0.0) == "#2a78d6"


def test_cvd_bad_args():
    with pytest.raises(ValueError, match="kind"):
        colors.simulate_cvd("#000000", "quadran")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="severity"):
        colors.simulate_cvd("#000000", "protan", severity=2)


def test_delta_e_reference_and_metric_properties():
    assert colors.delta_e("#2a78d6", "#eb6834") == pytest.approx(33.59, abs=0.01)
    assert colors.delta_e("#2a78d6", "#2a78d6") == 0.0
    assert colors.delta_e("#2a78d6", "#eb6834") == colors.delta_e("#eb6834", "#2a78d6")


@given(st.integers(0, 0xFFFFFF), st.integers(0, 0xFFFFFF), st.integers(0, 0xFFFFFF))
def test_delta_e_triangle_inequality(a, b, c):
    ha, hb, hc = (f"#{v:06x}" for v in (a, b, c))
    assert colors.delta_e(ha, hc) <= colors.delta_e(ha, hb) + colors.delta_e(hb, hc) + 1e-9


class TestAudit:
    def test_light_palette_passes_with_reference_numbers(self):
        report = colors.audit_palette(colors.CATEGORICAL_LIGHT, mode="light")
        assert report.ok
        by_name = {c.name: c for c in report.checks}
        assert "dE 9.1" in by_name["CVD separation"].detail
        assert "dE 19.6" in by_name["Normal-vision floor"].detail
        assert by_name["Contrast vs surface"].status == "warn"

    def test_dark_palette_passes(self):
        report = colors.audit_palette(colors.CATEGORICAL_DARK, mode="dark")
        assert report.ok
        assert all(c.status == "pass" for c in report.checks)
        assert report.worst_cvd_delta_e == pytest.approx(8.3, abs=0.1)

    def test_okabe_ito_fails_band_by_design(self):
        report = colors.audit_palette(colors.OKABE_ITO)
        assert not report.ok
        names = {c.name: c.status for c in report.checks}
        assert names["Lightness band"] == "fail"
        assert names["Chroma floor"] == "fail"
        assert names["CVD separation"] == "pass"

    def test_all_pairs_on_first_three(self):
        report = colors.audit_palette(colors.CATEGORICAL_LIGHT[:3], pairs="all")
        assert report.ok
        assert "dE 24.0" in report.checks[3].detail

    def test_single_colour(self):
        report = colors.audit_palette(["#2a78d6"])
        assert report.ok

    def test_text_render(self):
        text = colors.audit_palette(colors.CATEGORICAL_LIGHT).to_text()
        assert "ALL CHECKS PASS" in text
        assert "[PASS]" in text

    def test_bad_inputs(self):
        with pytest.raises(ValueError, match="at least one"):
            colors.audit_palette([])
        with pytest.raises(ValueError, match="pairs"):
            colors.audit_palette(["#000000", "#ffffff"], pairs="some")  # type: ignore[arg-type]


class TestOrdering:
    def test_order_palette_maximises_min_adjacent_cvd(self):
        shuffled = colors.CATEGORICAL_LIGHT[::-1]
        ordered = colors.order_palette(shuffled)
        assert sorted(ordered) == sorted(shuffled)
        assert colors.audit_palette(ordered).worst_cvd_delta_e >= colors.audit_palette(shuffled).worst_cvd_delta_e

    def test_order_palette_greedy_path_for_many_colours(self):
        many = [f"#{int(v):06x}" for v in np.linspace(0x102030, 0xF0E0D0, 10)]
        ordered = colors.order_palette(many, max_exhaustive=4)
        assert len(ordered) == 10
        assert set(ordered) == set(many)

    def test_dedup_and_short(self):
        assert colors.order_palette(["#000000", "#000000", "#ffffff"]) == ("#000000", "#ffffff")


def test_sequential_scale_monotone_lightness():
    ramp = colors.sequential_scale("#2a78d6", steps=6)
    ls = [colors.hex_to_oklch(c)[0] for c in ramp]
    assert ls == sorted(ls, reverse=True)
    dark = colors.sequential_scale("#2a78d6", steps=6, mode="dark")
    assert dark == ramp[::-1]
    with pytest.raises(ValueError, match="steps"):
        colors.sequential_scale("#2a78d6", steps=1)
