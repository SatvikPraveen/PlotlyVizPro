"""Research: audit a palette, reorder it for CVD safety, and build a sequential ramp."""

from plotlyvizpro.colors import PALETTES, audit_palette, order_palette, sequential_scale, simulate_cvd

brand = ["#0b5fff", "#ff6b00", "#00a878", "#ffc400", "#d62864", "#7b61ff"]
print(audit_palette(brand, mode="light").to_text())
print()
better = order_palette(brand)
print("CVD-optimal order:", ", ".join(better))
print(
    "worst adjacent CVD ΔE:",
    f"{audit_palette(brand).worst_cvd_delta_e:.1f} → {audit_palette(better).worst_cvd_delta_e:.1f}",
)
print()
for kind in ("protan", "deutan", "tritan"):
    print(f"{kind:7s}", " ".join(simulate_cvd(c, kind) for c in better))
print()
print("sequential blue ramp:", sequential_scale("#0b5fff", steps=7))
print()
for name, pal in PALETTES.items():
    mode = "dark" if name.endswith("dark") else "light"
    print(f"{name:10s} {'PASS' if audit_palette(pal, mode=mode).ok else 'FAIL'}")
