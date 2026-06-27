#!/usr/bin/env python3
"""
slow_vbee_audio.py
Apply FFmpeg atempo to all 28 Vbee raw MP3 files.

Input:  audio/vbee_raw/
Output: audio/vbee_slow_<NNN>/  (suffix _slow<NNN> appended to filenames)
Creates: <output-dir>/<dir_name>_manifest.json

Usage:
    python tools/audio/slow_vbee_audio.py                          # factor=0.82 (default)
    python tools/audio/slow_vbee_audio.py --factor 0.90            # lighter pace
    python tools/audio/slow_vbee_audio.py --factor 0.90 --dry-run
    python tools/audio/slow_vbee_audio.py --factor 0.90 --segment L008
    python tools/audio/slow_vbee_audio.py --factor 0.90 --output-dir audio/vbee_slow_090

Supported factors: 0.82, 0.90, 0.92 (any value in [0.5, 2.0] works)
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT  = Path(__file__).resolve().parent.parent.parent
AUDIO_IN = PROJECT / "audio" / "vbee_raw"
QA_JSON  = AUDIO_IN / "vbee_full_export_qa.json"

FFMPEG  = Path(r"C:\ffmpeg\ffmpeg-7.1.1-essentials_build\ffmpeg-7.1.1-essentials_build\bin\ffmpeg.exe")
FFPROBE = Path(r"C:\ffmpeg\ffmpeg-7.1.1-essentials_build\ffmpeg-7.1.1-essentials_build\bin\ffprobe.exe")

DEFAULT_FACTOR = 0.82


def factor_tag(factor: float) -> str:
    """0.82 → '082', 0.90 → '090', 0.92 → '092'"""
    return f"{round(factor * 100):03d}"


def probe_duration(path: Path) -> float:
    cmd = [str(FFPROBE), "-v", "quiet",
           "-show_entries", "format=duration",
           "-of", "csv=p=0", str(path)]
    try:
        return float(subprocess.check_output(cmd, text=True).strip())
    except Exception:
        return -1.0


def slow_file(in_path: Path, out_path: Path, factor: float, dry_run: bool) -> bool:
    cmd = [
        str(FFMPEG), "-y",
        "-i", str(in_path),
        "-filter:a", f"atempo={factor}",
        "-codec:a", "libmp3lame",
        "-q:a", "2",
        str(out_path),
    ]
    preview = " ".join(str(c) for c in cmd)
    if len(preview) > 220:
        preview = preview[:220] + " ..."
    print(f"  CMD: {preview}")
    if dry_run:
        print(f"  [DRY] Would write: {out_path.name}")
        return True
    result = subprocess.run([str(c) for c in cmd],
                            capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  [ERROR] ffmpeg exit {result.returncode}")
        if result.stderr:
            print(result.stderr[-600:])
        return False
    return True


def main():
    ap = argparse.ArgumentParser(
        description="Slow Vbee audio by FFmpeg atempo factor"
    )
    ap.add_argument("--factor", type=float, default=DEFAULT_FACTOR,
                    metavar="FLOAT",
                    help=f"atempo speed factor (default {DEFAULT_FACTOR}). "
                         "0.82=slow, 0.90=light, 0.92=very light. Range: 0.5-2.0")
    ap.add_argument("--output-dir", metavar="DIR",
                    help="Output directory (default: auto-derived from factor)")
    ap.add_argument("--dry-run", action="store_true",
                    help="Print commands without executing")
    ap.add_argument("--segment", metavar="LINE_ID",
                    help="Process only this line_id (e.g. L008)")
    args = ap.parse_args()

    factor = args.factor
    if not (0.5 <= factor <= 2.0):
        print(f"[ABORT] --factor {factor} out of valid range [0.5, 2.0]", file=sys.stderr)
        sys.exit(1)

    tag = factor_tag(factor)
    dir_name = f"vbee_slow_{tag}"

    if args.output_dir:
        audio_out = PROJECT / args.output_dir
    else:
        audio_out = PROJECT / "audio" / dir_name

    manifest_out = audio_out / f"{dir_name}_manifest.json"
    out_rel = audio_out.relative_to(PROJECT)

    audio_out.mkdir(parents=True, exist_ok=True)

    inverse = round(1.0 / factor, 2)
    print(f"\n{'='*62}")
    print(f"  Vbee Audio Pace Fix - atempo={factor}  (1/{factor} = {inverse}x longer)")
    print(f"  Input:  {AUDIO_IN}")
    print(f"  Output: {audio_out}")
    if args.dry_run:
        print(f"  MODE:   DRY RUN")
    print(f"{'='*62}\n")

    if not QA_JSON.exists():
        print(f"[ABORT] QA JSON not found: {QA_JSON}", file=sys.stderr)
        sys.exit(1)

    with open(QA_JSON, encoding="utf-8") as f:
        qa = json.load(f)

    segments = qa["segments"]
    total_in_sec = qa["summary"]["total_actual_duration_sec"]
    total_out_expected = round(total_in_sec / factor, 2)

    print(f"[INFO] {len(segments)} segments | "
          f"total_in={total_in_sec:.2f}s | "
          f"expected_out={total_out_expected:.2f}s\n")

    results = []
    ok_count = 0
    skip_count = 0
    fail_count = 0

    for seg in segments:
        line_id  = seg["line_id"]
        if args.segment and line_id != args.segment:
            continue

        filename   = seg["filename"]
        actual_sec = seg["actual_sec"]
        section    = seg.get("section", "")
        delivery   = seg.get("delivery_mode", "")
        sensitive  = seg.get("sensitive_content", False)

        in_path  = AUDIO_IN / filename
        out_name = Path(filename).stem + f"_slow{tag}.mp3"
        out_path = audio_out / out_name

        expected_out = round(actual_sec / factor, 3)

        print(f"[{line_id}] {filename}")
        print(f"  in={actual_sec:.2f}s  expected_out={expected_out:.2f}s  "
              f"section={section}  delivery={delivery}"
              + ("  [SENSITIVE]" if sensitive else ""))

        if not in_path.exists():
            print(f"  [WARN] Input missing: {in_path}")
            results.append({
                "line_id": line_id,
                "filename_in": filename,
                "filename_out": out_name,
                "output_path": f"{out_rel}/{out_name}",
                "status": "input_missing",
                "actual_in_sec": actual_sec,
                "expected_out_sec": expected_out,
                "actual_out_sec": None,
                "speed_factor": factor,
                "section": section,
                "delivery_mode": delivery,
                "sensitive_content": sensitive,
            })
            fail_count += 1
            print()
            continue

        ok = slow_file(in_path, out_path, factor, args.dry_run)

        if ok and not args.dry_run:
            dur_out = probe_duration(out_path)
        elif ok and args.dry_run:
            dur_out = expected_out
        else:
            dur_out = -1.0

        status = "ok" if ok else "failed"
        dur_str = f"{dur_out:.2f}s" if dur_out > 0 else "n/a"
        print(f"  actual_out={dur_str}  status={status}\n")

        results.append({
            "line_id": line_id,
            "filename_in": filename,
            "filename_out": out_name,
            "output_path": f"{out_rel}/{out_name}",
            "status": status,
            "actual_in_sec": actual_sec,
            "expected_out_sec": expected_out,
            "actual_out_sec": round(dur_out, 3) if dur_out > 0 else None,
            "speed_factor": factor,
            "section": section,
            "delivery_mode": delivery,
            "sensitive_content": sensitive,
        })
        if ok:
            ok_count += 1
        else:
            fail_count += 1

    total_out_actual = sum(
        r["actual_out_sec"] for r in results
        if r.get("actual_out_sec") is not None
    )

    manifest = {
        "schema_version": "1.1",
        "project_id": "hashima-island-mystery-ja",
        "document_type": f"{dir_name}_manifest",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "speed_factor": factor,
        "atempo_filter": f"atempo={factor}",
        "input_dir": "audio/vbee_raw/",
        "output_dir": f"{out_rel}/",
        "total_segments": len(results),
        "ok_count": ok_count,
        "fail_count": fail_count,
        "total_in_sec": total_in_sec,
        "total_out_expected_sec": total_out_expected,
        "total_out_actual_sec": round(total_out_actual, 3) if total_out_actual else None,
        "note": (
            f"All 28 narration files slowed by atempo={factor} "
            f"(playback at {round(factor*100)}% speed, {inverse}x longer). "
            f"Duration extended from {total_in_sec:.2f}s to approx {total_out_expected:.2f}s. "
            f"Use {out_rel}/ files with the matching timeline JSON for render."
        ),
        "files": results,
    }

    if not args.dry_run:
        with open(manifest_out, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        print(f"[MANIFEST] Written: {manifest_out}")

    print(f"\n{'='*62}")
    print(f"  DONE: {ok_count} ok  |  {fail_count} failed  |  {skip_count} skipped")
    print(f"  Factor:              {factor}  (atempo={factor})")
    print(f"  Input total:         {total_in_sec:.2f}s")
    print(f"  Expected output:     {total_out_expected:.2f}s")
    if total_out_actual:
        print(f"  Actual output:       {total_out_actual:.2f}s")
    print(f"  Output dir:          {audio_out}")
    print(f"  Next step:  python tools/audio/check_slow_audio_manifest.py "
          f"--audio-dir {out_rel} --factor {factor}")
    print(f"{'='*62}\n")

    if fail_count > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
