#!/usr/bin/env python3
"""Render a 1080x1920 vertical news reel (Facebook Reels / TikTok / Shorts) from SCENES.

Pure PIL + ffmpeg, no external assets or API keys: dark animated news background, a red
"TIN NÓNG" bar, text that slides/fades in per scene, and a progress bar. Silent by design —
add music / voice-over in CapCut (voice text: script/voice_script.txt).

Usage: python tools/render_reel.py            -> export/reel_1080x1920.mp4
"""
from __future__ import annotations
import math, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "export" / "reel_1080x1920.mp4"
W, H, FPS = 1080, 1920, 30
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

RED, YELLOW, WHITE, GREY = (220, 30, 40), (255, 210, 0), (255, 255, 255), (170, 178, 190)

# (seconds, kicker, headline, body)  — headline in yellow, body in white
SCENES = [
    (5.0, "CHIBA · NHẬT BẢN", "NGHI LỘ ĐỀ THI\nBẰNG LÁI\nTIẾNG VIỆT?", "Thí sinh nói: \"Tìm bằng ChatGPT\""),
    (5.5, "13/10 · SAU GIỜ THI", "CHỤP BẢNG ĐEN\nBẰNG ĐIỆN THOẠI", "Một phụ nữ quốc tịch Việt Nam\n(29 tuổi) bị giám thị chú ý"),
    (5.5, "GIÁM THỊ KIỂM TRA", "TRONG MÁY CÓ\nĐỀ THI TIẾNG VIỆT", "Đề lý thuyết bằng lái\nxe máy loại thường"),
    (5.5, "THEO CẢNH SÁT", "TRANG 1 – 4\nĐÃ ĐƯỢC ĐÁNH DẤU", "Nghi đã có đề bị lộ ra ngoài\ntừ trước khi thi"),
    (5.0, "LỜI KHAI", "\"TÌM BẰNG\nCHATGPT RỒI\nMANG ĐẾN\"", ""),
    (6.0, "HẬU QUẢ", "TẠM DỪNG THI\nBẰNG TIẾNG VIỆT", "Cho đến khi soạn xong\nbộ đề mới"),
    (6.0, "BẠN NGHĨ SAO?", "BÌNH LUẬN\nBÊN DƯỚI", "Vụ việc đang được điều tra\nNguồn: Fuji TV / Yahoo! News"),
]

# If make_audio.py has run, stretch each scene to fit its voice line.
TIMING = ROOT / "export" / "audio" / "timing.json"
if TIMING.exists():
    import json
    _durs = json.loads(TIMING.read_text())["scene_seconds"]
    SCENES = [(d, *s[1:]) for d, s in zip(_durs, SCENES)]

_fonts: dict[tuple[str, int], ImageFont.FreeTypeFont] = {}


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    key = (path, size)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(path, size)
    return _fonts[key]


def ease(x: float) -> float:
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


def background(t: float) -> Image.Image:
    """Dark navy gradient with a slowly drifting grid and a red glow."""
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    for y in range(0, H, 4):
        k = y / H
        d.rectangle([0, y, W, y + 4], fill=(int(8 + 10 * k), int(12 + 14 * k), int(28 + 30 * k)))
    off = int(t * 25) % 90
    for x in range(-90, W + 90, 90):
        d.line([(x + off, 0), (x + off, H)], fill=(25, 35, 62), width=1)
    for y in range(-90, H + 90, 90):
        d.line([(0, y + off), (W, y + off)], fill=(25, 35, 62), width=1)
    glow = Image.new("RGB", (W, H), (0, 0, 0))
    gd = ImageDraw.Draw(glow)
    r = 520 + 40 * math.sin(t * 1.3)
    cx, cy = W // 2, int(H * 0.42)
    for i in range(12, 0, -1):
        rr = r * i / 12
        gd.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=(int(70 * (1 - i / 12)) + 6, 4, 10))
    return Image.blend(img, glow, 0.35)


SAFE_X = 110
SAFE_W = W - 2 * SAFE_X


def fit(d: ImageDraw.ImageDraw, text: str, path: str, size: int, max_w: int) -> ImageFont.FreeTypeFont:
    """Largest font <= size whose widest line fits max_w."""
    f = font(path, size)
    while max(d.textlength(l, font=f) for l in text.split("\n")) > max_w and size > 24:
        size -= 2
        f = font(path, size)
    return f


def draw_center(d: ImageDraw.ImageDraw, text: str, y: int, fnt, fill, alpha: float, spacing=18) -> int:
    lines = text.split("\n")
    for ln in lines:
        w = d.textlength(ln, font=fnt)
        x = (W - w) / 2
        col = tuple(int(c * alpha) for c in fill)
        d.text((x + 4, y + 4), ln, font=fnt, fill=(0, 0, 0))  # drop shadow
        d.text((x, y), ln, font=fnt, fill=col)
        y += fnt.size + spacing
    return y


def frame(t: float, total: float) -> Image.Image:
    acc = 0.0
    for idx, (dur, kicker, head, body) in enumerate(SCENES):
        if t < acc + dur or idx == len(SCENES) - 1:
            lt = t - acc
            break
        acc += dur
    img = background(t)
    d = ImageDraw.Draw(img)

    # Everything sits inside SAFE (x 110..970, y 330..1590): survives the 4:5 feed crop,
    # player zoom-to-fill, and the Reels UI overlays at top/bottom.
    sx0, sx1 = SAFE_X, W - SAFE_X
    bar_w = 740
    bx = (W - bar_w) // 2
    d.rounded_rectangle([bx, 340, bx + bar_w, 430], radius=14, fill=(15, 18, 30))
    d.rounded_rectangle([bx, 340, bx + 300, 430], radius=14, fill=RED)
    d.text((bx + 32, 360), "TIN NÓNG", font=font(BOLD, 46), fill=WHITE)
    d.text((bx + 330, 364), "NHẬT BẢN 24H", font=font(BOLD, 40), fill=YELLOW)

    a1, a2, a3 = ease(lt / 0.5), ease((lt - 0.3) / 0.6), ease((lt - 0.9) / 0.6)
    fade_out = ease((dur - lt) / 0.35) if idx < len(SCENES) - 1 else 1.0

    # Kicker pill
    kf = fit(d, kicker, BOLD, 42, SAFE_W - 80)
    kw = d.textlength(kicker, font=kf)
    kx = (W - kw) / 2
    ky = 540 - int(40 * (1 - a1))
    d.rounded_rectangle([kx - 30, ky - 14, kx + kw + 30, ky + kf.size + 22], radius=40,
                        fill=tuple(int(c * a1 * fade_out) for c in RED))
    d.text((kx, ky), kicker, font=kf, fill=tuple(int(255 * a1 * fade_out) for _ in range(3)))

    hf = fit(d, head, BOLD, 100, SAFE_W)
    y = draw_center(d, head, 670 + int(60 * (1 - a2)), hf, YELLOW, a2 * fade_out)

    if body:
        bf = fit(d, body, REG, 48, SAFE_W)
        draw_center(d, body, y + 40 + int(40 * (1 - a3)), bf, WHITE, a3 * fade_out, spacing=14)

    # Bottom: disclaimer + progress bar
    df = font(REG, 32)
    note = "Thông tin đang được cảnh sát điều tra"
    d.text(((W - d.textlength(note, font=df)) / 2, 1480), note, font=df, fill=GREY)
    d.rectangle([sx0, 1545, sx1, 1555], fill=(40, 48, 70))
    d.rectangle([sx0, 1545, sx0 + int((sx1 - sx0) * t / total), 1555], fill=RED)
    return img


def main() -> None:
    total = sum(s[0] for s in SCENES)
    n = int(total * FPS)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
           "-movflags", "+faststart", str(OUT)]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(n):
        p.stdin.write(frame(i / FPS, total).tobytes())
        if i % 150 == 0:
            print(f"frame {i}/{n}", file=sys.stderr)
    p.stdin.close()
    sys.exit(p.wait())


if __name__ == "__main__":
    main()
