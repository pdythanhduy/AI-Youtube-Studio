# logs/ — Pipeline Logs and QA Report

This folder contains all runtime logs, stage-level logs, and the QA report. It is written and updated throughout the pipeline by the Director AI.

---

## Files

### `director_run_log.md` — Main pipeline log (all stages)

**Written by:** Director AI starting at Stage 0. Appended after every stage.

This is the complete record of what the Director AI did during this production run. It includes:
- Run header (project, inputs, start time)
- One entry per stage (start time, status, files written, checklist result, warnings, notes)
- Error entries (code, severity, description, action taken)
- Completion entry (total stages, total warnings, final status)

Use this file to:
- Understand why the pipeline stopped
- See which stages had warnings
- Audit the production process after the fact

---

### `stage_NN_name.log` — Per-stage execution log (one file per stage)

**Written by:** Director AI during each stage.

Naming convention: `stage_00_setup.log`, `stage_01_research.log`, `stage_02_source_verifier.log`, etc.

Each file contains a timestamped trace of everything the Director did during that stage:
- Which files were read
- Which placeholders were resolved
- Which checklist items passed or failed
- The exact warning or error message if something went wrong

These are the most detailed logs for debugging. If a stage fails, read the corresponding stage log first.

---

### `qa_report.md` — Final quality assurance report (Stage 11)

**Written by:** Director AI at Stage 11.

This is the output of the Final QA stage. It contains:
- **Critical Checks** — must all pass for export to proceed
- **Content Checks** — warnings if failed, but do not block export
- **Consistency Checks** — cross-file validation results
- **QA Score** — total checks passed / total checks
- **Overall Verdict** — `READY_FOR_EXPORT` / `NEEDS_REVISION` / `BLOCKED`

If the verdict is `BLOCKED`: read this file to find which critical checks failed and what to fix.

---

## Reading the Logs

### Pipeline stopped — what to do

1. Open `director_run_log.md`
2. Find the last stage entry — look for `Status: FAILED`
3. Open the corresponding `stage_NN_name.log`
4. Find the checklist item that failed — it will say `FAIL: {reason}`
5. Fix the issue in the relevant file
6. Resume the pipeline: `RESUME PROJECT: {project_slug}`

### QA blocked — what to do

1. Open `logs/qa_report.md`
2. Find all `[FAIL]` items under **Critical Checks**
3. Fix each issue in the relevant file
4. Re-run Stage 11 by resuming the pipeline

---

## What Does NOT Belong Here

- Content files (research, scripts, visuals, voice, SEO) — those go in their own folders
- The QA report from a human review — that is a separate document outside the project folder
