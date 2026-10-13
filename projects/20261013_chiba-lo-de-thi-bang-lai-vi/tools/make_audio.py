#!/usr/bin/env python3
"""Offline audio for the reel: espeak-ng Vietnamese voice-over + a synthesized tension bed.

1. One voice line per scene (espeak-ng, voice `vi`) -> export/audio/vo_NN.wav
2. Scene length = voice length + padding -> export/audio/timing.json (read by render_reel.py)
3. Music bed (numpy): low drone + clock tick + a soft hit on every scene change -> bed.wav
4. Voice track laid on the scene timeline -> voice.wav

Then: render_reel.py, then mux (see README in script/post_package.md):
  ffmpeg -i export/reel_1080x1920.mp4 -i export/audio/voice.wav -i export/audio/bed.wav \
    -filter_complex "[1]highpass=f=90,acompressor=threshold=-18dB:ratio=3,volume=1.6[v];\
[2]volume=0.35[b];[v][b]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5,\
aresample=48000,pan=stereo|c0=c0|c1=c0[a]" \
    -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -shortest export/reel_final.mp4

Usage: python tools/make_audio.py [--speed 150]
"""
from __future__ import annotations
import argparse, json, subprocess, wave
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "export" / "audio"
SR = 22050

LINES = [
    "Tin nóng từ Chiba, Nhật Bản. Nghi lộ đề thi bằng lái tiếng Việt.",
    "Ngày mười ba tháng mười, sau giờ thi, một phụ nữ Việt Nam hai mươi chín tuổi bị phát hiện chụp bảng đen bằng điện thoại.",
    "Giám thị kiểm tra, và thấy trong máy có đề thi bằng lái xe máy bản tiếng Việt.",
    "Theo cảnh sát, từ trang một đến trang bốn đã được đánh dấu sẵn. Nghi là đề bị lộ từ trước.",
    "Người phụ nữ khai: Tôi tìm bằng Chát Gi Pi Ti, rồi mang đến.",
    "Cảnh sát đã tạm dừng thi lý thuyết bằng tiếng Việt, cho đến khi có bộ đề mới.",
    "Bạn nghĩ sao về vụ việc này? Hãy bình luận bên dưới.",
]
LEAD, TAIL = 0.5, 0.7  # seconds of silence before / after each line


def read_wav(p: Path) -> np.ndarray:
    with wave.open(str(p)) as w:
        assert w.getframerate() == SR, w.getframerate()
        return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768


def write_wav(p: Path, x: np.ndarray) -> None:
    x = np.clip(x, -1, 1)
    with wave.open(str(p), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())


def music_bed(total: float, cuts: list[float]) -> np.ndarray:
    t = np.arange(int(total * SR)) / SR
    # drone: A1 + E2 with slow tremolo
    drone = (np.sin(2 * np.pi * 55 * t) + 0.6 * np.sin(2 * np.pi * 82.4 * t)) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.25 * t))
    bed = 0.18 * drone
    # clock tick every 0.5 s (short filtered click)
    tick_len = int(0.03 * SR)
    env = np.exp(-np.linspace(0, 8, tick_len))
    tick = np.sin(2 * np.pi * 1800 * np.arange(tick_len) / SR) * env
    for i, s in enumerate(np.arange(0, total, 0.5)):
        a = int(s * SR)
        seg = tick[: max(0, min(tick_len, len(bed) - a))]
        bed[a:a + len(seg)] += (0.22 if i % 2 == 0 else 0.12) * seg
    # boom on scene changes
    hit_len = int(1.2 * SR)
    ht = np.arange(hit_len) / SR
    hit = np.sin(2 * np.pi * (60 - 25 * ht) * ht) * np.exp(-ht * 3.5)
    for c in [0.0, *cuts]:
        a = int(c * SR)
        seg = hit[: max(0, min(hit_len, len(bed) - a))]
        bed[a:a + len(seg)] += 0.55 * seg
    # fade in/out
    f = int(0.4 * SR)
    bed[:f] *= np.linspace(0, 1, f); bed[-2 * f:] *= np.linspace(1, 0, 2 * f)
    return bed


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--speed", type=int, default=150)
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)

    clips, durs = [], []
    for i, line in enumerate(LINES, 1):
        p = OUT / f"vo_{i:02d}.wav"
        subprocess.run(["espeak-ng", "-v", "vi", "-s", str(args.speed), "-p", "45", "-w", str(p), line], check=True)
        x = read_wav(p)
        clips.append(x)
        durs.append(round(LEAD + len(x) / SR + TAIL, 2))

    total = sum(durs)
    voice = np.zeros(int(total * SR) + SR, dtype=np.float32)
    t0 = 0.0
    for x, d in zip(clips, durs):
        a = int((t0 + LEAD) * SR)
        voice[a:a + len(x)] += x / max(1e-6, np.abs(x).max()) * 0.9
        t0 += d
    voice = voice[: int(total * SR)]
    cuts = list(np.cumsum(durs)[:-1])

    write_wav(OUT / "voice.wav", voice)
    write_wav(OUT / "bed.wav", music_bed(total, cuts))
    (OUT / "timing.json").write_text(json.dumps({"scene_seconds": durs, "total": round(total, 2)}, indent=2))
    print(f"{len(LINES)} lines, total {total:.1f}s -> {OUT}")


if __name__ == "__main__":
    main()
