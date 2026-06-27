# Stage Runner — Single Stage Executor

Executes one stage of the pipeline. Called by `pipeline_executor.md` for stages 1–10. Handles prompt loading, context injection, placeholder resolution, output writing, and checklist validation.

---

## EXECUTION PROCEDURE

For a given stage N:

```
function execute(stage_number, retry=False, retry_constraint=""):

  stage = STAGE_REGISTRY[stage_number]

  // STEP 1: Announce stage start
  output_stage_banner(stage_number, stage.name)

  // STEP 2: Load prompt file
  prompt_content = read_file(stage.prompt_file)

  // STEP 3: Load template addendum
  addendum = context_loader.load_template_addendum(stage_number)

  // STEP 4: Load stage context files
  context_files = context_loader.load_stage_context(stage_number)

  // STEP 5: Resolve placeholders
  resolved_prompt = resolve_placeholders(prompt_content)

  // STEP 6: Append retry constraint if this is a retry
  if retry:
    resolved_prompt += "\n\n---\n" + retry_constraint

  // STEP 7: Mark stage as in_progress in manifest
  for output_file in stage.output_files:
    manifest_manager.update_asset(output_file, "in_progress")

  // STEP 8: Log stage start
  logging_system.write_stage_start(stage_number, stage.name)

  // STEP 9: Execute — generate content
  // Compose the full AI call:
  system_prompt = load_system_prompt(stage_number)
  context_block = format_context_block(context_files)
  full_prompt = system_prompt + "\n\n" + context_block + "\n\n" + resolved_prompt
  if addendum:
    full_prompt += "\n\n---\nTEMPLATE ADDENDUM\n" + addendum

  output = generate(full_prompt, model=stage.model_tier)

  // STEP 10: Write output files
  for (filename, content) in output.files:
    write_atomic("{project_dir}/{filename}", content)
    logging_system.log("[Stage {N}] Written: {filename}")

  // STEP 11: Update manifest
  for output_file in stage.output_files:
    manifest_manager.update_asset(output_file, "complete")

  // STEP 12: Run checklist
  checklist_result = run_checklist(stage_number)

  // STEP 13: Update manifest to validated or needs_revision
  if checklist_result.critical_all_pass:
    for output_file in stage.output_files:
      manifest_manager.update_asset(output_file, "validated")
  else:
    for f in checklist_result.critical_fails:
      manifest_manager.update_asset(f.file, "needs_revision")

  // STEP 14: Log result
  logging_system.write_stage_complete(stage_number, checklist_result)

  // STEP 15: Announce completion
  output_stage_complete(stage_number, checklist_result)

  // STEP 16: Return result
  return {
    status: derive_status(checklist_result),
    retry_eligible: checklist_result.retry_eligible,
    retry_constraint: checklist_result.retry_constraint,
    warnings: checklist_result.warnings
  }
```

---

## SYSTEM PROMPT PER STAGE

Every AI call begins with the same system prompt. Fill `{variables}` from runtime state.

```
You are the Director AI for the AI YouTube Studio OS — an automated video content production system.

You are executing Stage {N}: {Stage Name}.

Project: {project_slug}
Topic: {topic}
Language: {language}
Style: {style}
Niche: {niche}
Target word count: {target_words}

You are not answering a question. You are executing a production stage.
Produce the required output exactly as specified in the stage prompt.
Do not add commentary, preamble, or explanations outside the output structure.
Write only what belongs in the output file.
Do not fabricate facts, URLs, names, or sources.
All facts must come from the research_verified.md file provided in the context.
```

---

## PLACEHOLDER RESOLUTION TABLE

Replace all `{placeholder}` instances in the prompt file with these values:

| Placeholder | Value source |
|---|---|
| `{topic}` | `runtime_state.topic` |
| `{language}` | `runtime_state.language` |
| `{style}` | `runtime_state.style` |
| `{niche}` | `runtime_state.niche` |
| `{project_slug}` | `runtime_state.project_slug` |
| `{video_length_minutes}` | `runtime_state.duration_minutes` |
| `{target_words}` | `runtime_state.target_words` |
| `{min_words}` | `floor(target_words × 0.90)` |
| `{max_words}` | `ceil(target_words × 1.10)` |
| `{channel_name}` | `project.yaml → project.channel_name` or `"[Channel Name]"` |
| `{notes}` | `project.yaml → project.notes` or `""` |

Any placeholder left unresolved: log `[WARN ERR_WARN_999] Unresolved placeholder: {placeholder}`. Continue.

---

## CONTEXT BLOCK FORMAT

The context block is injected between the system prompt and the stage prompt. Format:

```
---
CONTEXT: {filename}
---
{file contents}

---
CONTEXT: {filename}
---
{file contents}

[repeat for each context file]
```

See `context_loader.md` for the exact list of context files per stage.

---

## ATOMIC FILE WRITE

Every file is written atomically to prevent partial writes:

```
1. Write content to: {project_dir}/{filename}.tmp
2. If write succeeds: rename .tmp to {filename}
3. If write fails: delete .tmp, log ERR_FAIL_001, return FAIL status
```

Never write directly to the final filename. Always use the `.tmp` → rename pattern.

---

## CHECKLIST EXECUTION

After output is written, run the stage checklist from `agents/director_project_checklist.md`:

```
function run_checklist(stage_number):
  checks = load_checklist_section(stage_number)  // from director_project_checklist.md

  result = {
    critical_all_pass: True,
    critical_fails: [],
    warnings: [],
    advisory_fails: [],
    retry_eligible: False,
    retry_constraint: ""
  }

  for check in checks:
    passes = evaluate_check(check)

    if not passes:
      if check.level == "CRITICAL":
        result.critical_all_pass = False
        result.critical_fails.append(check)
        if check.retry_eligible:
          result.retry_eligible = True
          result.retry_constraint = check.retry_constraint

      if check.level == "STANDARD":
        result.warnings.append(check)
        if check.retry_eligible:
          result.retry_eligible = True
          result.retry_constraint = check.retry_constraint

      if check.level == "ADVISORY":
        result.advisory_fails.append(check)
        logging_system.write_warning(check)

  return result
```

Checklist evaluation depends on the check type:

| Check type | How to evaluate |
|---|---|
| File existence | `os.path.exists({project_dir}/{file})` |
| File non-empty | `len(read_file({project_dir}/{file}).strip()) > 0` |
| Word count | Count space-separated words in the file content |
| Character count | `len(string)` |
| Contains substring | `substring in file_content` |
| Does not contain | `substring not in file_content` |
| Sequential numbers | Parse all integer IDs in order, check no gaps |
| Timecode overlap | Parse SRT timecodes, verify no end > next start |

---

## STAGE BANNER OUTPUT

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STAGE {N} — {STAGE NAME}
Project: {project_slug}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## STAGE COMPLETE OUTPUT

```
[STAGE {N} COMPLETE]
Output:     {comma-separated output filenames}
Checklist:  {critical_pass}/{critical_total} critical | {warn_count} warnings
Status:     {PASS | FLAGGED | FAIL}
──────────────────────────────────────────────
```

Status logic:
- `PASS` — all CRITICAL pass, all STANDARD pass
- `FLAGGED` — all CRITICAL pass, some STANDARD or ADVISORY warn
- `FAIL` — any CRITICAL fails

---

## STATUS RETURN MAPPING

```
if critical_all_pass and no standard_fails:  return "PASS"
if critical_all_pass and has standard_fails: return "FLAGGED"   // pipeline continues
if not critical_all_pass:                    return "FAIL"       // pipeline halts (or retries)
```

`pipeline_executor.md` only halts on `FAIL`. `FLAGGED` continues.

---

## SPECIAL CASE: STAGE 2 SOURCE VERDICT

After Stage 2 completes, read the `Overall Status` field from `research/source_report.md`:

```
if Overall Status == "FAIL":
  call manifest_manager.update_asset("research_verified", "needs_revision")
  return {status: "CRITICAL", retry_eligible: False}

if Overall Status == "NEEDS_REVISION":
  logging_system.write_warning("ERR_WARN_001", stage=2, detail="N flagged items")
  // continue — do not halt
```

This check happens AFTER the checklist, as an additional gate.

---

## SPECIAL CASE: STAGE 9 THREE OUTPUTS

Stage 9 produces three files. Each must be written and validated independently:

```
write_atomic("voice/voice_script.txt", output.voice_script)
write_atomic("voice/voice_direction.md", output.voice_direction)
write_atomic("voice/subtitles.srt", output.subtitles)
```

Run checklist items 9.1-9.7 against voice_script.txt.
Run checklist items 9.8-9.13 against subtitles.srt.
Run checklist items 9.14-9.17 against voice_direction.md.

All three must pass their respective CRITICAL items for Stage 9 to return PASS.
