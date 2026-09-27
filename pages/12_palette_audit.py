"""Audit any categorical palette for colour-vision-deficiency safety and contrast."""

from __future__ import annotations

import streamlit as st

from plotlyvizpro.colors import PALETTES, audit_palette, contrast_ratio, hex_to_oklch, order_palette, simulate_cvd

st.set_page_config(page_title="Palette audit", layout="wide")
st.title("Palette audit")
st.caption(
    "Checks: OKLCH lightness band, chroma floor, CVD separation (Machado 2009, protan/deutan, OKLab ΔE×100), "
    "normal-vision floor, WCAG contrast vs surface. Same rules as the CLI: `plotlyvizpro audit-palette`."
)

with st.sidebar:
    preset = st.selectbox("Start from", ["custom", *PALETTES])
    default = ",".join(PALETTES[preset]) if preset != "custom" else "#2a78d6,#eb6834,#1baf7a,#eda100"
    raw = st.text_area("Hex colours (comma-separated)", default, height=100)
    mode = st.radio("Surface mode", ["light", "dark"], horizontal=True)
    pairs = st.radio("Pair list", ["adjacent", "all"], horizontal=True, help="Use 'all' for scatter, bubble and maps.")
    surface = st.text_input("Surface colour (optional)", "")

colors = [c.strip() for c in raw.split(",") if c.strip()]
try:
    report = audit_palette(colors, mode=mode, surface=surface or None, pairs=pairs)  # type: ignore[arg-type]
except ValueError as exc:
    st.error(str(exc))
    st.stop()

st.markdown(f"### Result: {'✅ PASS' if report.ok else '❌ FAIL'}")
for check in report.checks:
    icon = {"pass": "✅", "warn": "⚠️", "fail": "❌"}[check.status]
    st.markdown(f"{icon} **{check.name}** — {check.detail}")

st.subheader("Swatches under simulated vision")
rows = [
    ("normal", lambda c: c),
    ("protan", lambda c: simulate_cvd(c, "protan")),
    ("deutan", lambda c: simulate_cvd(c, "deutan")),
    ("tritan", lambda c: simulate_cvd(c, "tritan")),
]
surface_hex = report.surface
ink = "#111" if mode == "light" else "#eee"
html = [f'<div style="background:{surface_hex};padding:12px;border-radius:8px">']
for label, fn in rows:
    html.append(
        '<div style="display:flex;align-items:center;gap:6px;margin:4px 0">'
        f'<span style="width:60px;color:{ink};font:12px sans-serif">{label}</span>'
    )
    for c in colors:
        html.append(
            f'<span title="{c}" style="display:inline-block;width:44px;height:28px;'
            f'border-radius:4px;background:{fn(c)}"></span>'
        )
    html.append("</div>")
html.append("</div>")
st.markdown("".join(html), unsafe_allow_html=True)

st.subheader("Per-colour metrics")
st.dataframe(
    [
        {
            "hex": c,
            "OKLCH L": round(hex_to_oklch(c)[0], 3),
            "OKLCH C": round(hex_to_oklch(c)[1], 3),
            "hue°": round(hex_to_oklch(c)[2], 1),
            "contrast vs surface": round(contrast_ratio(c, surface_hex), 2),
        }
        for c in colors
    ],
    use_container_width=True,
)

if len(colors) > 2:
    st.subheader("Suggested order (maximises minimum adjacent CVD ΔE)")
    ordered = order_palette(colors)
    st.code(",".join(ordered), language=None)
    st.caption(
        f"worst adjacent CVD ΔE: current {report.worst_cvd_delta_e:.1f} → "
        f"reordered {audit_palette(ordered, mode=mode, surface=surface or None).worst_cvd_delta_e:.1f}"
    )
