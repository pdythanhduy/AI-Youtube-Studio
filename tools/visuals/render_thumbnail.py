#!/usr/bin/env python3
"""Generate a YouTube thumbnail (1280x720) for an autopilot project from seo.md.

Picks a strong beat image as the background, darkens it for legibility, and overlays the
seo.md thumbnail headline (+ optional sub-text) in a bold JP serif, dark-documentary style
(white high-contrast text, lower-left). Output: export/thumbnail/<slug>_thumb.jpg.
General-purpose (reads the project's own seo.md) — not tied to any single project.

Usage: python tools/visuals/render_thumbnail.py --project <slug> [--bg beat_NN.jpg]
"""
from __future__ import annotations
import argparse, re, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageStat

REPO = Path(__file__).resolve().parents[2]
PROJECTS = REPO / "projects"
W, H = 1280, 720


def font_path() -> str | None:
    for c in [r"C:\Windows\Fonts\NotoSerifJP-VF.ttf",
              "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc",
              "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc",
              r"C:\Windows\Fonts\YuMin.ttf"]:
        if Path(c).exists():
            return c
    return None


def thumb_text(proj: Path) -> tuple[str, str]:
    head, sub = "", ""
    seo = proj / "seo.md"
    if seo.exists():
        t = seo.read_text(encoding="utf-8")
        m = re.search(r"###\s*Primary text[^\n]*\n+([^\n]+)", t)
        if m and not m.group(1).strip().startswith("#"):
            head = m.group(1).strip()
        m = re.search(r"###\s*Sub-text[^\n]*\n+([^\n]+)", t)
        if m and not m.group(1).strip().startswith("#"):
            sub = m.group(1).strip()
    if not head:
        inp = proj / "input.json"
        head = proj.name
        if inp.exists():
            import json
            head = json.loads(inp.read_text(encoding="utf-8")).get("topic", proj.name)[:18]
    return head, sub


def pick_bg(proj: Path, override: str | None) -> Path | None:
    imgs = sorted((proj / "assets" / "images").glob("beat_*.jpg")) + \
        sorted((proj / "assets" / "images").glob("beat_*.png"))
    if override:
        p = proj / "assets" / "images" / override
        if p.exists():
            return p
    best, bestv = None, -1.0
    for g in imgs:                       # most-detailed frame (highest stddev), skips near-black
        v = ImageStat.Stat(Image.open(g).convert("L")).stddev[0]
        if v > bestv:
            best, bestv = g, v
    return best


def wrap(draw: ImageDraw.ImageDraw, text: str, font, maxw: int) -> list[str]:
    lines, cur = [], ""
    for ch in text:                      # char-wrap (works for CJK; latin words rarely overflow here)
        if ch == "\n":
            lines.append(cur); cur = ""; continue
        if draw.textlength(cur + ch, font=font) > maxw and cur:
            lines.append(cur); cur = ch
        else:
            cur += ch
    if cur:
        lines.append(cur)
    return lines


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="Render a YouTube thumbnail from seo.md + a beat image")
    ap.add_argument("--project", required=True)
    ap.add_argument("--bg", help="specific background, e.g. beat_07.jpg (else most-detailed)")
    a = ap.parse_args()
    proj = PROJECTS / a.project
    bg = pick_bg(proj, a.bg)
    if not bg:
        sys.exit("[ERROR] no beat images to use as background (run generate_images first)")
    head, sub = thumb_text(proj)
    fp = font_path()
    if not fp:
        sys.exit("[ERROR] no usable JP font found")

    im = Image.open(bg).convert("RGB")                       # cover-crop to 1280x720
    scale = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
    im = im.crop(((im.width - W) // 2, (im.height - H) // 2,
                  (im.width - W) // 2 + W, (im.height - H) // 2 + H))
    # gradient darken (stronger toward the bottom where the text sits) + slight overall darken
    grad = Image.new("L", (W, H), 0)
    gd = ImageDraw.Draw(grad)
    for yy in range(H):
        gd.line([(0, yy), (W, yy)], fill=int(165 * (yy / H) ** 1.4))
    im = Image.composite(Image.new("RGB", (W, H), (0, 0, 0)), im, grad)
    im = Image.blend(im, Image.new("RGB", (W, H), (8, 10, 14)), 0.16)

    draw = ImageDraw.Draw(im)
    margin = 70
    fsize = 100
    font = ImageFont.truetype(fp, fsize)
    lines = wrap(draw, head, font, W - 2 * margin)
    while len(lines) > 3 and fsize > 52:                     # shrink to fit 3 lines max
        fsize -= 8
        font = ImageFont.truetype(fp, fsize)
        lines = wrap(draw, head, font, W - 2 * margin)
    lh = fsize + 14
    block_h = lh * len(lines) + (58 if sub else 0)
    ty = H - margin - block_h
    for ln in lines:
        draw.text((margin, ty), ln, font=font, fill=(255, 255, 255), stroke_width=6, stroke_fill=(0, 0, 0))
        ty += lh
    if sub:
        sf = ImageFont.truetype(fp, 46)
        draw.text((margin, ty + 8), sub, font=sf, fill=(232, 208, 120), stroke_width=3, stroke_fill=(0, 0, 0))

    out = proj / "export" / "thumbnail" / f"{a.project}_thumb.jpg"
    out.parent.mkdir(parents=True, exist_ok=True)
    im.save(out, "JPEG", quality=90)
    print(f"Thumbnail: {out.relative_to(proj)}  (bg={bg.name}, headline='{head}', sub='{sub}')")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
