# Autopilot Safety Gate — Integration into run_all.py (Report)

**Date:** 2026-06-29
**Scope:** Blocker #1 only — wire `tools/qa/final_gate.py` into the main autopilot
(`tools/run_all.py`) so no project is delivered to Telegram or marked READY unless the
gate passes. No Hashima change, no YouTube upload, no auto-publish, no weakened rules.

## Files modified
- `tools/run_all.py` — gate integrated as step 5/6; new `--skip-qa` / `--qa-no-llm` dev flags; state machine; blocked-delivery logic.
- `docs/autopilot_safety_gate.md` — added the "Where it sits / WIRED" section (flags + state-machine table).
- `production/autopilot_safety_gate_integration_report.md` — this file.
(`tools/qa/*` unchanged from the gate build.)

## Where final_gate is called
Pipeline order in `run_all.py`:
```
1 TEXT → 2 IMAGES → 3 TTS → 4 RENDER → 5 QA GATE (final_gate.py) → 6 DELIVER
```
The gate runs **after render, before any delivery**, and before any READY status is
exposed. It writes `runtime/<project_id>/human_review_manifest.json`; if no manifest is
produced, `run_all` aborts (no silent fallthrough). Non-passing checks are logged by name.

## READY / state-machine rules
| Gate outcome | `project_status` | Delivery | `upload_allowed` |
|---|---|---|---|
| all checks **pass** | `READY_FOR_HUMAN_REVIEW` | allowed — caption `[AUTOPILOT — NEEDS REVIEW]` | **false** |
| **warn / needs_review** | `BLOCKED_BY_QA` | blocked (logged) | **false** |
| **fail** | `BLOCKED_BY_QA` | blocked (logged) | **false** |
| `--skip-qa` (dev) | `UNVERIFIED_QA_SKIPPED` | never delivered | **false** |

`run_all` never sets `upload_allowed=true` and never uploads. Telegram delivery is for
human review only; publishing stays a separate explicit user action.

## Verification (3 paths)
1. **Forced FAIL** — a synthetic project (no sources, clickbait script `shocking`/`一夜で`,
   near-black image, no audio/video) → gate `BLOCKED`, all four checks FAIL, `upload_allowed=false`.
   Confirms the gate detects violations (incl. near-black-card detection).
2. **Blocked path (run_all, `--qa-no-llm`)** — semantic checks WARN → `gate_status=NEEDS_REVIEW`
   → `project_status=BLOCKED_BY_QA` → **"DELIVERY BLOCKED — Nothing sent to Telegram"**, non-passing
   checks logged. Confirms delivery is blocked whenever the gate is not PASS.
3. **PASS path (run_all, full LLM gate)** on `20260628_untitled` — source/script/image/render all PASS
   (LLM confirmed real sources, grounded & respectful forced-labor handling, no faces/gore) →
   `project_status=READY_FOR_HUMAN_REVIEW` → step 6/6 delivered the review video to Telegram (Drive
   link), `upload_allowed=false`.

## Commands
```
# full autopilot WITH mandatory QA (default):
python tools/run_all.py --topic "<topic>" --niche japanese_mystery --language ja --deliver
python tools/run_all.py --project <project_id> --deliver

# QA-only on an existing project (writes the manifest, no pipeline run):
python tools/qa/final_gate.py --project <project_id>
python tools/qa/final_gate.py --project <project_id> --no-llm   # fast, structural-only

# dev flags (do not ship):
python tools/run_all.py --project <id> --qa-no-llm --deliver    # structural QA → blocked
python tools/run_all.py --project <id> --skip-qa                # skip QA, delivery disabled
```

## Remaining blockers before Telegram go-live
2. **Approve/reject loop** — Telegram bot lets the owner set `human_decision` in the manifest;
   only an approved project is treated as approved; `upload_allowed` still needs a separate explicit
   upload approval. (Not done.)
3. **Full-scale validation** — exercise the gate on a complete video (all images + all TTS), not the
   2-asset proof. (Not done.)
4. **M4 go-live** — create `STUDIO_BOT_TOKEN` (BotFather), deploy `studio_bot.py` on the VPS.

Blocker #1 (gate integration) is complete and verified.
