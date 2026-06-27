# Manifest Manager — export_manifest.json Operations

All reads and writes to `export/export_manifest.json` go through this module. No other module writes the manifest file directly.

---

## MANIFEST FILE PATH

```
{project_dir}/export/export_manifest.json
```

---

## OPERATIONS

### READ MANIFEST

```
function read_manifest():
  content = read_file("{project_dir}/export/export_manifest.json")
  manifest = parse_json(content)
  return manifest
```

Returns the full manifest object. Called by:
- `director_runtime.md` during resume validation
- `pipeline_executor.md` Stage 12 to verify QA verdict
- `logging_system.md` to build project_report.md

---

### UPDATE ASSET STATUS

```
function update_asset(asset_key, new_status, extra_fields={}):
  manifest = read_manifest()

  manifest.assets[asset_key].status = new_status
  manifest.assets[asset_key].updated_at = ISO_datetime()

  if new_status == "in_progress":
    manifest.assets[asset_key].started_at = ISO_datetime()
    manifest.pipeline_stage = "stage_{NN}"   // current stage number, zero-padded

  if new_status == "complete":
    manifest.assets[asset_key].completed_at = ISO_datetime()

  if new_status == "validated":
    manifest.assets[asset_key].validated_at = ISO_datetime()
    manifest.assets[asset_key].checklist_score = extra_fields.get("checklist_score", "")

  if new_status == "needs_revision":
    manifest.assets[asset_key].failure_reason = extra_fields.get("failure_reason", "")
    manifest.status = "needs_revision"
    manifest.halt_at = ISO_datetime()
    manifest.halt_reason = extra_fields.get("halt_reason", "")

  manifest.updated_at = ISO_datetime()

  write_atomic("{project_dir}/export/export_manifest.json", json_serialize(manifest))
```

Valid `new_status` values: `absent`, `pending`, `in_progress`, `complete`, `validated`, `needs_revision`

---

### FINALIZE MANIFEST (Stage 12)

```
function finalize():
  manifest = read_manifest()

  // Mark all assets as validated
  for asset_key in manifest.assets:
    if manifest.assets[asset_key].status != "needs_revision":
      manifest.assets[asset_key].status = "validated"

  // Set top-level status
  manifest.status = "ready_for_production"
  manifest.pipeline_stage = "stage_12"
  manifest.exported_at = ISO_datetime()
  manifest.updated_at = ISO_datetime()

  write_atomic("{project_dir}/export/export_manifest.json", json_serialize(manifest))
```

---

### GET RESUME STAGE

```
function get_resume_stage():
  manifest = read_manifest()

  // Find the stage number of the earliest asset that isn't validated
  ASSET_TO_STAGE = {
    "research":          1,
    "source_report":     2,
    "research_verified": 2,
    "story_outline":     3,
    "script":            4,
    "story_bible":       5,
    "storyboard":        6,
    "image_plan":        7,
    "ai_image_prompts":  8,
    "voice_script":      9,
    "voice_direction":   9,
    "subtitles":         9,
    "thumbnail_prompt":  10,
    "seo":               10,
    "qa_report":         11,
    "export_manifest":   12,
    "project_report":    12
  }

  // Check if .tmp files exist (interrupted write) → reset those assets to absent
  for asset_key, asset in manifest.assets:
    tmp_path = "{project_dir}/{asset.file}.tmp"
    if tmp_path exists:
      delete tmp_path
      manifest.assets[asset_key].status = "absent"
      log: "[RESUME] Deleted interrupted write: {tmp_path}"

  write_atomic(manifest_path, json_serialize(manifest))

  // Find earliest non-validated stage
  earliest_incomplete = 12
  for asset_key, asset in manifest.assets:
    if asset.status != "validated":
      stage = ASSET_TO_STAGE[asset_key]
      if stage < earliest_incomplete:
        earliest_incomplete = stage

  return earliest_incomplete
```

---

### WRITE PROJECT REPORT (Stage 12)

```
function write_project_report():
  manifest = read_manifest()
  qa_report = read_file("{project_dir}/logs/qa_report.md")

  // Parse qa_report for scores
  qa_scores = parse_qa_scores(qa_report)

  // Count asset statistics from script.md
  script = read_file("{project_dir}/script/script.md")
  actual_word_count = count_words(script)

  storyboard = read_file("{project_dir}/visuals/storyboard.md")
  beat_count = count_beats(storyboard)
  real_count = count_beats_by_type(storyboard, "real")
  ai_count = count_beats_by_type(storyboard, "ai-generated")

  story_outline = read_file("{project_dir}/script/story_outline.md")
  scene_count = count_scenes(story_outline)

  report = format_project_report(
    project_slug, topic, language, style, duration_minutes,
    target_words, actual_word_count,
    scene_count, beat_count, real_count, ai_count,
    qa_scores,
    manifest.assets
  )

  write_atomic("{project_dir}/export/project_report.md", report)
  update_asset("project_report", "complete")
```

**Project report format:**

```markdown
# Project Report
**Project:**   {project_slug}
**Topic:**     {topic}
**Language:**  {language}
**Style:**     {style}
**Duration:**  {duration_minutes} min target
**Completed:** {ISO_datetime}

## Production Assets

| Asset | File | Status |
|---|---|---|
| Research | research/research.md | ✓ Complete |
| Source Report | research/source_report.md | ✓ Complete |
| Verified Research | research/research_verified.md | ✓ Complete |
| Story Outline | script/story_outline.md | ✓ Complete |
| Script | script/script.md | ✓ Complete |
| Story Bible | script/story_bible.md | ✓ Complete |
| Storyboard | visuals/storyboard.md | ✓ Complete |
| Image Plan | visuals/image_plan.md | ✓ Complete |
| AI Image Prompts | visuals/ai_image_prompts.md | ✓ Complete |
| Voice Script | voice/voice_script.txt | ✓ Complete |
| Voice Direction | voice/voice_direction.md | ✓ Complete |
| Subtitles | voice/subtitles.srt | ✓ Complete |
| Thumbnail Prompt | seo/thumbnail_prompt.md | ✓ Complete |
| SEO Package | seo/seo.md | ✓ Complete |

## Script Statistics

| Metric | Value |
|---|---|
| Target word count | {target_words} |
| Actual word count | {actual_word_count} |
| Deviation from target | {pct}% |
| Estimated runtime | {actual_word_count / wpm} min |
| Scene count | {scene_count} |
| Visual beats | {beat_count} |
| Real images planned | {real_count} |
| AI images planned | {ai_count} |

## QA Summary

| Check type | Passed | Total |
|---|---|---|
| Critical | {qa_scores.critical_pass} | {qa_scores.critical_total} |
| Content | {qa_scores.content_pass} | {qa_scores.content_total} |
| Consistency | {qa_scores.consistency_pass} | {qa_scores.consistency_total} |

Overall QA score: {total_pass}/{total_checks} ({pct}%)

## Editor Handoff

1. **Voice:** Paste `voice/voice_script.txt` into ElevenLabs.
   Apply settings from `voice/voice_direction.md`.
   Save audio as `voice/voice_output.mp3`.

2. **Images:** Source real images using `visuals/image_plan.md`.
   Generate AI images using `visuals/ai_image_prompts.md`.

3. **Editing:** Follow `visuals/storyboard.md` for shot sequence.
   Import `voice/subtitles.srt` — update timecodes after audio is final.

4. **Upload:** Use `seo/seo.md` for title, description, and tags.
   Use `seo/thumbnail_prompt.md` to design the thumbnail.
   Set to private. Review. Publish. Post pinned comment.

## Production Notes

{any_warnings_or_decisions_logged_during_run}
```

---

## WRITE RULES

1. Always use atomic write: `.tmp` → rename
2. Never write partial JSON — build the full object in memory, then write
3. After every write: re-read and verify the file can be parsed as valid JSON
4. If re-read fails: delete the corrupt file, write it again from the in-memory object
5. The manifest is the ground truth — if in-memory state conflicts with manifest, trust the manifest
