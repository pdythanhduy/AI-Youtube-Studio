# Telegram Human Review Loop — Implementation Report (Blocker #2)

**Date:** 2026-06-29
**Scope:** Add the owner approve/reject/revise loop after `READY_FOR_HUMAN_REVIEW`.
No YouTube upload, no auto-publish, no weakened QA rules, no Hashima change, no VPS
deploy. Tested token-free (dry-run) — the bot itself needs `STUDIO_BOT_TOKEN` to run.

## Files modified / created
- **created** `tools/review/update_human_decision.py` — pure decision logic + `build_review_card()` + CLI (testable without a bot token).
- **modified** `tools/bot/studio_bot.py` — `/review <id>`, `/status <id>`, inline Approve/Reject/Revise buttons, owner-only callback handling.
- **created** `docs/telegram_human_review_loop.md`, `production/telegram_human_review_loop_report.md`.

## Commands / callbacks added
- `/review <project_id>` → review card + inline buttons (Approve shown only if QA passed).
- `/status <project_id>` → gate/safety/human_decision/project_status/upload_allowed; `/status` → job status.
- Callbacks `approve:<id>` / `reject:<id>` / `revise:<id>` → `apply_decision()` → edits the message to the decision.

## Manifest fields updated on a decision
`human_decision`, `project_status` (HUMAN_APPROVED | HUMAN_REJECTED | NEEDS_REVISION),
`human_decision_by`, `human_decision_at`, optional `human_decision_reason`,
`upload_allowed` (**forced false**).

## State rules
| Decision | project_status | upload_allowed |
|---|---|---|
| approve (only if READY_FOR_HUMAN_REVIEW) | HUMAN_APPROVED | false |
| reject | HUMAN_REJECTED | false |
| revise | NEEDS_REVISION | false |
| approve on BLOCKED_BY_QA | **refused** | false |
| any decision by non-owner | **refused** | false |

## Test results (dry-run, no token, on temp manifests)
| # | Case | Result |
|---|---|---|
| 1 | READY → approve (owner) | `HUMAN_APPROVED`, upload_allowed=False ✅ |
| 2 | READY → reject | `HUMAN_REJECTED`, upload_allowed=False ✅ |
| 3 | READY → revise | `NEEDS_REVISION`, upload_allowed=False ✅ |
| 4 | BLOCKED_BY_QA → approve | **REFUSED** (`cannot approve: gate_status=BLOCKED_BY_QA`), rc=1 ✅ |
| 5 | READY → approve by unknown user (by≠owner) | **REFUSED** (`unauthorized`), rc=1 ✅ |

Bot module imports cleanly (syntax + cross-import); `build_review_card` renders the full
`[AUTOPILOT — NEEDS REVIEW]` card for the test project (`20260628_untitled`).

## Callback / button behaviour
Owner clicks a button → `answerCallbackQuery` ack → `apply_decision()` → on success the
message is edited to `[DECISION] <id> → <project_status> (by owner). upload_allowed=False`;
on refusal the bot replies with the reason. Non-owner clicks → "Not authorized", ignored.

## Remaining blockers before Telegram go-live
3. **Full-scale validation** — run a complete video (all images + all TTS) through the full
   pipeline + gate + review loop (current proof used the 2-asset test project).
4. **M4 go-live** — create `STUDIO_BOT_TOKEN` via @BotFather, deploy `studio_bot.py` on the VPS
   (tmux/systemd), and verify `/review` + buttons live. (YouTube upload remains a separate gate;
   no automation added.)
