#!/usr/bin/env python3
"""
Rebrand for dao-hoang-tom-hum-ca-map-ja-dub:
  1. cover the burned-in Vietnamese title bar (black, y=0..98) and draw a
     Japanese title in the same spot
  2. delogo the source channel watermark (@SinhTonRV, top-left under the bar)
  3. overlay the Japanese channel watermark in its place

    python tools/brand_watermark.py --input export/dao_hoang_tom_hum_ca_map_ja_dub.mp4 \
        [--title "無人島サバイバル挑戦"] [--text "ネタバレ映画館"] [--cpu]

Output: <input stem>_branded.mp4 next to the input.
"""
import argparse
import pathlib
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")

FONTS = [r"C:\Windows\Fonts\YuGothB.ttc", r"C:\Windows\Fonts\meiryob.ttc",
         r"C:\Windows\Fonts\msgothic.ttc"]

BAR_H = 98                    # burned-in title bar height at 1080p
OLD_WM = (55, 132, 250, 56)   # x, y, w, h of @SinhTonRV


def load_font(height_px):
    from PIL import ImageFont
    for path in FONTS:
        try:
            return ImageFont.truetype(path, height_px, index=0)
        except OSError:
            continue
    raise SystemExit("no Japanese font found")


def text_png(text, out_png, height_px, fill, stroke_fill, stroke_div=18):
    from PIL import Image, ImageDraw
    font = load_font(height_px)
    stroke = max(2, height_px // stroke_div)
    tmp = Image.new("RGBA", (10, 10))
    box = ImageDraw.Draw(tmp).textbbox((0, 0), text, font=font, stroke_width=stroke)
    pad = stroke + 4
    img = Image.new("RGBA", (box[2] - box[0] + 2 * pad, box[3] - box[1] + 2 * pad),
                    (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.text((pad - box[0], pad - box[1]), text, font=font, fill=fill,
              stroke_width=stroke, stroke_fill=stroke_fill)
    img.save(out_png)
    print(f"png -> {out_png} ({img.width}x{img.height})")
    return img.width, img.height


def render(inp, title_png, wm_png, use_cpu):
    x, y, w, h = OLD_WM
    out = inp.with_name(inp.stem + "_branded.mp4")
    vcodec = (["-c:v", "libx264", "-crf", "19", "-preset", "veryfast"] if use_cpu
              else ["-c:v", "h264_nvenc", "-cq", "19", "-preset", "p5",
                    "-b:v", "0", "-rc", "vbr"])
    fc = (
        f"[0:v]delogo=x={x}:y={y}:w={w}:h={h},"
        f"drawbox=x=0:y=0:w=iw:h={BAR_H}:color=black:t=fill[v0];"
        f"[v0][1:v]overlay=(main_w-overlay_w)/2:({BAR_H}-overlay_h)/2[v1];"
        f"[v1][2:v]overlay={x}:{y}[v]"
    )
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-stats",
           "-i", str(inp), "-i", str(title_png), "-i", str(wm_png),
           "-filter_complex", fc,
           "-map", "[v]", "-map", "0:a", *vcodec,
           "-c:a", "copy", "-movflags", "+faststart", str(out)]
    subprocess.run(cmd, check=True)
    print(f"branded video -> {out}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--title", default="無人島サバイバル挑戦")
    ap.add_argument("--text", default="ネタバレ映画館")
    ap.add_argument("--cpu", action="store_true")
    args = ap.parse_args()

    inp = pathlib.Path(args.input).resolve()
    title_png = inp.parent / "ja_title_bar.png"
    wm_png = inp.parent / "channel_watermark.png"
    # banner title: bold yellow with dark outline, like the source style
    text_png(args.title, title_png, 62, (255, 205, 20, 255), (20, 20, 20, 255),
             stroke_div=14)
    # channel watermark: subtle white
    text_png(args.text, wm_png, 42, (255, 255, 255, 150), (0, 0, 0, 110))
    render(inp, title_png, wm_png, args.cpu)


if __name__ == "__main__":
    main()
