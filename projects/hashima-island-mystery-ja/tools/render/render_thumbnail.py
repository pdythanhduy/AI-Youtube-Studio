#!/usr/bin/env python3
"""Render the YouTube thumbnail for hashima-island-mystery-ja.

Implements THUMB_A from data/thumbnail.json:
  - background : IMG001 (S001 island establishing, pre-dawn) — the AI image that
                 actually ships as the S001 visual in locked cut v7.
  - title      : 端島の謎
  - subtitle   : 軍艦島が語る静かな歴史
  - font       : Noto Serif JP (NotoSerifJP-VF.ttf)
  - style      : white, soft drop-shadow, no outline, bottom-center
  - grade      : dark_cinematic (subtle contrast + vignette + bottom scrim)
  - size       : 1280x720

Respectful-by-design: no death counts, no red arrows, no shock framing. Matches the
selected_pending_design concept exactly.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter

PROJ = Path(__file__).resolve().parents[2]
BG = PROJ / "assets/ai_images/generated/batch_3/IMG001_S001_island_establishing_predawn.png"


def _serif_fonts():
    """Cross-platform Noto Serif JP. Returns (kind, regular_path, bold_path).
    kind 'WIN_VF' = Windows variable font (weight via axes); 'STATIC' = Linux .ttc faces."""
    win = Path(r"C:\Windows\Fonts\NotoSerifJP-VF.ttf")
    if win.exists():
        return ("WIN_VF", str(win), str(win))
    for base in ("/usr/share/fonts/opentype/noto", "/usr/share/fonts/truetype/noto"):
        reg = Path(base) / "NotoSerifCJK-Regular.ttc"
        bold = Path(base) / "NotoSerifCJK-Bold.ttc"
        if reg.exists():
            return ("STATIC", str(reg), str(bold if bold.exists() else reg))
    return ("WIN_VF", str(win), str(win))  # will error clearly if truly absent


_FONT_KIND, _FONT_REG, _FONT_BOLD = _serif_fonts()
OUT_DIR = PROJ / "export/thumbnail"
OUT = OUT_DIR / "hashima_thumbnail_A_v1.png"

W, H = 1280, 720
TITLE = "端島の謎"
SUBTITLE = "軍艦島が語る静かな歴史"


def load_font(px, weight):
    if _FONT_KIND == "WIN_VF":
        f = ImageFont.truetype(_FONT_REG, px)
        try:
            f.set_variation_by_axes([weight])  # variable font: pick weight
        except Exception:
            pass
        return f
    # Linux static .ttc: heavy weight -> Bold face, else Regular (JP renders from face 0)
    return ImageFont.truetype(_FONT_BOLD if weight >= 600 else _FONT_REG, px)


def cover_resize(img, w, h):
    """Resize+center-crop to fill w×h (ratios are near-identical here)."""
    src_r, dst_r = img.width / img.height, w / h
    if src_r > dst_r:
        nh = h
        nw = round(h * src_r)
    else:
        nw = w
        nh = round(w / src_r)
    img = img.resize((nw, nh), Image.LANCZOS)
    left = (nw - w) // 2
    top = (nh - h) // 2
    return img.crop((left, top, left + w, top + h))


def vignette(size, strength=0.55):
    w, h = size
    mask = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(mask)
    # bright center ellipse, darkened edges
    d.ellipse([-w * 0.25, -h * 0.25, w * 1.25, h * 1.25], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(w * 0.18))
    dark = Image.new("RGB", (w, h), (0, 0, 0))
    base_alpha = Image.new("L", (w, h), int(255 * strength))
    # combine: where mask is bright keep image, edges get dark
    inv = Image.eval(mask, lambda v: int((255 - v) * strength))
    return inv  # alpha for a black overlay


def bottom_scrim(size, frac=0.55, opacity=170):
    w, h = size
    grad = Image.new("L", (1, h), 0)
    start = int(h * (1 - frac))
    for y in range(start, h):
        t = (y - start) / max(1, (h - start))
        grad.putpixel((0, y), int(opacity * (t ** 1.4)))
    grad = grad.resize((w, h))
    return grad


def draw_text_shadow(base, xy, text, font, fill, anchor, shadow_off=(0, 4),
                     shadow_blur=6, shadow_opacity=190):
    """Draw text with a soft blurred drop shadow."""
    w, h = base.size
    sh_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh_layer)
    sd.text((xy[0] + shadow_off[0], xy[1] + shadow_off[1]), text, font=font,
            fill=(0, 0, 0, shadow_opacity), anchor=anchor)
    sh_layer = sh_layer.filter(ImageFilter.GaussianBlur(shadow_blur))
    base.alpha_composite(sh_layer)
    d = ImageDraw.Draw(base)
    d.text(xy, text, font=font, fill=fill, anchor=anchor)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    img = Image.open(BG).convert("RGB")
    img = cover_resize(img, W, H)

    # dark_cinematic grade: gentle contrast, slight desaturation, cool already
    img = ImageEnhance.Contrast(img).enhance(1.08)
    img = ImageEnhance.Color(img).enhance(0.92)
    img = ImageEnhance.Brightness(img).enhance(0.97)

    # vignette (darken edges to focus the island silhouette)
    vmask = vignette((W, H), strength=0.45)
    black = Image.new("RGB", (W, H), (0, 0, 0))
    img = Image.composite(black, img, vmask)

    # bottom scrim for text legibility over the water
    smask = bottom_scrim((W, H), frac=0.5, opacity=160)
    img = Image.composite(black, img, smask)

    canvas = img.convert("RGBA")

    # ── Title ──
    title_font = load_font(118, 700)
    sub_font = load_font(46, 500)

    cx = W // 2
    title_y = 550
    sub_y = 648

    draw_text_shadow(canvas, (cx, title_y), TITLE, title_font,
                     fill=(255, 255, 255, 255), anchor="mm",
                     shadow_off=(0, 5), shadow_blur=9, shadow_opacity=210)

    draw_text_shadow(canvas, (cx, sub_y), SUBTITLE, sub_font,
                     fill=(222, 228, 234, 255), anchor="mm",
                     shadow_off=(0, 3), shadow_blur=6, shadow_opacity=190)

    out = canvas.convert("RGB")
    out.save(OUT, "PNG")
    # also a JPG (smaller, YouTube-friendly) under 2MB
    out.save(OUT.with_suffix(".jpg"), "JPEG", quality=92)
    print(f"Wrote {OUT} ({OUT.stat().st_size/1024:.0f} KB)")
    print(f"Wrote {OUT.with_suffix('.jpg')} "
          f"({OUT.with_suffix('.jpg').stat().st_size/1024:.0f} KB)")


if __name__ == "__main__":
    main()
