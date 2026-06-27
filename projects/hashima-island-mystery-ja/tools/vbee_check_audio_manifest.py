#!/usr/bin/env python3
"""
Vbee Audio Manifest Checker — hashima-island-mystery-ja
Verifies exported audio files and writes a QA report.

Usage:
    python tools/vbee_check_audio_manifest.py
    python tools/vbee_check_audio_manifest.py --tolerance 8

Requirements:
    pip install mutagen  (optional — for duration detection)
"""

import json
import sys
import argparse
import pathlib
from datetime import datetime, timezone

# ── Paths ─────────────────────────────────────────────────────────────────────
PROJECT_ROOT   = pathlib.Path(__file__).resolve().parent.parent
SEGMENT_JSON   = PROJECT_ROOT / 'voice' / 'vbee_export' / 'vbee_segmented_script.json'
TIMING_JSON    = PROJECT_ROOT / 'data' / 'timing_plan.json'
MANIFEST_JSON  = PROJECT_ROOT / 'audio' / 'vbee_raw' / 'vbee_export_manifest.json'
AUDIO_DIR      = PROJECT_ROOT / 'audio' / 'vbee_raw'
REPORT_OUT     = PROJECT_ROOT / 'production' / 'vbee_audio_manifest_check_report.md'

# Lines with special timeline placement — flag in report
PLACEMENT_FLAGS = {
    'L008': {'place_at': '2:37', 'note': 'TF-001 — starts in S007 visual, spans cut to S008'},
    'L028': {'place_at': '9:35', 'note': 'TF-002 — must start 5s before S021 to protect Ma beat'},
}

# Sensitive content lines — verify factual tone
SENSITIVE_LINES = {'L013', 'L014', 'L015', 'L016'}

# Default duration tolerance in seconds
DEFAULT_TOLERANCE = 6


# ── Duration detection ────────────────────────────────────────────────────────
def _detect_duration(path: pathlib.Path):
    try:
        ext = path.suffix.lower()
        if ext == '.mp3':
            from mutagen.mp3 import MP3
            return round(MP3(str(path)).info.length, 2)
        if ext == '.wav':
            from mutagen.wave import WAVE
            return round(WAVE(str(path)).info.length, 2)
        if ext in ('.m4a', '.aac'):
            from mutagen.mp4 import MP4
            return round(MP4(str(path)).info.length, 2)
    except ImportError:
        pass
    except Exception:
        pass
    return None


# ── Load data ─────────────────────────────────────────────────────────────────
def _load_json(path: pathlib.Path):
    if not path.exists():
        print(f"[WARNING] File not found: {path}", file=sys.stderr)
        return None
    with path.open(encoding='utf-8') as f:
        return json.load(f)


# ── Check one segment ─────────────────────────────────────────────────────────
def _check_segment(seg: dict, tolerance: float) -> dict:
    """Check a single segment. Returns a result dict."""
    line_id  = seg['line_id']
    filename = seg['export_filename']
    target   = seg.get('duration_target_sec')
    path     = AUDIO_DIR / filename

    result = {
        'line_id':             line_id,
        'scene_id':            seg.get('scene_id', ''),
        'section':             seg.get('section', ''),
        'filename':            filename,
        'expected_start':      seg.get('intended_start_time', '?'),
        'expected_end':        seg.get('intended_end_time', '?'),
        'duration_target_sec': target,
        'duration_actual_sec': None,
        'duration_delta_sec':  None,
        'file_exists':         path.is_file(),
        'file_size_bytes':     path.stat().st_size if path.is_file() else None,
        'sensitive_content':   line_id in SENSITIVE_LINES,
        'placement_flag':      line_id in PLACEMENT_FLAGS,
        'status':              'unknown',
        'flags':               [],
    }

    if not result['file_exists']:
        result['status'] = 'MISSING'
        result['flags'].append('FILE_MISSING')
        return result

    if result['file_size_bytes'] == 0:
        result['status'] = 'EMPTY'
        result['flags'].append('FILE_EMPTY')
        return result

    actual = _detect_duration(path)
    result['duration_actual_sec'] = actual

    if actual is not None and target is not None:
        delta = round(actual - target, 2)
        result['duration_delta_sec'] = delta
        if abs(delta) <= 3:
            result['flags'].append('DURATION_OK')
        elif abs(delta) <= tolerance:
            result['flags'].append('DURATION_WARN')
        else:
            result['flags'].append('DURATION_FAIL')
    elif actual is None:
        result['flags'].append('DURATION_UNKNOWN')

    if line_id in PLACEMENT_FLAGS:
        info = PLACEMENT_FLAGS[line_id]
        result['flags'].append(f"PLACEMENT_{info['place_at'].replace(':','')}")

    if line_id in SENSITIVE_LINES:
        result['flags'].append('SENSITIVE_REVIEW_REQUIRED')

    # Determine overall status
    if 'DURATION_FAIL' in result['flags']:
        result['status'] = 'WARN'
    elif 'DURATION_WARN' in result['flags']:
        result['status'] = 'NOTE'
    else:
        result['status'] = 'OK'

    return result


# ── Build markdown report ─────────────────────────────────────────────────────
def _build_report(segments: list, results: list, tolerance: float, checked_at: str) -> str:
    ok      = sum(1 for r in results if r['status'] == 'OK')
    warn    = sum(1 for r in results if r['status'] in ('WARN', 'NOTE'))
    missing = sum(1 for r in results if r['status'] == 'MISSING')
    empty   = sum(1 for r in results if r['status'] == 'EMPTY')

    lines = []
    lines.append(f"# Vbee Audio Manifest Check Report")
    lines.append(f"## hashima-island-mystery-ja")
    lines.append(f"**Checked at:** {checked_at}  ")
    lines.append(f"**Audio directory:** `audio/vbee_raw/`  ")
    lines.append(f"**Tolerance:** ±{tolerance}s from target duration  ")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"| Status | Count |")
    lines.append(f"|--------|-------|")
    lines.append(f"| ✅ OK | {ok} |")
    lines.append(f"| ⚠️ Warn / Note | {warn} |")
    lines.append(f"| ❌ Missing | {missing} |")
    lines.append(f"| 🚫 Empty file | {empty} |")
    lines.append(f"| **Total** | **{len(results)}** |")
    lines.append("")

    if missing == 0 and empty == 0 and warn == 0:
        lines.append("**All segments present and within duration tolerance. Ready for timeline assembly.**")
    else:
        if missing > 0:
            lines.append(f"⚠️ **{missing} file(s) missing.** Run the export script to generate them.")
        if empty > 0:
            lines.append(f"⚠️ **{empty} file(s) are empty.** Re-export with `--overwrite --segment <line_id>`.")
        if warn > 0:
            lines.append(f"⚠️ **{warn} segment(s) have duration issues.** See details below.")

    lines.append("")
    lines.append("---")
    lines.append("")

    # ── Special timing flags ──────────────────────────────────────────────────
    lines.append("## Critical Timeline Placement Checks")
    lines.append("")
    for r in results:
        if r['placement_flag']:
            lid  = r['line_id']
            info = PLACEMENT_FLAGS[lid]
            exist_str = "✅ Present" if r['file_exists'] else "❌ MISSING"
            dur_str = f"{r['duration_actual_sec']}s" if r['duration_actual_sec'] else "unknown"
            lines.append(f"### {lid} — MUST START AT {info['place_at']}")
            lines.append(f"- {info['note']}")
            lines.append(f"- File: `{r['filename']}`  {exist_str}")
            lines.append(f"- Actual duration: {dur_str}  |  Target: {r['duration_target_sec']}s")
            lines.append(f"- **Editor action:** Place this audio clip at {info['place_at']} in the timeline (not at the visual scene start).")
            lines.append("")

    # ── Ma beat reminder ──────────────────────────────────────────────────────
    lines.append("## Ma Beat Integrity Check")
    lines.append("")
    lines.append("The 40-second Ma beat (L031 / S022 / 10:20-11:00) is **NOT** a Vbee audio file.")
    lines.append("It is editor-created silence. Verify:")
    lines.append("")
    l031_path = AUDIO_DIR / "hashima_L031_act4_03.mp3"
    if l031_path.exists():
        lines.append(f"- ❌ **WARNING: `{l031_path.name}` exists in audio/vbee_raw/**")
        lines.append(f"  This file should NOT exist. The Ma beat must be editor silence, not Vbee audio.")
        lines.append(f"  Delete this file and remove it from the editing timeline.")
    else:
        lines.append(f"- ✅ `hashima_L031_act4_03.mp3` does NOT exist — correct.")
    lines.append(f"- ⬛ At 10:20-11:00 in the timeline: narration track SILENT, music/ocean waves only.")
    lines.append("")
    lines.append("---")
    lines.append("")

    # ── Sensitive content reminder ─────────────────────────────────────────────
    lines.append("## Sensitive Content Lines — Tone Review Required")
    lines.append("")
    lines.append("These segments must be reviewed manually for tone (factual, not dramatic, not horror):")
    lines.append("")
    lines.append("| Line | File | Present | Duration |")
    lines.append("|------|------|---------|----------|")
    for r in results:
        if r['sensitive_content']:
            exist_str = "✅" if r['file_exists'] else "❌ MISSING"
            dur_str = f"{r['duration_actual_sec']}s" if r['duration_actual_sec'] else "unknown"
            lines.append(f"| {r['line_id']} | `{r['filename']}` | {exist_str} | {dur_str} |")
    lines.append("")
    lines.append("> **L014 is the most critical.** If the TTS sounds dramatic, sensational, or horror-like,")
    lines.append("> re-export at lower speed (0.72x) or try a different Vbee voice. FIX-M1 requirement.")
    lines.append("")
    lines.append("---")
    lines.append("")

    # ── Full segment table ────────────────────────────────────────────────────
    lines.append("## All Segments")
    lines.append("")
    lines.append("| # | Line | Section | Start | End | Target | Actual | Delta | File | Status |")
    lines.append("|---|------|---------|-------|-----|--------|--------|-------|------|--------|")

    for r in results:
        target_str = f"{r['duration_target_sec']}s" if r['duration_target_sec'] else "—"
        actual_str = f"{r['duration_actual_sec']}s" if r['duration_actual_sec'] else "—"
        delta_str  = f"{r['duration_delta_sec']:+.1f}s" if r['duration_delta_sec'] is not None else "—"
        exist_icon = "✅" if r['file_exists'] else "❌"
        status_icon = {
            'OK':      '✅',
            'NOTE':    '⚠️',
            'WARN':    '⚠️',
            'MISSING': '❌',
            'EMPTY':   '🚫',
        }.get(r['status'], '?')

        extra = ''
        if r['placement_flag']:
            extra += ' 📍'
        if r['sensitive_content']:
            extra += ' ⚠️'

        lines.append(
            f"| {r['line_id']:5} | {r['section']:7} | "
            f"{r['expected_start']:5} | {r['expected_end']:5} | "
            f"{target_str:6} | {actual_str:6} | {delta_str:7} | "
            f"{exist_icon} | {status_icon}{extra} |"
        )

    lines.append("")
    lines.append("📍 = special timeline placement required  ⚠️ = sensitive content review required")
    lines.append("")
    lines.append("---")
    lines.append("")

    # ── Duration flag details ─────────────────────────────────────────────────
    flagged = [r for r in results if r['status'] in ('WARN', 'NOTE')]
    if flagged:
        lines.append("## Duration Issues — Action Required")
        lines.append("")
        for r in flagged:
            lines.append(f"### {r['line_id']} — {r['filename']}")
            lines.append(f"- Target: {r['duration_target_sec']}s  |  Actual: {r['duration_actual_sec']}s  |  Delta: {r['duration_delta_sec']:+.1f}s")
            if abs(r['duration_delta_sec'] or 0) > tolerance:
                if (r['duration_delta_sec'] or 0) > 0:
                    lines.append(f"- Audio is **too long** by {r['duration_delta_sec']}s. Re-export at higher speed (e.g. +0.05x).")
                else:
                    lines.append(f"- Audio is **too short** by {abs(r['duration_delta_sec'])}s. Re-export at lower speed (e.g. -0.05x).")
                lines.append(f"  Re-export: `python tools/vbee_export_segments.py --segment {r['line_id']} --overwrite`")
            lines.append("")
        lines.append("---")
        lines.append("")

    # ── Missing files ─────────────────────────────────────────────────────────
    miss = [r for r in results if r['status'] == 'MISSING']
    if miss:
        lines.append("## Missing Files")
        lines.append("")
        lines.append("These segments have no audio file. Run the export script:")
        lines.append("")
        for r in miss:
            lines.append(f"- `{r['filename']}` ({r['line_id']})")
        lines.append("")
        lines.append("```")
        lines.append("python tools/vbee_export_segments.py")
        lines.append("```")
        lines.append("")
        lines.append("---")
        lines.append("")

    # ── Next action ───────────────────────────────────────────────────────────
    lines.append("## Next Action")
    lines.append("")
    if missing == 0 and empty == 0 and warn == 0:
        lines.append("✅ **All 28 segments verified. Ready for timeline assembly.**")
        lines.append("")
        lines.append("1. Import all files from `audio/vbee_raw/` into your NLE.")
        lines.append("2. Place clips at timecodes from `data/timing_plan.json`.")
        lines.append("3. Place L008 at 2:37 (not 2:45).")
        lines.append("4. Place L028 at 9:35 (not 9:40).")
        lines.append("5. Insert 40s editor silence at 10:20-11:00 (Ma beat — narration track only).")
        lines.append("6. Listen to L013/L014/L015/L016 in context. Confirm factual tone.")
    else:
        lines.append("Resolve all ❌ and ⚠️ items above, then re-run this checker.")
        lines.append("")
        lines.append("```")
        lines.append("python tools/vbee_check_audio_manifest.py")
        lines.append("```")

    lines.append("")
    lines.append("---")
    lines.append(f"*Generated by tools/vbee_check_audio_manifest.py at {checked_at}*")

    return '\n'.join(lines)


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description='Check Vbee audio manifest for hashima-island-mystery-ja'
    )
    parser.add_argument(
        '--tolerance', type=float, default=DEFAULT_TOLERANCE,
        help=f'Duration tolerance in seconds (default: {DEFAULT_TOLERANCE})'
    )
    args = parser.parse_args()

    checked_at = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')

    # Load segment definitions
    script_data = _load_json(SEGMENT_JSON)
    if not script_data:
        print(f"[ERROR] Cannot load {SEGMENT_JSON}", file=sys.stderr)
        sys.exit(1)

    segments = script_data.get('segments', [])
    print(f"\nVbee Audio Manifest Checker — hashima-island-mystery-ja")
    print(f"Checking {len(segments)} expected segments in {AUDIO_DIR}\n")

    # Check each segment
    results = []
    for seg in segments:
        r = _check_segment(seg, args.tolerance)
        status_icon = {'OK': '✅', 'NOTE': '⚠️ ', 'WARN': '⚠️ ',
                       'MISSING': '❌', 'EMPTY': '🚫'}.get(r['status'], '?')
        dur_str = f"{r['duration_actual_sec']}s" if r['duration_actual_sec'] else 'no dur'
        delta_str = f"  Δ{r['duration_delta_sec']:+.1f}s" if r['duration_delta_sec'] is not None else ''
        flags_str = ' '.join(r['flags'])
        print(f"  {status_icon} {r['line_id']:6} {r['filename']:40} {dur_str:8}{delta_str}  {flags_str}")

    # Summary counts
    ok      = sum(1 for r in results if r['status'] == 'OK')
    warn    = sum(1 for r in results if r['status'] in ('WARN', 'NOTE'))
    missing = sum(1 for r in results if r['status'] == 'MISSING')

    print(f"\n  OK: {ok}  Warn: {warn}  Missing: {missing}  Total: {len(results)}")

    # Write report
    REPORT_OUT.parent.mkdir(parents=True, exist_ok=True)
    report_text = _build_report(segments, results, args.tolerance, checked_at)
    REPORT_OUT.write_text(report_text, encoding='utf-8')
    print(f"\nReport written: {REPORT_OUT}")

    sys.exit(0 if missing == 0 else 1)


if __name__ == '__main__':
    main()
