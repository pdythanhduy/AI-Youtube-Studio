#!/usr/bin/env python3
"""QA: script & narration safety.

Checks: script.md exists; clickbait/fake-shock & horror phrasing scan (script +
voice_script); (LLM) every factual claim is supported by research, no fabricated
shocking claims, no horror exaggeration, sensitive/historical content (forced
labor, victims, tragedy) treated factually and respectfully.
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (load_env, project_dir, result, worst, llm_text_judge,  # noqa: E402
                     CLICKBAIT, GORE)


def _scan(text: str, phrases: list[str]) -> list[str]:
    low = text.lower()
    return [p for p in phrases if p.lower() in low]


def run(project_id: str, use_llm: bool = True, publish: bool = False) -> dict:
    proj = project_dir(project_id)
    script = proj / "script.md"
    findings, statuses, details = [], [], {}

    if not script.exists():
        return result("script_check", "fail", ["script.md missing"], {})
    stext = script.read_text(encoding="utf-8", errors="ignore")
    vtext = (proj / "voice_script.txt").read_text(encoding="utf-8", errors="ignore") \
        if (proj / "voice_script.txt").exists() else ""
    combined = stext + "\n" + vtext

    hits_click = _scan(combined, CLICKBAIT)
    hits_gore = _scan(combined, GORE)
    details.update(clickbait_hits=hits_click, gore_hits=hits_gore)
    if hits_click:
        statuses.append("fail")
        findings.append(f"fake-shock/clickbait phrasing: {hits_click}")
    if hits_gore:
        statuses.append("fail")
        findings.append(f"gore/graphic phrasing in narration: {hits_gore}")
    if not (hits_click or hits_gore):
        statuses.append("pass")

    if use_llm:
        research = (proj / "research.md").read_text(encoding="utf-8", errors="ignore") \
            if (proj / "research.md").exists() else "(no research.md)"
        v = llm_text_judge(
            "You are a strict editorial QA reviewer for a respectful documentary channel. "
            "Apply: no fabricated facts, no fake shocking/clickbait claims, no horror exaggeration, "
            "and sensitive/historical topics (forced labor, victims, death, tragedy) must be factual, "
            "neutral, and respectful — no sensationalising suffering, no asserting disputed numbers as fact.",
            "RESEARCH (ground truth):\n" + research[:9000]
            + "\n\n---\nSCRIPT to review:\n" + stext[:9000]
            + "\n\nverdict 'fail' for any unsupported/fabricated claim, fake-shock framing, horror "
              "exaggeration, or disrespectful handling of sensitive content; 'warn' for borderline; "
              "'pass' if clean. List specific findings.")
        if v:
            statuses.append(v["verdict"])
            findings += [f"[LLM] {f}" for f in v.get("findings", [])]
            details["llm_verdict"] = v["verdict"]
    else:
        statuses.append("warn")
        findings.append("LLM claim-grounding/respect judgement skipped (--no-llm)")

    return result("script_check", worst(*statuses), findings, details)


if __name__ == "__main__":
    load_env()
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--no-llm", action="store_true")
    a = ap.parse_args()
    print(json.dumps(run(a.project, use_llm=not a.no_llm), ensure_ascii=False, indent=2))
