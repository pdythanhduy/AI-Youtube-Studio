#!/usr/bin/env python3
"""
check_slow_audio_manifest.py
Verify slowed audio files exist and have correct durations.
Reads: <audio-dir>/<dir_name>_manifest.json
Writes: production/<dir_name>_manifest_check_report.md

Usage:
    python tools/audio/check_slow_audio_manifest.py
    python tools/audio/check_slow_audio_manifest.py --audio-dir audio/vbee_slow_090 --factor 0.90
    python tools/audio/check_slow_audio_manifest.py --audio-dir audio/vbee_slow_082 --factor 0.82
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

PROJECT    = Path(__file__).resolve().parent.parent.parent
QA_JSON    = PROJECT / "audio" / "vbee_raw" / "vbee_full_export_qa.json"
PRODUCTION = PROJECT / "production"

FFPROBE = Path(r"C:\ffmpeg\ffmpeg-7.1.1-essentials_build\ffmpeg-7.1.1-essentials_build\bin\ffprobe.exe")

EXPECTED_TOTAL_IN = 345.12
DURATION_TOL_PCT  = 0.05    # 5% tolerance per file
DEFAULT_AUDIO_DIR = "audio/vbee_slow_082"
DEFAULT_FACTOR    = 0.82


def probe_duration(path: Path) -> float:
    cmd = [str(FFPROBE), "-v", "quiet",
           "-show_entries", "format=duration",
           "-of", "csv=p=0", str(path)]
    try:
        return float(subprocess.check_output(cmd, text=True).strip())
    except Exception:
        return -1.0


def main():
    ap = argparse.ArgumentParser(
        description="Check slowed Vbee audio manifest"
    )
    ap.add_argument("--audio-dir", default=DEFAULT_AUDIO_DIR, metavar="DIR",
                    help=f"Slowed audio directory (default: {DEFAULT_AUDIO_DIR})")
    ap.add_argument("--factor", type=float, default=DEFAULT_FACTOR, metavar="FLOAT",
                    help=f"Speed factor used to produce files (default: {DEFAULT_FACTOR})")
    args = ap.parse_args()

    factor         = args.factor
    audio_slow     = PROJECT / args.audio_dir
    dir_name       = audio_slow.name
    manifest_in    = audio_slow / f"{dir_name}_manifest.json"
    report_out     = PRODUCTION / f"{dir_name}_manifest_check_report.md"
    expected_total = round(EXPECTED_TOTAL_IN / factor, 2)

    print(f"\n{'='*60}")
    print(f"  Vbee Slow Audio Manifest Check")
    print(f"  Dir:      {audio_slow}")
    print(f"  Factor:   {factor}")
    print(f"  Manifest: {manifest_in.name}")
    print(f"{'='*60}\n")

    if not manifest_in.exists():
        print(f"[ABORT] Manifest not found: {manifest_in}", file=sys.stderr)
        print(f"  Run: python tools/audio/slow_vbee_audio.py --factor {factor}", file=sys.stderr)
        sys.exit(1)

    with open(manifest_in, encoding="utf-8") as f:
        manifest = json.load(f)

    files      = manifest["files"]
    n_expected = manifest.get("total_segments", len(files))

    check_results = []
    missing       = []
    abnormal_dur  = []
    total_out_dur = 0.0

    for entry in files:
        line_id      = entry["line_id"]
        out_name     = entry["filename_out"]
        out_path     = audio_slow / out_name
        expected_in  = entry["actual_in_sec"]
        expected_out = entry["expected_out_sec"]

        exists = out_path.exists()
        if not exists:
            actual_out = None
            missing.append(line_id)
            status = "MISSING"
        else:
            actual_out = probe_duration(out_path)
            total_out_dur += actual_out

            tol = expected_out * DURATION_TOL_PCT
            if abs(actual_out - expected_out) > tol:
                abnormal_dur.append({
                    "line_id": line_id,
                    "expected_out": expected_out,
                    "actual_out": actual_out,
                    "delta": round(actual_out - expected_out, 3),
                })
                status = "DURATION_FLAG"
            else:
                status = "OK"

        print(f"[{line_id}] {out_name}")
        if exists:
            print(f"  exists=YES  in={expected_in:.2f}s  "
                  f"exp_out={expected_out:.2f}s  "
                  f"act_out={actual_out:.2f}s  status={status}")
        else:
            print(f"  exists=NO  status=MISSING")

        check_results.append({
            "line_id": line_id,
            "filename_out": out_name,
            "exists": exists,
            "actual_in_sec": expected_in,
            "expected_out_sec": expected_out,
            "actual_out_sec": round(actual_out, 3) if actual_out else None,
            "status": status,
        })

    n_ok      = sum(1 for r in check_results if r["status"] == "OK")
    n_missing = len(missing)
    n_abnorm  = len(abnormal_dur)
    total_delta = round(total_out_dur - expected_total, 2)

    print(f"\n[SUMMARY]")
    print(f"  Factor:            {factor}  (atempo={factor})")
    print(f"  Files expected:    {n_expected}")
    print(f"  Files found OK:    {n_ok}")
    print(f"  Files MISSING:     {n_missing}")
    print(f"  Duration anomalies:{n_abnorm}")
    print(f"  Original total:    {EXPECTED_TOTAL_IN:.2f}s")
    print(f"  Expected slowed:   {expected_total:.2f}s")
    print(f"  Actual slowed:     {total_out_dur:.2f}s")
    print(f"  Delta vs expected: {total_delta:+.2f}s")

    overall = "PASS" if n_missing == 0 and n_abnorm == 0 else "FAIL"
    print(f"  STATUS: {overall}")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    pct = round(factor * 100)
    inverse = round(1.0 / factor, 2)
    lines = [
        f"# {dir_name} Manifest Check Report",
        "",
        f"**Stage:** Voice Pace Fix  ",
        f"**Date:** {now}  ",
        f"**Speed factor:** {factor} (atempo={factor}, {pct}% speed, {inverse}x longer)  ",
        f"**Audio dir:** `{args.audio_dir}`  ",
        f"**Status:** {overall}",
        "",
        "---",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Speed factor | {factor} (atempo={factor}) |",
        f"| Files expected | {n_expected} |",
        f"| Files found (OK) | {n_ok} |",
        f"| Files MISSING | {n_missing} |",
        f"| Duration anomalies | {n_abnorm} |",
        f"| Original total duration | {EXPECTED_TOTAL_IN:.2f}s |",
        f"| Expected slowed duration | {expected_total:.2f}s |",
        f"| Actual slowed duration | {total_out_dur:.2f}s |",
        f"| Delta vs expected | {total_delta:+.2f}s |",
        "",
        "---",
        "",
    ]

    if missing:
        lines += [
            "## Missing Files",
            "",
            "| Line ID | Filename |",
            "|---------|---------|",
        ]
        for r in check_results:
            if r["status"] == "MISSING":
                lines.append(f"| {r['line_id']} | {r['filename_out']} |")
        lines += [
            "",
            f"**Action:** Re-run `python tools/audio/slow_vbee_audio.py --factor {factor}`",
            "",
        ]

    if abnormal_dur:
        lines += [
            "## Duration Anomalies (>5% from expected)",
            "",
            "| Line ID | Expected | Actual | Delta |",
            "|---------|----------|--------|-------|",
        ]
        for a in abnormal_dur:
            lines.append(
                f"| {a['line_id']} | {a['expected_out']:.2f}s | "
                f"{a['actual_out']:.2f}s | {a['delta']:+.3f}s |"
            )
        lines.append("")

    lines += [
        "## File-by-File Results",
        "",
        "| Line | In (s) | Exp Out (s) | Act Out (s) | Status |",
        "|------|--------|-------------|-------------|--------|",
    ]
    for r in check_results:
        act = f"{r['actual_out_sec']:.2f}" if r["actual_out_sec"] else "n/a"
        lines.append(
            f"| {r['line_id']} | {r['actual_in_sec']:.2f} | "
            f"{r['expected_out_sec']:.2f} | {act} | {r['status']} |"
        )

    tl_suffix = dir_name.replace("vbee_slow_", "")
    lines += [
        "",
        "---",
        "",
        "## Next Steps",
        "",
        "If all files are present and durations are OK:",
        "",
        f"1. Use `data/timeline_assembly_plan_v2_{tl_suffix}.json` for render",
        f"2. Audio source: `{args.audio_dir}/`",
        f"3. Render: `python tools/render/render_rough_video.py "
        f"--timeline data/timeline_assembly_plan_v2_{tl_suffix}.json --concat-only`",
        "",
    ]

    report_out.write_text("\n".join(lines), encoding="utf-8")
    print(f"\n[REPORT] Written: {report_out}")
    print(f"{'='*60}\n")

    if overall == "FAIL":
        sys.exit(1)


if __name__ == "__main__":
    main()
