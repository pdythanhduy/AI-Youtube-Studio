#!/usr/bin/env python3
"""
Rebrand watermark — remove the source channel logo (static, top-left) and
overlay a text watermark for the Japanese channel.

    python tools/brand_watermark.py --input export/sieu_trom_iq300_ja_dub.mp4 \
        --text "ネタバレ映画館" [--bbox 6,6,300,88] [--cpu]

Output: <input stem>_branded.mp4 next to the input.
"""
import argparse
import pathlib
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")

FONTS = [r"C:\Windows\Fonts\YuGothB.ttc", r"C:\Windows\Fonts\meiryob.ttc",
         r"C:\Windows\Fonts\msgothic.ttc"]


def make_watermark_png(text: str, out_png: pathlib.Path, height_px: int = 54):
    from PIL import Image, ImageDraw, ImageFont
    font = None
    for path in FONTS:
        try:
            font = ImageFont.truetype(path, height_px, index=0)
            break
        except OSError:
            continue
    if font is None:
        raise SystemExit("no Japanese font found")
    stroke = max(2, height_px // 18)
    tmp = Image.new("RGBA", (10, 10))
    box = ImageDraw.Draw(tmp).textbbox((0, 0), text, font=font, stroke_width=stroke)
    pad = stroke + 4
    img = Image.new("RGBA", (box[2] - box[0] + 2 * pad, box[3] - box[1] + 2 * pad),
                    (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.text((pad - box[0], pad - box[1]), text, font=font,
              fill=(255, 255, 255, 150), stroke_width=stroke,
              stroke_fill=(0, 0, 0, 110))
    img.save(out_png)
    print(f"watermark png -> {out_png} ({img.width}x{img.height})")


def render(inp: pathlib.Path, png: pathlib.Path, bbox, use_cpu: bool):
    x, y, w, h = bbox
    out = inp.with_name(inp.stem + "_branded.mp4")
    vcodec = (["-c:v", "libx264", "-crf", "19", "-preset", "veryfast"] if use_cpu
              else ["-c:v", "h264_nvenc", "-cq", "19", "-preset", "p5",
                    "-b:v", "0", "-rc", "vbr"])
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-stats",
           "-i", str(inp), "-i", str(png),
           "-filter_complex",
           f"[0:v]delogo=x={x}:y={y}:w={w}:h={h}[v0];[v0][1:v]overlay=24:18[v]",
           "-map", "[v]", "-map", "0:a", *vcodec,
           "-c:a", "copy", "-movflags", "+faststart", str(out)]
    subprocess.run(cmd, check=True)
    print(f"branded video -> {out}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--text", default="ネタバレ映画館")
    ap.add_argument("--bbox", default="6,6,300,88",
                    help="x,y,w,h of the old watermark to delogo")
    ap.add_argument("--height", type=int, default=54)
    ap.add_argument("--cpu", action="store_true", help="use libx264 instead of NVENC")
    args = ap.parse_args()

    inp = pathlib.Path(args.input).resolve()
    png = inp.parent / "channel_watermark.png"
    make_watermark_png(args.text, png, args.height)
    bbox = [int(v) for v in args.bbox.split(",")]
    render(inp, png, bbox, args.cpu)


if __name__ == "__main__":
    main()
