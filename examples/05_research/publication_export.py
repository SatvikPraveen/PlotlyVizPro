"""Research: size a figure for a journal column and export with provenance."""

import plotlyvizpro as pvp
from plotlyvizpro.data import load
from plotlyvizpro.provenance import Provenance
from plotlyvizpro.theme import JOURNAL_PRESETS

df = load("superstore")
fig = pvp.box_plot(df, "Category", "Sales", notched=True, title="Sales by category (notched boxes)")

for preset in ("nature_single", "ieee_double"):
    spec = JOURNAL_PRESETS[preset]
    pvp.apply_journal_preset(fig, preset)
    rec = Provenance(parameters={"preset": preset, "notched": True}).add_input("superstore", df)
    written = pvp.save_figure(fig, f"fig_sales_{preset}", formats=("html", "json", "png", "svg", "pdf"), provenance=rec)
    print(f"{preset}: {spec.width_in} x {spec.height_in} in @ {spec.dpi} dpi -> {sorted(written)}")
