# File Lifecycle — AI YouTube Studio OS

Defines how every file in the system is created, validated, updated, passed between stages, and eventually archived. Understanding the lifecycle prevents data loss, version conflicts, and broken pipelines.

---

## Lifecycle Overview

Every project output file passes through these states:

```
[ABSENT] → [PENDING] → [IN_PROGRESS] → [COMPLETE] → [VALIDATED] → [ARCHIVED]
                              ↕
                      [NEEDS_REVISION]
```

| State | Meaning |
|---|---|
| `absent` | File does not yet exist. Stage has not started. |
| `pending` | Stage is queued but not yet executing. |
| `in_progress` | Stage is actively running. File may be partially written. |
| `complete` | Stage finished writing. File exists but not yet validated. |
| `needs_revision` | Validation failed. File exists but contains errors. |
| `validated` | QA engine confirmed the file meets all quality criteria. |
| `archived` | Project published. Files moved to archive. No further writes. |

The `export_manifest.json` tracks the state of every file in the project. The QA engine updates states. No other engine changes state directly.

---

## File Creation Rules

### Rule 1: Atomic Writes
No file is written partially. An engine must complete the full output in memory before writing to disk. A partial file in `in_progress` state that is interrupted must be deleted before the stage is retried — never left in a corrupted state.

### Rule 2: Write Once, Revise Explicitly
A stage output file is written once per run. If the stage is re-run due to revision, the old file is renamed with a `.bak` suffix before the new file is written:
```
research.md        → research.md.bak
research.md (new)  → research.md
```
Only one `.bak` is kept. If a second revision is needed, the `.bak` is overwritten.

### Rule 3: No Stage Skipping
A file cannot be created unless all its upstream dependencies are in `validated` state. The workflow engine must check dependency state before executing any stage.

```
research.md must be validated before source_report.md is created.
research_verified.md must be validated before story_outline.md is created.
story_outline.md must be validated before script.md is created.
script.md must be validated before story_bible.md, storyboard.md, voice_script.txt are created.
[All stage outputs] must be validated before export_manifest.json is set to ready_for_production.
```

### Rule 4: System Files Are Read-Only at Runtime
Files in `core/`, `engine/`, `configs/`, `prompts/`, `templates/`, `knowledge/` (except databases) are read-only during a production run. No engine may write to these directories during pipeline execution. Updates to system files require a manual commit outside of production runs.

---

## File Dependency Graph

```
input.json
    │
    ▼
research.md ──────────────────────────────────────────────┐
    │                                                      │
    ▼                                                      │
source_report.md                                           │
    │                                                      │
    ▼                                                      │
research_verified.md                                       │
    │                                                      │
    ▼                                                      │
story_outline.md                                           │
    │                                                      │
    ▼                                                      │
script.md ──────────────────────────────────────────────  │
    │                  │                   │              │
    ▼                  ▼                   ▼              │
story_bible.md     storyboard.md      voice_script.txt   │
    │                  │               voice_direction.md  │
    └──────────────────┤                   │              │
                       ▼                   ▼              │
                   image_plan.md       subtitles.srt      │
                       │                                   │
                       ▼                                   │
               ai_image_prompts.md                        │
                                                          │
                                   ┌──────────────────────┘
                                   ▼
                           thumbnail_prompt.md
                           seo.md
                               │
                               ▼
                        export_manifest.json
```

---

## State Transition Rules

| Transition | Triggered by | Condition |
|---|---|---|
| `absent` → `pending` | Director engine | All upstream files are `validated` |
| `pending` → `in_progress` | Workflow engine | Stage begins executing |
| `in_progress` → `complete` | Workflow engine | Stage finishes writing output |
| `complete` → `validated` | QA engine | All checklist items pass |
| `complete` → `needs_revision` | QA engine | One or more checklist items fail |
| `needs_revision` → `in_progress` | Director engine | Human or auto-retry approved |
| `validated` → `archived` | Export engine | Project marked as published |

---

## The `export_manifest.json` as Lifecycle Registry

The manifest is updated after every state transition. It is the single source of truth for project state. No engine queries the file system to determine state — all state comes from the manifest.

```json
{
  "project_id": "20260627_disappearance-of-elisa-lam",
  "schema_version": "1.0",
  "status": "in_progress",
  "pipeline_stage": "stage_04",
  "created_at": "2026-06-27T10:00:00Z",
  "updated_at": "2026-06-27T10:45:00Z",
  "assets": {
    "research": {
      "file": "research.md",
      "status": "validated",
      "completed_at": "2026-06-27T10:10:00Z",
      "validated_at": "2026-06-27T10:12:00Z",
      "word_count": 1240,
      "revision_count": 0
    },
    "source_report": {
      "file": "source_report.md",
      "status": "validated",
      "overall_verdict": "needs_revision",
      "flags_count": 2,
      "fails_count": 0,
      "completed_at": "2026-06-27T10:15:00Z",
      "validated_at": "2026-06-27T10:16:00Z"
    },
    "research_verified": {
      "file": "research_verified.md",
      "status": "validated"
    },
    "story_outline": {
      "file": "story_outline.md",
      "status": "validated"
    },
    "script": {
      "file": "script.md",
      "status": "in_progress",
      "started_at": "2026-06-27T10:43:00Z"
    },
    "story_bible": { "file": "story_bible.md", "status": "pending" },
    "storyboard": { "file": "storyboard.md", "status": "absent" },
    "image_plan": { "file": "image_plan.md", "status": "absent" },
    "ai_image_prompts": { "file": "ai_image_prompts.md", "status": "absent" },
    "voice_script": { "file": "voice_script.txt", "status": "absent" },
    "voice_direction": { "file": "voice_direction.md", "status": "absent" },
    "subtitles": { "file": "subtitles.srt", "status": "absent" },
    "thumbnail_prompt": { "file": "thumbnail_prompt.md", "status": "absent" },
    "seo": { "file": "seo.md", "status": "absent" }
  }
}
```

---

## Revision Handling

When the QA engine marks a file as `needs_revision`, the following happens:

1. **QA engine writes a `[filename]_qa_report.md`** in the project folder with specific failure details.
2. **Director engine evaluates** whether to auto-retry or halt for human review.
3. **Auto-retry conditions** (director engine retries automatically):
   - Word count out of range by ≤15%
   - Pacing markers missing from voice_script
   - SRT timecodes out of sequence (fixable algorithmically)
   - Tag count under minimum (add more tags)
4. **Human review conditions** (pipeline halts, human must approve before continuing):
   - Fabricated URLs detected in research
   - [FAIL] rating in source_report
   - Script contains facts not in research_verified.md
   - Export manifest overall status cannot reach `ready_for_production`
5. **Maximum auto-retry count:** 2 per file per run. After 2 failed retries, always escalate to human.

---

## Archive Policy

After a video is published on YouTube:

1. The `export_manifest.json` status is updated to `archived`.
2. All project files are moved to: `projects/archive/YYYYMMDD_topic-slug/`
3. Key metadata (word counts, image counts, SEO title, publish date) is written to `knowledge/memory_database.md` for cross-project learning.
4. The working project folder `projects/YYYYMMDD_topic-slug/` is removed.
5. The `.bak` files are permanently deleted at archive time.

Archive is permanent. Archived files are not modified.

---

## Temporary Files

Temporary files generated during processing (intermediate outputs, debug logs, partial renders) must:
- Use the `.tmp` extension: `script.md.tmp`
- Live in the project folder only — never in system directories
- Be deleted by the engine that created them before the stage is marked `complete`
- Never appear in `export_manifest.json`

If a `.tmp` file exists in a project folder at startup, the director engine treats it as evidence of an interrupted run and triggers recovery mode before proceeding.
