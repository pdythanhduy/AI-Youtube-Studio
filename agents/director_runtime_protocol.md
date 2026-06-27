# Director Runtime Protocol — AI YouTube Studio OS

Defines the runtime behavior of the Director AI during pipeline execution: how it tracks state, formats logs, updates the manifest, communicates progress, and handles the stage dispatch cycle.

---

## Runtime State

The Director AI maintains internal state across the entire pipeline session. This state is reflected in `export_manifest.json` after every stage. State is never assumed — it is always derived from reading the manifest.

### Pipeline State Model

```
PIPELINE STATE
├── project_slug        string     — project identifier
├── current_stage       int        — 0-12
├── pipeline_status     enum       — booting / running / paused / failed / complete
├── stages_complete     int[]      — list of completed stage numbers
├── stages_failed       int[]      — list of failed stage numbers
├── warnings            string[]   — accumulated non-critical warnings
├── word_count_target   int        — DURATION_MINUTES × 130
└── run_start_time      datetime   — when pipeline began
```

---

## Manifest Update Protocol

The Director AI updates `export/export_manifest.json` after every stage event.

### Update After Stage Start

When a stage begins execution:
```json
{
  "pipeline_stage": "stage_NN",
  "updated_at": "{current_datetime}",
  "assets": {
    "{asset_name}": { "status": "in_progress", "started_at": "{datetime}" }
  }
}
```

### Update After Stage Complete

When a stage writes its output file(s):
```json
{
  "updated_at": "{current_datetime}",
  "assets": {
    "{asset_name}": {
      "status": "complete",
      "completed_at": "{datetime}",
      "file_path": "{subfolder/filename}"
    }
  }
}
```

### Update After Stage Validated

When the stage checklist passes:
```json
{
  "assets": {
    "{asset_name}": {
      "status": "validated",
      "validated_at": "{datetime}",
      "checklist_score": "{N}/{total}"
    }
  }
}
```

### Update on Stage Failure

When a stage fails a critical check:
```json
{
  "status": "needs_revision",
  "pipeline_stage": "stage_NN",
  "halt_reason": "{specific reason}",
  "halt_at": "{datetime}",
  "assets": {
    "{asset_name}": {
      "status": "needs_revision",
      "failure_reason": "{specific check that failed}"
    }
  }
}
```

---

## Director Run Log Format

`logs/director_run_log.md` is initialized at Stage 0 and updated throughout the pipeline.

### Log Header (written at Stage 0)

```markdown
# Director Run Log
**Project:** {project_slug}
**Topic:** {topic}
**Language:** {language}
**Duration target:** {duration_minutes} min
**Style:** {style}
**Pipeline started:** {ISO datetime}
**Director AI version:** v1.0

---
```

### Stage Entry Format

For every stage, append an entry:

```markdown
## Stage {N} — {Stage Name}
**Started:** {ISO datetime}
**Status:** {COMPLETE / FAILED / SKIPPED}
**Duration:** {seconds or "N/A"}

**Output files written:**
- {subfolder/filename.ext}

**Checklist result:** {N}/{total} passed

**Warnings:**
- {Any warnings, or "None"}

**Notes:**
- {Any decisions made, flags raised, or notable observations}

---
```

### Stage Log File Format

Each stage also writes its own dedicated log: `logs/stage_NN_name.log`

```
[{ISO datetime}] STAGE {N} — {STAGE NAME} — STARTED
[{ISO datetime}] Reading prompt: prompts/NN_name.md
[{ISO datetime}] Reading context: {list of input files}
[{ISO datetime}] Applying template: {template name}, section: Stage Addendum stage_NN
[{ISO datetime}] Resolving placeholders: {N} placeholders resolved
[{ISO datetime}] Generating output...
[{ISO datetime}] Output written: {subfolder/filename}
[{ISO datetime}] Running checklist ({N} items)...
[{ISO datetime}] Checklist: {item 1} — PASS
[{ISO datetime}] Checklist: {item 2} — PASS
[{ISO datetime}] Checklist: {item 3} — WARN: {detail}
[{ISO datetime}] Checklist complete: {N}/{total} passed
[{ISO datetime}] Manifest updated: {asset_name}.status = validated
[{ISO datetime}] STAGE {N} — COMPLETE
```

---

## Stage Dispatch Cycle

For every stage N from 0 to 12, the Director follows this exact cycle:

```
DISPATCH CYCLE for Stage N:

1. ANNOUNCE: Print stage banner
2. CHECK DEPENDENCIES: Verify all prerequisite files exist
   → If any prerequisite missing: HALT with dependency error
3. READ PROMPT: Load prompts/NN_name.md (if applicable)
4. READ TEMPLATE ADDENDUM: Load stage_NN section from template file (if applicable)
5. LOAD CONTEXT: Read all input files for this stage
6. RESOLVE PLACEHOLDERS: Replace all {vars} in prompt
7. MARK STARTED: Update manifest asset status to "in_progress"
8. EXECUTE: Generate stage output
9. WRITE OUTPUT: Write files to project subfolder (atomic: write to .tmp first, then rename)
10. RUN CHECKLIST: Evaluate all items from director_project_checklist.md for this stage
11. LOG: Write stage entry to director_run_log.md and stage-specific log file
12. EVALUATE: 
    → If all critical checks PASS: update manifest to "validated", advance to Stage N+1
    → If any critical check FAILS: update manifest to "needs_revision", HALT
    → If only warnings: update manifest to "validated" with warning flag, advance
13. ANNOUNCE COMPLETE: Print stage complete summary
```

---

## Progress Reporting Format

The Director reports progress in a consistent, readable format throughout the pipeline.

### Stage Banner
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STAGE {N} — {STAGE NAME}
Project: {project_slug}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Stage Progress Line
```
[Stage {N}] Reading {file}...
[Stage {N}] Generating {output_type}...
[Stage {N}] Writing {filename}...
[Stage {N}] Running checklist ({N} items)...
```

### Stage Complete Summary
```
[STAGE {N} COMPLETE]
Output:     {list of files written}
Checklist:  {N}/{total} passed
Warnings:   {N} (see log)
Status:     {PASS / FLAGGED / FAIL}
──────────────────────────────────────────────
```

### Warning Format
```
[WARNING - Stage {N}] {Description of warning}
Action: {What was done: logged / flagged / skipped}
Impact: {None / Minor / Will need human review}
```

### Critical Failure Format
```
⛔ CRITICAL FAILURE — Stage {N}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Failed check: {exact check name}
File:         {exact file path}
Issue:        {specific description of the problem}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PIPELINE HALTED.

Required action: {Exact steps the human must take to resolve}
Resume: Re-run Director AI after resolving. The pipeline will
        detect completed stages and resume from Stage {N}.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Resume Protocol

If the pipeline is interrupted (by a critical failure, a human stopping it, or a session timeout), it can be resumed.

When the Director AI is re-activated for a project that has an existing `export_manifest.json`:

1. Read the manifest
2. Find the earliest stage where any asset status is NOT `validated`
3. Check if the `.tmp` file exists for that stage (evidence of interrupted write)
4. If `.tmp` exists: delete it, set that stage's asset status back to `absent`
5. Announce: `[RESUME] Resuming from Stage {N}. Stages 0-{N-1} already complete.`
6. Continue from that stage

The resume detection trigger phrase is:
```
RESUME PROJECT: {project_slug}
```

When the human types this, the Director reads the existing manifest and resumes automatically.

---

## Dependency Map

The Director uses this map to verify prerequisites before each stage:

| Stage | Required files before starting |
|---|---|
| Stage 0 | Valid input (4 fields) |
| Stage 1 | `input/input.json` |
| Stage 2 | `research/research.md` |
| Stage 3 | `research/research_verified.md` |
| Stage 4 | `script/story_outline.md` + `research/research_verified.md` |
| Stage 5 | `script/script.md` + `research/research_verified.md` |
| Stage 6 | `script/script.md` + `script/story_bible.md` |
| Stage 7 | `visuals/storyboard.md` + `script/story_bible.md` |
| Stage 8 | `visuals/storyboard.md` + `visuals/image_plan.md` + `script/story_bible.md` |
| Stage 9 | `script/script.md` + `script/story_bible.md` + `script/story_outline.md` |
| Stage 10 | `script/script.md` + `research/research_verified.md` + `script/story_bible.md` + `script/story_outline.md` |
| Stage 11 | All previous stage outputs |
| Stage 12 | `logs/qa_report.md` with verdict `READY_FOR_EXPORT` |

If a required file is missing when a stage begins, this is a **dependency error** — not a content error. The pipeline halts with:
```
⛔ DEPENDENCY ERROR — Stage {N}
Missing required file: {filepath}
This file should have been created in Stage {M}.
Action: Re-run Stage {M}, then resume.
```

---

## Placeholder Resolution Reference

All `{placeholders}` in prompt files are resolved before the AI call:

| Placeholder | Source |
|---|---|
| `{topic}` | `input/input.json` → `topic` |
| `{language}` | `input/input.json` → `language` |
| `{style}` | `input/input.json` → `style` |
| `{niche}` | `input/input.json` → `niche` |
| `{project_slug}` | `input/input.json` → `project_id` |
| `{video_length_minutes}` | `input/input.json` → `video_length_minutes` |
| `{channel_name}` | `input/input.json` → `channel_name` (or empty string) |
| `{target_words}` | `input/input.json` → `target_word_count` |
| `{min_words}` | `target_words × 0.90` |
| `{max_words}` | `target_words × 1.10` |
| `{notes}` | `input/input.json` → `notes` (or empty string) |

Any unresolved placeholder causes a `[WARNING]` in the log. If the placeholder is required for the stage (e.g., `{topic}` in research), it causes a CRITICAL FAILURE.
