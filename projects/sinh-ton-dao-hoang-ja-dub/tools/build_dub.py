#!/usr/bin/env python3
"""
Japanese dub builder — sieu-trom-iq300-ja-dub

Recreates a Vietnamese movie-review video with a Japanese narration track,
segment-by-segment time-aligned to the original caption timestamps.

Steps:
    python tools/build_dub.py --synth      # edge-tts per segment + time-fit
    python tools/build_dub.py --assemble   # place segments on a full-length voice track
    python tools/build_dub.py --mix        # voice + separated background -> final audio + mux video
    python tools/build_dub.py --all

Inputs:
    data/segments_vi.json     [{id, start_ms, end_ms, dur_ms, vi}]
    data/ja_translations.json {id: japanese_text}
    --video / --background paths for the source video and demucs no_vocals stem
"""
import argparse
import asyncio
import json
import pathlib
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
AUDIO = ROOT / "audio"
SEG_RAW = AUDIO / "ja_raw"
SEG_FIT = AUDIO / "ja_fit"
EXPORT = ROOT / "export"

VOICE = "ja-JP-KeitaNeural"
BASE_RATE = "+10%"
GAP_MS = 150          # breathing room at the end of each slot
MAX_TEMPO = 1.60      # hard cap on additional atempo compression


def ffprobe_dur(path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


def load_segments():
    segs = json.loads((DATA / "segments_vi.json").read_text(encoding="utf-8"))
    ja = json.loads((DATA / "ja_translations.json").read_text(encoding="utf-8"))
    missing = [s["id"] for s in segs if s["id"] not in ja]
    if missing:
        raise SystemExit(f"missing translations: {missing}")
    for s in segs:
        s["ja"] = ja[s["id"]]
    return segs


async def synth_all(segs):
    import edge_tts
    SEG_RAW.mkdir(parents=True, exist_ok=True)
    sem = asyncio.Semaphore(6)

    async def one(seg):
        out = SEG_RAW / f"{seg['id']}.mp3"
        if out.exists() and out.stat().st_size > 1000:
            return
        async with sem:
            for attempt in range(4):
                try:
                    tts = edge_tts.Communicate(seg["ja"], VOICE, rate=BASE_RATE)
                    await tts.save(str(out))
                    return
                except Exception as e:
                    if attempt == 3:
                        raise
                    await asyncio.sleep(2 * (attempt + 1))

    await asyncio.gather(*[one(s) for s in segs])


def fit_all(segs):
    SEG_FIT.mkdir(parents=True, exist_ok=True)
    report = []
    for seg in segs:
        raw = SEG_RAW / f"{seg['id']}.mp3"
        fit = SEG_FIT / f"{seg['id']}.wav"
        slot = (seg["end_ms"] - GAP_MS) / 1000.0 - seg["start_ms"] / 1000.0
        dur = ffprobe_dur(raw)
        tempo = dur / slot
        filters = ["loudnorm=I=-16:TP=-1.5:LRA=11"]
        applied = 1.0
        if tempo > 1.0:
            applied = min(tempo, MAX_TEMPO)
            t = applied
            chain = []
            while t > 1.5:          # atempo supports 0.5..2 per instance; stay gentle
                chain.append("atempo=1.5")
                t /= 1.5
            chain.append(f"atempo={t:.5f}")
            filters = chain + filters
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-i", str(raw),
             "-af", ",".join(filters), "-ar", "44100", "-ac", "1", str(fit)],
            check=True)
        fitted = ffprobe_dur(fit)
        overflow = fitted - slot
        report.append({"id": seg["id"], "slot_s": round(slot, 2),
                       "raw_s": round(dur, 2), "tempo": round(applied, 3),
                       "fit_s": round(fitted, 2),
                       "overflow_s": round(max(0.0, overflow), 2)})
        flag = " OVERFLOW" if overflow > 0.05 else ""
        print(f"{seg['id']} slot={slot:6.2f}s raw={dur:6.2f}s tempo={applied:.3f}"
              f" fit={fitted:6.2f}s{flag}")
    (DATA / "fit_report.json").write_text(
        json.dumps(report, indent=1), encoding="utf-8")
    bad = [r for r in report if r["overflow_s"] > 0.3]
    print(f"\nsegments: {len(report)}, overflow>0.3s: {len(bad)}")
    for r in bad:
        print("  ", r)


def assemble(segs, total_ms):
    import numpy as np
    import soundfile as sf
    sr = 44100
    track = np.zeros(int(total_ms / 1000.0 * sr) + sr, dtype=np.float32)
    for seg in segs:
        data, fsr = sf.read(SEG_FIT / f"{seg['id']}.wav", dtype="float32")
        assert fsr == sr
        if data.ndim > 1:
            data = data.mean(axis=1)
        start = int(seg["start_ms"] / 1000.0 * sr)
        end = min(start + len(data), len(track))
        track[start:end] += data[: end - start]
    np.clip(track, -1.0, 1.0, out=track)
    EXPORT.mkdir(parents=True, exist_ok=True)
    out = EXPORT / "ja_voice_track.wav"
    sf.write(out, track, sr)
    print(f"voice track -> {out} ({len(track)/sr:.1f}s)")
    return out


def mix_and_mux(video, background):
    voice = EXPORT / "ja_voice_track.wav"
    final_audio = EXPORT / "ja_full_mix.wav"
    # Write to a temp file and rename atomically: the mux below (and any
    # concurrent run) must never read a half-written mix.
    tmp_audio = final_audio.with_suffix(".tmp.wav")
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error",
         "-i", str(voice), "-i", str(background),
         "-filter_complex",
         "[1:a]volume=0.9[bg];"
         "[bg][0:a]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=400[duck];"
         "[duck][0:a]amix=inputs=2:duration=first:weights=1 1.6:normalize=0,"
         "loudnorm=I=-14:TP=-1.0:LRA=11[out]",
         "-map", "[out]", "-ar", "44100", "-ac", "2", str(tmp_audio)],
        check=True)
    tmp_audio.replace(final_audio)
    print(f"mixed audio -> {final_audio}")
    final_video = EXPORT / f"{ROOT.name.replace('-', '_')}.mp4"
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error",
         "-i", str(video), "-i", str(final_audio),
         "-map", "0:v:0", "-map", "1:a:0",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
         "-movflags", "+faststart", "-shortest", str(final_video)],
        check=True)
    print(f"final video -> {final_video} ({ffprobe_dur(final_video):.1f}s)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--synth", action="store_true")
    ap.add_argument("--assemble", action="store_true")
    ap.add_argument("--mix", action="store_true")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--video", default="")
    ap.add_argument("--background", default="")
    args = ap.parse_args()

    segs = load_segments()
    total_ms = max(s["end_ms"] for s in segs)

    if args.synth or args.all:
        asyncio.run(synth_all(segs))
        print(f"synthesized {len(segs)} segments")
        fit_all(segs)
    if args.assemble or args.all:
        assemble(segs, total_ms)
    if args.mix or args.all:
        if not args.video or not args.background:
            raise SystemExit("--mix requires --video and --background")
        mix_and_mux(args.video, args.background)


if __name__ == "__main__":
    main()
