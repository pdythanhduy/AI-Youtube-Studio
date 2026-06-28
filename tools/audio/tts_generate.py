#!/usr/bin/env python3
"""Asset stage: Vbee TTS from a project's voice_script.txt.

Bridges the orchestrator's stage-9 output (prompts/09 -> voice_script.txt, clean
text + pacing markers) to Vbee. Strips the editor markers ([PAUSE:1s], [SLOW],
[WHISPER], ...) — they are not spoken — segments the text by sentence, and calls
Vbee per segment (async: submit -> poll tts/{request_id}/callback-result), saving
mp3s to projects/<slug>/assets/audio/seg_NN.mp3.

Reuses the exact Vbee contract proven in hashima-island-mystery-ja:
  POST https://vbee.vn/api/v1/tts  (bearer auth, token=VBEE_API_KEY)
  payload: inputText, voiceCode, audioType=mp3, callbackUrl (required), app_id
  NO speed field (Vbee /api/v1/tts rejects it)
  poll GET https://vbee.vn/api/v1/tts/{request_id}/callback-result for audio_url

Credentials from .env (upward search), never printed.

Usage:
  python tools/audio/tts_generate.py --project <slug> --list
  python tools/audio/tts_generate.py --project <slug> --limit 2
  python tools/audio/tts_generate.py --project <slug>          # all segments
"""
from __future__ import annotations
import argparse, json, os, re, sys, time, urllib.request, urllib.error, urllib.parse
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PROJECTS = REPO / "projects"


def load_env() -> None:
    for d in [Path(__file__).resolve().parent, *Path(__file__).resolve().parents]:
        f = d / ".env"
        if f.is_file():
            for line in f.read_text(encoding="utf-8", errors="ignore").splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, _, v = line.partition("=")
                    os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
            return


def cfg(*names, default=None):
    for n in names:
        v = os.environ.get(n)
        if v:
            return v
    return default


API_URL = "https://vbee.vn/api/v1/tts"
RESULT_URL = "https://vbee.vn/api/v1/tts/{request_id}/callback-result"


def segments_from_voice(raw: str) -> list[str]:
    txt = re.sub(r"\[[^\]]*\]", "", raw)      # drop [PAUSE]/[SLOW]/[WHISPER]/... markers
    txt = txt.replace("\r", "").replace("\n", "")
    parts = re.split(r"(?<=[。！？!?])", txt)   # keep sentence-ending punctuation
    segs = [p.strip() for p in parts if p.strip()]
    # merge very short fragments into the previous segment
    merged: list[str] = []
    for s in segs:
        if merged and len(s) < 6:
            merged[-1] += s
        else:
            merged.append(s)
    return merged


def _post(url: str, headers: dict, body: dict) -> dict:
    r = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST")
    for k, v in headers.items():
        r.add_header(k, v)
    try:
        with urllib.request.urlopen(r, timeout=60) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code}: {e.read().decode()[:300]}") from None


def _get(url: str, headers: dict) -> dict:
    r = urllib.request.Request(url, method="GET")
    for k, v in headers.items():
        r.add_header(k, v)
    with urllib.request.urlopen(r, timeout=60) as resp:
        return json.loads(resp.read().decode())


def _find(d, *keys):
    """Deep search for the first of `keys` anywhere in a nested dict/list.
    Vbee nests the audio URL at result.payload.audio_link, so we must recurse fully."""
    if isinstance(d, dict):
        for k in keys:
            if d.get(k):
                return d[k]
        for v in d.values():
            got = _find(v, *keys)
            if got:
                return got
    elif isinstance(d, list):
        for v in d:
            got = _find(v, *keys)
            if got:
                return got
    return None


def synth(text: str, token: str, app_id: str | None, voice: str, callback: str) -> bytes:
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    payload = {"inputText": text, "voiceCode": voice, "audioType": "mp3", "callbackUrl": callback}
    if app_id:
        payload["app_id"] = app_id
    resp = _post(API_URL, headers, payload)
    req_id = _find(resp, "request_id", "requestId", "id")
    if not req_id:
        raise RuntimeError(f"no request_id in submit response: {json.dumps(resp)[:200]}")
    # poll for the finished audio
    for _ in range(60):
        time.sleep(3)
        try:
            res = _get(RESULT_URL.format(request_id=urllib.parse.quote(str(req_id), safe="")), headers)
        except urllib.error.HTTPError:
            continue
        url = _find(res, "audio_url", "audioUrl", "file_url", "fileUrl", "url", "audio_link", "link")
        if url:
            with urllib.request.urlopen(url, timeout=120) as a:
                return a.read()
        status = _find(res, "status") or ""
        if str(status).upper() in ("FAILED", "ERROR"):
            raise RuntimeError(f"Vbee job {req_id} {status}")
    raise TimeoutError(f"Vbee job {req_id} not ready in time")


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    load_env()
    ap = argparse.ArgumentParser(description="Vbee TTS from voice_script.txt")
    ap.add_argument("--project", required=True)
    ap.add_argument("--limit", type=int, default=0, help="only first N segments (0=all)")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()

    proj = PROJECTS / a.project
    vs = proj / "voice_script.txt"
    if not vs.is_file():
        sys.exit(f"[ERROR] {vs} not found (run stage 9 first)")
    segs = segments_from_voice(vs.read_text(encoding="utf-8"))
    if a.list:
        for i, s in enumerate(segs, 1):
            print(f"  seg {i:02d} ({len(s)} chars): {s[:48]}")
        print(f"total: {len(segs)} segments")
        return 0
    if a.limit:
        segs = segs[:a.limit]

    token = cfg("VBEE_ACCESS_TOKEN", "VBEE_API_KEY", "EXPO_PUBLIC_VBEE_API_KEY")
    app_id = cfg("VBEE_APP_ID", "EXPO_PUBLIC_VBEE_APP_ID")
    voice = cfg("VBEE_VOICE_ID", "EXPO_PUBLIC_VBEE_JA_VOICE_CODE", default="ja-JP-Standard-C")
    callback = cfg("VBEE_CALLBACK_URL", default="https://example.com/vbee-callback")
    if not token:
        sys.exit("[ERROR] VBEE_API_KEY (or VBEE_ACCESS_TOKEN) missing in .env")

    outdir = proj / "assets" / "audio"
    rows = []
    for i, s in enumerate(segs, 1):
        out = outdir / f"seg_{i:02d}.mp3"
        if out.exists() and not a.force:
            print(f"SKIP seg {i:02d} (exists)")
            continue
        try:
            print(f"TTS  seg {i:02d} ({len(s)} chars) ...", flush=True)
            audio = synth(s, token, app_id, voice, callback)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(audio)
            rows.append({"seg": i, "file": str(out.relative_to(proj)),
                         "chars": len(s), "bytes": len(audio), "text": s})
            print(f"     saved {out.relative_to(proj)} ({len(audio)//1024} KB)")
        except Exception as e:
            print(f"[ERROR] seg {i:02d}: {e}", file=sys.stderr)
    if rows:
        mf = proj / "audio_manifest.json"
        prev = {r["seg"]: r for r in json.loads(mf.read_text())["segments"]} if mf.exists() else {}
        for r in rows:
            prev[r["seg"]] = r
        mf.write_text(json.dumps({"voice": voice, "segments": list(prev.values())},
                                 ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\nManifest: {mf.relative_to(proj)} (+{len(rows)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
