#!/usr/bin/env python3
"""Render/assembly stage: TTS audio + beat images -> a motion video (Hashima-style).

Audio-driven: concatenate the per-segment Vbee mp3s into one narration track, measure
its real duration, spread the beat images across that timeline. Each image becomes a
1920x1080 clip with a slow **Ken Burns** zoom + fade in/out (so it is not static); the
first clip carries a fading **title card** overlay. Clips are concatenated and the
narration muxed on top.

Inputs:  projects/<slug>/assets/audio/seg_NN.mp3, assets/images/beat_NN.jpg
Output:  projects/<slug>/export/rough/<slug>_rough.mp4

Still a rough auto-cut (no motion-graphic data cards / ambience bed yet — those remain
the polish backlog), but now with image motion + title, much closer to the hand-made bar.

Usage: python tools/render/assemble_video.py --project <slug>
"""
from __future__ import annotations
import argparse, json, re, shutil, subprocess, sys, tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PROJECTS = REPO / "projects"
W, H, FPS = 1920, 1080, 30


def numkey(p: Path) -> int:
    m = re.search(r"(\d+)", p.stem)
    return int(m.group(1)) if m else 0


def run(cmd: list[str], cwd: str | None = None) -> None:
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
    if r.returncode != 0:
        sys.exit(f"[ffmpeg ERROR] {' '.join(cmd[:8])}...\n{r.stderr[-900:]}")


def duration(path: Path) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=nk=1:nw=1", str(path)], capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


def serif_font() -> str | None:
    """Cross-platform JP serif font file (Windows VF or Linux Noto Serif CJK)."""
    cands = [r"C:\Windows\Fonts\NotoSerifJP-VF.ttf",
             "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc",
             "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc"]
    for c in cands:
        if Path(c).exists():
            return c
    return None


def title_text(proj: Path) -> str:
    inp = proj / "input.json"
    if inp.exists():
        try:
            return json.loads(inp.read_text(encoding="utf-8")).get("topic", proj.name)
        except Exception:
            pass
    return proj.name


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="Assemble TTS audio + beat images into a motion video")
    ap.add_argument("--project", required=True)
    ap.add_argument("--no-motion", action="store_true", help="disable Ken Burns (static fallback)")
    a = ap.parse_args()
    proj = PROJECTS / a.project
    audio = sorted((proj / "assets" / "audio").glob("seg_*.mp3"), key=numkey)
    images = sorted((proj / "assets" / "images").glob("beat_*.jpg"), key=numkey) \
        + sorted((proj / "assets" / "images").glob("beat_*.png"), key=numkey)
    if not audio:
        sys.exit("[ERROR] no assets/audio/seg_*.mp3 (run tts_generate.py first)")
    if not images:
        sys.exit("[ERROR] no assets/images/beat_*.jpg (run generate_images.py first)")

    work = Path(tempfile.mkdtemp(prefix="assemble_", dir=str(proj)))
    try:
        # 1) narration
        alist = work / "audio.txt"
        alist.write_text("".join(f"file '{p.resolve().as_posix()}'\n" for p in audio), encoding="utf-8")
        narration = work / "narration.m4a"
        run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(alist),
             "-c:a", "aac", "-b:a", "192k", str(narration)])
        total = duration(narration)
        if total <= 0:
            sys.exit("[ERROR] narration has zero duration")

        n = len(images)
        per = round(total / n, 3)
        print(f"narration {total:.1f}s | {len(audio)} audio segs | {n} images | ~{per:.1f}s/image")

        # title-card font (relative name in work/ to dodge Windows colon escaping)
        font = serif_font()
        if font:
            shutil.copy(font, work / "f.ttf")
            (work / "title.txt").write_text(title_text(proj), encoding="utf-8")

        clips = []
        for i, img in enumerate(images):
            d = round(total - per * (n - 1), 3) if i == n - 1 else per
            frames = max(2, round(d * FPS))
            clip = work / f"clip_{i:03d}.mp4"
            if a.no_motion:
                vf = (f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},format=yuv420p")
            else:
                # Ken Burns: slow zoom-in within an upscaled frame, plus fade in/out
                vf = (f"scale=2400:-1,"
                      f"zoompan=z='min(max(pzoom,1)+0.0008,1.16)':d=1:"
                      f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps={FPS},"
                      f"trim=duration={d},"
                      f"fade=t=in:st=0:d=0.7,fade=t=out:st={max(0.1, d-0.7):.2f}:d=0.7,"
                      f"format=yuv420p")
            if i == 0 and font:  # title overlay on the opening clip, fades out ~6s
                vf += (f",drawtext=fontfile=f.ttf:textfile=title.txt:fontcolor=white:fontsize=70:"
                       f"x=(w-text_w)/2:y=h*0.70:box=1:boxcolor=black@0.45:boxborderw=26:"
                       f"alpha='if(lt(t,4.5),1,max(0,(6-t)/1.5))'")
            run(["ffmpeg", "-y", "-loop", "1", "-i", str(img.resolve()), "-t", f"{d}", "-r", str(FPS),
                 "-vf", vf, "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", str(clip)],
                cwd=str(work))
            clips.append(clip)
            print(f"  clip {i+1}/{n}: {img.name} ({d:.1f}s){' +title' if i == 0 and font else ''}")

        clist = work / "clips.txt"
        clist.write_text("".join(f"file '{c.resolve().as_posix()}'\n" for c in clips), encoding="utf-8")
        video_raw = work / "video_raw.mp4"
        run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(clist), "-c", "copy", str(video_raw)])

        out = proj / "export" / "rough" / f"{a.project}_rough.mp4"
        out.parent.mkdir(parents=True, exist_ok=True)
        run(["ffmpeg", "-y", "-i", str(video_raw), "-i", str(narration),
             "-c:v", "copy", "-c:a", "aac", "-shortest", "-movflags", "+faststart", str(out)])
        print(f"\nRendered: {out.relative_to(proj)} ({duration(out):.1f}s, {out.stat().st_size/1048576:.1f} MB)")
        return 0
    finally:
        for f in work.glob("*"):
            f.unlink(missing_ok=True)
        work.rmdir()


if __name__ == "__main__":
    raise SystemExit(main())
