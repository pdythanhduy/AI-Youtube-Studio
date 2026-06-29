# Autopilot Safety & QA Gate — Implementation Report

**Date:** 2026-06-29
**Scope:** Add a mandatory automatic QA/safety gate + human-approval manifest between
autopilot generation and delivery/publish. Purely additive — no change to the
orchestrator/render/asset tools, the Hashima locked project, or existing contracts.
No upload performed; Telegram bot not deployed.

---

## Files created

| File | Role |
|---|---|
| `tools/qa/_common.py` | shared helpers: .env load, paths, result schema, ffmpeg/ffprobe, Claude text + vision judges, clickbait/gore phrase lists |
| `tools/qa/source_check.py` | research sources & citations |
| `tools/qa/script_check.py` | script/narration: grounding, no fake-shock/horror, respectful sensitive content |
| `tools/qa/image_policy_check.py` | DRAMATIZATION labels, no black placeholders, vision: no faces/gore/victims |
| `tools/qa/render_check.py` | audio + video integrity, thumbnail (if publishing) |
| `tools/qa/final_gate.py` | runs all four → human-review manifest → enforces READY rule |
| `docs/autopilot_safety_gate.md` | design & usage doc |
| `runtime/<project_id>/human_review_manifest.json` | per-run human approval manifest (written by the gate) |

## Checks implemented

- required files exist (10 text outputs + images + audio + video presence)
- source citations exist (≥3 named sources / URLs; Sources section; stage-2 verification)
- no unsupported claims / no fabricated sources — **LLM** (script grounded against research)
- no fake "shocking" claims, no horror exaggeration — keyword scan + **LLM**
- no victim / gore / suffering imagery — phrase scan + **LLM vision per image**
- no real-person-face misuse — **LLM vision per image**
- sensitive historical content treated respectfully (forced labor / victims / tragedy) — **LLM**
- no black placeholder images (near-black detection via PIL brightness/stddev)
- audio exists and duration is valid (ffprobe per segment)
- rendered video exists and decodes cleanly (`ffmpeg -v error -f null`)
- thumbnail exists **iff** a publish package is requested (`--publish`)

Deterministic checks always run; semantic checks use Claude (Opus 4.8) when the
`ANTHROPIC` key is present, else return WARN ("needs human review") — never a false pass.

## Result on the latest test project (`20260628_untitled`, auto-generated 軍艦島 documentary)

Full gate (LLM on):

| Check | Status | Notes |
|---|---|---|
| source | **PASS** | facts real & named-sourced; no fabricated URLs. Minor: many sources are tourism sites, few primary/academic. |
| script | **PASS** | claims grounded in research; forced-labor topic neutral & respectful (both sides, no asserted numbers); no clickbait/horror; `[Unverified]` items honestly marked. |
| image | **PASS** | vision on both beat images: no identifiable faces, no gore/victims. |
| render | **PASS** | 2 audio segments valid; rough video decodes cleanly. (No thumbnail — not required without `--publish`.) |

`safety_status = pass` · `automatic_checks_passed = true` · `gate_status = READY_FOR_HUMAN_REVIEW`
· `required_human_decision = approve` · **`upload_allowed = false`**.

Structural-only run (`--no-llm`) returns `NEEDS_REVIEW` (semantic checks → WARN), confirming the
gate refuses to report READY without the semantic safety pass.

## READY rule (enforced by `final_gate.py`)

Output is **READY_FOR_HUMAN_REVIEW** only when every automatic check passes. A human must then set
`human_decision = "approve"` in the manifest, and `upload_allowed` stays **false** until a separate,
explicit per-action user upload approval. The gate never uploads and never auto-approves.

## Dry-run command

```
python tools/qa/final_gate.py --project 20260628_untitled
# fast structural-only (no API cost):
python tools/qa/final_gate.py --project 20260628_untitled --no-llm
```

## Remaining blockers before Telegram go-live

1. **Wire the gate into `run_all.py`** — call `final_gate.py` after render and **before** delivery;
   deliver to Telegram only when `automatic_checks_passed` (for human review), never auto-publish.
2. **Human approve/reject loop** — the Telegram bot must let the owner set `human_decision` and only
   then treat the video as approved; `upload_allowed` still needs a separate explicit upload approval.
3. **Full-scale validation** — current test had 2 images / 2 audio segments; run a complete video
   (all assets) through the gate before trusting it in production.
4. (M4 go-live, unchanged) create `STUDIO_BOT_TOKEN` via BotFather, deploy bot on VPS.

The gate itself is complete and verified; items above are integration/deployment, not gate work.
