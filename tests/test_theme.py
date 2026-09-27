"""Tests for plotlyvizpro.theme."""

from __future__ import annotations

import plotly.graph_objects as go
import plotly.io as pio
import pytest

from plotlyvizpro import theme
from plotlyvizpro.colors import CATEGORICAL_DARK, CATEGORICAL_LIGHT


@pytest.fixture(autouse=True)
def _restore_default():
    original = pio.templates.default
    yield
    pio.templates.default = original


def test_templates_registered_with_validated_palettes():
    assert list(pio.templates["pvp_light"].layout.colorway) == list(CATEGORICAL_LIGHT)
    assert list(pio.templates["pvp_dark"].layout.colorway) == list(CATEGORICAL_DARK)


def test_register_sets_default_when_asked():
    theme.register_templates(set_default=True)
    assert pio.templates.default == "pvp_light"


def test_apply_theme_plain():
    assert theme.apply_theme("pvp_dark") == "pvp_dark"
    assert pio.templates.default == "pvp_dark"


def test_apply_theme_font_override_is_idempotent_and_non_mutating():
    before = pio.templates["plotly_white"].layout.font.family
    name = theme.apply_theme("plotly_white", font_family="Georgia", font_size=9)
    theme.apply_theme("plotly_white", font_family="Georgia", font_size=9)
    assert name == "plotly_white_pvp_font"
    assert pio.templates[name].layout.font.family == "Georgia"
    assert pio.templates["plotly_white"].layout.font.family == before


def test_apply_theme_unknown():
    with pytest.raises(ValueError, match="Unknown template"):
        theme.apply_theme("nope")


def test_apply_dark_theme():
    fig = theme.apply_dark_theme(go.Figure())
    assert fig.layout.paper_bgcolor == "#1a1a19"
    assert fig.layout.template.layout.paper_bgcolor == "#1a1a19"


@pytest.mark.parametrize("name", list(theme.JOURNAL_PRESETS))
def test_journal_presets_geometry(name):
    fig = theme.apply_journal_preset(go.Figure(), name)
    spec = theme.JOURNAL_PRESETS[name]
    assert fig.layout.width == spec.width_px
    assert fig.layout.height == spec.height_px
    assert fig.layout.meta["journal_preset"]["dpi"] == spec.dpi
    assert fig.layout.meta["journal_preset"]["scale"] == pytest.approx(spec.dpi / 96)


def test_journal_preset_custom_object():
    spec = theme.JournalPreset(2.0, 1.0, 96, 10, "custom")
    fig = theme.apply_journal_preset(go.Figure(), spec, font_family="Times")
    assert (fig.layout.width, fig.layout.height) == (192, 96)
    assert fig.layout.font.family == "Times"
    assert fig.layout.meta["journal_preset"]["name"] == "custom"
