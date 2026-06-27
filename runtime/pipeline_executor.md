# Pipeline Executor — Stage Loop Controller

Owns the stage execution loop. Called by `director_runtime.md` after system boot. Calls `stage_runner.md` for each stage. Makes continue/halt decisions. Handles retry.

---

## STAGE REGISTRY

The complete pipeline. Every stage is defined here. No stages exist outside this table.

| N | Name | Prompt file | Output files | Model tier |
|---|---|---|---|---|
| 0 | Project Setup | (none — project_initializer.md) | input/input.json, input/project.yaml, export/export_manifest.json, logs/director_run_log.md | — |
| 1 | Research | prompts/01_research.md | research/research.md | primary |
| 2 | Source Verification | prompts/02_source_verifier.md | research/source_report.md, research/research_verified.md | primary |
| 3 | Story Outline | prompts/03_story_outline.md | script/story_outline.md | primary |
| 4 | Script Writing | prompts/04_script_writer.md | script/script.md | primary |
| 5 | Story Bible | prompts/05_story_bible.md | script/story_bible.md | secondary |
| 6 | Scene Splitting | prompts/06_scene_splitter.md | visuals/storyboard.md | secondary |
| 7 | Image Planning | prompts/07_image_finder.md | visuals/image_plan.md | secondary |
| 8 | AI Image Prompts | prompts/08_image_prompt_generator.md | visuals/ai_image_prompts.md | secondary |
| 9 | Voice Direction | prompts/09_voice_director.md | voice/voice_script.txt, voice/voice_direction.md, voice/subtitles.srt | primary |
| 10 | YouTube SEO | prompts/10_youtube_seo.md | seo/seo.md, seo/thumbnail_prompt.md | secondary |
| 11 | Final QA | (none — inline) | logs/qa_report.md | primary |
| 12 | Export | (none — inline) | export/export_manifest.json (final), export/project_report.md | — |

Model tiers resolve from `input/project.yaml`:
- `primary` → `models.primary` (default: claude-opus-4-8)
- `secondary` → `models.secondary` (default: claude-sonnet-4-6)

---

## DEPENDENCY MAP

Before calling `stage_runner.md` for stage N, verify all prerequisite files exist. If any are missing: halt with `ERR_CRITICAL_005`.

| Stage N | Required files before execution |
|---|---|
| 0 | (none) |
| 1 | input/input.json |
| 2 | research/research.md |
| 3 | research/research_verified.md |
| 4 | script/story_outline.md, research/research_verified.md |
| 5 | script/script.md, research/research_verified.md |
| 6 | script/script.md, script/story_bible.md |
| 7 | visuals/storyboard.md, script/story_bible.md |
| 8 | visuals/storyboard.md, visuals/image_plan.md, script/story_bible.md |
| 9 | script/script.md, script/story_bible.md, script/story_outline.md |
| 10 | script/script.md, research/research_verified.md, script/story_bible.md, script/story_outline.md |
| 11 | research/research.md, research/source_report.md, research/research_verified.md, script/story_outline.md, script/script.md, script/story_bible.md, visuals/storyboard.md, visuals/image_plan.md, visuals/ai_image_prompts.md, voice/voice_script.txt, voice/voice_direction.md, voice/subtitles.srt, seo/seo.md, seo/thumbnail_prompt.md |
| 12 | logs/qa_report.md (with verdict READY_FOR_EXPORT) |

**Dependency check procedure:**

```
for each required_file in dependency_map[N]:
    if file does not exist at {project_dir}/{required_file}:
        call logging_system.md → write_error(ERR_CRITICAL_005, stage=N, file=required_file)
        output dependency_error_message(N, required_file)
        STOP pipeline
```

**Dependency error message:**

```
⛔ DEPENDENCY ERROR — Stage {N}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Missing: {project_dir}/{required_file}
Expected from: Stage {source_stage}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Action: Re-run Stage {source_stage}, then resume.
RESUME PROJECT: {project_slug}
```

---

## EXECUTION LOOP

```
function run_pipeline(start_stage, stop_after_stage):

  for N in range(start_stage, stop_after_stage + 1):

    // 1. Check dependencies
    check_dependencies(N)                 // halts on failure (see above)

    // 2. Dispatch stage
    if N == 0:
      result = project_initializer.execute()
    elif N == 11:
      result = run_final_qa()
    elif N == 12:
      result = run_export()
    else:
      result = stage_runner.execute(N)   // stage_runner.md

    // 3. Handle result
    if result.status == "CRITICAL":
      write_stage_log(N, result)
      output_halt_message(N, result)
      STOP

    if result.status == "FAIL":
      if result.retry_eligible:
        retry_result = stage_runner.execute(N, retry=True, constraint=result.retry_constraint)
        if retry_result.status in ("PASS", "FLAGGED"):
          result = retry_result
        else:
          write_stage_log(N, retry_result)
          output_fail_message(N, retry_result)
          STOP
      else:
        write_stage_log(N, result)
        output_fail_message(N, result)
        STOP

    // 4. Log completion
    write_stage_log(N, result)
    stages_complete.append(N)

  // 5. All stages done
  director_runtime.completion_report()
```

---

## RETRY ELIGIBILITY

Before halting on a FAIL result, check if the failed check is retry-eligible:

| Failed check | Retry eligible | Retry constraint to append to prompt |
|---|---|---|
| Script word count outside ±10% but within ±15% | Yes | `WORD COUNT CONSTRAINT: The script must be between {min_words} and {max_words} words. This is a hard requirement. Count words before finishing.` |
| Missing [PAUSE:3s] in voice_script | Yes | `PACING CONSTRAINT: The voice script must contain exactly one [PAUSE:3s]. Add it at the most dramatic moment.` |
| SRT segment > 7 seconds | Yes | `SRT CONSTRAINT: No subtitle segment may exceed 7 seconds. Split any segment longer than 7 seconds.` |
| SRT line > 42 characters | Yes | `SRT CONSTRAINT: No subtitle line may exceed 42 characters. Wrap earlier.` |
| SEO tag count < 15 | Yes | `TAG CONSTRAINT: You must provide at least 15 tags. Add more specific and long-tail tags to reach the minimum.` |
| Markdown in voice_script.txt | Yes | `PLAIN TEXT CONSTRAINT: voice_script.txt must contain ONLY plain text and approved pacing markers. Remove all markdown: no #, *, _, >, |` |
| Output file empty or missing | No | — (re-run stage entirely, not retry) |
| Hook > 65 words | No | — |
| Hook is a greeting | No | — |
| Source report FAIL | No | — |

**Retry announcement:**

```
[RETRY] Stage {N} — {reason}
Adjusting: {constraint label}
Re-running Stage {N}...
```

**Retry failure:**

```
[RETRY FAILED] Stage {N} — second attempt also failed.
Check: {failed_check}
```

Then halt with standard FAIL message.

---

## STAGE 11: FINAL QA (inline execution)

Stage 11 does not call stage_runner. Execute it directly.

```
function run_final_qa():

  // Read all output files and check them
  // See agents/director_project_checklist.md Stage 11 for the full item list

  critical_pass = 0
  critical_fail = 0
  critical_fails = []
  content_warn = 0
  consistency_warn = 0

  // Run all checks from checklist Stage 11
  // CRITICAL checks: 11.1 – 11.8
  // CONTENT checks: 11.9 – 11.13
  // CONSISTENCY checks: 11.14 – 11.18

  for each check in critical_checks:
    if passes: critical_pass += 1
    else:
      critical_fail += 1
      critical_fails.append(check.name)

  for each check in content_checks:
    if fails: content_warn += 1

  for each check in consistency_checks:
    if fails: consistency_warn += 1

  // Determine verdict
  if critical_fail > 0:
    verdict = "BLOCKED"
    result.status = "CRITICAL"
    result.retry_eligible = False
  else:
    verdict = "READY_FOR_EXPORT"
    result.status = "PASS"

  // Write qa_report.md
  write_qa_report(
    project_slug, critical_pass, critical_fail, critical_fails,
    content_warn, consistency_warn, verdict
  )

  // Update manifest
  manifest_manager.update_asset("qa_report", "validated")

  // QA score for completion report
  qa_score.pass = critical_pass + (total_content - content_warn) + (total_consistency - consistency_warn)
  qa_score.total = total_checks

  if verdict == "BLOCKED":
    output:
    "⛔ QA BLOCKED — Export cannot proceed."
    "Failed checks: {critical_fails}"
    "Fix these files, then resume from Stage 11:"
    "RESUME PROJECT: {project_slug}"

  return result
```

---

## STAGE 12: EXPORT (inline execution)

Only executes if Stage 11 verdict = `READY_FOR_EXPORT`.

```
function run_export():

  // Verify QA verdict
  read qa_report.md
  if verdict != "READY_FOR_EXPORT":
    halt with ERR_CRITICAL_008

  // Finalize manifest
  manifest_manager.finalize()        // sets all assets to "validated", status to "ready_for_production"

  // Write project_report.md
  write_project_report()             // see manifest_manager.md

  // Complete the run log
  logging_system.write_completion_entry()

  return {status: "PASS"}
```

---

## HALT MESSAGES

### Critical halt:

```
⛔ CRITICAL FAILURE — Stage {N}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Error:  {error_code}
Check:  {failed_check_name}
File:   {project_dir}/{affected_file}
Issue:  {specific description}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Action: {what the human must do}
Resume: RESUME PROJECT: {project_slug}
```

### Stage fail halt:

```
❌ STAGE FAIL — Stage {N} — {Stage Name}
──────────────────────────────────────────────
Error:   {error_code}
Check:   {failed_check_name}
File:    {project_dir}/{affected_file}
Issue:   {specific description}
──────────────────────────────────────────────
Action: {fix instruction}
Resume: RESUME PROJECT: {project_slug}
```
