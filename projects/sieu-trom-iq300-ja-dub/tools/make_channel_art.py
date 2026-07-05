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


def banner():
    W, H = 2048, 1152
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # vertical gradient
    for i in range(H):
        t = i / H
        c = tuple(int(a + (b - a) * t) for a, b in zip((24, 24, 34), (12, 12, 18)))
        d.line([(0, i), (W, i)], fill=c)
    # safe area: 1235x338 centered
    cx, cy = W // 2, H // 2
    # film strips above and below the title
    for y in (cy - 150, cy + 96):
        d.rectangle([cx - 590, y, cx + 590, y + 54], fill=RED)
        perforations(d, cx - 570, y + 15, cx + 570, 24, 22, BG)
    # title
    font = ImageFont.truetype(FONT, 150, index=0)
    text = "ネタバレ映画館"
    box = d.textbbox((0, 0), text, font=font)
    w, h = box[2] - box[0], box[3] - box[1]
    d.text((cx - w / 2 - box[0], cy - h / 2 - box[1] - 6), text,
           font=font, fill=WHITE)
    # tagline inside safe area
    f2 = ImageFont.truetype(FONT, 44, index=0)
    tag = "映画をまるごとネタバレ解説 — 結末まで一気見"
    b2 = d.textbbox((0, 0), tag, font=f2)
    d.text((cx - (b2[2] - b2[0]) / 2, cy + 190), tag, font=f2, fill=GRAY)
    img.save(OUT / "banner_2048x1152.png")
    print("banner ->", OUT / "banner_2048x1152.png")


if __name__ == "__main__":
    avatar()
    banner()
