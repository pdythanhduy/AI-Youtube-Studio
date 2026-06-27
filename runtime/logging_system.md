# Logging System — Runtime Log Writer

All log writes go through this module. Two log targets per stage: the main `director_run_log.md` (append entries) and the stage-specific `stage_NN_name.log` (one file per stage). Plus the warning counter used by `director_runtime.md` for the completion report.

---

## LOG FILE PATHS

```
Main log:          {project_dir}/logs/director_run_log.md    (append-only)
Stage log:         {project_dir}/logs/stage_{NN}_{name}.log  (one per stage)
QA report:         {project_dir}/logs/qa_report.md           (written by Stage 11)
```

Stage log filename examples:
```
stage_01_research.log
stage_02_source_verifier.log
stage_03_story_outline.log
stage_04_script_writer.log
stage_05_story_bible.log
stage_06_scene_splitter.log
stage_07_image_finder.log
stage_08_image_prompt_generator.log
stage_09_voice_director.log
stage_10_youtube_seo.log
stage_11_final_qa.log
stage_12_export.log
```

---

## WRITE STAGE START

Called at the beginning of each stage, before AI generation.

**Appends to director_run_log.md:**

```markdown
## Stage {N} — {Stage Name}
**Started:** {ISO_datetime}
**Status:** IN PROGRESS
```

**Creates and writes stage log file:**

```
[{ISO_datetime}] STAGE {N} — {STAGE NAME} — STARTED
[{ISO_datetime}] Prompt file: prompts/{NN_name.md}
[{ISO_datetime}] Context files loaded: {count}
[{ISO_datetime}]   → {file1}
[{ISO_datetime}]   → {file2}
[{ISO_datetime}]   → ...
[{ISO_datetime}] Template addendum: {template_file} section stage_{NN}
[{ISO_datetime}] Placeholders resolved: {count}
[{ISO_datetime}] Model tier: {primary|secondary} ({model_id})
[{ISO_datetime}] Generating output...
```

---

## WRITE STAGE COMPLETE

Called after stage_runner returns a result.

**Appends to director_run_log.md:**

```markdown
**Completed:** {ISO_datetime}
**Status:** {COMPLETE | FAILED}
**Duration:** {elapsed_seconds}s

**Output files written:**
{for each file: "- {subfolder/filename}"}

**Checklist result:** {critical_pass}/{critical_total} critical | {warn_count} warnings

**Warnings:**
{if none: "- None"}
{if any: "- {warning_message}" for each warning}

**Notes:**
{any notable decisions — e.g. "Stage 2: NEEDS_REVISION. 2 flagged claims logged."}

---

```

**Appends to stage log file:**

```
[{ISO_datetime}] Output written: {filename1} ({word_count} words)
[{ISO_datetime}] Output written: {filename2}
[{ISO_datetime}] Running checklist ({total} items)...
[{ISO_datetime}] CHECK {N}: {check_name} — PASS
[{ISO_datetime}] CHECK {N}: {check_name} — PASS
[{ISO_datetime}] CHECK {N}: {check_name} — WARN: {detail}
[{ISO_datetime}] CHECK {N}: {check_name} — FAIL: {detail}
[{ISO_datetime}] Checklist complete: {pass}/{total}
[{ISO_datetime}] Manifest updated: {asset}.status = validated
[{ISO_datetime}] STAGE {N} — {STATUS} — {elapsed_seconds}s
```

---

## WRITE WARNING

Called whenever a WARN-level check fails or an ERR_WARN_NNN event occurs.

```
function write_warning(error_code, stage, detail=""):
  warning_message = "[⚠ WARN {error_code}] Stage {stage}: {detail}"

  // Output to console
  print(warning_message)
  print(f"  Action: Logged. Continuing pipeline.")

  // Append to stage log
  append_to_stage_log(stage, f"[{ISO_datetime}] WARNING {error_code}: {detail}")

  // Increment global counter
  runtime_state.total_warnings += 1
```

---

## WRITE ERROR

Called when any ERR_CRITICAL or ERR_FAIL event occurs.

```
function write_error(error_code, stage, file="", description="", action=""):
  error_entry = """
### Error: {error_code}
**Time:** {ISO_datetime}
**Severity:** {severity}
**Stage:** {stage}
**File:** {file or "N/A"}
**Description:** {description}
**Action taken:** {action}
**Resolved:** No — awaiting human
"""

  // Append to main log under current stage entry
  append_to_run_log(error_entry)

  // Append to stage log
  append_to_stage_log(stage, f"[{ISO_datetime}] ERROR {error_code}: {description}")
```

---

## WRITE QA REPORT

Called by `pipeline_executor.md` Stage 11 execution.

Writes to `{project_dir}/logs/qa_report.md`:

```markdown
# QA Report
**Project:**   {project_slug}
**QA Date:**   {ISO_datetime}
**QA Score:**  {total_pass}/{total_checks} ({pct}%)

---

## CRITICAL CHECKS
_(Any failure = BLOCKED verdict)_

- [{PASS|FAIL}] 11.1 All 15 output files exist and are non-empty
- [{PASS|FAIL}] 11.2 source_report.md Overall Status ≠ FAIL
- [{PASS|FAIL}] 11.3 script.md word count within ±10% of target ({actual} / {target})
- [{PASS|FAIL}] 11.4 voice_script.txt has no markdown characters
- [{PASS|FAIL}] 11.5 subtitles.srt is sequential, non-overlapping, correct format
- [{PASS|FAIL}] 11.6 image_plan.md has no TBD entries
- [{PASS|FAIL}] 11.7 Every AI-escalated beat has a prompt in ai_image_prompts.md
- [{PASS|FAIL}] 11.8 All 3 SEO titles are ≤70 characters

---

## CONTENT CHECKS
_(Warnings only — do not block export)_

- [{PASS|WARN}] 11.9  Hook section ≤65 words (actual: {N} words)
- [{PASS|WARN}] 11.10 All storyboard beats have visual assignments
- [{PASS|WARN}] 11.11 Pronunciation guide covers all proper nouns
- [{PASS|WARN}] 11.12 SEO tag count is 15–30 (actual: {N})
- [{PASS|WARN}] 11.13 Thumbnail prompt is self-contained

---

## CONSISTENCY CHECKS
_(Warnings only — do not block export)_

- [{PASS|WARN}] 11.14 Spot-check: 5 names match story_bible canonical forms
- [{PASS|WARN}] 11.15 Spot-check: 3 dates consistent across files
- [{PASS|WARN}] 11.16 SEO chapters match story_outline scene names
- [{PASS|WARN}] 11.17 Image count in image_plan matches storyboard beat count
- [{PASS|WARN}] 11.18 Voice script word count within ±5% of script.md

---

## SUMMARY

| Check type | Passed | Total |
|---|---|---|
| Critical | {critical_pass} | 8 |
| Content | {content_pass} | 5 |
| Consistency | {consistency_pass} | 5 |

Critical failures: {critical_fail}
Content warnings: {content_warn}
Consistency warnings: {consistency_warn}

**Overall verdict: {READY_FOR_EXPORT | NEEDS_REVISION | BLOCKED}**

{if BLOCKED:
"### Failed critical checks:
{for each failure: "- {check_id}: {check_name} — {specific detail}"}
Action: Fix each file listed above, then resume from Stage 11:
RESUME PROJECT: {project_slug}"}
```

---

## WRITE COMPLETION ENTRY

Called by `pipeline_executor.md` after Stage 12 succeeds. Appends to `director_run_log.md`:

```markdown
## Pipeline Complete
**Completed:**    {ISO_datetime}
**Total stages:** 13 / 13
**Total warnings:** {total_warnings}
**QA score:**     {qa_pass}/{qa_total} ({pct}%)
**Status:**       READY FOR PRODUCTION ✓
```

---

## LOG APPEND PROTOCOL

The main `director_run_log.md` is append-only. Never rewrite it. Never truncate it.

```
function append_to_run_log(content):
  existing = read_file(run_log_path)
  new_content = existing + content
  write_atomic(run_log_path, new_content)
```

Stage log files are created fresh per stage. Each stage creates its own log file.

```
function append_to_stage_log(stage_number, line):
  stage_log_path = "{project_dir}/logs/stage_{NN}_{name}.log"
  existing = read_file(stage_log_path) or ""
  write_atomic(stage_log_path, existing + line + "\n")
```

Use atomic write for both. Never write a partial log entry.
