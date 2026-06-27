# script/ — Story, Script, and Reference

This folder contains all narrative content. It is written by Stages 3, 4, and 5.

---

## Files

### `story_outline.md` — Scene-by-scene narrative plan (Stage 3)

**Written by:** Director AI running `prompts/03_story_outline.md`

Contains:
- **Hook Moment** — the opening image or question (not the full hook text)
- **Scene Breakdown** — every scene with title, purpose label, and viewer emotion
- **Beat Summary** — what happens in each scene
- **Word Count Plan** — target word counts per scene summing to `video_length_minutes × 130`
- **Narrative Arc** — the emotional journey from curiosity to resolution (or open question)
- **Speculation Flags** — any beats that rely on unverified speculation

This is the blueprint. The script writer follows this structure exactly.

**Status after stage:** `story_outline.status = complete` in manifest

---

### `script.md` — Full narration script (Stage 4)

**Written by:** Director AI running `prompts/04_script_writer.md`

Contains:
- **Word count header** — actual word count vs target
- **Hook** — ≤65 words, no channel greeting
- **Scene sections** — each labeled `## Scene Name (X:XX - X:XX)`
- **Full narration** — all dialogue/narration text
- **[SPECULATION]** labels where facts are not in `research_verified.md`

This is the file that gets read by the voice director in Stage 9.

**Target word count:** `video_length_minutes × 130` (±10%)

**Status after stage:** `script.status = complete` in manifest

---

### `story_bible.md` — Canonical reference (Stage 5)

**Written by:** Director AI running `prompts/05_story_bible.md`

Contains:
- **People Index** — every named person with role, key facts, canonical name form
- **Locations Index** — every named location with canonical form, geographic context
- **Timeline** — all dates in ISO format with human-readable equivalents
- **Terminology** — specialized terms and their definitions
- **Pronunciation Guide** — phonetic guides for all non-English proper nouns
- **Canonical Name Index** — alphabetical quick-reference table
- **Consistency Flags** — any conflicts found and how they were resolved

This is the single source of truth for names and facts. All subsequent stages must use the canonical forms from this file.

**Status after stage:** `story_bible.status = complete` in manifest

---

## Human Review Points

After Stage 3: You may adjust the scene structure or word count distribution before Stage 4 runs.

After Stage 4: Review the full script. You may edit it directly. If you do, update `script.status` back to `in_progress` and re-run Stage 5 (story bible must reflect the updated script).

After Stage 5: Review the canonical name list. Confirm pronunciation guides are correct, especially for Japanese/Vietnamese names.

---

## What Does NOT Belong Here

- Research files (go in `research/`)
- Visual planning (go in `visuals/`)
- Voice files (go in `voice/`)
