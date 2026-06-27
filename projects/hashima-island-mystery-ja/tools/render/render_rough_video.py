#!/usr/bin/env python3
"""
render_rough_video.py
Rough video assembly pipeline for hashima-island-mystery-ja.

Reads data/timeline_assembly_plan.json and renders a 1920x1080 draft video
from approved image assets and Vbee narration audio.

Default output: export/rough/hashima_rough_v1.mp4
Override:       --output export/rough/hashima_rough_v3_tight.mp4

Usage:
    python tools/render/render_rough_video.py [options]

Options:
    --skip-existing     Skip scene clips that already exist in render cache
    --concat-only       Skip scene rendering; only run concat + audio mix + mux
    --no-motion         Use static (no zoom/pan) - fastest render, ~10 min
    --fps N             Override output FPS (default 24)
    --dry-run           Print ffmpeg commands without executing them
    --timeline FILE     Override timeline JSON (default: data/timeline_assembly_plan.json)
    --output FILE       Override output file path (default: export/rough/hashima_rough_v1.mp4)
                        Does NOT overwrite v1 unless you explicitly point --output at v1.

Estimated render time (Intel i7 / AMD Ryzen 7, ultrafast preset):
    With motion (zoompan):  ~30-60 min
    --no-motion flag:       ~8-15 min
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

# ─── Paths ────────────────────────────────────────────────────────────────────

PROJECT = Path(__file__).resolve().parent.parent.parent
DATA_DIR     = PROJECT / "data"
AUDIO_DIR    = PROJECT / "audio" / "vbee_raw"
ASSETS_DIR   = PROJECT / "assets"
EXPORT_DIR   = PROJECT / "export" / "rough"
CACHE_DIR    = PROJECT / "timeline" / "render_cache"

FFMPEG  = Path(r"C:\ffmpeg\ffmpeg-7.1.1-essentials_build\ffmpeg-7.1.1-essentials_build\bin\ffmpeg.exe")
FFPROBE = Path(r"C:\ffmpeg\ffmpeg-7.1.1-essentials_build\ffmpeg-7.1.1-essentials_build\bin\ffprobe.exe")

TIMELINE_JSON = DATA_DIR / "timeline_assembly_plan.json"
OUTPUT_FILE   = EXPORT_DIR / "hashima_rough_v1.mp4"

# ─── Video config (rough draft) ───────────────────────────────────────────────

W, H           = 1920, 1080
TOTAL_DURATION = 720.0          # overridden from timeline meta if present
V_PRESET       = "ultrafast"    # fast encode; switch to "medium" for fine cut
V_CRF          = 28             # coarser than final (23), fine for review

# ─── Motion graphics placeholder text ────────────────────────────────────────

MG_TEXT = {
    "MG001": "[TITLE CARD] Hashima / Gunkanjima",
    "MG002": "[ANIMATED MAP] Nagasaki Port to Hashima approx 15-18km",
    "MG003": "[DATA GRAPHIC] Disputed labor statistics 1939-1945",
    "MG004": "[DATE OVERLAY] 1974-01-15 Island abandonment date",
}

# ─── Helpers ──────────────────────────────────────────────────────────────────

def run(cmd: list, dry_run: bool = False, label: str = "") -> int:
    cmd_strs = [str(c) for c in cmd]
    preview = " ".join(cmd_strs)
    if len(preview) > 300:
        preview = preview[:300] + " ..."
    if label:
        print(f"\n[{label}] {preview}")
    else:
        print(f"\n[CMD] {preview}")
    if dry_run:
        return 0
    result = subprocess.run(cmd_strs)
    if result.returncode != 0:
        print(f"[ERROR] Command failed (code {result.returncode})", file=sys.stderr)
        sys.exit(result.returncode)
    return result.returncode


def resolve(rel: str) -> Path:
    p = Path(rel)
    return p if p.is_absolute() else PROJECT / p


# ─── Video filter builders ────────────────────────────────────────────────────

def vf_motion(motion: str, duration: float, fps: int, no_motion: bool) -> str:
    """Return the ffmpeg -vf filter chain for a given motion type."""
    fill = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}"
    total_frames = max(1, int(duration * fps))

    if no_motion or not motion or motion in ("static", "animated_inherent"):
        return fill

    if motion in ("slow_zoom_in", "ken_burns_zoom_in"):
        zp = (f"zoompan="
              f"z='1+0.1*on/{total_frames}':"
              f"x='iw/2-(iw/zoom/2)':"
              f"y='ih/2-(ih/zoom/2)':"
              f"d=1:s={W}x{H}:fps={fps}")
        return f"{fill},{zp}"

    if motion == "slow_zoom_out":
        zp = (f"zoompan="
              f"z='max(1.0,1.1-0.1*on/{total_frames})':"
              f"x='iw/2-(iw/zoom/2)':"
              f"y='ih/2-(ih/zoom/2)':"
              f"d=1:s={W}x{H}:fps={fps}")
        return f"{fill},{zp}"

    if motion == "very_slow_pan_right":
        pan = int(W * 0.06)           # ~115 px
        pw  = W + pan
        return (f"scale={pw}:{H}:force_original_aspect_ratio=increase,crop={pw}:{H},"
                f"crop={W}:{H}:x='min({pan},t/{duration:.4f}*{pan})':y=0")

    if motion == "slow_pan_right":
        pan = int(W * 0.12)           # ~230 px
        pw  = W + pan
        return (f"scale={pw}:{H}:force_original_aspect_ratio=increase,crop={pw}:{H},"
                f"crop={W}:{H}:x='min({pan},t/{duration:.4f}*{pan})':y=0")

    if motion == "slow_pan_left":
        pan = int(W * 0.12)
        pw  = W + pan
        return (f"scale={pw}:{H}:force_original_aspect_ratio=increase,crop={pw}:{H},"
                f"crop={W}:{H}:x='max(0,{pan}-t/{duration:.4f}*{pan})':y=0")

    # Fallback for any unknown motion value
    return fill


def vf_color(scene: dict) -> str:
    """Return optional eq filter for scene-level color treatment."""
    sid = scene.get("scene_id", "")
    iid = scene.get("image_id", "")

    # S010: IMG003 dual-use - slightly cooler + desaturated (vine/concrete read)
    if sid == "S010":
        return "eq=saturation=0.80:gamma_r=0.95:gamma_b=1.02"

    # S019: IMG010 dual-use - warm shift for concrete/rust read
    if sid == "S019":
        return "eq=saturation=0.88:gamma_r=1.08:gamma_b=0.92"

    # IMG002 (S002): heavy desaturation + darken (post-process approximation)
    if iid == "IMG002":
        return "eq=saturation=0.35:brightness=-0.07"

    # IMG008 (S009): reduce warm sepia
    if iid == "IMG008":
        return "eq=saturation=0.72"

    # IMG016 (S020): desaturate sky slightly, preserve warm dusk
    if iid == "IMG016":
        return "eq=saturation=0.83"

    return ""


def build_vf(scene: dict, fps: int, no_motion: bool) -> str:
    """Assemble the complete -vf filter string for a scene."""
    sid      = scene.get("scene_id", "")
    motion   = scene.get("visual_motion", "static")
    duration = float(scene["scene_duration_sec"])

    parts = [vf_motion(motion, duration, fps, no_motion)]

    color = vf_color(scene)
    if color:
        parts.append(color)

    # Fade in from black on first scene
    if sid == "S001":
        parts.append("fade=in:st=0:d=1.0")

    # Ma beat scene: dissolve in + out
    if sid == "S022":
        parts.append("fade=in:st=0:d=1.0")
        parts.append(f"fade=out:st={duration - 1.5:.2f}:d=1.5")

    # Fade out to black on last scene
    if sid == "S024":
        parts.append(f"fade=out:st={max(0.0, duration - 2.0):.2f}:d=2.0")

    return ",".join(parts)


# ─── Scene rendering ──────────────────────────────────────────────────────────

def render_image_scene(scene: dict, out: Path, fps: int, no_motion: bool, dry_run: bool):
    img = resolve(scene["image_file"])
    if not img.exists():
        print(f"[WARN] Image not found: {img} - skipping")
        return False

    duration = float(scene["scene_duration_sec"])
    vf       = build_vf(scene, fps, no_motion)

    cmd = [
        str(FFMPEG), "-y",
        "-loop", "1", "-framerate", str(fps),
        "-i", str(img),
        "-vf", vf,
        "-t", f"{duration:.4f}",
        "-r", str(fps),
        "-c:v", "libx264",
        "-preset", V_PRESET,
        "-crf", str(V_CRF),
        "-pix_fmt", "yuv420p",
        "-an",
        str(out),
    ]
    run(cmd, dry_run=dry_run, label=f"SCENE {scene['scene_id']}")
    return True


def render_mg_scene(scene: dict, out: Path, fps: int, dry_run: bool):
    mg_id    = scene.get("mg_id", "MG???")
    duration = float(scene["scene_duration_sec"])
    text     = MG_TEXT.get(mg_id, f"[{mg_id}]").replace("'", "").replace(":", " -")

    # Fade in + out for all MG cards
    fade_vf = f"fade=in:st=0:d=0.5,fade=out:st={max(0.0, duration - 0.5):.2f}:d=0.5"

    cmd = [
        str(FFMPEG), "-y",
        "-f", "lavfi",
        "-i", f"color=c=0x0a0a18:s={W}x{H}:r={fps}",
        "-vf", (f"drawtext=text='{text}':fontcolor=white:fontsize=38:"
                f"x=(w-text_w)/2:y=(h-text_h)/2:box=1:"
                f"boxcolor=black@0.65:boxborderw=14,{fade_vf}"),
        "-t", f"{duration:.4f}",
        "-c:v", "libx264",
        "-preset", V_PRESET,
        "-crf", str(V_CRF),
        "-pix_fmt", "yuv420p",
        "-an",
        str(out),
    ]
    run(cmd, dry_run=dry_run, label=f"SCENE {scene['scene_id']} (MG)")
    return True


# ─── Audio helpers ────────────────────────────────────────────────────────────

def collect_audio_placements(scenes: list) -> list[tuple[Path, float]]:
    """
    Return sorted [(path, start_sec), ...], deduplicated by filename.
    Files that span scene cuts appear in multiple scene entries - keep
    the earliest start_sec occurrence.
    """
    seen: dict[str, tuple[Path, float]] = {}

    for scene in scenes:
        files  = scene.get("audio_files", [])
        starts = scene.get("audio_start_sec", [])
        for f, s in zip(files, starts):
            if not f:
                continue
            fname = Path(f).name
            path  = resolve(f)
            if fname not in seen or s < seen[fname][1]:
                seen[fname] = (path, float(s))

    return sorted(seen.values(), key=lambda x: x[1])


def build_audio_mix(placements: list[tuple[Path, float]],
                    out: Path, dry_run: bool):
    """Mix all narration files into a single {TOTAL_DURATION}s WAV track."""
    n = len(placements)
    if n == 0:
        print("[WARN] No audio placements - skipping audio mix")
        return

    print(f"\n[AUDIO] Mixing {n} narration files into {TOTAL_DURATION:.0f}s track ...")

    # Write filter_complex to a script file to avoid CLI length limits on Windows
    filter_lines = []
    for i, (_, start_sec) in enumerate(placements):
        delay_ms = int(start_sec * 1000)
        filter_lines.append(f"[{i}]adelay={delay_ms}|{delay_ms}[a{i}]")

    mix_in = "".join(f"[a{i}]" for i in range(n))
    filter_lines.append(
        f"{mix_in}amix=inputs={n}:duration=longest:normalize=0,"
        f"apad=whole_dur={int(TOTAL_DURATION)}[aout]"
    )

    script = CACHE_DIR / "audio_filter.txt"
    if not dry_run:
        # ffmpeg filter_complex requires ";" as chain separator (newlines alone cause parse error)
        script.write_text(";\n".join(filter_lines), encoding="utf-8")
    else:
        print(f"[DRY] Would write filter script: {script}")

    cmd = [str(FFMPEG), "-y"]
    for path, _ in placements:
        cmd.extend(["-i", str(path)])
    cmd.extend([
        "-/filter_complex", str(script),
        "-map", "[aout]",
        "-t", str(TOTAL_DURATION),
        "-ar", "44100",
        "-ac", "2",
        "-c:a", "pcm_s16le",
        str(out),
    ])
    run(cmd, dry_run=dry_run, label="AUDIO MIX")


# ─── Verification helpers ─────────────────────────────────────────────────────

def probe_duration(path: Path) -> float:
    """Return duration in seconds from ffprobe; -1.0 on failure."""
    cmd = [
        str(FFPROBE), "-v", "quiet",
        "-show_entries", "format=duration",
        "-of", "csv=p=0",
        str(path),
    ]
    try:
        out = subprocess.check_output(cmd, text=True).strip()
        return float(out)
    except Exception:
        return -1.0


# ─── Asset verification ───────────────────────────────────────────────────────

def verify_assets(scenes: list,
                  placements: list[tuple[Path, float]]) -> tuple[list, list]:
    missing_img = []
    missing_aud = []

    for scene in scenes:
        img_file = scene.get("image_file")
        if img_file and scene.get("image_source") != "MOTION_GRAPHICS":
            p = resolve(img_file)
            if not p.exists():
                missing_img.append(str(p))

    for path, _ in placements:
        if not path.exists():
            missing_aud.append(str(path))

    return missing_img, missing_aud


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(
        description="Render hashima-island-mystery-ja rough video v1"
    )
    ap.add_argument("--skip-existing", action="store_true",
                    help="Skip scene clips that already exist in render cache")
    ap.add_argument("--concat-only", action="store_true",
                    help="Skip scene rendering, only run concat + mux")
    ap.add_argument("--no-motion", action="store_true",
                    help="Static only - skips zoompan, fastest render")
    ap.add_argument("--fps", type=int, default=24,
                    help="Output frame rate (default 24; use 12 for extra speed)")
    ap.add_argument("--dry-run", action="store_true",
                    help="Print commands without executing")
    ap.add_argument("--timeline", metavar="FILE",
                    help="Override timeline JSON (default: data/timeline_assembly_plan.json)")
    ap.add_argument("--output", metavar="FILE",
                    help="Override output file path. Default: export/rough/hashima_rough_v1.mp4. "
                         "Does NOT overwrite v1 unless you explicitly point here.")
    args = ap.parse_args()

    global TIMELINE_JSON, OUTPUT_FILE, TOTAL_DURATION
    if args.timeline:
        TIMELINE_JSON = PROJECT / args.timeline
    if args.output:
        OUTPUT_FILE = PROJECT / args.output
        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    fps = args.fps
    tl_label = Path(TIMELINE_JSON).stem
    print(f"\n{'='*60}")
    print(f"  hashima-island-mystery-ja - Rough Assembly")
    print(f"  Timeline: {tl_label}")
    print(f"  Output:   {OUTPUT_FILE}")
    print(f"  FPS={fps}  motion={'OFF' if args.no_motion else 'ON'}  "
          f"preset={V_PRESET}  crf={V_CRF}")
    print(f"{'='*60}")

    # Ensure directories exist
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    # ── Load timeline ─────────────────────────────────────────────────────────
    print(f"\n[LOAD] {TIMELINE_JSON}")
    with open(TIMELINE_JSON, encoding="utf-8") as f:
        plan = json.load(f)

    scenes = plan["scenes"]
    total_scenes = len(scenes)

    # Read duration from timeline meta if present (overrides compiled-in default)
    meta_dur = plan.get("meta", {}).get("total_video_duration_sec")
    if meta_dur is not None:
        TOTAL_DURATION = float(meta_dur)

    print(f"[INFO] {total_scenes} scenes  |  {TOTAL_DURATION:.0f}s total ({int(TOTAL_DURATION)//60}:{int(TOTAL_DURATION)%60:02d})")

    # ── Collect audio placements ──────────────────────────────────────────────
    placements = collect_audio_placements(scenes)
    print(f"[INFO] {len(placements)} unique narration audio tracks")

    # ── Verify assets ─────────────────────────────────────────────────────────
    missing_img, missing_aud = verify_assets(scenes, placements)

    if missing_img:
        print(f"\n[WARN] Missing image files ({len(missing_img)}):")
        for m in missing_img: print(f"       {m}")
    else:
        img_count = sum(1 for s in scenes if s.get("image_file"))
        print(f"[OK]   All {img_count} image assets verified")

    if missing_aud:
        print(f"\n[WARN] Missing audio files ({len(missing_aud)}):")
        for m in missing_aud: print(f"       {m}")
    else:
        print(f"[OK]   All {len(placements)} audio assets verified")

    if missing_img or missing_aud:
        print("\n[ABORT] Missing assets. Resolve before rendering.")
        sys.exit(1)

    # ── Render scene clips ────────────────────────────────────────────────────
    clip_paths: list[Path] = []

    if not args.concat_only:
        print(f"\n[RENDER] Rendering {total_scenes} scene clips to {CACHE_DIR} ...")
        zoom_scenes  = sum(1 for s in scenes
                           if s.get("visual_motion") in
                           ("slow_zoom_in", "slow_zoom_out", "ken_burns_zoom_in"))
        print(f"[INFO]   {zoom_scenes} zoom scenes (zoompan filter - slower)")

        for idx, scene in enumerate(scenes, 1):
            sid  = scene["scene_id"]
            clip = CACHE_DIR / f"{sid.lower()}.mp4"
            clip_paths.append(clip)

            tc   = scene.get("timecode_start", "?:??")
            dur  = scene.get("scene_duration_sec", "?")
            src  = scene.get("image_source", "")
            mot  = scene.get("visual_motion", "static")
            print(f"\n  [{idx:02d}/{total_scenes}] {sid}  {tc}  {dur}s  "
                  f"src={src}  motion={mot}")

            if args.skip_existing and clip.exists():
                print(f"       [SKIP] {clip.name} already exists")
                continue

            if src == "MOTION_GRAPHICS":
                render_mg_scene(scene, clip, fps, dry_run=args.dry_run)
            elif scene.get("image_file"):
                render_image_scene(scene, clip, fps, args.no_motion,
                                   dry_run=args.dry_run)
            else:
                print(f"       [WARN] No image for {sid} - black placeholder")
                blk = [
                    str(FFMPEG), "-y", "-f", "lavfi",
                    "-i", f"color=c=black:s={W}x{H}:r={fps}",
                    "-t", str(scene["scene_duration_sec"]),
                    "-c:v", "libx264", "-preset", V_PRESET,
                    "-crf", str(V_CRF), "-pix_fmt", "yuv420p", "-an",
                    str(clip),
                ]
                run(blk, dry_run=args.dry_run, label=f"SCENE {sid} (black)")
    else:
        for scene in scenes:
            clip_paths.append(CACHE_DIR / f"{scene['scene_id'].lower()}.mp4")

    # ── Verify all scene clips exist (warn; don't abort) ──────────────────────
    missing_clips = [p for p in clip_paths if not p.exists() and not args.dry_run]
    if missing_clips:
        print(f"\n[WARN] {len(missing_clips)} scene clip(s) not found "
              f"(render may have failed):")
        for p in missing_clips:
            print(f"       {p.name}")

    # ── Concatenate scenes ────────────────────────────────────────────────────
    concat_list = CACHE_DIR / "concat.txt"
    if not args.dry_run:
        with open(concat_list, "w", encoding="utf-8") as f:
            for p in clip_paths:
                f.write(f"file '{p.as_posix()}'\n")
    else:
        print(f"\n[DRY] Would write concat list: {concat_list}")

    raw_video = CACHE_DIR / "video_raw.mp4"
    print(f"\n[CONCAT] Concatenating {len(clip_paths)} clips ...")
    run([
        str(FFMPEG), "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-c:v", "copy",
        str(raw_video),
    ], dry_run=args.dry_run, label="CONCAT")

    # ── Audio mix ─────────────────────────────────────────────────────────────
    audio_mix = CACHE_DIR / "audio_mix.wav"
    build_audio_mix(placements, audio_mix, dry_run=args.dry_run)

    # ── Final mux ─────────────────────────────────────────────────────────────
    print(f"\n[MUX] Final mux → {OUTPUT_FILE}")
    run([
        str(FFMPEG), "-y",
        "-i", str(raw_video),
        "-i", str(audio_mix),
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        str(OUTPUT_FILE),
    ], dry_run=args.dry_run, label="FINAL MUX")

    # ── Summary ───────────────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    if not args.dry_run and OUTPUT_FILE.exists():
        size_mb = OUTPUT_FILE.stat().st_size / 1_048_576
        dur_probe = probe_duration(OUTPUT_FILE)
        print(f"  OUTPUT: {OUTPUT_FILE}")
        print(f"  SIZE:   {size_mb:.1f} MB")
        print(f"  DUR:    {dur_probe:.2f}s  (target {TOTAL_DURATION:.0f}s)")
        tl_arg = f" --timeline {args.timeline}" if args.timeline else ""
        vid_arg = f" --video {OUTPUT_FILE}" if args.output else ""
        print(f"\n  NEXT: python tools/render/verify_rough_timeline.py{tl_arg}{vid_arg}")
    else:
        print(f"  DRY RUN complete. Remove --dry-run to render.")
        print(f"  Expected output: {OUTPUT_FILE}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
