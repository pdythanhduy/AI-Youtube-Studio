#!/usr/bin/env python3
"""Shared helpers for the autopilot QA/safety gate (tools/qa/*).

Purely additive — does not touch the orchestrator, render, or asset tools, the
Hashima locked project, or any existing contract. Each check module exposes
run(project_id, use_llm, publish) -> result dict and can also run standalone.

Result schema: {"check","status"("pass"|"warn"|"fail"),"findings":[str],"details":{}}
- pass: meets policy.   warn: needs human attention / could not auto-verify.   fail: violates policy.

Deterministic checks always run. Semantic checks (claim-grounding, exaggeration,
respect, faces/gore) use a Claude judge when ANTHROPIC key is present; with
--no-llm they return WARN ("needs human review") rather than a false pass — so the
gate never reports READY on unverified semantic safety.
"""
from __future__ import annotations
import base64, json, os, subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PROJECTS = REPO / "projects"
RUNTIME = REPO / "runtime"
MODEL = "claude-opus-4-8"

# clickbait / fake-shock / horror phrasing to flag (en / ja / vi)
CLICKBAIT = ["shocking", "you won't believe", "you wont believe", "insane", "must see",
             "100% real", "gone wrong", "no one survived", "衝撃", "信じられない", "驚愕の真実",
             "一夜で", "一夜にして", "だった！？", "ဖ", "không thể tin", "gây sốc", "rùng rợn nhất"]
GORE = ["gore", "mutilat", "dismember", "corpse", "dead body", "bloody", "torture", "massacre",
        "遺体", "死体", "惨殺", "グロ", "血まみれ", "xác chết", "thi thể", "tra tấn"]


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


def anthropic_key() -> str | None:
    return os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("EXPO_PUBLIC_ANTHROPIC_API_KEY")


def project_dir(pid: str) -> Path:
    return PROJECTS / Path(pid).name


def runtime_dir(pid: str) -> Path:
    d = RUNTIME / Path(pid).name
    d.mkdir(parents=True, exist_ok=True)
    return d


def result(check: str, status: str, findings=None, details=None) -> dict:
    return {"check": check, "status": status, "findings": findings or [], "details": details or {}}


def worst(*statuses: str) -> str:
    order = {"pass": 0, "warn": 1, "fail": 2}
    flat = [s for s in statuses if s]
    return max(flat, key=lambda s: order.get(s, 0)) if flat else "pass"


def ffprobe_duration(path: Path) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=nk=1:nw=1", str(path)], capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


def ffmpeg_decode_ok(path: Path) -> tuple[bool, str]:
    """Full decode of both streams; clean = exit 0 with no stderr."""
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-f", "null", "-"],
                       capture_output=True, text=True)
    return (r.returncode == 0 and not r.stderr.strip()), r.stderr.strip()[-400:]


_JUDGE_SCHEMA = {
    "type": "object",
    "properties": {
        "verdict": {"type": "string", "enum": ["pass", "warn", "fail"]},
        "findings": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["verdict", "findings"],
    "additionalProperties": False,
}


def _parse_judge(resp) -> dict | None:
    try:
        text = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")
        return json.loads(text)
    except Exception:
        return None


def llm_text_judge(system: str, user: str) -> dict | None:
    """Return {'verdict','findings'} or None if no key / call failed."""
    key = anthropic_key()
    if not key:
        return None
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=key)
        resp = client.messages.create(
            model=MODEL, max_tokens=4000, thinking={"type": "adaptive"},
            system=system, messages=[{"role": "user", "content": user}],
            output_config={"format": {"type": "json_schema", "schema": _JUDGE_SCHEMA}},
        )
        if getattr(resp, "stop_reason", "") == "refusal":
            return {"verdict": "warn", "findings": ["LLM declined to judge — needs human review"]}
        return _parse_judge(resp)
    except Exception as e:
        return {"verdict": "warn", "findings": [f"LLM judge error: {e}"]}


def llm_image_judge(image_path: Path, question: str) -> dict | None:
    key = anthropic_key()
    if not key:
        return None
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=key)
        media = "image/jpeg" if image_path.suffix.lower() in (".jpg", ".jpeg") else "image/png"
        b64 = base64.standard_b64encode(image_path.read_bytes()).decode()
        resp = client.messages.create(
            model=MODEL, max_tokens=1500, thinking={"type": "adaptive"},
            messages=[{"role": "user", "content": [
                {"type": "image", "source": {"type": "base64", "media_type": media, "data": b64}},
                {"type": "text", "text": question},
            ]}],
            output_config={"format": {"type": "json_schema", "schema": _JUDGE_SCHEMA}},
        )
        if getattr(resp, "stop_reason", "") == "refusal":
            return {"verdict": "warn", "findings": ["LLM declined to judge image — needs human review"]}
        return _parse_judge(resp)
    except Exception as e:
        return {"verdict": "warn", "findings": [f"LLM image judge error: {e}"]}
