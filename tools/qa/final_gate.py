#!/usr/bin/env python3
"""Autopilot final QA/safety gate.

Runs all check modules (source, script, image_policy, render), writes a human
approval manifest to runtime/<project_id>/human_review_manifest.json, and enforces
the rule: NO autopilot output may be marked READY unless every automatic check
passes, the manifest exists, and upload_allowed stays false until explicit user
approval. The gate never auto-approves and never uploads.

Usage:
  python tools/qa/final_gate.py --project <project_id>
  python tools/qa/final_gate.py --project <project_id> --no-llm   # fast structural-only
  python tools/qa/final_gate.py --project <project_id> --publish   # also require thumbnail
"""
from __future__ import annotations
import argparse, json, re, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import load_env, project_dir, runtime_dir, worst  # noqa: E402
import source_check, script_check, image_policy_check, render_check  # noqa: E402

TEXT_FILES = ["research.md", "research_verified.md", "story.md", "story_bible.md", "script.md",
              "storyboard.md", "image_plan.md", "image_prompts.md", "voice_script.txt", "seo.md"]


def _title(proj: Path) -> str:
    seo = proj / "seo.md"
    if seo.exists():
        m = re.search(r"(?m)^#\s+(?:SEO Package:\s*)?(.+)$", seo.read_text(encoding="utf-8", errors="ignore"))
        if m:
            return m.group(1).strip()
    return proj.name


def _topic(proj: Path) -> str:
    inp = proj / "input.json"
    if inp.exists():
        try:
            return json.loads(inp.read_text(encoding="utf-8")).get("topic", "")
        except Exception:
            pass
    return ""


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    load_env()
    ap = argparse.ArgumentParser(description="Autopilot final QA/safety gate")
    ap.add_argument("--project", required=True, help="project_id (folder under projects/)")
    ap.add_argument("--no-llm", action="store_true", help="skip semantic LLM checks (structural only)")
    ap.add_argument("--publish", action="store_true", help="treat as publish package (require thumbnail)")
    a = ap.parse_args()
    pid = Path(a.project).name
    proj = project_dir(pid)
    if not proj.exists():
        sys.exit(f"[ERROR] project not found: {proj}")
    use_llm = not a.no_llm

    checks = {
        "source": source_check.run(pid, use_llm, a.publish),
        "script": script_check.run(pid, use_llm, a.publish),
        "image": image_policy_check.run(pid, use_llm, a.publish),
        "render": render_check.run(pid, use_llm, a.publish),
    }
    statuses = [c["status"] for c in checks.values()]
    safety = worst(*statuses)
    all_pass = all(s == "pass" for s in statuses)
    any_fail = any(s == "fail" for s in statuses)

    gate_status = ("READY_FOR_HUMAN_REVIEW" if all_pass
                   else "BLOCKED" if any_fail else "NEEDS_REVIEW")
    decision = "approve" if all_pass else ("revise" if any_fail else "review")
    readiness = ("ready_pending_human_approval" if all_pass
                 else "needs_revision" if any_fail else "needs_human_review")

    generated = {f: (proj / f).exists() for f in TEXT_FILES}
    generated["images"] = len(list((proj / "assets" / "images").glob("beat_*.*")))
    generated["audio"] = len(list((proj / "assets" / "audio").glob("seg_*.mp3")))
    generated["rough_video"] = bool(list((proj / "export" / "rough").glob("*_rough.mp4")))

    manifest = {
        "schema_version": "1.0",
        "project_id": pid,
        "title": _title(proj),
        "topic": _topic(proj),
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "llm_checks": use_llm,
        "generated_files": generated,
        "source_status": checks["source"]["status"],
        "script_status": checks["script"]["status"],
        "image_status": checks["image"]["status"],
        "render_status": checks["render"]["status"],
        "safety_status": safety,
        "automatic_checks_passed": all_pass,
        "gate_status": gate_status,
        "publish_readiness": readiness,
        "required_human_decision": decision,   # approve | review | revise
        "human_decision": None,                # set by a human later
        "upload_allowed": False,               # never true here; needs explicit separate approval
        "checks": checks,
        "rule": ("Output is NOT READY unless automatic_checks_passed=true AND a human sets "
                 "human_decision='approve'. upload_allowed stays false until a separate, explicit "
                 "user upload approval. The gate never uploads or auto-approves."),
    }
    rd = runtime_dir(pid)
    mf = rd / "human_review_manifest.json"
    mf.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    # summary
    icon = {"pass": "PASS", "warn": "WARN", "fail": "FAIL"}
    print(f"\n=== QA GATE: {pid} ===")
    for name, c in checks.items():
        print(f"  [{icon[c['status']]}] {name:7} {c['check']}")
        for f in c["findings"][:6]:
            print(f"          - {f}")
    print(f"\n  safety_status        : {safety}")
    print(f"  automatic_checks_pass: {all_pass}")
    print(f"  gate_status          : {gate_status}")
    print(f"  required_human_decision: {decision}")
    print(f"  upload_allowed       : False")
    print(f"  manifest             : {mf.relative_to(Path(__file__).resolve().parents[2])}")
    return 0 if not any_fail else 1


if __name__ == "__main__":
    raise SystemExit(main())
