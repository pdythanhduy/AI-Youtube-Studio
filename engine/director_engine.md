# Director Engine — AI YouTube Studio OS

The Director Engine is the top-level orchestrator of the entire production pipeline. It owns the run lifecycle: it starts runs, sequences stages, monitors progress, handles failures, and shuts down cleanly. Every other engine reports to the Director. No engine communicates directly with another engine — all inter-engine communication flows through the Director.

---

## Responsibility

The Director Engine is responsible for **what happens** and **in what order**. It does not perform any content generation itself — that belongs to the Workflow Engine. It does not validate content — that belongs to the QA Engine. It decides: what stage runs next, what to do when a stage fails, and when the pipeline is complete.

**Single sentence:** The Director Engine is the project manager — it delegates all work and oversees the result.

---

## Inputs

| Input | Source | Description |
|---|---|---|
| `input.json` | `projects/{slug}/` | User-provided production parameters |
| `export_manifest.json` | `projects/{slug}/` | Current pipeline state (created by Director on first run) |
| `configs/configuration_system.md` | `configs/` | Global system settings |
| Engine status responses | All engines | Result signals after each stage |

---

## Outputs

| Output | Destination | Description |
|---|---|---|
| `export_manifest.json` (created) | `projects/{slug}/` | Initialized manifest on new run |
| `export_manifest.json` (updated) | `projects/{slug}/` | State updated after each stage |
| Stage dispatch signals | Workflow Engine | Instructions to execute a specific stage |
| Halt signals | All engines | Stop signal on unrecoverable failure |
| Archive signals | Export Engine | Trigger archival on completion |

---

## Dependencies

| Dependency | Type | Purpose |
|---|---|---|
| Workflow Engine | downstream | Executes individual stages |
| QA Engine | downstream | Validates stage outputs |
| Memory Engine | downstream | Logs run metadata |
| Analytics Engine | downstream | Records timing and metrics |
| Export Engine | downstream | Triggers final packaging |
| `core/file_lifecycle.md` | reference | State transition rules |
| `core/naming_conventions.md` | reference | Canonical file names |

---

## Behavior Specification

### On New Run (no existing manifest)

1. Read and validate `input.json` — check all required fields, types, and enum values.
2. If `input.json` is invalid: halt immediately, return specific validation error. Do not create a manifest.
3. Create `export_manifest.json` with all asset statuses set to `absent`.
4. Set pipeline stage to `stage_01`.
5. Dispatch `stage_01` to Workflow Engine.

### On Resume Run (manifest exists)

1. Read `export_manifest.json`.
2. Find the earliest stage that is not `validated`.
3. If any `.tmp` files exist: enter recovery mode.
   - Recovery mode: delete all `.tmp` files, set `in_progress` assets back to `pending`, resume from that stage.
4. Dispatch the earliest non-validated stage to Workflow Engine.

### Stage Sequencing Logic

```
For each stage in pipeline order (stage_01 through stage_10):
  Check dependency states (from manifest)
  If all dependencies are "validated":
    Dispatch stage to Workflow Engine
    Wait for completion signal
    If signal = "complete":
      Dispatch stage to QA Engine for validation
      Wait for validation signal
      If validation = "pass":
        Update manifest: set asset status to "validated"
        Continue to next stage
      If validation = "fail":
        Evaluate failure severity:
          If auto-recoverable:
            Increment retry count
            If retry count ≤ 2: re-dispatch stage to Workflow Engine
            If retry count > 2: halt, request human review
          If not auto-recoverable:
            Halt pipeline
            Write failure details to manifest
            Notify operator
    If signal = "error":
      Write error to manifest
      Halt pipeline
      Notify operator
  Else:
    Dependencies not met — this should not happen if sequencing is correct
    Log anomaly, halt
```

### Completion

When all stages are `validated`:
1. Set manifest top-level `status` to `ready_for_production`.
2. Dispatch to Export Engine for final packaging.
3. Dispatch to Analytics Engine for run summary.
4. Dispatch to Memory Engine for cross-project data extraction.

### Failure Classification

| Failure Type | Auto-Retry? | Halt? | Escalate to Human? |
|---|---|---|---|
| Word count out of range ≤15% | Yes (up to 2x) | No | Only if 2 retries fail |
| Missing pacing markers | Yes (up to 2x) | No | Only if 2 retries fail |
| Fabricated URL detected | No | Yes | Yes — immediately |
| Source report: FAIL verdict | No | Yes | Yes — immediately |
| Script fact not in research | No | Yes | Yes — immediately |
| SRT timecode error | Yes (up to 2x) | No | Only if 2 retries fail |
| Missing required field in input.json | No | Yes | Yes — before pipeline starts |
| Engine runtime error | No | Yes | Yes — with error log |

---

## Interface Contract

The Director Engine communicates via structured signals (future implementation will use a message queue or event bus):

### Dispatch Signal (Director → Workflow Engine)
```json
{
  "signal": "execute_stage",
  "stage_id": "stage_04",
  "project_slug": "20260627_topic",
  "prompt_file": "prompts/04_script_writer.md",
  "template_file": "templates/mystery_template.md",
  "config_overrides": {}
}
```

### Completion Signal (Workflow Engine → Director)
```json
{
  "signal": "stage_complete",
  "stage_id": "stage_04",
  "project_slug": "20260627_topic",
  "output_file": "script.md",
  "word_count": 1547,
  "duration_seconds": 42
}
```

### Validation Signal (QA Engine → Director)
```json
{
  "signal": "validation_result",
  "stage_id": "stage_04",
  "project_slug": "20260627_topic",
  "result": "pass",
  "checklist_items": 14,
  "passed": 14,
  "failed": 0,
  "flags": []
}
```

---

## Future Automation Points

| Point | Description |
|---|---|
| MCP integration | Director Engine becomes an MCP server — Claude Code agents invoke it via tool calls |
| Parallel stage execution | Independent stages (image_plan + voice_script) run concurrently when dependencies allow |
| Priority queue | Multiple projects queued and dispatched by priority |
| Human approval gate | Configurable checkpoints where Director waits for explicit human sign-off |
| Webhook notifications | Director sends Slack/email/webhook on completion or failure |
| Rollback | Director can roll back to any previous validated state |
