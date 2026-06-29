#!/usr/bin/env python3
"""QA: image policy & safety.

Checks: images exist; DRAMATIZATION labels present in image_prompts.md; no near-black
placeholder images; (LLM vision) no identifiable real human faces, no gore/corpses/
victim/suffering imagery, nothing disrespectful for sensitive topics.
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import load_env, project_dir, result, worst, llm_image_judge  # noqa: E402

VISION_Q = ("This is a documentary scene image. Answer strictly for content safety. "
            "verdict 'fail' if it contains: an identifiable real person's face, gore, blood, a corpse, "
            "a victim, depicted suffering/violence, or disrespectful treatment of a sensitive subject. "
            "verdict 'warn' if a face is partially visible or it is borderline. verdict 'pass' if it is "
            "atmospheric / no identifiable faces / no graphic content. List what you see that drove the verdict.")


def _is_black_card(path: Path) -> tuple[bool, dict]:
    try:
        from PIL import Image, ImageStat
        im = Image.open(path).convert("L")
        st = ImageStat.Stat(im)
        mean, std = st.mean[0], st.stddev[0]
        return (mean < 8 and std < 6), {"mean": round(mean, 1), "stddev": round(std, 1)}
    except Exception as e:
        return False, {"error": str(e)}


def run(project_id: str, use_llm: bool = True, publish: bool = False) -> dict:
    proj = project_dir(project_id)
    findings, statuses, details = [], [], {}
    images = sorted((proj / "assets" / "images").glob("beat_*.jpg")) \
        + sorted((proj / "assets" / "images").glob("beat_*.png"))
    prompts_md = proj / "image_prompts.md"

    if not images:
        return result("image_policy_check", "fail", ["no generated images in assets/images/"], {})
    details["image_count"] = len(images)

    # DRAMATIZATION labels (AI scenes must be labelled, per MASTER_RULE image policy)
    if prompts_md.exists():
        n_label = len(re.findall(r"DRAMATIZATION|AI-GENERATED", prompts_md.read_text(encoding="utf-8", errors="ignore")))
        details["dramatization_labels"] = n_label
        if n_label == 0:
            statuses.append("warn")
            findings.append("no DRAMATIZATION/AI-GENERATED labels in image_prompts.md")

    # near-black placeholder detection
    blacks = []
    for img in images:
        is_black, stat = _is_black_card(img)
        if is_black:
            blacks.append(img.name)
    if blacks:
        statuses.append("fail")
        findings.append(f"near-black placeholder image(s): {blacks}")
    else:
        statuses.append("pass")

    # vision safety per image
    if use_llm:
        per = {}
        for img in images:
            v = llm_image_judge(img, VISION_Q)
            if v:
                per[img.name] = v["verdict"]
                statuses.append(v["verdict"])
                if v["verdict"] != "pass":
                    findings += [f"[vision {img.name}] {f}" for f in v.get("findings", [])]
        details["vision_verdicts"] = per
    else:
        statuses.append("warn")
        findings.append("LLM vision face/gore check skipped (--no-llm)")

    return result("image_policy_check", worst(*statuses), findings, details)


if __name__ == "__main__":
    load_env()
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--no-llm", action="store_true")
    a = ap.parse_args()
    print(json.dumps(run(a.project, use_llm=not a.no_llm), ensure_ascii=False, indent=2))
