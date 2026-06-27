# Project Template — AI YouTube Studio OS

This folder (`_PROJECT_TEMPLATE/`) is the canonical structure for every video production project. When you start a new production run, the Director AI copies this structure to `projects/{project_slug}/`.

Do not run the Director AI inside `_PROJECT_TEMPLATE/`. This is a template only.

---

## How a Project Folder Is Used

### 1. Initiate a run

Provide the four required inputs to the Director AI:

```
TOPIC: Your video topic
LANGUAGE: en / ja / vi
DURATION_MINUTES: 5–60
STYLE: dark_documentary / reddit_narration / mystery_investigation / japanese_mystery
```

### 2. Director AI creates the project folder

The Director generates a project slug: `YYYYMMDD_topic-slug`

It creates: `projects/YYYYMMDD_topic-slug/` with this same folder structure.

### 3. Pipeline runs stages 0–12

Each stage writes its output files to the correct subfolder. See below for what each folder contains.

### 4. Review outputs

When the pipeline finishes, review the files in each subfolder. The `export/` folder contains the final packaged assets.

---

## Folder Structure

```
{project_slug}/
├── input/          ← Production inputs (you fill these in before running)
├── research/       ← Stage 1-2: Research and verified facts
├── script/         ← Stage 3-5: Outline, script, story bible
├── visuals/        ← Stage 6-8: Storyboard, image plan, AI prompts
├── voice/          ← Stage 9: Voice script, direction, subtitles
├── seo/            ← Stage 10: Titles, description, tags, thumbnail
├── export/         ← Stage 12: Final packaged assets
└── logs/           ← All stages: Run log, stage logs, QA report
```

---

## Project Lifecycle

| Status | Meaning |
|---|---|
| `in_progress` | Pipeline is running |
| `needs_revision` | A critical check failed — human action required |
| `ready_for_production` | All stages complete, QA passed |
| `archived` | Project is complete and moved to long-term storage |

Current project status is tracked in `export/export_manifest.json`.

---

## Resuming an Interrupted Run

If the pipeline was stopped (by a failure, a session timeout, or manual halt), resume it with:

```
RESUME PROJECT: {project_slug}
```

The Director AI reads `export/export_manifest.json` to find where it left off and resumes from the earliest incomplete stage.

---

## Files You Should Never Edit Manually

- `export/export_manifest.json` — managed by the Director AI
- `logs/director_run_log.md` — managed by the Director AI
- `logs/stage_*.log` — managed by the Director AI

---

## Files You Can Review and Edit

All content files are plain text and can be reviewed and edited by a human:

- `research/research.md` — if you want to add missing context before Stage 2
- `script/script.md` — if you want to revise the narration after Stage 4
- `seo/seo.md` — if you want to adjust titles or description after Stage 10

If you edit a file after the Director AI has validated it, set that asset's status back to `in_progress` in `export_manifest.json` and re-run the affected stage.
