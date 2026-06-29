#!/usr/bin/env python3
"""Autopilot capstone — one command: topic -> full rough video -> (optional) Telegram.

Chains the validated stage tools as subprocesses:
  1. orchestrator   run_pipeline.py --init/--all   (10 text stages, Claude API)
  2. images         visuals/generate_images.py     (FLUX from image_prompts.md)
  3. tts            audio/tts_generate.py           (Vbee from voice_script.txt)
  4. render         render/assemble_video.py        (audio-driven ffmpeg assembly)
  5. deliver        deliver/drive_send.py --notify  (Drive link via Telegram bot)

Each step is resumable/idempotent (the underlying tools skip existing outputs), so
re-running continues where it stopped. YouTube upload is NOT performed — delivery is
to the user's Telegram for review (upload stays a separate, human-gated action).

Usage:
  python tools/run_all.py --topic "軍艦島 端島の歴史" --niche japanese_mystery --language ja --deliver
  python tools/run_all.py --project <slug> --deliver
  python tools/run_all.py --project <slug> --limit-images 3 --limit-audio 4   # cheap test
"""
from __future__ import annotations
import argparse, json, re, subprocess, sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PY = sys.executable


def step(title: str, cmd: list[str]) -> None:
    print(f"\n===== {title} =====", flush=True)
    r = subprocess.run([PY, *cmd], cwd=str(REPO))
    if r.returncode != 0:
        sys.exit(f"[run_all] step failed: {title}")


def project_title(proj: Path) -> str:
    inp = proj / "input.json"
    if inp.exists():
        try:
            return json.loads(inp.read_text(encoding="utf-8")).get("topic", proj.name)
        except Exception:
            pass
    return proj.name


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="Autopilot: topic -> rough video -> Telegram")
    ap.add_argument("--topic")
    ap.add_argument("--project")
    ap.add_argument("--niche", default="japanese_mystery")
    ap.add_argument("--language", default="ja")
    ap.add_argument("--length", type=int, default=12)
    ap.add_argument("--limit-images", type=int, default=0)
    ap.add_argument("--limit-audio", type=int, default=0)
    ap.add_argument("--deliver", action="store_true", help="send the rough video to Telegram (Drive link)")
    a = ap.parse_args()
    if not (a.topic or a.project):
        sys.exit("[ERROR] need --topic (new) or --project (existing)")

    orch = "tools/orchestrator/run_pipeline.py"
    slug = a.project
    if a.topic:
        out = subprocess.run([PY, orch, "--init", a.topic, "--niche", a.niche,
                              "--language", a.language, "--length", str(a.length)],
                             cwd=str(REPO), capture_output=True, text=True)
        sys.stdout.write(out.stdout)
        m = re.search(r"--project (\S+)", out.stdout)
        if not m:
            sys.exit(f"[ERROR] could not init project:\n{out.stdout}\n{out.stderr}")
        slug = m.group(1)

    proj = REPO / "projects" / slug
    step("1/5 TEXT (research -> seo)", [orch, "--project", slug, "--all"])
    img_cmd = ["tools/visuals/generate_images.py", "--project", slug]
    if a.limit_images:
        img_cmd += ["--limit", str(a.limit_images)]
    step("2/5 IMAGES (FLUX)", img_cmd)
    tts_cmd = ["tools/audio/tts_generate.py", "--project", slug]
    if a.limit_audio:
        tts_cmd += ["--limit", str(a.limit_audio)]
    step("3/5 TTS (Vbee)", tts_cmd)
    step("4/5 RENDER", ["tools/render/assemble_video.py", "--project", slug])

    rough = proj / "export" / "rough" / f"{slug}_rough.mp4"
    if a.deliver:
        if not rough.exists():
            sys.exit("[ERROR] render produced no file; cannot deliver")
        step("5/5 DELIVER (Telegram)", [
            "tools/deliver/drive_send.py", "--upload", str(rough.relative_to(REPO)),
            "--caption", f"[AUTOPILOT] {project_title(proj)}", "--notify"])
    print(f"\n[run_all] DONE — {rough.relative_to(REPO) if rough.exists() else '(no video)'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
