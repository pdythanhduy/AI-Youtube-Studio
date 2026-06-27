# Director Runtime — Execution Entry Point

This file is the first runtime module Claude Code executes. It acts as the conductor: validates inputs, calls each module in order, and owns the top-level pass/fail decision.

---

## ACTIVATION

Claude Code reads this file when a user provides the four production inputs:

```
TOPIC: <string>
LANGUAGE: en | ja | vi
DURATION_MINUTES: <int 5-60>
STYLE: dark_documentary | reddit_narration | mystery_investigation | japanese_mystery
```

Or when resuming:

```
RESUME PROJECT: <project_slug>
```

---

## EXECUTION SEQUENCE

Execute the following in order. Do not skip steps. Do not reorder steps.

```
STEP 1  → INPUT VALIDATION         (this file, Section: Input Validation)
STEP 2  → SYSTEM BOOT              (context_loader.md, Section: System Boot Load)
STEP 3  → PROJECT DETECTION        (this file, Section: New vs Resume)
STEP 4  → STAGE LOOP               (pipeline_executor.md)
STEP 5  → COMPLETION REPORT        (this file, Section: Completion Report)
```

---

## INPUT VALIDATION

### New Run Validation

Check each field against its constraint. Stop immediately if any fails.

| Field | Constraint | Fail action |
|---|---|---|
| `TOPIC` | Non-empty string | Output: `Missing TOPIC. Provide a topic string.` → Stop |
| `LANGUAGE` | One of: `en`, `ja`, `vi` | Output: `Language '{value}' is not supported. Use: en, ja, vi.` → Stop |
| `DURATION_MINUTES` | Integer 5–60 | Output: `Duration must be an integer between 5 and 60.` → Stop |
| `STYLE` | One of: `dark_documentary`, `reddit_narration`, `mystery_investigation`, `japanese_mystery` | Output: `Style '{value}' not recognized. Use one of the four valid styles.` → Stop |

If all fields pass, compute derived values:

```
niche         ← derive_niche(STYLE, TOPIC)
project_slug  ← YYYYMMDD + "_" + slugify(TOPIC)
target_words  ← compute_target_words(DURATION_MINUTES, LANGUAGE)
template_file ← resolve_template(niche)
```

### Niche Derivation: `derive_niche(style, topic)`

```
if style == "reddit_narration"   → niche = "reddit_mystery"
if style == "japanese_mystery"   → niche = "japanese_mystery"
if style == "mystery_investigation" → niche = "internet_mystery"
if style == "dark_documentary":
    if topic contains Japanese location or cultural references → niche = "japanese_mystery"
    if topic references Reddit, r/, post, OP, update → niche = "reddit_mystery"
    else → niche = "internet_mystery"
```

Log the niche decision: `[INFO ERR_INFO_002] Niche '{niche}' derived from style and topic.`

### Word Count: `compute_target_words(duration, language)`

```
base = duration × 130
if language == "ja": target = round(base × 0.77)
if language == "vi": target = round(base × 0.92)
if language == "en": target = base
```

### Slug: `slugify(topic)`

```
1. Lowercase
2. Remove: ', ", (, ), !, ?, ., ,, :, ;
3. Replace spaces with hyphens
4. Remove leading articles: the-, a-, an-
5. Truncate to 40 characters at a word boundary
6. Remove trailing hyphen
```

Example: `"The Mystery of Hashima Island"` → `"mystery-of-hashima-island"`

### Template Resolution: `resolve_template(niche)`

```
"japanese_mystery"  → "templates/japan_template.md"
"reddit_mystery"    → "templates/reddit_template.md"
"internet_mystery"  → "templates/mystery_template.md"
```

### Resume Run Validation

```
1. Check that projects/{project_slug}/ exists
2. Check that projects/{project_slug}/export/export_manifest.json exists
3. If either missing → Output: "Project '{slug}' not found. Check the project slug." → Stop
4. Call manifest_manager.md → Section: Read Manifest
5. Determine resume_from_stage (earliest stage with status ≠ validated)
6. Output: "[RESUME] Resuming project '{slug}' from Stage {N}."
7. Skip Steps 2-3, proceed to pipeline_executor.md with resume_from_stage = N
```

---

## SYSTEM BOOT DISPLAY

After input validation passes (new run), output:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DIRECTOR AI v1 — BOOTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Loading system files...
```

Then call `context_loader.md → Section: System Boot Load`.

After context_loader returns, output:

```
System files loaded:   ✓
Template loaded:       {template_file}
Language profile:      {language}
Style profile:         {style}
Prompt files:          10/10 ✓

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PRODUCTION JOB CONFIRMED
Topic:          {TOPIC}
Language:       {LANGUAGE}
Duration:       {DURATION_MINUTES} min
Style:          {STYLE}
Niche:          {niche}
Target words:   {target_words}
Project slug:   {project_slug}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Starting pipeline. Stand by.
```

---

## NEW VS RESUME ROUTING

```
if RESUME command:
    → validate resume (see above)
    → go to pipeline_executor.md with resume_from_stage

if NEW command:
    → run system boot
    → go to pipeline_executor.md with start_stage = 0
```

---

## COMPLETION REPORT

Called by pipeline_executor.md when Stage 12 completes successfully.

Output:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DIRECTOR AI v1 — PIPELINE COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Project: {project_slug}
Status:  READY FOR PRODUCTION ✓

Output folder: projects/{project_slug}/

Files ready for editor:
  → voice/voice_script.txt       (TTS / voice actor)
  → visuals/storyboard.md        (shot list)
  → visuals/image_plan.md        (image sourcing)
  → visuals/ai_image_prompts.md  (AI image generation)
  → voice/subtitles.srt          (subtitle import)
  → seo/thumbnail_prompt.md      (thumbnail design)
  → seo/seo.md                   (YouTube upload)

QA Score:          {qa_pass}/{qa_total} ({qa_pct}%)
Total warnings:    {total_warnings}
Stages completed:  13 / 13
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Next: Open projects/{project_slug}/export/project_report.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## GLOBAL STATE

Director Runtime maintains this state throughout the pipeline session. All other modules read from this state.

```
RUNTIME STATE (in-memory, not written to disk):
  project_slug        ← set at input validation
  topic               ← from input
  language            ← from input
  duration_minutes    ← from input
  style               ← from input
  niche               ← derived
  target_words        ← computed
  template_file       ← resolved
  project_dir         ← "projects/{project_slug}/"
  total_warnings      ← 0, incremented by logging_system
  stages_complete     ← [], populated by pipeline_executor
  qa_score            ← set by Stage 11
```

All `{variable}` references in other runtime modules resolve from this state.
