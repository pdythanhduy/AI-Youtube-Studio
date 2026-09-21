#!/usr/bin/env python3
"""Generate avatar + banner for the ネタバレ映画館 channel (minimal cinema style)."""
import pathlib
import sys

from PIL import Image, ImageDraw, ImageFont, ImageFilter

sys.stdout.reconfigure(encoding="utf-8")

OUT = pathlib.Path(__file__).resolve().parents[1] / "export" / "channel_art"
OUT.mkdir(parents=True, exist_ok=True)
FONT = r"C:\Windows\Fonts\YuGothB.ttc"

BG = (18, 18, 26)
RED = (229, 57, 70)
WHITE = (245, 245, 245)
GRAY = (170, 170, 180)


def film_strip(draw, x0, y0, x1, y1, hole=14, gap=10):
    draw.rectangle([x0, y0, x1, y1], fill=RED)
    y = y0 + gap
    while y + hole < y1:
        pass
        y += hole + gap


def perforations(draw, x0, y, x1, size, gap, color):
    x = x0
    while x + size <= x1:
        draw.rounded_rectangle([x, y, x + size, y + size], radius=size // 4,
                               fill=color)
        x += size + gap


def avatar():
    s = 800
    img = Image.new("RGB", (s, s), BG)
    d = ImageDraw.Draw(img)
    # subtle radial glow
    glow = Image.new("L", (s, s), 0)
    gd = ImageDraw.Draw(glow)
    gd.ellipse([s * 0.15, s * 0.1, s * 0.85, s * 0.8], fill=60)
    glow = glow.filter(ImageFilter.GaussianBlur(120))
    img.paste(Image.new("RGB", (s, s), (60, 30, 40)), (0, 0), glow)
    d = ImageDraw.Draw(img)
    # big ネ
    font = ImageFont.truetype(FONT, 430, index=0)
    box = d.textbbox((0, 0), "ネ", font=font)
    w, h = box[2] - box[0], box[3] - box[1]
    d.text(((s - w) / 2 - box[0], (s - h) / 2 - box[1] - 40), "ネ",
           font=font, fill=WHITE)
    # red film bar with perforations
    bar_y = 620
    d.rectangle([120, bar_y, 680, bar_y + 56], fill=RED)
    perforations(d, 140, bar_y + 16, 660, 24, 22, BG)
    img.save(OUT / "avatar_800.png")
    print("avatar ->", OUT / "avatar_800.png")


FRAMES = pathlib.Path(__file__).resolve().parent / "frames"


def panel(name, box, size, tint=(120, 20, 30)):
    """Crop a still (clean of watermark/overlay text), scale to panel size, grade it."""
    im = Image.open(FRAMES / name).convert("RGB").crop(box)
    im = im.resize(size, Image.LANCZOS).filter(ImageFilter.GaussianBlur(1.2))
    im = Image.blend(im, Image.new("RGB", size, tint), 0.22)
    return im


def banner():
    W, H = 2048, 1152
    GOLD = (240, 196, 92)
    img = Image.new("RGB", (W, H), (10, 10, 16))
    # movie stills band (crop boxes skip the source channel's logo and overlay text)
    top, bh, pw = 190, 772, W // 4 + 1
    stills = [
        ("still_w1.jpg", (170, 95, 400, 385)),
        ("still_helmet.jpg", (505, 100, 875, 655)),
        ("still_w2.jpg", (200, 95, 470, 385)),
        ("still_w3.jpg", (300, 95, 570, 385)),
    ]
    for i, (n, b) in enumerate(stills):
        img.paste(panel(n, b, (pw, bh)), (i * (W // 4), top))
    # dark vignette + centre shade so the text pops
    shade = Image.new("L", (W, H), 0)
    sd = ImageDraw.Draw(shade)
    sd.rectangle([0, top, W, top + bh], fill=45)
    sd.ellipse([W / 2 - 760, H / 2 - 260, W / 2 + 760, H / 2 + 260], fill=95)
    shade = shade.filter(ImageFilter.GaussianBlur(70))
    img.paste(Image.new("RGB", (W, H), (6, 6, 10)), (0, 0), shade)
    d = ImageDraw.Draw(img)
    # edge fade of the band into the background
    fade = Image.new("L", (W, H), 0)
    fd = ImageDraw.Draw(fade)
    for k in range(120):
        a = int(255 * (1 - k / 120))
        fd.line([(0, top + k), (W, top + k)], fill=a)
        fd.line([(0, top + bh - k), (W, top + bh - k)], fill=a)
    img.paste(Image.new("RGB", (W, H), (10, 10, 16)), (0, 0), fade)
    d = ImageDraw.Draw(img)
    for y in (70, H - 70 - 60):
        d.rectangle([0, y, W, y + 60], fill=(28, 28, 36))
        perforations(d, 10, y + 18, W, 24, 22, (10, 10, 16))
        d.line([(0, y), (W, y)], fill=RED, width=4)
        d.line([(0, y + 60), (W, y + 60)], fill=RED, width=4)
    cx, cy = W // 2, H // 2
    font = ImageFont.truetype(FONT, 168, index=0)
    text = "ネタバレ映画館"
    box = d.textbbox((0, 0), text, font=font)
    w, h = box[2] - box[0], box[3] - box[1]
    tx, ty = cx - w / 2 - box[0], cy - h / 2 - box[1] + 4
    for dx, dy in [(-3, -3), (3, -3), (-3, 3), (3, 3), (0, 6)]:
        d.text((tx + dx, ty + dy), text, font=font, fill=(90, 12, 22))
    d.text((tx, ty), text, font=font, fill=WHITE)
    d.line([(cx - 260, cy + 110), (cx + 260, cy + 110)], fill=GOLD, width=3)
    f2 = ImageFont.truetype(FONT, 46, index=0)
    tag = "結末まで全部見せます。あらすじ＆ラスト完全解説"
    b2 = d.textbbox((0, 0), tag, font=f2)
    for dx, dy in [(-2, 0), (2, 0), (0, 2), (0, -2)]:
        d.text((cx - (b2[2] - b2[0]) / 2 - b2[0] + dx, cy + 122 + dy), tag, font=f2, fill=(0, 0, 0))
    d.text((cx - (b2[2] - b2[0]) / 2 - b2[0], cy + 122), tag, font=f2, fill=GOLD)
    img.save(OUT / "banner_2048x1152.png")
    print("banner ->", OUT / "banner_2048x1152.png")


if __name__ == "__main__":
    avatar()
    banner()
