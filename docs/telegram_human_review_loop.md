# Telegram Human Review Loop (Approve / Reject / Revise)

After a project passes QA and reaches `READY_FOR_HUMAN_REVIEW`, the owner reviews it
in Telegram and records a decision. **No decision here ever enables upload** —
`upload_allowed` stays `false`; publishing to YouTube remains a separate future gate.

## Architecture

The decision logic is a **pure, token-free module** so it is testable without a bot:

- `tools/review/update_human_decision.py` — `apply_decision()` + `build_review_card()` + CLI.
- `tools/bot/studio_bot.py` — thin Telegram I/O layer that calls the module.

## Decision rules (`apply_decision`)

| Rule | Behaviour |
|---|---|
| authorization | `by != owner` → **refused** (`unauthorized`) |
| valid decision | must be `approve` / `reject` / `revise` |
| approve guard | **refused** unless `gate_status == READY_FOR_HUMAN_REVIEW` (QA passed) |
| reject / revise | allowed in any state |
| upload invariant | `upload_allowed` forced **false** on every decision — never enabled here |

Manifest fields written on a decision (`runtime/<project_id>/human_review_manifest.json`):
`human_decision` (approve/reject/revise), `project_status` (HUMAN_APPROVED / HUMAN_REJECTED /
NEEDS_REVISION), `human_decision_by`, `human_decision_at`, optional `human_decision_reason`,
`upload_allowed` (false).

## Bot commands & buttons (`studio_bot.py`)

| Command / action | Effect |
|---|---|
| `/review <project_id>` | sends the `[AUTOPILOT — NEEDS REVIEW]` card (project_id, title, topic, lang/niche, video path, thumbnail if any, QA status, per-check summary, upload_allowed) + inline buttons |
| inline `✅ Approve` | only shown when `READY_FOR_HUMAN_REVIEW`; sets HUMAN_APPROVED |
| inline `❌ Reject` | sets HUMAN_REJECTED |
| inline `🔁 Revise` | sets NEEDS_REVISION |
| `/status <project_id>` | shows gate/safety/human_decision/project_status/upload_allowed |
| `/status` (no arg) | shows whether a `/make` job is running |

## Safety

- **Owner-only.** Commands accept only the owner chat id; callback (button) clicks check
  `callback_query.from.id == owner` — non-owner clicks are answered "Not authorized" and ignored.
- If a project is **not** `READY_FOR_HUMAN_REVIEW`, the Approve button is not shown and an
  approve attempt is refused (`cannot approve: gate_status=...`).
- A blocked (`BLOCKED_BY_QA`) project shows its status and offers only Reject/Revise.

## Usage / simulate a decision without the bot

```bash
# show the review card
python tools/review/update_human_decision.py --project <id> --show

# apply a decision (owner must match)
python tools/review/update_human_decision.py --project <id> --decision approve --by <owner_id> --owner <owner_id>
python tools/review/update_human_decision.py --project <id> --decision reject  --by <owner_id> --owner <owner_id> --reason "tone"
python tools/review/update_human_decision.py --project <id> --decision revise  --by <owner_id> --owner <owner_id>
# test refusals:
python tools/review/update_human_decision.py --manifest <blocked.json> --decision approve --by 5 --owner 5   # refused (not READY)
python tools/review/update_human_decision.py --project <id> --decision approve --by 999 --owner 5            # refused (unauthorized)
```

The bot (`tools/bot/studio_bot.py`) needs `STUDIO_BOT_TOKEN` to run; the loop is not
deployed to the VPS yet. The decision module works and is tested without a token.
