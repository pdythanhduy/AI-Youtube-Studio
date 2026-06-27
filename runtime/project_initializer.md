# Project Initializer — Stage 0 Executor

Handles Stage 0: Project Setup. Creates the project folder, writes all initialization files, and initializes the manifest and run log. Called by `pipeline_executor.md` when N = 0.

---

## EXECUTION PROCEDURE

```
function execute():

  // 1. Create project directory tree
  create_directories()

  // 2. Write input.json
  write_input_json()

  // 3. Copy and fill project.yaml
  write_project_yaml()

  // 4. Write initial export_manifest.json
  write_initial_manifest()

  // 5. Initialize director_run_log.md
  write_run_log_header()

  // 6. Run Stage 0 checklist
  result = run_stage0_checklist()

  // 7. Announce complete
  output_stage_complete(0, result)

  return result
```

---

## STEP 1: CREATE DIRECTORIES

Create the following paths under `projects/{project_slug}/`:

```
projects/{project_slug}/
projects/{project_slug}/input/
projects/{project_slug}/research/
projects/{project_slug}/script/
projects/{project_slug}/visuals/
projects/{project_slug}/voice/
projects/{project_slug}/seo/
projects/{project_slug}/export/
projects/{project_slug}/logs/
```

If `projects/{project_slug}/` already exists: this is a resume — skip directory creation, proceed to checklist.

---

## STEP 2: WRITE input.json

Write to `projects/{project_slug}/input/input.json`:

```json
{
  "project_id": "{project_slug}",
  "topic": "{topic}",
  "language": "{language}",
  "video_length_minutes": {duration_minutes},
  "style": "{style}",
  "niche": "{niche}",
  "target_word_count": {target_words},
  "channel_name": "{channel_name_from_yaml_or_empty}",
  "notes": "{notes_from_yaml_or_empty}",
  "created_at": "{ISO_datetime}",
  "schema_version": "1.0"
}
```

Fill every `{variable}` from runtime state. `channel_name` and `notes` come from `project.yaml → project.channel_name` and `project.yaml → project.notes`. If those keys are absent or empty, write `""`.

---

## STEP 3: WRITE project.yaml

If the user placed a `project.yaml` in the same directory as their inputs before running:
- Read it
- Copy it to `projects/{project_slug}/input/project.yaml`

If no project.yaml was provided:
- Write a minimal project.yaml from runtime state:

```yaml
project:
  topic: "{topic}"
  language: "{language}"
  video_length_minutes: {duration_minutes}
  style: "{style}"
  niche: "{niche}"
  channel_name: ""
  notes: ""

pipeline:
  start_stage: 0
  stop_after_stage: 12
  max_retries_per_stage: 1
  halt_on_advisory: false

quality:
  word_count_tolerance: 0.10
  min_verified_facts: 5
  min_sources: 3
  require_source_pass: false

models:
  primary: "claude-opus-4-8"
  secondary: "claude-sonnet-4-6"
  stage_overrides: {}

images:
  max_ai_escalation_rate: 0.50
  minimum_license: "cc_by"
  allow_fair_use: true

voice:
  elevenlabs_voice_id: ""

seo:
  tag_count_min: 15
  tag_count_max: 30
  extra_tags: []

export:
  bundle_export_assets: true
  include_run_log: true
  generate_editor_handoff: true

analytics:
  write_to_memory: true
  project_tags: []

schema_version: "1.0"
```

---

## STEP 4: WRITE INITIAL export_manifest.json

Write to `projects/{project_slug}/export/export_manifest.json`:

```json
{
  "project_id": "{project_slug}",
  "schema_version": "1.0",
  "status": "in_progress",
  "pipeline_stage": "stage_00",
  "created_at": "{ISO_datetime}",
  "updated_at": "{ISO_datetime}",
  "assets": {
    "research":           { "file": "research/research.md",           "status": "absent" },
    "source_report":      { "file": "research/source_report.md",      "status": "absent" },
    "research_verified":  { "file": "research/research_verified.md",  "status": "absent" },
    "story_outline":      { "file": "script/story_outline.md",        "status": "absent" },
    "script":             { "file": "script/script.md",               "status": "absent" },
    "story_bible":        { "file": "script/story_bible.md",          "status": "absent" },
    "storyboard":         { "file": "visuals/storyboard.md",          "status": "absent" },
    "image_plan":         { "file": "visuals/image_plan.md",          "status": "absent" },
    "ai_image_prompts":   { "file": "visuals/ai_image_prompts.md",    "status": "absent" },
    "voice_script":       { "file": "voice/voice_script.txt",         "status": "absent" },
    "voice_direction":    { "file": "voice/voice_direction.md",       "status": "absent" },
    "subtitles":          { "file": "voice/subtitles.srt",            "status": "absent" },
    "thumbnail_prompt":   { "file": "seo/thumbnail_prompt.md",        "status": "absent" },
    "seo":                { "file": "seo/seo.md",                     "status": "absent" },
    "export_manifest":    { "file": "export/export_manifest.json",    "status": "in_progress" },
    "project_report":     { "file": "export/project_report.md",       "status": "absent" },
    "qa_report":          { "file": "logs/qa_report.md",              "status": "absent" }
  }
}
```

---

## STEP 5: INITIALIZE director_run_log.md

Write to `projects/{project_slug}/logs/director_run_log.md`:

```markdown
# Director Run Log
**Project:**       {project_slug}
**Topic:**         {topic}
**Language:**      {language}
**Duration:**      {duration_minutes} min
**Style:**         {style}
**Niche:**         {niche}
**Target words:**  {target_words}
**Started:**       {ISO_datetime}
**Director AI:**   v1.0

---

## Stage 0 — Project Setup
**Started:**  {ISO_datetime}
**Status:**   COMPLETE

**Directories created:**
- input/
- research/
- script/
- visuals/
- voice/
- seo/
- export/
- logs/

**Files written:**
- input/input.json
- input/project.yaml
- export/export_manifest.json
- logs/director_run_log.md

**Checklist result:** 7/7 passed
**Warnings:** None

---

```

The `---` at the bottom is where subsequent stage entries will be appended.

---

## STAGE 0 CHECKLIST

Run these checks after all files are written:

| Check | Level | How to verify |
|---|---|---|
| 0.1 Project slug valid | CRITICAL | `slug matches /^\d{8}_[a-z0-9-]+$/` |
| 0.2 All 8 subdirectories exist | CRITICAL | Check each path |
| 0.3 input.json has all required fields | CRITICAL | `project_id, topic, language, video_length_minutes, style, niche, target_word_count` all non-empty |
| 0.4 project.yaml exists | STANDARD | File exists and non-empty |
| 0.5 export_manifest.json has 17 assets | CRITICAL | Count asset keys = 17 |
| 0.6 director_run_log.md initialized | STANDARD | File exists and has run header |
| 0.7 target_word_count > 0 | CRITICAL | `target_word_count >= 390` (5 min × 130 × 0.60) |

If all CRITICAL checks pass: return `{status: "PASS"}`.
If any CRITICAL check fails: halt with `ERR_CRITICAL_001`.

---

## STAGE 0 COMPLETE OUTPUT

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STAGE 0 — PROJECT SETUP
Project: {project_slug}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Stage 0] Creating project directory: projects/{project_slug}/
[Stage 0] Creating 8 subdirectories...
[Stage 0] Writing input/input.json...
[Stage 0] Writing input/project.yaml...
[Stage 0] Writing export/export_manifest.json (17 assets)...
[Stage 0] Initializing logs/director_run_log.md...
[Stage 0] Running checklist (7 items)...

[STAGE 0 COMPLETE]
Output:     input/input.json, input/project.yaml, export/export_manifest.json, logs/director_run_log.md
Checklist:  7/7 passed
Status:     PASS
──────────────────────────────────────────────
```
