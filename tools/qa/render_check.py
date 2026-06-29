#!/usr/bin/env python3
"""QA: rendered assets integrity.

Checks: TTS audio segments exist + decode + non-zero duration; the rough video
exists and decodes cleanly (full ffmpeg decode, no errors); if a publish package is
requested, a thumbnail exists. Deterministic only (no LLM needed).
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (load_env, project_dir, result, worst,  # noqa: E402
                     ffprobe_duration, ffmpeg_decode_ok)


def run(project_id: str, use_llm: bool = False, publish: bool = False) -> dict:
    proj = project_dir(project_id)
    findings, statuses, details = [], [], {}

    # audio
    audio = sorted((proj / "assets" / "audio").glob("seg_*.mp3"))
    if not audio:
        statuses.append("fail")
        findings.append("no TTS audio in assets/audio/")
    else:
        bad = [a.name for a in audio if ffprobe_duration(a) <= 0]
        total = round(sum(ffprobe_duration(a) for a in audio), 1)
        details.update(audio_segments=len(audio), audio_total_sec=total, audio_zero_duration=bad)
        if bad:
            statuses.append("fail"); findings.append(f"audio with zero/invalid duration: {bad}")
        elif total < 3:
            statuses.append("warn"); findings.append(f"total narration very short ({total}s)")
        else:
            statuses.append("pass")

    # video
    vids = sorted((proj / "export" / "rough").glob("*_rough.mp4"))
    if not vids:
        statuses.append("fail"); findings.append("no rough video in export/rough/")
    else:
        vid = vids[-1]
        dur = ffprobe_duration(vid)
        ok, err = ffmpeg_decode_ok(vid)
        details.update(video=vid.name, video_sec=round(dur, 1), decode_clean=ok)
        if not ok:
            statuses.append("fail"); findings.append(f"video decode errors: {err}")
        elif dur <= 0:
            statuses.append("fail"); findings.append("video has zero duration")
        else:
            statuses.append("pass")

    # thumbnail — only required when a publish package is requested
    thumbs = sorted((proj / "export" / "thumbnail").glob("*.jpg")) \
        + sorted((proj / "export" / "thumbnail").glob("*.png"))
    details["thumbnail_present"] = bool(thumbs)
    if publish and not thumbs:
        statuses.append("fail"); findings.append("publish requested but no thumbnail in export/thumbnail/")
    elif not thumbs:
        findings.append("no thumbnail yet (not required unless publishing)")

    return result("render_check", worst(*statuses), findings, details)


if __name__ == "__main__":
    load_env()
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--publish", action="store_true")
    a = ap.parse_args()
    print(json.dumps(run(a.project, publish=a.publish), ensure_ascii=False, indent=2))
