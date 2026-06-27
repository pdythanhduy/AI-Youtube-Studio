# Context Loader — File Loading and Injection

Handles all file reading for the runtime. Two functions: system boot load (read once at startup) and stage context load (read per stage). Called by `director_runtime.md` and `stage_runner.md`.

---

## SYSTEM BOOT LOAD

Called once during system boot. Read all system files into memory. If any file is missing, halt with `ERR_CRITICAL_004`.

**Read order** (read in this sequence — each file may reference content from files above it):

```
GROUP 1 — Core rules (read first, these govern everything)
  MASTER_RULE.md
  MASTER_PLAN.md
  WORKFLOW.md
  STYLE_GUIDE.md

GROUP 2 — Architecture
  core/naming_conventions.md
  core/file_lifecycle.md

GROUP 3 — Engines (read in dependency order)
  engine/director_engine.md
  engine/workflow_engine.md
  engine/routing_engine.md
  engine/decision_engine.md
  engine/qa_engine.md
  engine/export_engine.md

GROUP 4 — Configuration
  configs/configuration_system.md
  configs/language_profiles.md
  configs/style_profiles.md
  configs/output_profiles.md

GROUP 5 — Template (only the one that matches this niche)
  {template_file}               ← resolved at input validation

GROUP 6 — All prompt files
  prompts/01_research.md
  prompts/02_source_verifier.md
  prompts/03_story_outline.md
  prompts/04_script_writer.md
  prompts/05_story_bible.md
  prompts/06_scene_splitter.md
  prompts/07_image_finder.md
  prompts/08_image_prompt_generator.md
  prompts/09_voice_director.md
  prompts/10_youtube_seo.md

GROUP 7 — Runtime support
  agents/director_runtime_protocol.md
  agents/director_error_handling.md
  agents/director_project_checklist.md
```

**On missing file:**

```
⛔ BOOT FAILED — Required file missing
File: {filepath}
Action: Restore the missing file from the repository before running.
HALT.
```

**On successful load:**

Count files in each group. Report:
```
[BOOT] Core rules:      4/4 ✓
[BOOT] Architecture:    2/2 ✓
[BOOT] Engines:         6/6 ✓
[BOOT] Configuration:   4/4 ✓
[BOOT] Template:        1/1 ✓ ({template_file})
[BOOT] Prompt files:   10/10 ✓
[BOOT] Runtime:         3/3 ✓
```

---

## STAGE CONTEXT LOAD

Called by `stage_runner.md` before each stage executes. Returns the list of project files to inject as context for that stage.

Files are injected in the order listed. Always inject system files first, then project files.

### Stage 0 — Project Setup
```
(no context files — reads only from runtime state)
```

### Stage 1 — Research
```
SYSTEM:
  configs/language_profiles.md   (language-specific research norms)
  configs/style_profiles.md      (style niche for research focus)
  {template_file}                (niche-specific research requirements)

PROJECT:
  input/input.json               (topic, language, style, niche, target_words)
```

### Stage 2 — Source Verification
```
SYSTEM:
  configs/language_profiles.md

PROJECT:
  input/input.json
  research/research.md           (the file being audited)
```

### Stage 3 — Story Outline
```
SYSTEM:
  configs/language_profiles.md
  configs/style_profiles.md
  {template_file}                (required narrative beats for this niche)

PROJECT:
  input/input.json
  research/research_verified.md  (facts to structure into scenes)
```

### Stage 4 — Script Writing
```
SYSTEM:
  configs/language_profiles.md   (wpm, sentence length, number rules)
  configs/style_profiles.md      (tone, pacing, forbidden phrases)
  {template_file}                (forbidden framings, required beats)

PROJECT:
  input/input.json
  research/research_verified.md  (ALL facts come from here — no exceptions)
  script/story_outline.md        (scene structure to follow)
```

### Stage 5 — Story Bible
```
SYSTEM:
  configs/language_profiles.md   (name conventions, furigana policy)

PROJECT:
  input/input.json
  research/research_verified.md  (source of truth for facts)
  script/script.md               (extract all entities from here)
```

### Stage 6 — Scene Splitting
```
SYSTEM:
  configs/style_profiles.md      (transition types, visual preferences)
  {template_file}                (image source priorities)

PROJECT:
  input/input.json
  script/script.md               (the narration to split into beats)
  script/story_bible.md          (canonical names for visual descriptions)
```

### Stage 7 — Image Planning
```
SYSTEM:
  configs/style_profiles.md      (image type preferences per style)
  {template_file}                (priority image sources for this niche)

PROJECT:
  input/input.json
  visuals/storyboard.md          (beats that need real/stock images)
  script/story_bible.md          (canonical names for search terms)
```

### Stage 8 — AI Image Prompts
```
SYSTEM:
  configs/style_profiles.md      (color palette, aesthetic for this style)
  {template_file}                (AI prompt visual vocabulary)

PROJECT:
  input/input.json
  visuals/storyboard.md          (beats that need AI images)
  visuals/image_plan.md          (escalation list + concept notes)
  script/story_bible.md          (canonical names — no invented characters)
```

### Stage 9 — Voice Direction
```
SYSTEM:
  configs/language_profiles.md   (wpm, pacing markers, SRT spec)
  configs/style_profiles.md      (voice character, pause budget)
  configs/output_profiles.md     (plain_text_tts spec, srt_subtitles spec)
  {template_file}                (pacing overrides — e.g. japan Ma principle)

PROJECT:
  input/input.json
  script/script.md               (the narration to convert)
  script/story_bible.md          (pronunciation guide source)
  script/story_outline.md        (scene timing reference)
```

### Stage 10 — YouTube SEO
```
SYSTEM:
  configs/language_profiles.md   (non-English: English Tags Addendum rule)
  configs/style_profiles.md      (thumbnail aesthetic)

PROJECT:
  input/input.json
  research/research_verified.md  (keywords and topic context for tags)
  script/script.md               (title and description inspiration)
  script/story_bible.md          (canonical names for title/tags)
  script/story_outline.md        (chapter names and order)
```

### Stage 11 — Final QA
```
ALL project output files (read to validate):
  research/research.md
  research/source_report.md
  research/research_verified.md
  script/story_outline.md
  script/script.md
  script/story_bible.md
  visuals/storyboard.md
  visuals/image_plan.md
  visuals/ai_image_prompts.md
  voice/voice_script.txt
  voice/voice_direction.md
  voice/subtitles.srt
  seo/seo.md
  seo/thumbnail_prompt.md
```

### Stage 12 — Export
```
PROJECT:
  logs/qa_report.md              (verdict must be READY_FOR_EXPORT)
  export/export_manifest.json    (to finalize)
```

---

## TEMPLATE ADDENDUM LOAD

For stages that use a template addendum, load the corresponding section from `{template_file}`.

Template files define addenda with this header pattern: `## Stage Addendum: stage_NN`

```
function load_template_addendum(stage_number):
  section_header = "## Stage Addendum: stage_0{stage_number}"
  content = extract_section({template_file}, section_header)
  if content is None:
    return ""   // no addendum for this stage in this template
  return content
```

Stages that load template addenda: 1, 3, 4, 6, 7, 8, 9

Stages that do NOT load addenda: 0, 2, 5, 10, 11, 12

---

## FILE READ ERRORS

```
if file not found at boot:        → ERR_CRITICAL_004, HALT
if file not found at stage load:  → ERR_CRITICAL_005, HALT
if file is empty at stage load:   → log ERR_WARN_099 "Empty context file: {file}", continue with empty content
if file too large (>500KB):       → read first 500KB, log "[INFO] Context file truncated: {file} ({size}KB)"
```
