#!/usr/bin/env python3
"""Motion-graphic data cards for the autopilot (title + chapter cards), dark-documentary style.

Renders full-screen 1920x1080 cards used as interludes in the video: a TITLE card (opening)
and CHAPTER cards (one per seo.md chapter). Background is a heavily blurred + darkened beat
image with a vignette; text is white serif with a thin gold accent line. assemble_video
imports these helpers and places the cards in the timeline (narration plays over them, so
no audio desync). Standalone `main()` renders previews to export/cards/ (free, no API).

Usage (preview): python tools/visuals/render_cards.py --project <slug>
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageStat, ImageFilter

REPO = Path(__file__).resolve().parents[2]
PROJECTS = REPO / "projects"
W, H = 1920, 1080
GOLD = (224, 196, 110)


def font_path() -> str | None:
    for c in [r"C:\Windows\Fonts\NotoSerifJP-VF.ttf",
              "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc",
              "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc",
              r"C:\Windows\Fonts\YuMin.ttf"]:
        if Path(c).exists():
            return c
    return None


def _pick_bg(proj: Path) -> Path | None:
    imgs = sorted((proj / "assets" / "images").glob("beat_*.jpg")) + \
        sorted((proj / "assets" / "images").glob("beat_*.png"))
    best, bestv = None, -1.0
    for g in imgs:
        v = ImageStat.Stat(Image.open(g).convert("L")).stddev[0]
        if v > bestv:
            best, bestv = g, v
    return best


def card_bg(proj: Path, bg_img: Path | None = None) -> Image.Image:
    """Blurred + darkened beat image with a vignette (or near-black if no image)."""
    src = bg_img or _pick_bg(proj)
    if src and Path(src).exists():
        im = Image.open(src).convert("RGB")
        scale = max(W / im.width, H / im.height)
        im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
        im = im.crop(((im.width - W) // 2, (im.height - H) // 2,
                      (im.width - W) // 2 + W, (im.height - H) // 2 + H))
        im = im.filter(ImageFilter.GaussianBlur(20))
        im = Image.blend(im, Image.new("RGB", (W, H), (6, 8, 12)), 0.62)
    else:
        im = Image.new("RGB", (W, H), (8, 10, 14))
    vig = Image.new("L", (W, H), 0)
    vd = ImageDraw.Draw(vig)
    vd.ellipse([-W * 0.3, -H * 0.3, W * 1.3, H * 1.3], fill=110)
    vig = vig.filter(ImageFilter.GaussianBlur(180))
    return Image.composite(im, Image.new("RGB", (W, H), (0, 0, 0)), vig)


def _wrap(draw, text, font, maxw):
    lines, cur = [], ""
    for ch in text:
        if ch == "\n":
            lines.append(cur); cur = ""; continue
        if draw.textlength(cur + ch, font=font) > maxw and cur:
            lines.append(cur); cur = ch
        else:
            cur += ch
    if cur:
        lines.append(cur)
    return lines


def _center(draw, y, text, font, fill, stroke=4):
    w = draw.textlength(text, font=font)
    draw.text(((W - w) / 2, y), text, font=font, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))


def recommended_title(proj: Path) -> str:
    seo = proj / "seo.md"
    if seo.exists():
        t = seo.read_text(encoding="utf-8")
        m = re.search(r"Recommended:\**\s*Option\s*(\d)", t)
        opt = m.group(1) if m else "1"
        mo = re.search(rf"###\s*Option\s*{opt}\b[^\n]*\n+([^\n]+)", t)
        if mo:
            return re.sub(r"\s*\[\d+\s*characters?\]\s*$", "", mo.group(1)).strip().strip("「」\" ")
    inp = proj / "input.json"
    if inp.exists():
        return json.loads(inp.read_text(encoding="utf-8")).get("topic", proj.name)
    return proj.name


def parse_chapters(proj: Path) -> list[tuple[int, str]]:
    """(seconds, title) from the seo.md CHAPTERS block."""
    seo = proj / "seo.md"
    out: list[tuple[int, str]] = []
    if not seo.exists():
        return out
    t = seo.read_text(encoding="utf-8")
    mb = re.search(r"CHAPTERS\s*\n[━─\-\s]*\n(.+?)(?:\n[━─]{3,}|\n##|\Z)", t, re.S)
    block = mb.group(1) if mb else t
    for line in block.splitlines():
        m = re.match(r"\s*(\d+):(\d{2})\s+(.+)", line)
        if m:
            out.append((int(m.group(1)) * 60 + int(m.group(2)), m.group(3).strip()))
    return out


def render_title_card(proj: Path, out: Path, bg_img: Path | None = None) -> None:
    im = card_bg(proj, bg_img)
    draw = ImageDraw.Draw(im)
    fp = font_path()
    title = recommended_title(proj)
    niche = "DOCUMENTARY"
    inp = proj / "input.json"
    if inp.exists():
        niche = json.loads(inp.read_text(encoding="utf-8")).get("niche", "documentary").replace("_", " ").upper()
    kicker = ImageFont.truetype(fp, 40)
    _center(draw, H * 0.30, "  ".join(niche), kicker, GOLD, stroke=2)
    fsize = 110
    font = ImageFont.truetype(fp, fsize)
    lines = _wrap(draw, title, font, W * 0.82)
    while len(lines) > 3 and fsize > 60:
        fsize -= 8
        font = ImageFont.truetype(fp, fsize)
        lines = _wrap(draw, title, font, W * 0.82)
    draw.line([(W * 0.42, H * 0.40), (W * 0.58, H * 0.40)], fill=GOLD, width=3)
    ty = H * 0.46
    for ln in lines:
        _center(draw, ty, ln, font, (255, 255, 255), stroke=6)
        ty += fsize + 16
    im.save(out, "JPEG", quality=90)


def render_chapter_card(proj: Path, idx: int, ntotal: int, title: str, out: Path,
                        bg_img: Path | None = None) -> None:
    im = card_bg(proj, bg_img)
    draw = ImageDraw.Draw(im)
    fp = font_path()
    kicker = ImageFont.truetype(fp, 38)
    _center(draw, H * 0.34, f"CHAPTER {idx} / {ntotal}", kicker, GOLD, stroke=2)
    draw.line([(W * 0.43, H * 0.43), (W * 0.57, H * 0.43)], fill=GOLD, width=3)
    fsize = 84
    font = ImageFont.truetype(fp, fsize)
    lines = _wrap(draw, title, font, W * 0.80)
    while len(lines) > 2 and fsize > 50:
        fsize -= 8
        font = ImageFont.truetype(fp, fsize)
        lines = _wrap(draw, title, font, W * 0.80)
    ty = H * 0.49
    for ln in lines:
        _center(draw, ty, ln, font, (255, 255, 255), stroke=5)
        ty += fsize + 14
    im.save(out, "JPEG", quality=90)


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="Preview the title + chapter cards")
    ap.add_argument("--project", required=True)
    a = ap.parse_args()
    proj = PROJECTS / a.project
    if not font_path():
        sys.exit("[ERROR] no usable JP font")
    outdir = proj / "export" / "cards"
    outdir.mkdir(parents=True, exist_ok=True)
    render_title_card(proj, outdir / "card_title.jpg")
    chapters = parse_chapters(proj)
    for i, (_, title) in enumerate(chapters, 1):
        render_chapter_card(proj, i, len(chapters), title, outdir / f"card_ch{i:02d}.jpg")
    print(f"Cards: {outdir.relative_to(proj)} — 1 title + {len(chapters)} chapter cards")
    print(f"title = '{recommended_title(proj)}'")
    for i, (s, t) in enumerate(chapters, 1):
        print(f"  ch{i}: {s//60}:{s%60:02d}  {t}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
