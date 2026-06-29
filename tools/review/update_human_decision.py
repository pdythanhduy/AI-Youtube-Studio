#!/usr/bin/env python3
"""Human-review decision logic for the autopilot (pure, token-free, testable).

The Telegram bot is a thin I/O layer; the decision rules + safety live here so they
can be unit-tested via CLI without a bot token. Applies an owner decision
(approve/reject/revise) to runtime/<project_id>/human_review_manifest.json.

HARD RULES enforced here:
- Only the owner may decide (by == owner), else 'unauthorized'.
- decision must be approve | reject | revise.
- APPROVE is refused unless gate_status == READY_FOR_HUMAN_REVIEW (i.e. QA passed).
  reject/revise are allowed in any state.
- upload_allowed is ALWAYS forced false here — no human-review decision can ever
  enable upload. Publishing remains a separate, future, explicit gate.

CLI (for tests / manual):
  python tools/review/update_human_decision.py --project <id> --decision approve --by 5 --owner 5
  python tools/review/update_human_decision.py --project <id> --show
  # tests can target a specific manifest file:
  python tools/review/update_human_decision.py --manifest <path> --decision reject --by 5 --owner 5
"""
from __future__ import annotations
import argparse, io, json, sys, time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
RUNTIME = REPO / "runtime"
PROJECTS = REPO / "projects"

DECISION_STATUS = {"approve": "HUMAN_APPROVED", "reject": "HUMAN_REJECTED", "revise": "NEEDS_REVISION"}


def manifest_path(pid: str) -> Path:
    return RUNTIME / Path(pid).name / "human_review_manifest.json"


def load_manifest(path: Path) -> dict:
    return json.loads(io.open(path, encoding="utf-8").read())


def apply_decision(decision: str, by, owner, project_id: str | None = None,
                   reason: str | None = None, mf_path: Path | None = None) -> dict:
    """Apply a human decision. Returns {ok, error, project_status, manifest}."""
    if str(by) != str(owner):
        return {"ok": False, "error": "unauthorized: only the owner may approve/reject/revise"}
    if decision not in DECISION_STATUS:
        return {"ok": False, "error": f"invalid decision '{decision}' (use approve|reject|revise)"}
    path = mf_path or (manifest_path(project_id) if project_id else None)
    if not path or not Path(path).exists():
        return {"ok": False, "error": f"manifest not found: {path}"}
    path = Path(path)
    m = load_manifest(path)

    if decision == "approve" and m.get("gate_status") != "READY_FOR_HUMAN_REVIEW":
        return {"ok": False,
                "error": f"cannot approve: gate_status={m.get('gate_status')} (QA not passed). "
                         f"safety_status={m.get('safety_status')}.",
                "project_status": m.get("gate_status"), "manifest": m}

    m["human_decision"] = decision
    m["project_status"] = DECISION_STATUS[decision]
    m["human_decision_by"] = str(by)
    m["human_decision_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    if reason:
        m["human_decision_reason"] = reason
    m["upload_allowed"] = False  # invariant — never enabled by human review
    path.write_text(json.dumps(m, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"ok": True, "error": None, "project_status": m["project_status"], "manifest": m}


def build_review_card(project_id: str, m: dict | None = None) -> str:
    """Telegram-ready review card text for a project."""
    pid = Path(project_id).name
    if m is None:
        p = manifest_path(pid)
        m = load_manifest(p) if p.exists() else {}
    proj = PROJECTS / pid
    # language / niche from input.json (not in manifest)
    lang = niche = "?"
    inp = proj / "input.json"
    if inp.exists():
        try:
            d = json.loads(inp.read_text(encoding="utf-8"))
            lang, niche = d.get("language", "?"), d.get("niche", "?")
        except Exception:
            pass
    vids = sorted((proj / "export" / "rough").glob("*_rough.mp4"))
    thumbs = sorted((proj / "export" / "thumbnail").glob("*.jpg")) + \
        sorted((proj / "export" / "thumbnail").glob("*.png"))
    checklist = " | ".join(f"{k.replace('_status','')}:{m.get(k,'?')}"
                           for k in ("source_status", "script_status", "image_status", "render_status"))
    lines = [
        "[AUTOPILOT — NEEDS REVIEW]",
        f"project_id : {pid}",
        f"title      : {m.get('title', pid)}",
        f"topic      : {m.get('topic', '')}",
        f"lang/niche : {lang} / {niche}",
        f"video      : {vids[-1].relative_to(REPO) if vids else '(none)'}",
        f"thumbnail  : {thumbs[-1].relative_to(REPO) if thumbs else '(none — not required)'}",
        f"QA status  : safety={m.get('safety_status','?')}  gate={m.get('gate_status','?')}",
        f"checks     : {checklist}",
        f"upload_allowed: {m.get('upload_allowed', False)}",
        "",
        "Decide: ✅ Approve · ❌ Reject · 🔁 Revise  (approve only if QA passed; upload stays gated)",
    ]
    return "\n".join(lines)


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="Apply / show a human-review decision")
    ap.add_argument("--project")
    ap.add_argument("--manifest", help="explicit manifest path (tests)")
    ap.add_argument("--decision", choices=list(DECISION_STATUS))
    ap.add_argument("--by")
    ap.add_argument("--owner")
    ap.add_argument("--reason")
    ap.add_argument("--show", action="store_true", help="print the review card and exit")
    a = ap.parse_args()
    if a.show:
        print(build_review_card(a.project))
        return 0
    if not a.decision:
        ap.error("--decision required (or use --show)")
    res = apply_decision(a.decision, a.by, a.owner, project_id=a.project, reason=a.reason,
                         mf_path=Path(a.manifest) if a.manifest else None)
    if res["ok"]:
        print(f"OK  decision={a.decision}  project_status={res['project_status']}  "
              f"upload_allowed={res['manifest']['upload_allowed']}")
        return 0
    print(f"REFUSED  {res['error']}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
