#!/usr/bin/env python3
"""
verify_rough_timeline.py
Verifies rough video output against timeline requirements.

Checks:
  1. Output file exists
  2. Total duration matches timeline meta (±3s tolerance)
  3. Video stream present (1920x1080)
  4. Audio stream present
  5. Ma beat window is narration-free (derived from timeline meta)
  6. All audio files in timeline exist on disk
  7. No audio end_sec exceeds total video duration
  8. Scene count matches timeline [V1 only: L008/L028 anchor checks]

Writes: production/{video_stem}_verification_report.md

Usage:
    python tools/render/verify_rough_timeline.py [--video PATH] [--timeline FILE]

Examples:
    # V1 (default)
    python tools/render/verify_rough_timeline.py

    # V3 tight
    python tools/render/verify_rough_timeline.py \\
        --timeline data/timeline_assembly_plan_v3_tight.json \\
        --video export/rough/hashima_rough_v3_tight.mp4
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# ─── Paths ────────────────────────────────────────────────────────────────────

PROJECT = Path(__file__).resolve().parent.parent.parent

FFPROBE          = Path(r"C:\ffmpeg\ffmpeg-7.1.1-essentials_build\ffmpeg-7.1.1-essentials_build\bin\ffprobe.exe")
DEFAULT_TIMELINE = PROJECT / "data" / "timeline_assembly_plan.json"
DEFAULT_VIDEO    = PROJECT / "export" / "rough" / "hashima_rough_v1.mp4"
CACHE_DIR        = PROJECT / "timeline" / "render_cache"

# ─── Timing constants (overridden from timeline meta when available) ───────────

TOTAL_DURATION_TARGET = 720.0
TOTAL_DURATION_TOL    = 3.0

MA_BEAT_START = 620.0
MA_BEAT_END   = 660.0

# V1-specific anchors (only checked for V1 timeline)
L008_TARGET   = 157.0
L028_TARGET   = 575.0
ANCHOR_TOL    = 2.0

# ─── Load timeline + derive constants ────────────────────────────────────────

def load_timeline(tl_path: Path) -> dict:
    with open(tl_path, encoding="utf-8") as f:
        plan = json.load(f)
    return plan


def derive_constants(plan: dict) -> None:
    """Read timing constants from timeline meta if present."""
    global TOTAL_DURATION_TARGET, MA_BEAT_START, MA_BEAT_END
    meta = plan.get("meta", {})
    if "total_video_duration_sec" in meta:
        TOTAL_DURATION_TARGET = float(meta["total_video_duration_sec"])
    if "ma_beat_start_sec" in meta:
        MA_BEAT_START = float(meta["ma_beat_start_sec"])
    if "ma_beat_end_sec" in meta:
        MA_BEAT_END = float(meta["ma_beat_end_sec"])


def is_v1_timeline(plan: dict) -> bool:
    """True if this is the original V1/V2 timeline with fixed L008/L028 anchors."""
    doc_type = plan.get("document_type", "")
    variant  = plan.get("variant", "")
    return ("v3" not in doc_type.lower() and "v3" not in variant.lower()
            and "tight" not in doc_type.lower() and "tight" not in variant.lower())

# ─── ffprobe helpers ──────────────────────────────────────────────────────────

def probe(path: Path, entries: str, of: str = "json") -> dict:
    cmd = [
        str(FFPROBE), "-v", "quiet",
        "-show_entries", entries,
        "-of", of,
        str(path),
    ]
    out = subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL)
    if of == "json":
        return json.loads(out)
    return {"raw": out.strip()}


def get_format_info(path: Path) -> dict:
    return probe(path, "format=duration,size,bit_rate")


def get_streams(path: Path) -> list:
    d = probe(path, "stream=index,codec_type,codec_name,width,height,sample_rate,channels")
    return d.get("streams", [])


# ─── Check functions ──────────────────────────────────────────────────────────

def check_file_exists(video: Path) -> tuple[bool, str]:
    ok = video.exists()
    return ok, ("PASS" if ok else f"FAIL - file not found: {video}")


def check_duration(video: Path) -> tuple[bool, str, float]:
    try:
        d = get_format_info(video)
        dur = float(d["format"]["duration"])
        delta = abs(dur - TOTAL_DURATION_TARGET)
        ok = delta <= TOTAL_DURATION_TOL
        mm, ss = divmod(int(dur), 60)
        msg = (f"PASS - {dur:.2f}s  ({mm}:{ss:02d})  "
               f"delta={delta:.2f}s vs target {TOTAL_DURATION_TARGET:.0f}s")
        if not ok:
            msg = (f"FAIL - {dur:.2f}s  delta={delta:.2f}s "
                   f"exceeds tolerance +-{TOTAL_DURATION_TOL}s "
                   f"(target {TOTAL_DURATION_TARGET:.0f}s)")
        return ok, msg, dur
    except Exception as e:
        return False, f"FAIL - probe error: {e}", -1.0


def check_video_stream(video: Path) -> tuple[bool, str]:
    try:
        streams = get_streams(video)
        v = [s for s in streams if s.get("codec_type") == "video"]
        if not v:
            return False, "FAIL - no video stream found"
        s = v[0]
        w, h = s.get("width", 0), s.get("height", 0)
        codec = s.get("codec_name", "?")
        ok = (w == 1920 and h == 1080)
        msg = f"PASS - {codec} {w}x{h}" if ok else f"FAIL - {codec} {w}x{h} (expected 1920x1080)"
        return ok, msg
    except Exception as e:
        return False, f"FAIL - {e}"


def check_audio_stream(video: Path) -> tuple[bool, str]:
    try:
        streams = get_streams(video)
        a = [s for s in streams if s.get("codec_type") == "audio"]
        if not a:
            return False, "FAIL - no audio stream found"
        s = a[0]
        codec = s.get("codec_name", "?")
        sr    = s.get("sample_rate", "?")
        ch    = s.get("channels", "?")
        return True, f"PASS - {codec}  {sr}Hz  {ch}ch"
    except Exception as e:
        return False, f"FAIL - {e}"


def check_ma_beat(plan: dict) -> tuple[bool, str]:
    """
    Verify no narration audio overlaps the Ma beat window.
    Uses audio_start_sec / audio_end_sec from timeline JSON directly.
    Works for both V1 (vbee_raw) and V3 (vbee_slow_090) timelines.
    """
    try:
        violations = []
        for scene in plan["scenes"]:
            files     = scene.get("audio_files", [])
            starts    = scene.get("audio_start_sec", [])
            ends      = scene.get("audio_end_sec", [])

            for fname, start, end in zip(files, starts, ends):
                if not fname or end is None:
                    continue
                s = float(start)
                e = float(end)
                if e > MA_BEAT_START and s < MA_BEAT_END:
                    violations.append(
                        f"{Path(fname).name}: {s:.1f}s-{e:.1f}s "
                        f"overlaps Ma beat [{MA_BEAT_START:.0f}-{MA_BEAT_END:.0f}]"
                    )

        ma_start_tc = f"{int(MA_BEAT_START)//60}:{int(MA_BEAT_START)%60:02d}"
        ma_end_tc   = f"{int(MA_BEAT_END)//60}:{int(MA_BEAT_END)%60:02d}"
        dur_s       = MA_BEAT_END - MA_BEAT_START

        if violations:
            return False, (f"FAIL - {len(violations)} narration track(s) overlap Ma beat:\n"
                           + "\n".join(f"       {v}" for v in violations))
        return True, (f"PASS - Ma beat [{MA_BEAT_START:.0f}-{MA_BEAT_END:.0f}s] "
                      f"({ma_start_tc}-{ma_end_tc}, {dur_s:.0f}s) is narration-free")
    except Exception as e:
        return False, f"WARN - Ma beat check error: {e}"


def check_audio_files(plan: dict) -> tuple[bool, str]:
    """Verify all audio files listed in the timeline exist on disk."""
    missing = []
    seen: set[str] = set()
    for scene in plan["scenes"]:
        for fname in scene.get("audio_files", []):
            if not fname or fname in seen:
                continue
            seen.add(fname)
            p = PROJECT / fname
            if not p.exists():
                missing.append(fname)

    total = len(seen)
    if missing:
        return False, (f"FAIL - {len(missing)}/{total} audio files missing:\n"
                       + "\n".join(f"       {f}" for f in missing[:10])
                       + (f"\n       ... ({len(missing)-10} more)" if len(missing) > 10 else ""))
    return True, f"PASS - {total} audio files present on disk"


def check_no_overflow(plan: dict) -> tuple[bool, str]:
    """Verify no audio end_sec exceeds total video duration."""
    overflows = []
    for scene in plan["scenes"]:
        files = scene.get("audio_files", [])
        ends  = scene.get("audio_end_sec", [])
        for fname, end in zip(files, ends):
            if not fname or end is None:
                continue
            e = float(end)
            if e > TOTAL_DURATION_TARGET + 1.0:
                overflows.append(
                    f"{Path(fname).name} ends at {e:.1f}s "
                    f"(video total {TOTAL_DURATION_TARGET:.0f}s)"
                )

    if overflows:
        return False, (f"FAIL - {len(overflows)} audio track(s) extend past video end:\n"
                       + "\n".join(f"       {v}" for v in overflows))
    return True, f"PASS - no audio exceeds {TOTAL_DURATION_TARGET:.0f}s"


def check_scene_count(plan: dict, expected: int = 25) -> tuple[bool, str]:
    n = len(plan["scenes"])
    ok = (n == expected)
    return ok, f"{'PASS' if ok else 'FAIL'} - {n} scenes (expected {expected})"


def check_timeline_anchors(plan: dict) -> list[tuple[bool, str]]:
    """V1/V2 only: verify L008 at 157s and L028 at 575s."""
    results = []
    # Build audio-placement lookup
    placements: dict[str, float] = {}
    for scene in plan["scenes"]:
        for fname, start in zip(
            scene.get("audio_files", []),
            scene.get("audio_start_sec", []),
        ):
            if fname:
                key = Path(fname).name
                if key not in placements or float(start) < placements[key]:
                    placements[key] = float(start)

    for label, target, filename in [
        ("L008 anchor (2:37)", L008_TARGET, "hashima_L008_act1_04.mp3"),
        ("L028 anchor (9:35)", L028_TARGET, "hashima_L028_act4_02.mp3"),
    ]:
        actual = placements.get(filename)
        if actual is None:
            results.append((False, f"{label} - audio file not found in timeline"))
        else:
            delta = abs(actual - target)
            ok = delta <= ANCHOR_TOL
            mm, ss = divmod(int(actual), 60)
            if ok:
                results.append((True, f"{label} - PASS  placed at {actual:.1f}s ({mm}:{ss:02d})  "
                                       f"target {target:.0f}s  delta={delta:.1f}s"))
            else:
                results.append((False, f"{label} - FAIL  placed at {actual:.1f}s "
                                        f"(expected ~{target:.0f}s +-{ANCHOR_TOL}s)"))
    return results


# ─── Report writer ────────────────────────────────────────────────────────────

def write_report(video: Path, plan: dict, results: dict, report_path: Path) -> None:
    passed = sum(1 for ok, _ in results.values() if ok)
    total  = len(results)
    now    = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    variant = plan.get("meta", {}).get("document_type", "unknown")
    dur_tc  = plan.get("meta", {}).get("total_video_timecode", f"{int(TOTAL_DURATION_TARGET)//60}:{int(TOTAL_DURATION_TARGET)%60:02d}")
    ma_tc_s = f"{int(MA_BEAT_START)//60}:{int(MA_BEAT_START)%60:02d}"
    ma_tc_e = f"{int(MA_BEAT_END)//60}:{int(MA_BEAT_END)%60:02d}"

    lines = [
        f"# Rough Video Verification Report",
        f"## {variant}",
        "",
        f"**Generated:** {now}",
        f"**Video file:** `{video}`",
        f"**Target duration:** {TOTAL_DURATION_TARGET:.0f}s ({dur_tc})",
        f"**Ma beat:** {MA_BEAT_START:.0f}-{MA_BEAT_END:.0f}s ({ma_tc_s}-{ma_tc_e})",
        f"**Status:** {'ALL CHECKS PASSED' if passed == total else f'{passed}/{total} checks passed'}",
        "",
        "---",
        "",
        "## Check Results",
        "",
        "| Check | Result | Detail |",
        "|-------|--------|--------|",
    ]

    for key, (ok, detail) in results.items():
        icon = "PASS" if ok else "FAIL"
        lines.append(f"| {key} | {icon} | {detail} |")

    lines += [
        "",
        "---",
        "",
        "## Ma Beat",
        "",
        f"| Field | Value |",
        f"|-------|-------|",
        f"| Window | {MA_BEAT_START:.0f}-{MA_BEAT_END:.0f}s ({ma_tc_s}-{ma_tc_e}) |",
        f"| Duration | {MA_BEAT_END - MA_BEAT_START:.0f}s |",
        f"| Status | {results.get('ma_beat', (False,'N/A'))[1]} |",
        "",
        "---",
        "",
        "## Human Review Checklist",
        "",
        "- [ ] Duration matches expected in playback",
        "- [ ] Ma beat window is silent (music/waves only, no narration)",
        "- [ ] Sensitive scenes S011a/S011b: factual tone, no horror inflection",
        "- [ ] S010 / S019 crop differentiation: reads as different from primary scene",
        "- [ ] IMG009 (S011a): human producer review before fine cut",
        "- [ ] IMG004 (S005): 参考映像 caption overlay added",
        "- [ ] Overall pacing: feels engaged and documentary-paced",
        "",
    ]

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\n[REPORT] Written: {report_path}")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description="Verify rough video output")
    ap.add_argument("--video", type=Path, default=DEFAULT_VIDEO,
                    help=f"Path to video file (default: {DEFAULT_VIDEO})")
    ap.add_argument("--timeline", type=Path, default=DEFAULT_TIMELINE,
                    help=f"Timeline JSON to verify against (default: {DEFAULT_TIMELINE})")
    args = ap.parse_args()

    video    = args.video
    tl_path  = PROJECT / args.timeline if not args.timeline.is_absolute() else args.timeline

    # Load timeline + override global constants from meta
    plan = load_timeline(tl_path)
    derive_constants(plan)
    v1_mode = is_v1_timeline(plan)

    # Derive report path from video stem
    report_path = PROJECT / "production" / f"{video.stem}_verification_report.md"

    results: dict[str, tuple[bool, str]] = {}

    print(f"\n{'='*60}")
    print(f"  Rough Video - Verification")
    print(f"  Video:    {video}")
    print(f"  Timeline: {tl_path.name}")
    print(f"  Target:   {TOTAL_DURATION_TARGET:.0f}s  "
          f"Ma beat: {MA_BEAT_START:.0f}-{MA_BEAT_END:.0f}s")
    print(f"  Report:   {report_path.name}")
    print(f"{'='*60}\n")

    check_n = 0

    # 1. File exists
    check_n += 1
    ok, msg = check_file_exists(video)
    results["1. File exists"] = (ok, msg)
    print(f"[{check_n}] File exists          : {msg}")
    if not ok:
        print("\n[ABORT] Output file not found. Run render_rough_video.py first.")
        write_report(video, plan, results, report_path)
        sys.exit(1)

    # 2. Duration
    check_n += 1
    ok, msg, _ = check_duration(video)
    results["2. Duration"] = (ok, msg)
    print(f"[{check_n}] Duration             : {msg}")

    # 3. Video stream
    check_n += 1
    ok, msg = check_video_stream(video)
    results["3. Video stream"] = (ok, msg)
    print(f"[{check_n}] Video stream         : {msg}")

    # 4. Audio stream
    check_n += 1
    ok, msg = check_audio_stream(video)
    results["4. Audio stream"] = (ok, msg)
    print(f"[{check_n}] Audio stream         : {msg}")

    # 5. Ma beat narration-free
    check_n += 1
    ok, msg = check_ma_beat(plan)
    results["5. Ma beat clear"] = (ok, msg)
    print(f"[{check_n}] Ma beat clear        : {msg}")

    # 6. Audio files exist on disk
    check_n += 1
    ok, msg = check_audio_files(plan)
    results["6. Audio files present"] = (ok, msg)
    print(f"[{check_n}] Audio files present  : {msg}")

    # 7. No audio overflow
    check_n += 1
    ok, msg = check_no_overflow(plan)
    results["7. No audio overflow"] = (ok, msg)
    print(f"[{check_n}] No audio overflow    : {msg}")

    # 8. Scene count
    check_n += 1
    ok, msg = check_scene_count(plan, expected=25)
    results["8. Scene count"] = (ok, msg)
    print(f"[{check_n}] Scene count          : {msg}")

    # 9-10. V1 anchor checks (L008 @ 157s, L028 @ 575s) — V1/V2 only
    if v1_mode:
        anchor_results = check_timeline_anchors(plan)
        l008_ok, l008_msg = anchor_results[0] if len(anchor_results) > 0 else (False, "N/A")
        l028_ok, l028_msg = anchor_results[1] if len(anchor_results) > 1 else (False, "N/A")
        check_n += 1
        results["9. L008 anchor (2:37)"] = (l008_ok, l008_msg)
        print(f"[{check_n}] L008 anchor (2:37)  : {l008_msg}")
        check_n += 1
        results["10. L028 anchor (9:35)"] = (l028_ok, l028_msg)
        print(f"[{check_n}] L028 anchor (9:35)  : {l028_msg}")
    else:
        print(f"    [INFO] V3+ timeline: L008/L028 anchor checks skipped (no fixed anchors)")

    # ── Summary ───────────────────────────────────────────────────────────────
    passed = sum(1 for ok, _ in results.values() if ok)
    total  = len(results)
    print(f"\n{'='*60}")
    print(f"  Result: {passed}/{total} checks passed")
    if passed == total:
        print("  STATUS: READY FOR HUMAN REVIEW")
    else:
        print("  STATUS: ISSUES FOUND - see report")
    print(f"{'='*60}\n")

    write_report(video, plan, results, report_path)
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
