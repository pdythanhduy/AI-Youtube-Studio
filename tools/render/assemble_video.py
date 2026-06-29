#!/usr/bin/env python3
"""Render/assembly stage: turn a project's TTS audio + beat images into a rough video.

Audio-driven assembly (robust for autopilot): the per-segment Vbee mp3s are the
ground truth for timing, so we concatenate them into one narration track, measure
its real duration, then spread the beat images evenly across that timeline. Each
image becomes a 1920x1080 clip (scaled+cropped) for its share of the time; clips
are concatenated and the narration is muxed on top.

Inputs (produced by earlier asset stages):
  projects/<slug>/assets/audio/seg_NN.mp3   (tts_generate.py)
  projects/<slug>/assets/images/beat_NN.jpg (generate_images.py)
Output:
  projects/<slug>/export/rough/<slug>_rough.mp4

This is a rough auto-cut (no motion-graphic cards / ambience / hand-timed beats —
those are the polished-edit layer). It proves end-to-end render for the autopilot.

Usage:
  python tools/render/assemble_video.py --project <slug>
"""
from __future__ import annotations
import argparse, re, subprocess, sys, tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PROJECTS = REPO / "projects"
W, H, FPS = 1920, 1080, 30


def numkey(p: Path) -> int:
    m = re.search(r"(\d+)", p.stem)
    return int(m.group(1)) if m else 0


def run(cmd: list[str]) -> None:
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"[ffmpeg ERROR] {' '.join(cmd[:6])}...\n{r.stderr[-800:]}")


def duration(path: Path) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=nk=1:nw=1", str(path)], capture_output=True, text=True)
    return float(r.stdout.strip() or 0)


def main() -> int:
    ap = argparse.ArgumentParser(description="Assemble TTS audio + beat images into a rough video")
    ap.add_argument("--project", required=True)
    a = ap.parse_args()
    proj = PROJECTS / a.project
    audio = sorted((proj / "assets" / "audio").glob("seg_*.mp3"), key=numkey)
    images = sorted((proj / "assets" / "images").glob("beat_*.jpg"), key=numkey)
    if not audio:
        sys.exit("[ERROR] no assets/audio/seg_*.mp3 (run tts_generate.py first)")
    if not images:
        sys.exit("[ERROR] no assets/images/beat_*.jpg (run generate_images.py first)")

    work = Path(tempfile.mkdtemp(prefix="assemble_", dir=str(proj)))
    try:
        # 1) concatenate narration audio (re-encode to avoid mp3-frame gaps)
        alist = work / "audio.txt"
        alist.write_text("".join(f"file '{p.resolve().as_posix()}'\n" for p in audio), encoding="utf-8")
        narration = work / "narration.m4a"
        run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(alist),
             "-c:a", "aac", "-b:a", "192k", str(narration)])
        total = duration(narration)
        if total <= 0:
            sys.exit("[ERROR] narration has zero duration")

        # 2) per-image span (even split; last image absorbs rounding)
        n = len(images)
        per = round(total / n, 3)
        print(f"narration {total:.1f}s | {len(audio)} audio segs | {n} images | ~{per:.1f}s/image")

        # 3) one 1920x1080 clip per image
        clips = []
        for i, img in enumerate(images):
            d = round(total - per * (n - 1), 3) if i == n - 1 else per
            clip = work / f"clip_{i:03d}.mp4"
            run(["ffmpeg", "-y", "-loop", "1", "-i", str(img), "-t", f"{d}",
                 "-r", str(FPS),
                 "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,"
                        f"crop={W}:{H},format=yuv420p",
                 "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", str(clip)])
            clips.append(clip)
            print(f"  clip {i+1}/{n}: {img.name} ({d:.1f}s)")

        # 4) concat clips, then mux narration
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
