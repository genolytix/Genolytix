#!/usr/bin/env python3
"""
Builds the Genolytix logo set.

The mark is a genuine 2D projection of a 3D double helix: node depth is
cos(phase), and that depth drives radius, colour and opacity — the same
depth language the site's background lattice uses. Two strands of sampled
points, rungs between them. Geno (the helix) and lytix (the sampling)
are both in the mark.

The wordmark is Fraunces, the same face as the site's headings, converted
to outlines so the SVG is self-contained and needs no webfont.
"""

import math
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen

NAVY = "#0A2540"
NAVY_DEEP = "#061726"
CYAN = "#00BCD4"
MINT = "#5EEAD4"
WHITE = "#FFFFFF"


def outline(text, font_path, size, axes, tracking=0.0):
    """Return (svg_path_d, advance_width) for text at the given pixel size."""
    font = instantiateVariableFont(TTFont(font_path), axes, updateFontNames=False)
    upm = font["head"].unitsPerEm
    cmap = font.getBestCmap()
    glyphset = font.getGlyphSet()
    hmtx = font["hmtx"]
    scale = size / upm

    parts = []
    x = 0.0
    for ch in text:
        name = cmap.get(ord(ch))
        if name is None:
            x += size * 0.4
            continue
        pen = SVGPathPen(glyphset)
        glyphset[name].draw(pen)
        d = pen.getCommands()
        if d:
            # y flips: font units go up, SVG goes down
            parts.append(
                f'<g transform="translate({x:.3f} 0) scale({scale:.6f} {-scale:.6f})">'
                f'<path d="{d}"/></g>'
            )
        x += hmtx[name][0] * scale + tracking
    return "".join(parts), x - tracking


def helix(w, h, periods=1.25, nodes_per_strand=8, horizontal=True,
          node_scale=1.0, stroke=1.7):
    """Two strands, rungs, depth-sorted nodes. Returns SVG fragment.

    The curve is sampled finely for smoothness but nodes are placed
    sparsely — a node every sample reads as a chain, not a molecule."""
    amp = h * 0.36
    mid = h / 2
    curve_samples = 60

    def strand_points(count, s):
        out = []
        for i in range(count):
            u = i / (count - 1)
            p = u * periods * 2 * math.pi + (math.pi if s else 0)
            out.append((u * w, mid + amp * math.sin(p), math.cos(p)))
        return out

    pts = [strand_points(curve_samples, 0), strand_points(curve_samples, 1)]
    node_pts = [strand_points(nodes_per_strand, 0), strand_points(nodes_per_strand, 1)]
    samples = curve_samples

    def xy(p):
        return (p[0], p[1]) if horizontal else (p[1], p[0])

    out = []

    # Rungs, drawn first so nodes sit on top. Faded by how edge-on they are.
    for i in range(nodes_per_strand):
        a, b = node_pts[0][i], node_pts[1][i]
        sep = abs(a[1] - b[1]) / (2 * amp)
        if sep < 0.12:
            continue
        ax, ay = xy(a)
        bx, by = xy(b)
        out.append(
            f'<line x1="{ax:.2f}" y1="{ay:.2f}" x2="{bx:.2f}" y2="{by:.2f}" '
            f'stroke="{CYAN}" stroke-width="{0.8 + sep * 0.5:.2f}" '
            f'stroke-opacity="{0.16 + sep * 0.38:.3f}" stroke-linecap="round"/>'
        )

    # Strands.
    for s in (0, 1):
        d = " ".join(
            ("M" if i == 0 else "L") + f"{xy(p)[0]:.2f} {xy(p)[1]:.2f}"
            for i, p in enumerate(pts[s])
        )
        out.append(
            f'<path d="{d}" fill="none" stroke="url(#strand)" '
            f'stroke-width="{stroke}" stroke-linecap="round" stroke-opacity=".8"/>'
        )

    # Nodes, far ones painted first.
    nodes = [p for s in (0, 1) for p in node_pts[s]]
    for p in sorted(nodes, key=lambda p: p[2]):
        t = (p[2] + 1) / 2  # 0 back, 1 front
        cx, cy = xy(p)
        out.append(
            f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{(1.2 + t * 1.7) * node_scale:.2f}" '
            f'fill="{MINT if t > 0.5 else CYAN}" opacity="{0.4 + t * 0.55:.3f}"/>'
        )

    return "\n    ".join(out)


GRADIENT = f"""  <defs>
    <linearGradient id="strand" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{CYAN}"/>
      <stop offset="1" stop-color="{MINT}"/>
    </linearGradient>
  </defs>"""


def wordmark_svg(colour, filename, sub_colour=None):
    """Mark + 'Genolytix', sized to sit in the 169x46 header slot."""
    mark_w, mark_h = 40, 26   # helix run, then across; drawn vertically
    mark_pad = 5
    gap = 16
    word, word_w = outline(
        "Genolytix",
        "/home/claude/Fraunces5BSOFT2CWONK2Copsz2Cwght5D.ttf",
        29,
        {"wght": 600, "opsz": 144, "SOFT": 0, "WONK": 0},
        tracking=-0.35,
    )
    sub, sub_w = outline(
        "TECHNOLOGY",
        "/home/claude/SplineSans5Bwght5D.ttf",
        8.2,
        {"wght": 600},
        tracking=2.6,
    )

    total_w = mark_h + mark_pad * 2 + gap + max(word_w, sub_w)
    baseline = 28.5

    mark_h_box = 46
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {total_w:.1f} {mark_h_box}" \
width="{total_w:.1f}" height="{mark_h_box}" role="img" aria-label="Genolytix Technology">
{GRADIENT}
  <g transform="translate({mark_pad} {(mark_h_box - mark_w) / 2:.1f})">
    {helix(mark_w, mark_h, periods=1.5, nodes_per_strand=8, horizontal=False,
           node_scale=1.05, stroke=1.8)}
  </g>
  <g fill="{colour}" transform="translate({mark_h + mark_pad * 2 + gap:.1f} {baseline})">{word}</g>
  <g fill="{sub_colour or colour}" opacity="{'1' if sub_colour else '.6'}" \
transform="translate({mark_h + mark_pad * 2 + gap + 1.5:.1f} {baseline + 11.5})">{sub}</g>
</svg>
"""
    open(filename, "w").write(svg)
    return total_w


def mark_svg(filename, size=96, boxed=True):
    """Square, vertical helix. For favicons and app icons."""
    pad = size * 0.2
    inner = size - pad * 2
    box = (
        f'<rect width="{size}" height="{size}" rx="{size * 0.22:.1f}" fill="{NAVY}"/>'
        if boxed else ""
    )
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" \
width="{size}" height="{size}" role="img" aria-label="Genolytix">
{GRADIENT}
  {box}
  <g transform="translate({pad + inner * 0.07:.1f} {pad:.1f})">
    {helix(inner * 0.86, inner, periods=1.25, nodes_per_strand=7, horizontal=False, node_scale=1.25, stroke=2.2)}
  </g>
</svg>
"""
    open(filename, "w").write(svg)


def cover_svg(filename):
    """1200x630 social card."""
    word, word_w = outline(
        "Genolytix",
        "/home/claude/Fraunces5BSOFT2CWONK2Copsz2Cwght5D.ttf",
        104,
        {"wght": 600, "opsz": 144, "SOFT": 0, "WONK": 0},
        tracking=-1.2,
    )
    tag, tag_w = outline(
        "AI for drug discovery and accessible eye care",
        "/home/claude/SplineSans5Bwght5D.ttf",
        31,
        {"wght": 400},
    )
    eyebrow, _ = outline(
        "GENOLYTIX TECHNOLOGY",
        "/home/claude/SplineSans5Bwght5D.ttf",
        17,
        {"wght": 600},
        tracking=4.2,
    )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="1200" height="630">
  <defs>
    <linearGradient id="strand" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{CYAN}"/>
      <stop offset="1" stop-color="{MINT}"/>
    </linearGradient>
    <linearGradient id="bg" x1="0" y1="0" x2=".7" y2="1">
      <stop offset="0" stop-color="{NAVY_DEEP}"/>
      <stop offset=".55" stop-color="{NAVY}"/>
      <stop offset="1" stop-color="#0E3559"/>
    </linearGradient>
    <radialGradient id="glow" cx=".15" cy="1" r=".7">
      <stop offset="0" stop-color="{CYAN}" stop-opacity=".28"/>
      <stop offset="1" stop-color="{CYAN}" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <rect width="1200" height="630" fill="url(#bg)"/>
  <rect width="1200" height="630" fill="url(#glow)"/>

  <g transform="translate(870 92)" opacity=".85">
    {helix(450, 210, periods=2.4, nodes_per_strand=14, horizontal=False, node_scale=2.9, stroke=3.4)}
  </g>

  <g fill="{MINT}" transform="translate(84 232)">{eyebrow}</g>
  <g fill="{WHITE}" transform="translate(80 368)">{word}</g>
  <g fill="#D0E0EC" transform="translate(84 433)">{tag}</g>
  <rect x="84" y="487" width="86" height="4" rx="2" fill="{CYAN}"/>
</svg>
"""
    open(filename, "w").write(svg)


if __name__ == "__main__":
    w = wordmark_svg(WHITE, "logo.svg")
    wordmark_svg(NAVY, "logo-on-light.svg", sub_colour=None)
    mark_svg("logo-mark.svg", 96, boxed=True)
    mark_svg("logo-mark-plain.svg", 96, boxed=False)
    cover_svg("og-cover.svg")
    print(f"wordmark width {w:.1f}px at 46px tall")
