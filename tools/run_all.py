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


def review_caption(proj: Path) -> str:
    """Telegram review caption: recommended title + description + hashtags from seo.md,
    so the owner reviews the full publish package (not just the video). Capped for Telegram."""
    title, desc, tags = project_title(proj), "", ""
    seo = proj / "seo.md"
    if seo.exists():
        txt = seo.read_text(encoding="utf-8")
        m = re.search(r"Recommended:\**\s*Option\s*(\d)", txt)          # which title option
        opt = m.group(1) if m else "1"
        mo = re.search(rf"###\s*Option\s*{opt}\b[^\n]*\n+([^\n]+)", txt)
        if mo:
            title = re.sub(r"\s*\[\d+\s*characters?\]\s*$", "", mo.group(1)).strip().strip("「」\" ")
        md = re.search(r"##\s*Description\s*\n+(.+?)(?:\n##\s|\Z)", txt, re.S)  # description body
        if md:
            body = re.split(r"━{3,}|^CHAPTERS|^TAGS", md.group(1), maxsplit=1, flags=re.M)[0].strip()
            desc = body[:700].rstrip()
        seen: list[str] = []                                            # hashtags (dedup)
        for h in re.findall(r"#[^\s#、。]+", txt):
            if h not in seen:
                seen.append(h)
        tags = " ".join(seen[:8])
    parts = ["[AUTOPILOT — NEEDS REVIEW]", f"📺 {title}"]
    if desc:
        parts.append("\n" + desc)
    if tags:
        parts.append("\n🏷 " + tags)
    parts.append("\n⚠️ upload_allowed=false — review only; YouTube upload là bước riêng.")
    return "\n".join(parts)[:3500]


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
    ap.add_argument("--skip-qa", action="store_true",
                    help="DEV ONLY: skip the mandatory QA/safety gate. Output is left UNVERIFIED and "
                         "will NOT be delivered. Never use for anything that ships.")
    ap.add_argument("--qa-no-llm", action="store_true",
                    help="DEV: run the QA gate structurally only (no LLM judges). Semantic checks "
                         "become WARN, so the gate will NOT report PASS and delivery stays blocked.")
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
    step("4/6 RENDER", ["tools/render/assemble_video.py", "--project", slug])
    rough = proj / "export" / "rough" / f"{slug}_rough.mp4"
    if not rough.exists():
        sys.exit("[ERROR] render produced no file")

    # ── 5/6 QA / SAFETY GATE — mandatory, after render, BEFORE any delivery ──
    manifest = None
    if a.skip_qa:
        print("\n" + "!" * 64)
        print("!! --skip-qa: QA/SAFETY GATE SKIPPED — DEV ONLY.")
        print("!! Output is UNVERIFIED for safety and will NOT be delivered.")
        print("!! Never use --skip-qa for anything that ships.")
        print("!" * 64)
    else:
        gate_cmd = [PY, "tools/qa/final_gate.py", "--project", slug]
        if a.qa_no_llm:
            gate_cmd.append("--no-llm")
        print("\n===== 5/6 QA / SAFETY GATE =====", flush=True)
        subprocess.run(gate_cmd, cwd=str(REPO))  # prints its own summary; do NOT exit on rc
        mf = REPO / "runtime" / slug / "human_review_manifest.json"
        if not mf.exists():
            sys.exit("[run_all] QA gate produced no manifest — aborting (no silent fallthrough)")
        manifest = json.loads(mf.read_text(encoding="utf-8"))

    # ── State machine (upload_allowed stays false everywhere; run_all never publishes) ──
    passed = bool(manifest and manifest.get("automatic_checks_passed"))
    project_status = ("UNVERIFIED_QA_SKIPPED" if a.skip_qa
                      else "READY_FOR_HUMAN_REVIEW" if passed else "BLOCKED_BY_QA")
    print(f"\n[run_all] project_status = {project_status}   upload_allowed = False")
    if manifest and not passed:
        nonpass = [f"{k.replace('_status','')}={manifest[k]}" for k in
                   ("source_status", "script_status", "image_status", "render_status")
                   if manifest.get(k) != "pass"]
        print(f"[run_all] gate did NOT pass — non-passing checks: {nonpass}")

    # ── 6/6 DELIVERY — only when the gate PASSED ──
    if a.deliver:
        if passed:
            step("6/6 DELIVER (Telegram — for human review)", [
                "tools/deliver/drive_send.py", "--upload", str(rough.relative_to(REPO)),
                "--caption", review_caption(proj), "--notify"])
        else:
            why = "QA skipped (--skip-qa)" if a.skip_qa else project_status
            print(f"\n[run_all] DELIVERY BLOCKED by QA gate ({why}). Nothing sent to Telegram.")
    print(f"\n[run_all] DONE — status={project_status}, video={rough.relative_to(REPO)}")
    return 0 if (a.skip_qa or passed) else 2


if __name__ == "__main__":
    raise SystemExit(main())
