#!/usr/bin/env python3
"""QA: research sources & citations.

Checks: research.md exists; enough named sources; a Sources section / URLs present;
stage-2 verification present; (LLM) no fabricated-looking sources or unsupported
core claims. Returns a result dict (see _common).
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import load_env, project_dir, result, worst, llm_text_judge  # noqa: E402


def run(project_id: str, use_llm: bool = True, publish: bool = False) -> dict:
    proj = project_dir(project_id)
    research = proj / "research.md"
    findings, statuses, details = [], [], {}

    if not research.exists():
        return result("source_check", "fail", ["research.md missing"], {})
    text = research.read_text(encoding="utf-8", errors="ignore")

    n_src_lines = len(re.findall(r"(?:Source:|出典|Nguồn:)", text))
    n_urls = len(re.findall(r"https?://", text))
    has_sources_section = bool(re.search(r"(?im)^##\s*(Sources|出典|参考|Nguồn)", text))
    n_unconfirmed = len(re.findall(r"URL not confirmed|要確認|chưa xác nhận", text, re.I))
    details.update(source_lines=n_src_lines, urls=n_urls,
                   sources_section=has_sources_section, unconfirmed_urls=n_unconfirmed)

    if n_src_lines >= 3 or n_urls >= 3:
        statuses.append("pass")
    else:
        statuses.append("fail")
        findings.append(f"too few cited sources (source lines={n_src_lines}, urls={n_urls}; need >=3)")
    if not has_sources_section:
        statuses.append("warn")
        findings.append("no explicit Sources section heading")
    if (proj / "research_verified.md").exists():
        details["stage2_verification"] = True
    else:
        statuses.append("warn")
        findings.append("research_verified.md (source-verifier stage) missing")

    if use_llm:
        v = llm_text_judge(
            "You are a fact-checking QA reviewer for a documentary pipeline. Judge ONLY sourcing quality.",
            "Below is a research brief. Decide: do the key facts have named sources, and do any sources "
            "or URLs look fabricated/implausible? verdict 'fail' only for clearly fabricated sources or "
            "core claims with no source; 'warn' for thin/uncertain sourcing; 'pass' if well-sourced.\n\n"
            + text[:12000])
        if v:
            statuses.append(v["verdict"])
            findings += [f"[LLM] {f}" for f in v.get("findings", [])]
            details["llm_verdict"] = v["verdict"]
    else:
        statuses.append("warn")
        findings.append("LLM source judgement skipped (--no-llm)")

    return result("source_check", worst(*statuses), findings, details)


if __name__ == "__main__":
    load_env()
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--no-llm", action="store_true")
    a = ap.parse_args()
    print(json.dumps(run(a.project, use_llm=not a.no_llm), ensure_ascii=False, indent=2))
