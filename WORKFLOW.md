# WORKFLOW — AI YouTube Studio OS

Step-by-step production pipeline from raw topic to publish-ready assets.

---

## Overview

The workflow has 10 stages. Each stage produces a specific output file. Stages run in order. No stage may be skipped.

```
Stage 0 → input.json
Stage 1 → research.md
Stage 2 → script.md
Stage 3 → storyboard.md
Stage 4 → image_plan.md
Stage 5 → voice_script.txt
Stage 6 → subtitles.srt
Stage 7 → thumbnail_prompt.md
Stage 8 → seo.md
Stage 9 → export_manifest.json
```

**Total production time (AI-assisted):** approximately 25-40 minutes per video.

---

## Stage 0: Project Setup

**Who runs this:** Human operator or orchestration agent.

**Steps:**

1. Create a new project folder:
   ```
   projects/YYYYMMDD_topic-slug/
   ```

2. Create `input.json` with the four required fields:
   ```json
   {
     "topic": "...",
     "language": "en",
     "video_length_minutes": 12,
     "style": "dark_documentary"
   }
   ```

3. Validate `input.json`:
   - All four required fields present
   - `language` is a valid ISO 639-1 code
   - `video_length_minutes` is between 5 and 60
   - `style` exists in STYLE_GUIDE.md

4. If validation passes → proceed to Stage 1.
   If validation fails → stop, report which field is invalid.

**Output:** Valid `input.json` in project folder.

---

## Stage 1: Research

**Who runs this:** Claude Code agent using `templates/research_prompt.md`.

**Steps:**

1. Read `input.json`.

2. Apply the research prompt template. Instruct the AI to:
   - Research the topic thoroughly
   - Generate a structured research brief
   - Identify key facts, timeline, people, locations
   - Flag unverified claims
   - Include at least 3 real, verifiable sources (no fabricated URLs)

3. Write output to `research.md`.

4. Validate `research.md`:
   - Minimum 5 distinct facts present
   - At least 3 sources listed
   - Timeline section present (if topic has a time-based narrative)
   - No placeholder text or "TBD" entries

**Output:** `research.md`

**Common failure:** AI fabricates source URLs. Mitigation: prompt explicitly instructs "If you are not certain a URL exists, write the source name and description only — do not fabricate a URL."

---

## Stage 2: Script Writing

**Who runs this:** Claude Code agent using `templates/script_prompt.md`.

**Steps:**

1. Read `input.json` and `research.md`.

2. Calculate target word count from `video_length_minutes`:
   ```
   target_words = video_length_minutes * 130
   ```

3. Apply the script prompt template. Instruct the AI to:
   - Write a full narration script
   - Use the style defined in `input.json` (see STYLE_GUIDE.md)
   - Structure: Hook → Introduction → 3-5 Scenes → Conclusion
   - Hook must be ≤ 30 seconds (≤ 65 words)
   - Hit target word count within ±10%
   - Use only facts from `research.md` (no new fabricated facts)

4. Write output to `script.md`.

5. Validate `script.md`:
   - Word count within target range
   - Hook section present and under 65 words
   - All scenes labeled with timecode estimates
   - No facts present that are not in `research.md`

**Output:** `script.md`

---

## Stage 3: Storyboard

**Who runs this:** Claude Code agent using `templates/storyboard_prompt.md`.

**Steps:**

1. Read `script.md`.

2. Break the script into 30-60 second beats.

3. For each beat, define:
   - Timecode range
   - Narration excerpt (first line of that beat)
   - Visual description (what appears on screen)
   - Image type: `real`, `ai-generated`, `stock`, `screenshot`, `text-overlay`, `b-roll`
   - Brief source note or AI prompt idea
   - Background music mood

4. Write output to `storyboard.md`.

5. Validate `storyboard.md`:
   - Every scene from `script.md` has at least one visual beat
   - Every visual has an assigned image type
   - No beats longer than 60 seconds without a visual change
   - Music mood specified for every scene

**Output:** `storyboard.md`

---

## Stage 4: Image Plan

**Who runs this:** Claude Code agent.

**Steps:**

1. Read `storyboard.md`.

2. For every visual in the storyboard, generate a row in the image plan table:
   - Scene number and name
   - Image type (real / ai-generated / stock / screenshot)
   - Source strategy: where to find or how to generate it
   - Search terms (for real images) or generation prompt (for AI images)

3. Apply image policy from `MASTER_RULE.md` Rule 5:
   - Real events → real images
   - Dramatizations → AI images, labeled
   - Atmosphere/mood → AI images acceptable
   - Screenshots of original content → take actual screenshots

4. Write output to `image_plan.md`.

5. Validate `image_plan.md`:
   - Row count matches visual count in `storyboard.md`
   - No row has "TBD" in source strategy
   - AI-generated images that depict real events are marked `[DRAMATIZATION]`

**Output:** `image_plan.md`

---

## Stage 5: Voice Script

**Who runs this:** Claude Code agent.

**Steps:**

1. Read `script.md`.

2. Strip all markdown formatting:
   - Remove `##` headers
   - Remove `**bold**`, `*italic*`
   - Remove scene labels and timecode annotations
   - Remove parenthetical stage directions

3. Add pacing markers based on punctuation and scene context:
   - Period at end of sentence → `[PAUSE:1s]`
   - Scene transition → `[PAUSE:1.5s]` on a new line
   - Dramatic reveal moment → `[PAUSE:2s]`
   - Rapid-fire fact sequence → `[FAST]` at start, `[NORMAL]` at end

4. Write output to `voice_script.txt`.

5. Validate `voice_script.txt`:
   - No markdown characters remaining (`#`, `*`, `_`, `[` except pacing markers, `]`)
   - Pacing markers present at scene transitions
   - Word count matches `script.md` ±5%
   - File is plain UTF-8 text, no special encoding

**Output:** `voice_script.txt`

---

## Stage 6: Subtitles

**Who runs this:** Claude Code agent.

**Steps:**

1. Read `voice_script.txt`.

2. Segment the text into subtitle blocks:
   - Target: 3-4 seconds per segment
   - Maximum: 7 seconds per segment
   - Maximum: 42 characters per line
   - Maximum: 2 lines per segment

3. Assign sequential timecodes. Use the word count and average speaking pace to estimate timing:
   ```
   Seconds per word ≈ 60 / (words_per_minute)
   English: ~130 wpm → ~0.46 seconds per word
   Japanese: ~300 mpm (morae) → adjust accordingly
   ```

4. Format as standard SRT:
   ```
   [index]
   HH:MM:SS,mmm --> HH:MM:SS,mmm
   [line 1]
   [line 2 if needed]
   [blank line]
   ```

5. Write output to `subtitles.srt`.

6. Validate `subtitles.srt`:
   - All indices sequential starting at 1
   - No timecode overlaps
   - No line exceeds 42 characters
   - No segment shorter than 1 second
   - No segment longer than 7 seconds

**Output:** `subtitles.srt`

---

## Stage 7: Thumbnail Prompt

**Who runs this:** Claude Code agent.

**Steps:**

1. Read `input.json` and the hook section of `script.md`.

2. Identify the single most visually compelling element of the video:
   - A person (real or composite)
   - A location (specific or atmospheric)
   - An object or symbol central to the mystery
   - An emotional state (fear, shock, confusion)

3. Design a thumbnail concept:
   - Central image: what is the main visual?
   - Text overlay: 2-4 bold words that create curiosity or shock
   - Color palette: consistent with niche (see STYLE_GUIDE.md)
   - Composition: rule of thirds, subject left or right of frame

4. Write a complete, self-contained image generation prompt.

5. Write output to `thumbnail_prompt.md`.

6. Validate `thumbnail_prompt.md`:
   - Concept section present
   - Image generation prompt is self-contained (works without reading the script)
   - Text overlay specified (max 4 words)
   - Color palette described

**Output:** `thumbnail_prompt.md`

---

## Stage 8: SEO Package

**Who runs this:** Claude Code agent using `templates/seo_prompt.md`.

**Steps:**

1. Read `input.json`, `script.md`, and `research.md`.

2. Identify primary keywords:
   - Main subject name(s)
   - Location name(s)
   - Event type (disappearance, haunting, mystery, etc.)
   - Niche keywords (true crime, unexplained, unsolved, etc.)

3. Generate:
   - 3 title options (max 70 chars each, with primary keyword)
   - Full description (min 300 words, hook in first 150 chars, timestamps, tags section)
   - Tags list (15-30 tags)
   - Hashtags (3-5, for description)
   - Chapter timestamps matching `script.md` scene structure

4. Write output to `seo.md`.

5. Validate `seo.md`:
   - All 3 titles ≤ 70 characters
   - Description first 150 chars is a hook (no channel intro)
   - ≥ 15 tags
   - Timestamps match scene structure in `script.md`

**Output:** `seo.md`

---

## Stage 9: Export Manifest

**Who runs this:** Claude Code agent (orchestrator).

**Steps:**

1. Read all output files from the project folder.

2. Run the full export readiness checklist from `MASTER_RULE.md` Rule 12.

3. For each check:
   - If passed: set status to `"complete"`
   - If failed: set status to `"needs_revision"` and add `"error"` key with description

4. Write output to `export_manifest.json`.

5. Set top-level `"status"`:
   - `"ready_for_production"` — all checks passed
   - `"needs_revision"` — one or more checks failed

**Output:** `export_manifest.json`

---

## Post-Production Handoff

Once `export_manifest.json` shows `"ready_for_production"`, the project package is handed to the editor:

| Editor Task | Source File |
|---|---|
| Voice recording / TTS | `voice_script.txt` |
| Image sourcing | `image_plan.md` |
| Scene assembly | `storyboard.md` |
| Subtitle import | `subtitles.srt` |
| Thumbnail design | `thumbnail_prompt.md` |
| YouTube upload | `seo.md` |

The editor does not need to read `research.md` or `script.md` — those are upstream documents that informed the production files.

---

## Error Handling

| Error Type | Action |
|---|---|
| Missing required input | Stop at Stage 0. Report which field is missing. |
| Fabricated URL in research | Flag in research.md. Do not proceed until resolved. |
| Script word count out of range | Re-run Stage 2 with explicit word count constraint. |
| Inconsistent names/dates | Fix in all affected files before Stage 9. |
| SRT timecode overlap | Re-run Stage 6. |
| Image plan has TBDs | Resolve all TBDs before Stage 9. |
| Export manifest not all green | Report failing checks. Do not set `ready_for_production`. |

---

## Automation Notes

When run by a Claude Code agent, each stage follows this pattern:

```
SYSTEM: You are a production assistant for AI-Youtube-Studio.
Task: [Stage Name]
Read: [input files]
Template: templates/[template_name].md
Output: projects/[project_id]/[output_file]
Rules: MASTER_RULE.md
Validate before writing: [checklist items for this stage]
```

The orchestration agent maintains the project state in `export_manifest.json` and resumes from the last completed stage if interrupted.
