# Autopilot Safety & QA Gate

A mandatory check layer between autopilot **generation** and **delivery/publish**. No
autopilot output may be marked READY, sent to Telegram for approval, or considered
publishable until it passes these checks and a human approves. The gate **never
uploads and never auto-approves**; `upload_allowed` stays `false` until a separate,
explicit user upload approval.

It is purely additive — it does not modify the orchestrator, render, or asset tools,
the Hashima locked project, or any existing contract.

## Modules (`tools/qa/`)

| Module | Responsibility |
|---|---|
| `_common.py` | shared helpers: `.env` load, paths, result schema, ffmpeg/ffprobe, Claude text + vision judges, clickbait/gore phrase lists |
| `source_check.py` | research.md exists; ≥3 named sources / URLs; Sources section; stage-2 verification; (LLM) no fabricated sources / unsupported core claims |
| `script_check.py` | script.md exists; clickbait/fake-shock & gore phrasing scan; (LLM) claims grounded in research, no horror exaggeration, sensitive/historical content factual & respectful |
| `image_policy_check.py` | images exist; DRAMATIZATION labels present; no near-black placeholder images; (LLM vision) no identifiable real faces, no gore/corpses/victims/suffering, nothing disrespectful |
| `render_check.py` | TTS audio decodes + valid duration; rough video exists + decodes cleanly (`ffmpeg -f null`); thumbnail present **iff** publish requested |
| `final_gate.py` | runs all four, writes the human-review manifest, enforces the READY rule, prints a summary |

Each check returns `{check, status, findings[], details{}}` with `status ∈ pass|warn|fail`.
- **pass** meets policy · **warn** needs human attention / could not auto-verify · **fail** violates policy.

## Deterministic vs semantic

Deterministic checks (files, source counts, phrase scans, DRAMATIZATION labels,
near-black detection, audio/video integrity, thumbnail) always run. Semantic checks
(claim-grounding, exaggeration, respect, faces/gore) use a **Claude judge** (text +
vision) when `ANTHROPIC` key is present. With `--no-llm` those return **WARN
("needs human review")**, never a false pass — so the gate never reports READY on
unverified semantic safety.

## The READY rule

```
gate_status = READY_FOR_HUMAN_REVIEW   iff  every check == pass   (automatic_checks_passed)
              BLOCKED                  if   any check == fail
              NEEDS_REVIEW             if   warns but no fail
```
Even at READY_FOR_HUMAN_REVIEW the output is only *ready for a human to review* — a
human must set `human_decision = "approve"`, and `upload_allowed` remains `false`
until a separate explicit user upload approval. The gate produces no public action.

## Human review manifest

Written to `runtime/<project_id>/human_review_manifest.json`:
`project_id, title, topic, generated_files, source_status, script_status, image_status,
render_status, safety_status, automatic_checks_passed, gate_status, publish_readiness,
required_human_decision (approve|review|revise), human_decision (null until a human sets it),
upload_allowed (false), checks{...}`.

## Usage

```bash
# full gate (semantic LLM checks on) — writes the manifest
python tools/qa/final_gate.py --project <project_id>

# fast structural-only (no API cost; semantic checks -> WARN)
python tools/qa/final_gate.py --project <project_id> --no-llm

# publish package (also require a thumbnail)
python tools/qa/final_gate.py --project <project_id> --publish

# run a single check standalone
python tools/qa/script_check.py --project <project_id>
```
Exit code is non-zero if any check fails (CI / automation friendly).

## Where it sits in the autopilot

`run_all.py` (text → images → TTS → render) should call `final_gate.py` **before**
the delivery step; deliver to Telegram only at `automatic_checks_passed` (for human
review), and never set `upload_allowed=true` without explicit per-action user approval.
(Wiring the gate into run_all and the Telegram approve/reject loop is a follow-up.)
