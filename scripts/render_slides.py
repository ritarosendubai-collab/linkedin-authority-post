#!/usr/bin/env python3
"""Render a carousel deck to 1080x1350 PNGs and a document-post PDF.

Deterministic renderer: the deck is data, so a corrected number means a
re-run, not a rebuild by hand. Enforces the skill's typographic floor --
if copy will not fit at the minimum body size, the slide FAILS rather than
silently shrinking the type. Cut the copy instead.

Usage:
    python3 scripts/render_slides.py deck.json --out slides/ --pdf carousel.pdf
    python3 scripts/render_slides.py deck.json --out slides/ --fonts /path/to/fonts

Requires: Pillow.
"""

from __future__ import annotations

import argparse
import json
import sys
import zlib
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("error: Pillow is required (pip install Pillow)", file=sys.stderr)
    raise SystemExit(2)

W, H = 1080, 1350
MARGIN = 88
MIN_BODY = 36          # the skill's legibility floor, in px
RULE = 2

THEMES = {
    # Restrained consultancy-report palette. Deliberately not modelled on any
    # firm's brand identity -- see references/rendering-and-design-system.md.
    "neutral-consultancy": {
        "paper": "#FBFAF8",
        "ink": "#14171A",
        "muted": "#6E6A63",
        "rule": "#D8D5D0",
        "accent": "#2F4F45",
        "accent_ink": "#FBFAF8",
    },
}

FONT_CANDIDATES = {
    "display": ["InstrumentSans-Bold.ttf", "WorkSans-Bold.ttf", "DejaVuSans-Bold.ttf"],
    "head":    ["InstrumentSans-Bold.ttf", "WorkSans-Bold.ttf", "DejaVuSans-Bold.ttf"],
    "body":    ["WorkSans-Regular.ttf", "InstrumentSans-Regular.ttf", "DejaVuSans.ttf"],
    "mono":    ["IBMPlexMono-Regular.ttf", "JetBrainsMono-Regular.ttf", "DejaVuSansMono.ttf"],
}

SYSTEM_FONT_DIRS = [
    "/usr/share/fonts/truetype/dejavu",
    "/usr/share/fonts/truetype",
    "/Library/Fonts",
    "/System/Library/Fonts",
]


class Fonts:
    def __init__(self, font_dir: Path | None):
        self.dirs = [font_dir] if font_dir else []
        self.dirs += [Path(d) for d in SYSTEM_FONT_DIRS]
        self._cache: dict[tuple[str, int], ImageFont.FreeTypeFont] = {}
        self._resolved: dict[str, Path] = {}
        self.warnings: list[str] = []
        for role, names in FONT_CANDIDATES.items():
            for name in names:
                hit = self._find(name)
                if hit:
                    self._resolved[role] = hit
                    break
            if role not in self._resolved:
                self.warnings.append(f"no font found for role '{role}'; using PIL default")

    def _find(self, name: str) -> Path | None:
        for d in self.dirs:
            if not d or not d.exists():
                continue
            direct = d / name
            if direct.exists():
                return direct
            for hit in d.rglob(name):
                return hit
        return None

    def get(self, role: str, size: int) -> ImageFont.FreeTypeFont:
        key = (role, size)
        if key not in self._cache:
            path = self._resolved.get(role)
            if path:
                self._cache[key] = ImageFont.truetype(str(path), size)
            else:
                self._cache[key] = ImageFont.load_default(size)
        return self._cache[key]


def text_h(draw: ImageDraw.ImageDraw, s: str, font) -> int:
    box = draw.textbbox((0, 0), s or "x", font=font)
    return box[3] - box[1]


def wrap(draw: ImageDraw.ImageDraw, text: str, font, max_w: int) -> list[str]:
    lines: list[str] = []
    for para in text.split("\n"):
        words, cur = para.split(), ""
        if not words:
            lines.append("")
            continue
        for word in words:
            trial = f"{cur} {word}".strip()
            if draw.textlength(trial, font=font) <= max_w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
    return lines


def fit_block(draw, text, role, fonts, max_w, max_h, start, minimum, leading=1.34):
    """Shrink to fit, but never below `minimum`. Returns None if it cannot fit."""
    size = start
    while size >= minimum:
        font = fonts.get(role, size)
        lines = wrap(draw, text, font, max_w)
        line_h = int(size * leading)
        if len(lines) * line_h <= max_h:
            return font, lines, line_h
        size -= 2
    return None


def draw_block(draw, x, y, lines, font, line_h, fill) -> int:
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += line_h
    return y


def footer(draw, fonts, theme, ref: str, n: int, total: int):
    f = fonts.get("mono", 26)
    draw.line([(MARGIN, H - 132), (W - MARGIN, H - 132)], fill=theme["rule"], width=RULE)
    if ref:
        draw.text((MARGIN, H - 108), ref, font=f, fill=theme["muted"])
    label = f"{n:02d}/{total:02d}"
    draw.text((W - MARGIN - draw.textlength(label, font=f), H - 108), label,
              font=f, fill=theme["muted"])


def render_slide(slide: dict, fonts: Fonts, theme: dict, total: int) -> tuple[Image.Image, list[str]]:
    errs: list[str] = []
    kind = slide.get("type", "claim")
    accent_bg = kind in {"cover", "turn"}
    bg = theme["accent"] if accent_bg else theme["paper"]
    fg = theme["accent_ink"] if accent_bg else theme["ink"]
    sub_fg = "#C8D6CF" if accent_bg else theme["muted"]

    img = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(img)
    inner = W - 2 * MARGIN
    n = slide.get("n", 0)

    if kind == "cover":
        y = 300
        if slide.get("kicker"):
            kf = fonts.get("mono", 28)
            d.text((MARGIN, 176), slide["kicker"].upper(), font=kf, fill=sub_fg)
            d.line([(MARGIN, 226), (MARGIN + 96, 226)], fill=sub_fg, width=3)
        fit = fit_block(d, slide["hero"], "display", fonts, inner, 420, 168, 84, 1.02)
        if not fit:
            errs.append(f"slide {n}: hero does not fit")
            return img, errs
        font, lines, lh = fit
        y = draw_block(d, MARGIN, y, lines, font, lh, fg)
        if slide.get("sub"):
            fit = fit_block(d, slide["sub"], "display", fonts, inner, 220, 76, 48, 1.12)
            if not fit:
                errs.append(f"slide {n}: sub does not fit")
            else:
                sf, sl, slh = fit
                y = draw_block(d, MARGIN, y + 26, sl, sf, slh, sub_fg)
        if slide.get("standfirst"):
            fit = fit_block(d, slide["standfirst"], "body", fonts, inner, 300, 42, MIN_BODY)
            if not fit:
                errs.append(f"slide {n}: standfirst does not fit at >={MIN_BODY}px")
            else:
                bf, bl, blh = fit
                draw_block(d, MARGIN, y + 56, bl, bf, blh, sub_fg)
        if slide.get("masthead"):
            mf = fonts.get("mono", 26)
            d.line([(MARGIN, H - 172), (W - MARGIN, H - 172)], fill=sub_fg, width=RULE)
            d.text((MARGIN, H - 148), slide["masthead"].upper(), font=mf, fill=sub_fg)
        return img, errs

    if kind == "closing":
        y = 260
        fit = fit_block(d, slide.get("question", ""), "head", fonts, inner, 500, 68, 44, 1.24)
        if not fit:
            errs.append(f"slide {n}: question does not fit")
        else:
            qf, ql, qlh = fit
            y = draw_block(d, MARGIN, y, ql, qf, qlh, fg)
        d.line([(MARGIN, y + 60), (W - MARGIN, y + 60)], fill=theme["rule"], width=RULE)
        sf = fonts.get("mono", 24)
        sl = wrap(d, slide.get("source", ""), sf, inner)
        yy = draw_block(d, MARGIN, y + 96, sl, sf, 34, theme["muted"])
        if slide.get("contact"):
            d.text((MARGIN, yy + 28), slide["contact"], font=fonts.get("head", 34), fill=theme["accent"])
        return img, errs

    # claim / turn / list / statement
    y = 232
    if slide.get("head"):
        fit = fit_block(d, slide["head"], "head", fonts, inner, 300, 82, 48, 1.14)
        if not fit:
            errs.append(f"slide {n}: head does not fit")
        else:
            hf, hl, hlh = fit
            y = draw_block(d, MARGIN, y, hl, hf, hlh, fg)
            d.line([(MARGIN, y + 34), (MARGIN + 120, y + 34)], fill=sub_fg, width=3)
            y += 82

    avail = (H - 200) - y
    if slide.get("body"):
        fit = fit_block(d, slide["body"], "body", fonts, inner, avail - 40, 46, MIN_BODY)
        if not fit:
            errs.append(f"slide {n}: body will not fit at >={MIN_BODY}px -- cut the copy")
        else:
            bf, bl, blh = fit
            y = draw_block(d, MARGIN, y, bl, bf, blh, fg if accent_bg else theme["ink"])

    if slide.get("items"):
        bf = fonts.get("body", 40)
        blh = int(40 * 1.34)
        for item in slide["items"]:
            lines = wrap(d, item, bf, inner - 44)
            d.text((MARGIN, y + 6), "—", font=bf, fill=theme["accent"])
            y = draw_block(d, MARGIN + 44, y, lines, bf, blh, theme["ink"]) + 16
        if y > H - 200:
            errs.append(f"slide {n}: list overflows -- cut an item")

    if slide.get("callout"):
        box_top = y + 34
        fit = fit_block(d, slide["callout"], "body", fonts, inner - 56, (H - 200) - box_top - 40, 40, MIN_BODY)
        if not fit:
            errs.append(f"slide {n}: callout will not fit at >={MIN_BODY}px")
        else:
            cf, cl, clh = fit
            box_h = len(cl) * clh + 56
            d.rectangle([MARGIN, box_top, W - MARGIN, box_top + box_h],
                        fill=theme["accent"] if not accent_bg else theme["paper"])
            draw_block(d, MARGIN + 28, box_top + 28, cl, cf, clh,
                       theme["accent_ink"] if not accent_bg else theme["ink"])

    footer(d, fonts, theme, slide.get("ref", ""), n, total)
    return img, errs


def write_pdf(images, png_dir: Path, pdf_path: Path) -> bool:
    """Assemble the document-post PDF with Flate-compressed RGB pages.

    Written by hand rather than delegated: Pillow's PDF writer routes RGB
    through its JPEG encoder (absent from some builds) and writes paletted
    images uncompressed, which turns a 12-slide deck into tens of megabytes.
    ImageMagick is blocked by policy on many hosts. Flate on flat-colour
    typographic slides compresses to a fraction of either, with no artefacts
    around the type — which matters, because the document post is the format
    this skill recommends.
    """
    try:
        objects: list[bytes] = []

        def add(body: bytes) -> int:
            objects.append(body)
            return len(objects)

        kids, page_refs = [], []
        for im in images:
            rgb = im.convert("RGB")
            w, h = rgb.size
            data = zlib.compress(rgb.tobytes(), 9)
            img_id = add(
                b"<< /Type /XObject /Subtype /Image /Width %d /Height %d "
                b"/ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /FlateDecode "
                b"/Length %d >>\nstream\n" % (w, h, len(data)) + data + b"\nendstream"
            )
            content = b"q %d 0 0 %d 0 0 cm /Im0 Do Q" % (w, h)
            cdata = zlib.compress(content, 9)
            con_id = add(
                b"<< /Filter /FlateDecode /Length %d >>\nstream\n" % len(cdata)
                + cdata + b"\nendstream"
            )
            page_refs.append((img_id, con_id, w, h))

        pages_id = len(objects) + len(page_refs) + 1
        for img_id, con_id, w, h in page_refs:
            pid = add(
                b"<< /Type /Page /Parent %d 0 R /MediaBox [0 0 %d %d] "
                b"/Resources << /XObject << /Im0 %d 0 R >> >> /Contents %d 0 R >>"
                % (pages_id, w, h, img_id, con_id)
            )
            kids.append(pid)

        add(b"<< /Type /Pages /Count %d /Kids [%s] >>"
            % (len(kids), b" ".join(b"%d 0 R" % k for k in kids)))
        root_id = add(b"<< /Type /Catalog /Pages %d 0 R >>" % pages_id)

        out, offsets = bytearray(b"%PDF-1.4\n"), []
        for i, body in enumerate(objects, start=1):
            offsets.append(len(out))
            out += b"%d 0 obj\n" % i + body + b"\nendobj\n"
        xref = len(out)
        out += b"xref\n0 %d\n" % (len(objects) + 1)
        out += b"0000000000 65535 f \n"
        for off in offsets:
            out += b"%010d 00000 n \n" % off
        out += (b"trailer\n<< /Size %d /Root %d 0 R >>\nstartxref\n%d\n%%%%EOF\n"
                % (len(objects) + 1, root_id, xref))
        pdf_path.write_bytes(bytes(out))
        return True
    except (OSError, ValueError, zlib.error):
        return False


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("deck", type=Path)
    ap.add_argument("--out", type=Path, default=Path("slides"))
    ap.add_argument("--pdf", type=Path, default=None)
    ap.add_argument("--fonts", type=Path, default=None)
    args = ap.parse_args()

    deck = json.loads(args.deck.read_text(encoding="utf-8"))
    theme = THEMES.get(deck.get("theme", "neutral-consultancy"))
    if theme is None:
        print(f"error: unknown theme {deck.get('theme')!r}", file=sys.stderr)
        return 2

    fonts = Fonts(args.fonts)
    for w in fonts.warnings:
        print(f"  warning {w}")

    args.out.mkdir(parents=True, exist_ok=True)
    slides = deck["slides"]
    total = len(slides)
    images, all_errs = [], []

    for slide in slides:
        img, errs = render_slide(slide, fonts, theme, total)
        all_errs += errs
        name = f"{slide.get('n', 0):02d}-{slide.get('type', 'slide')}.png"
        img.save(args.out / name)
        images.append(img)
        print(f"  wrote {args.out / name}")

    if args.pdf and images:
        if write_pdf(images, args.out, args.pdf):
            print(f"  wrote {args.pdf}")
        else:
            print(f"  not_run: {args.pdf} — no PDF encoder available; PNGs written, "
                  "upload as an image post or assemble the PDF locally")

    if all_errs:
        print("\nLEGIBILITY FAILURES (copy must be cut, not shrunk):")
        for e in all_errs:
            print(f"  ERROR {e}")
        return 1
    print(f"\nOK: {total} slides rendered, all copy fits at >={MIN_BODY}px")
    return 0


if __name__ == "__main__":
    sys.exit(main())
