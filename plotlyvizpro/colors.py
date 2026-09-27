"""Colour science for accessible palettes.

This module implements, in pure NumPy, the computable checks that decide
whether a categorical palette is safe for readers with colour-vision
deficiency (CVD):

* sRGB <-> linear <-> OKLab / OKLCH conversions (Ottosson 2020);
* CVD simulation with the Machado, Oliveira & Fernandes (2009) matrices at
  severity 1.0 for protanopia, deuteranopia and tritanopia;
* perceptual distance as Euclidean distance in OKLab (x100);
* WCAG 2.x relative-luminance contrast ratio.

:func:`audit_palette` bundles these into a report, and :func:`order_palette`
searches for the slot order that maximises the minimum adjacent CVD distance.

References
----------
- Machado, G. M., Oliveira, M. M., & Fernandes, L. A. F. (2009). A physiologically-based
  model for simulation of color vision deficiency. *IEEE TVCG*, 15(6), 1291-1298.
- Ottosson, B. (2020). A perceptual color space for image processing. https://bottosson.github.io/posts/oklab/
- Okabe, M., & Ito, K. (2008). Color Universal Design (CUD): How to make figures and
  presentations that are friendly to colorblind people.
- Tol, P. (2021). Colour schemes. SRON/EPS/TN/09-002.
"""

from __future__ import annotations

import itertools
from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Literal

import numpy as np

from plotlyvizpro._typing import FloatArray

CVDType = Literal["protan", "deutan", "tritan"]

# --- palettes -----------------------------------------------------------------

#: Eight-hue categorical order validated for adjacent-pair CVD separation on a light surface.
CATEGORICAL_LIGHT: tuple[str, ...] = (
    "#2a78d6",
    "#eb6834",
    "#1baf7a",
    "#eda100",
    "#e87ba4",
    "#008300",
    "#4a3aa7",
    "#e34948",
)
#: Dark-surface counterpart: same hue families, lightness re-stepped for a dark surface.
CATEGORICAL_DARK: tuple[str, ...] = (
    "#3987e5",
    "#d95926",
    "#199e70",
    "#c98500",
    "#d55181",
    "#008300",
    "#9085e9",
    "#e66767",
)
#: Okabe & Ito (2008) colour-universal-design palette, the de-facto standard in scientific publishing.
OKABE_ITO: tuple[str, ...] = (
    "#E69F00",
    "#56B4E9",
    "#009E73",
    "#F0E442",
    "#0072B2",
    "#D55E00",
    "#CC79A7",
    "#000000",
)
#: Paul Tol "bright" qualitative scheme.
TOL_BRIGHT: tuple[str, ...] = ("#4477AA", "#EE6677", "#228833", "#CCBB44", "#66CCEE", "#AA3377", "#BBBBBB")
#: Paul Tol "muted" qualitative scheme.
TOL_MUTED: tuple[str, ...] = (
    "#CC6677",
    "#332288",
    "#DDCC77",
    "#117733",
    "#88CCEE",
    "#882255",
    "#44AA99",
    "#999933",
    "#AA4499",
)

PALETTES: dict[str, tuple[str, ...]] = {
    "pvp_light": CATEGORICAL_LIGHT,
    "pvp_dark": CATEGORICAL_DARK,
    "okabe_ito": OKABE_ITO,
    "tol_bright": TOL_BRIGHT,
    "tol_muted": TOL_MUTED,
}

DEFAULT_SURFACE: dict[str, str] = {"light": "#fcfcfb", "dark": "#1a1a19"}

# --- thresholds (shared with the dataviz validator) ----------------------------
LIGHTNESS_BAND: dict[str, tuple[float, float]] = {"light": (0.43, 0.77), "dark": (0.48, 0.67)}
CHROMA_FLOOR = 0.10
CVD_TARGET = 8.0
CVD_FLOOR = 6.0
NORMAL_FLOOR = 15.0
CONTRAST_MIN = 3.0

# Machado, Oliveira & Fernandes (2009), severity 1.0, applied in linear RGB.
MACHADO_2009: dict[CVDType, FloatArray] = {
    "protan": np.array(
        [[0.152286, 1.052583, -0.204868], [0.114503, 0.786281, 0.099216], [-0.003882, -0.048116, 1.051998]]
    ),
    "deutan": np.array(
        [[0.367322, 0.860646, -0.227968], [0.280085, 0.672501, 0.047413], [-0.011820, 0.042940, 0.968881]]
    ),
    "tritan": np.array(
        [[1.255528, -0.076749, -0.178779], [-0.078411, 0.930809, 0.147602], [0.004733, 0.691367, 0.303900]]
    ),
}

_M1 = np.array(
    [
        [0.4122214708, 0.5363325363, 0.0514459929],
        [0.2119034982, 0.6806995451, 0.1073969566],
        [0.0883024619, 0.2817188376, 0.6299787005],
    ]
)
_M2 = np.array(
    [
        [0.2104542553, 0.7936177850, -0.0040720468],
        [1.9779984951, -2.4285922050, 0.4505937099],
        [0.0259040371, 0.7827717662, -0.8086757660],
    ]
)


# --- conversions ----------------------------------------------------------------


def hex_to_rgb(color: str) -> FloatArray:
    """Parse ``#rrggbb`` (or ``rrggbb``) into sRGB components in [0, 1]."""
    s = color.strip().lstrip("#")
    if len(s) == 3:
        s = "".join(ch * 2 for ch in s)
    if len(s) != 6:
        raise ValueError(f"Invalid hex colour {color!r}")
    try:
        return np.array([int(s[i : i + 2], 16) / 255.0 for i in (0, 2, 4)])
    except ValueError as exc:
        raise ValueError(f"Invalid hex colour {color!r}") from exc


def rgb_to_hex(rgb: FloatArray) -> str:
    """Format sRGB components in [0, 1] as ``#rrggbb`` (clipping out-of-gamut values)."""
    clipped = np.clip(np.asarray(rgb, dtype=float), 0.0, 1.0)
    return "#" + "".join(f"{round(c * 255):02x}" for c in clipped)


def srgb_to_linear(rgb: FloatArray) -> FloatArray:
    """Apply the inverse sRGB transfer function."""
    c = np.asarray(rgb, dtype=float)
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def linear_to_srgb(lin: FloatArray) -> FloatArray:
    """Apply the sRGB transfer function, clipping to [0, 1] first."""
    c = np.clip(np.asarray(lin, dtype=float), 0.0, 1.0)
    return np.where(c <= 0.0031308, 12.92 * c, 1.055 * np.power(c, 1 / 2.4) - 0.055)


def linear_to_oklab(lin: FloatArray) -> FloatArray:
    """Convert linear sRGB to OKLab ``(L, a, b)``."""
    lms = _M1 @ np.asarray(lin, dtype=float)
    return _M2 @ np.cbrt(lms)


def hex_to_oklab(color: str) -> FloatArray:
    """Convert a hex colour to OKLab."""
    return linear_to_oklab(srgb_to_linear(hex_to_rgb(color)))


def hex_to_oklch(color: str) -> tuple[float, float, float]:
    """Convert a hex colour to OKLCH ``(L, C, h_degrees)``."""
    L, a, b = hex_to_oklab(color)
    chroma = float(np.hypot(a, b))
    hue = float(np.degrees(np.arctan2(b, a)) % 360.0)
    return float(L), chroma, hue


def relative_luminance(color: str) -> float:
    """WCAG 2.x relative luminance of a hex colour."""
    r, g, b = srgb_to_linear(hex_to_rgb(color))
    return float(0.2126 * r + 0.7152 * g + 0.0722 * b)


def contrast_ratio(a: str, b: str) -> float:
    """WCAG 2.x contrast ratio between two colours (>= 1.0)."""
    la, lb = relative_luminance(a), relative_luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def simulate_cvd(color: str, kind: CVDType, severity: float = 1.0) -> str:
    """Simulate how ``color`` appears under a colour-vision deficiency.

    Parameters
    ----------
    color:
        Hex colour.
    kind:
        ``"protan"``, ``"deutan"`` or ``"tritan"``.
    severity:
        Interpolation weight in [0, 1] between identity (0) and the full
        Machado 2009 matrix (1). Only ``1.0`` is used by the audit thresholds.
    """
    if kind not in MACHADO_2009:
        raise ValueError(f"kind must be one of {list(MACHADO_2009)}, got {kind!r}")
    if not 0.0 <= severity <= 1.0:
        raise ValueError("severity must lie in [0, 1]")
    matrix = (1 - severity) * np.eye(3) + severity * MACHADO_2009[kind]
    lin = srgb_to_linear(hex_to_rgb(color))
    return rgb_to_hex(linear_to_srgb(matrix @ lin))


def delta_e(a: str, b: str) -> float:
    """Perceptual distance: Euclidean distance in OKLab scaled by 100."""
    return float(np.linalg.norm(hex_to_oklab(a) - hex_to_oklab(b)) * 100.0)


def cvd_delta_e(a: str, b: str) -> dict[CVDType, float]:
    """Perceptual distance between two colours under each simulated deficiency."""
    return {k: delta_e(simulate_cvd(a, k), simulate_cvd(b, k)) for k in MACHADO_2009}


# --- audit ------------------------------------------------------------------------


@dataclass
class CheckResult:
    """Outcome of one palette check."""

    name: str
    status: Literal["pass", "warn", "fail"]
    detail: str


@dataclass
class PaletteAudit:
    """Full audit report for a categorical palette."""

    palette: tuple[str, ...]
    mode: str
    surface: str
    pairs: str
    checks: list[CheckResult] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        """``True`` when no check hard-failed (warnings are allowed)."""
        return all(c.status != "fail" for c in self.checks)

    @property
    def worst_cvd_delta_e(self) -> float:
        """Minimum protan/deutan distance over the audited pairs."""
        return min(
            (
                min(cvd_delta_e(a, b)["protan"], cvd_delta_e(a, b)["deutan"])
                for a, b in _pairs(self.palette, self.pairs)
            ),
            default=float("inf"),
        )

    def to_text(self) -> str:
        """Render the report as aligned plain text."""
        lines = [f"Palette ({self.mode}, surface {self.surface}, {self.pairs} pairs): {len(self.palette)} slots"]
        for c in self.checks:
            lines.append(f"  [{c.status.upper():4}] {c.name:<22} {c.detail}")
        lines.append("  -> " + ("ALL CHECKS PASS" if self.ok else "FAILED - fix the marked checks"))
        return "\n".join(lines)


def _pairs(palette: Sequence[str], pairs: str) -> list[tuple[str, str]]:
    if pairs == "adjacent":
        return list(itertools.pairwise(palette))
    if pairs == "all":
        return list(itertools.combinations(palette, 2))
    raise ValueError("pairs must be 'adjacent' or 'all'")


def audit_palette(
    palette: Sequence[str],
    mode: Literal["light", "dark"] = "light",
    surface: str | None = None,
    pairs: Literal["adjacent", "all"] = "adjacent",
) -> PaletteAudit:
    """Run the computable categorical-palette checks.

    Checks
    ------
    1. Lightness band: OKLCH L within the mode's band.
    2. Chroma floor: OKLCH C >= 0.10 so every hue still reads as a hue.
    3. CVD separation: min(protan, deutan) OKLab distance on the pair list;
       >= 8 passes, 6-8 warns (needs secondary encoding), < 6 fails.
    4. Normal-vision floor: worst unsimulated pair distance >= 15 (hard gate).
    5. Contrast vs surface: WCAG ratio >= 3:1, otherwise a warning that obliges
       a relief channel (direct labels or a table view).
    """
    if len(palette) < 1:
        raise ValueError("palette must contain at least one colour")
    palette = tuple(palette)
    surface = surface or DEFAULT_SURFACE[mode]
    for c in (*palette, surface):
        hex_to_rgb(c)
    report = PaletteAudit(palette, mode, surface, pairs)
    lo, hi = LIGHTNESS_BAND[mode]

    out_band = [(c, round(hex_to_oklch(c)[0], 3)) for c in palette if not lo <= hex_to_oklch(c)[0] <= hi]
    report.checks.append(
        CheckResult(
            "Lightness band",
            "fail" if out_band else "pass",
            f"outside L {lo}-{hi}: {out_band}" if out_band else f"all within L {lo}-{hi}",
        )
    )

    low_chroma = [(c, round(hex_to_oklch(c)[1], 3)) for c in palette if hex_to_oklch(c)[1] < CHROMA_FLOOR]
    report.checks.append(
        CheckResult(
            "Chroma floor",
            "fail" if low_chroma else "pass",
            f"below C {CHROMA_FLOOR}: {low_chroma}" if low_chroma else f"all C >= {CHROMA_FLOOR}",
        )
    )

    pair_list = _pairs(palette, pairs)
    if pair_list:
        scored = [(min(cvd_delta_e(a, b)["protan"], cvd_delta_e(a, b)["deutan"]), a, b) for a, b in pair_list]
        worst_d, wa, wb = min(scored)
        status: Literal["pass", "warn", "fail"] = (
            "pass" if worst_d >= CVD_TARGET else "warn" if worst_d >= CVD_FLOOR else "fail"
        )
        suffix = "" if status == "pass" else " - needs secondary encoding" if status == "warn" else " - below floor"
        report.checks.append(CheckResult("CVD separation", status, f"worst {wa} vs {wb} dE {worst_d:.1f}{suffix}"))

        normal = [(delta_e(a, b), a, b) for a, b in pair_list]
        nd, na, nb = min(normal)
        report.checks.append(
            CheckResult(
                "Normal-vision floor",
                "pass" if nd >= NORMAL_FLOOR else "fail",
                f"worst {na} vs {nb} dE {nd:.1f}" + ("" if nd >= NORMAL_FLOOR else f" - below {NORMAL_FLOOR:.0f}"),
            )
        )
    else:
        report.checks.append(CheckResult("CVD separation", "pass", "single colour - nothing to separate"))
        report.checks.append(CheckResult("Normal-vision floor", "pass", "single colour"))

    low_contrast = [
        (c, round(contrast_ratio(c, surface), 2)) for c in palette if contrast_ratio(c, surface) < CONTRAST_MIN
    ]
    report.checks.append(
        CheckResult(
            "Contrast vs surface",
            "warn" if low_contrast else "pass",
            f"below {CONTRAST_MIN}:1 - relief required: {low_contrast}" if low_contrast else f"all >= {CONTRAST_MIN}:1",
        )
    )
    return report


def order_palette(colors: Sequence[str], max_exhaustive: int = 8) -> tuple[str, ...]:
    """Reorder ``colors`` to maximise the minimum adjacent CVD distance.

    For up to ``max_exhaustive`` colours every permutation is scored (8! = 40 320
    orders, well under a second). Beyond that a greedy farthest-neighbour walk
    seeded from each colour is used.
    """
    colors = tuple(dict.fromkeys(colors))
    n = len(colors)
    if n <= 2:
        return colors
    dist = np.zeros((n, n))
    for i, j in itertools.combinations(range(n), 2):
        d = cvd_delta_e(colors[i], colors[j])
        dist[i, j] = dist[j, i] = min(d["protan"], d["deutan"])

    def score(order: Sequence[int]) -> float:
        return float(min(dist[a, b] for a, b in itertools.pairwise(order)))

    if n <= max_exhaustive:
        best = max(itertools.permutations(range(n)), key=score)
        return tuple(colors[i] for i in best)

    best_order: list[int] = []
    best_score = -1.0
    for start in range(n):
        order = [start]
        remaining = set(range(n)) - {start}
        while remaining:
            nxt = max(remaining, key=lambda j: dist[order[-1], j])
            order.append(nxt)
            remaining.remove(nxt)
        s = score(order)
        if s > best_score:
            best_score, best_order = s, order
    return tuple(colors[i] for i in best_order)


def sequential_scale(hue_hex: str, steps: int = 7, mode: Literal["light", "dark"] = "light") -> list[str]:
    """Build a one-hue sequential ramp by stepping OKLCH lightness.

    The chroma is scaled down towards the light end so pale steps stay in gamut.
    On a dark surface the ramp is reversed so "more" reads as lighter.
    """
    if steps < 2:
        raise ValueError("steps must be >= 2")
    _, chroma, hue = hex_to_oklch(hue_hex)
    ls = np.linspace(0.93, 0.35, steps)
    out = []
    for i, L in enumerate(ls):
        c = chroma * (0.35 + 0.65 * i / (steps - 1))
        out.append(_oklch_to_hex(float(L), float(c), hue))
    return out[::-1] if mode == "dark" else out


def _oklch_to_hex(L: float, C: float, h_deg: float) -> str:
    a = C * np.cos(np.radians(h_deg))
    b = C * np.sin(np.radians(h_deg))
    lms_ = np.linalg.solve(_M2, np.array([L, a, b]))
    lin = np.linalg.solve(_M1, lms_**3)
    return rgb_to_hex(linear_to_srgb(lin))
