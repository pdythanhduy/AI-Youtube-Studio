# Director Project Checklist — AI YouTube Studio OS

Per-stage validation checklists used by the Director AI after executing each stage. The Director reads this file during boot and applies the relevant section after each stage completes.

A checklist item is either:
- **CRITICAL** — Failure halts the pipeline
- **STANDARD** — Failure raises ERR_FAIL but allows one auto-retry
- **ADVISORY** — Failure raises ERR_WARN and logs but does not halt

---

## Stage 0 — Project Setup Checklist

| # | Item | Level | Pass Condition |
|---|---|---|---|
| 0.1 | Project slug is valid | CRITICAL | Lowercase, date prefix YYYYMMDD_, no spaces, no special chars, ≤50 chars total |
| 0.2 | All 8 subdirectories created | CRITICAL | input/, research/, script/, visuals/, voice/, seo/, export/, logs/ all exist |
| 0.3 | input.json written | CRITICAL | File exists at `input/input.json` and contains all 6 required fields |
| 0.4 | project.yaml written | STANDARD | File exists at `input/project.yaml` |
| 0.5 | export_manifest.json initialized | CRITICAL | File exists at `export/export_manifest.json` with all 17 asset entries at status `absent` |
| 0.6 | director_run_log.md initialized | STANDARD | File exists at `logs/director_run_log.md` with run header |
| 0.7 | Target word count calculated | CRITICAL | `target_word_count = video_length_minutes × 130` present in input.json |

---

## Stage 1 — Research Checklist

| # | Item | Level | Pass Condition |
|---|---|---|---|
| 1.1 | research.md exists | CRITICAL | File exists at `research/research.md` and is non-empty |
| 1.2 | Summary section present | STANDARD | Section `## Summary` present with 2-3 sentences |
| 1.3 | Key Facts section present | STANDARD | Section `## Key Facts` present |
| 1.4 | Minimum fact count | ADVISORY | At least 5 distinct facts listed |
| 1.5 | Sources section present | STANDARD | Section `## Sources` present |
| 1.6 | Minimum source count | ADVISORY | At least 3 sources with name, outlet, year |
| 1.7 | No confirmed-fake URLs | CRITICAL | No URL in file that is a plausible fabrication (suspiciously generic, no real outlet match) |
| 1.8 | Unresolved Questions section | STANDARD | Section `## Unresolved Questions` present |
| 1.9 | Correct language | CRITICAL | Content is written in `input.json.language` |
| 1.10 | Manifest updated | CRITICAL | `research.status = complete` in export_manifest.json |

---

## Stage 2 — Source Verification Checklist

| # | Item | Level | Pass Condition |
|---|---|---|---|
| 2.1 | source_report.md exists | CRITICAL | File exists at `research/source_report.md` |
| 2.2 | research_verified.md exists | CRITICAL | File exists at `research/research_verified.md` |
| 2.3 | Overall Status set | CRITICAL | One of: `PASS`, `NEEDS_REVISION`, `FAIL` |
| 2.4 | Overall Status is not FAIL | CRITICAL | Status = FAIL triggers pipeline halt |
| 2.5 | Every fact has a rating | STANDARD | Each fact in research.md has PASS/FLAG/FAIL assigned |
| 2.6 | No FAIL facts in verified | CRITICAL | research_verified.md contains no facts rated [FAIL] |
| 2.7 | NEEDS_REVISION warning logged | ADVISORY | If NEEDS_REVISION: ERR_WARN_001 in run log |
| 2.8 | Manifest updated | CRITICAL | `source_report.status = complete`, `research_verified.status = complete` |

---

## Stage 3 — Story Outline Checklist

| # | Item | Level | Pass Condition |
|---|---|---|---|
| 3.1 | story_outline.md exists | CRITICAL | File exists at `script/story_outline.md` |
| 3.2 | Hook moment identified | STANDARD | `## Hook` section present with moment description |
| 3.3 | All scenes have purpose labels | STANDARD | Every scene has one of: Setup / Rising Tension / Revelation / Dead End / Climax / Resolution / Open Question |
| 3.4 | All scenes have emotion labels | ADVISORY | Every scene has viewer emotion: Curiosity / Unease / Dread / Shock / Sadness / Confusion / Intrigue |
| 3.5 | Word count plan present | STANDARD | `## Word Count Plan` table present |
| 3.6 | Total word count matches target | ADVISORY | Total in plan within ±10% of `input.json.target_word_count` |
| 3.7 | Conclusion is open question or honest | CRITICAL | No fabricated resolution at end |
| 3.8 | Niche structure requirements met | STANDARD | For reddit_mystery: post/community/update beats present. For japanese_mystery: cultural context beat present |
| 3.9 | Speculation flags section present | ADVISORY | Section present (may be empty if no speculation) |
| 3.10 | Manifest updated | CRITICAL | `story_outline.status = complete` |

---

## Stage 4 — Script Writing Checklist

| # | Item | Level | Pass Condition |
|---|---|---|---|
| 4.1 | script.md exists | CRITICAL | File exists at `script/script.md` |
| 4.2 | Word count within range | STANDARD | Actual ≥ `target × 0.90` AND ≤ `target × 1.10` |
| 4.3 | Word count stated at top | ADVISORY | `**Word count:** {N}` appears at top of file |
| 4.4 | Hook ≤65 words | STANDARD | Hook section ≤65 words |
| 4.5 | Hook is not a greeting | CRITICAL | Hook does not begin with Hi / Hello / Welcome / Hey |
| 4.6 | All scenes labeled with timecodes | STANDARD | Every scene has `## Scene Name (X:XX - X:XX)` |
| 4.7 | No unverified facts without label | CRITICAL | All claims in script are either in research_verified.md or labeled as speculation |
| 4.8 | Scene structure matches outline | STANDARD | Same scenes in same order as story_outline.md |
| 4.9 | Tone matches style profile | ADVISORY | Dark/authoritative for dark_documentary; conversational for reddit_narration; etc. |
| 4.10 | Call to action once only | ADVISORY | Conclusion has max 1 CTA sentence |
| 4.11 | Language register correct | CRITICAL | Japanese: です/ます throughout. All languages: style register applied. |
| 4.12 | Manifest updated | CRITICAL | `script.status = complete` |

---

## Stage 5 — Story Bible Checklist

| # | Item | Level | Pass Condition |
|---|---|---|---|
| 5.1 | story_bible.md exists | CRITICAL | File exists at `script/story_bible.md` |
| 5.2 | Every named person has entry | STANDARD | People section covers all named individuals in script.md |
| 5.3 | Every location has entry | STANDARD | Locations section covers all named locations in script.md |
| 5.4 | All dates in timeline table | STANDARD | Timeline covers all dates mentioned in script.md |
| 5.5 | Dates in ISO format | ADVISORY | All dates: YYYY-MM-DD format with human-readable alongside |
| 5.6 | Pronunciation guide present | STANDARD | All non-English proper nouns have phonetic guide |
| 5.7 | Canonical Name Index present | CRITICAL | Quick-reference alphabetical index at bottom of file |
| 5.8 | Consistency flags documented | ADVISORY | Section present (may be empty) |
| 5.9 | Manifest updated | CRITICAL | `story_bible.status = complete` |

---

## Stage 6 — Scene Splitting Checklist

| # | Item | Level | Pass Condition |
|---|---|---|---|
| 6.1 | storyboard.md exists | CRITICAL | File exists at `visuals/storyboard.md` |
| 6.2 | All script scenes covered | CRITICAL | Every scene from script.md has at least one visual beat |
| 6.3 | No beat > 90 seconds | STANDARD | No single beat's timecode span exceeds 90 seconds |
| 6.4 | Image type assigned | CRITICAL | Every beat has image type: real/ai-generated/stock/screenshot/text-overlay/b-roll/map/screen-recording |
| 6.5 | Music mood per scene | STANDARD | Music mood specified for every scene (not every beat) |
| 6.6 | Visual Summary table present | STANDARD | Summary table with counts by image type |
| 6.7 | Names match story_bible | CRITICAL | All entity names match canonical forms from story_bible.md |
| 6.8 | Real events → real images | CRITICAL | Beats depicting real verified events use `real` type, not `ai-generated` |
| 6.9 | Dramatizations labeled | CRITICAL | All `ai-generated` beats that depict real events have `[DRAMATIZATION]` flag |
| 6.10 | Manifest updated | CRITICAL | `storyboard.status = complete` |

---

## Stage 7 — Image Planning Checklist

| # | Item | Level | Pass Condition |
|---|---|---|---|
| 7.1 | image_plan.md exists | CRITICAL | File exists at `visuals/image_plan.md` |
| 7.2 | All applicable beats covered | CRITICAL | Every real/stock/screenshot/map/screen-recording beat has a sourcing brief |
| 7.3 | Each brief has ≥2 search strategies | STANDARD | Every sourcing brief has Strategy A + Strategy B at minimum |
| 7.4 | License specified | STANDARD | Every strategy specifies the license type to check |
| 7.5 | No TBD entries | CRITICAL | "TBD" does not appear in any source strategy field |
| 7.6 | AI Escalation List present | STANDARD | Section present (may be empty if all beats can be real-sourced) |
| 7.7 | Escalated beats have concept notes | STANDARD | Each escalated beat has a concept note for Stage 8 |
| 7.8 | Search terms from story_bible | ADVISORY | Search terms use canonical name forms from story_bible.md |
| 7.9 | Manifest updated | CRITICAL | `image_plan.status = complete` |

---

## Stage 8 — AI Image Prompts Checklist

| # | Item | Level | Pass Condition |
|---|---|---|---|
| 8.1 | ai_image_prompts.md exists | CRITICAL | File exists at `visuals/ai_image_prompts.md` |
| 8.2 | One prompt per AI beat | CRITICAL | Every ai-generated beat + every escalated beat has one prompt |
| 8.3 | Prompts are self-contained | STANDARD | Each prompt specifies: subject, setting, mood, lighting, color, angle, style, aspect ratio |
| 8.4 | Negative prompts present | STANDARD | Every prompt entry has a negative prompt |
| 8.5 | No real person depicted realistically | CRITICAL | No prompt asks for a photorealistic likeness of a real named individual |
| 8.6 | No fake evidence | CRITICAL | No prompt could produce something resembling a fake document, screenshot, or crime scene photo |
| 8.7 | Dramatizations labeled | CRITICAL | All prompts for dramatization beats labeled `[DRAMATIZATION — NOT REAL]` |
| 8.8 | Style reference matches style profile | ADVISORY | Color palette and aesthetic in prompts matches `configs/style_profiles.md` for this style |
| 8.9 | Alternative prompts present | ADVISORY | Each entry has a simplified alternative prompt |
| 8.10 | Manifest updated | CRITICAL | `ai_image_prompts.status = complete` |

---

## Stage 9 — Voice Direction Checklist

### voice_script.txt

| # | Item | Level | Pass Condition |
|---|---|---|---|
| 9.1 | voice_script.txt exists | CRITICAL | File exists at `voice/voice_script.txt` |
| 9.2 | No markdown characters | CRITICAL | No `#`, `*`, `_`, `>`, `|` outside pacing markers |
| 9.3 | Pacing markers valid | STANDARD | All `[PAUSE:Xs]` use exact approved values; all `[SLOW]`/`[FAST]`/`[WHISPER]` are in approved list |
| 9.4 | [PAUSE:2s] present | STANDARD | At least one `[PAUSE:2s]` in file |
| 9.5 | [PAUSE:3s] present exactly once | STANDARD | Exactly one `[PAUSE:3s]` in file |
| 9.6 | [SLOW] tags closed | STANDARD | Every `[SLOW]` has a matching `[NORMAL]` after it |
| 9.7 | Word count matches script | STANDARD | Word count of voice_script.txt within 5% of script.md word count |

### subtitles.srt

| # | Item | Level | Pass Condition |
|---|---|---|---|
| 9.8 | subtitles.srt exists | CRITICAL | File exists at `voice/subtitles.srt` |
| 9.9 | Sequential indices | CRITICAL | Indices start at 1 and increment by 1 with no gaps |
| 9.10 | No timecode overlaps | CRITICAL | No segment starts before previous segment ends |
| 9.11 | Timecode format correct | CRITICAL | Format: `HH:MM:SS,mmm --> HH:MM:SS,mmm` (comma, not period) |
| 9.12 | Line length ≤42 chars | STANDARD | No subtitle line exceeds 42 characters |
| 9.13 | Segment duration 1-7 seconds | STANDARD | All segments between 1.0 and 7.0 seconds |

### voice_direction.md

| # | Item | Level | Pass Condition |
|---|---|---|---|
| 9.14 | voice_direction.md exists | STANDARD | File exists at `voice/voice_direction.md` |
| 9.15 | Voice character section | STANDARD | Defines register, speed, emotional character |
| 9.16 | Critical Moments section | STANDARD | Covers hook, climax, and closing line |
| 9.17 | Pronunciation guide | ADVISORY | Covers all proper nouns from story_bible.md |

### Manifest

| # | Item | Level | Pass Condition |
|---|---|---|---|
| 9.18 | Manifest updated | CRITICAL | `voice_script.status`, `voice_direction.status`, `subtitles.status` = complete |

---

## Stage 10 — YouTube SEO Checklist

| # | Item | Level | Pass Condition |
|---|---|---|---|
| 10.1 | seo.md exists | CRITICAL | File exists at `seo/seo.md` |
| 10.2 | 3 title options present | STANDARD | Exactly 3 title options labeled Option 1, 2, 3 |
| 10.3 | All titles ≤70 chars | CRITICAL | Character count stated; all options ≤70 chars |
| 10.4 | Description present | CRITICAL | Full description section present |
| 10.5 | Description hook in first 150 chars | CRITICAL | First 150 chars of description is not a channel greeting |
| 10.6 | Tag count 15-30 | STANDARD | Count tags; must be between 15 and 30 |
| 10.7 | Long-tail tags present | STANDARD | At least 2 tags are 5+ words |
| 10.8 | Chapters match outline | STANDARD | Chapter names and order match story_outline.md |
| 10.9 | 2 pinned comment options | ADVISORY | Section present with 2 options |
| 10.10 | thumbnail_prompt.md exists | CRITICAL | File exists at `seo/thumbnail_prompt.md` |
| 10.11 | Thumbnail text ≤4 words | STANDARD | Primary text overlay is 4 words or fewer |
| 10.12 | Thumbnail prompt self-contained | CRITICAL | Concept, prompt, text overlay, and color palette all specified |
| 10.13 | Manifest updated | CRITICAL | `seo.status = complete`, `thumbnail_prompt.status = complete` |

---

## Stage 11 — Final QA Checklist

### Critical Gate Checks (any FAIL = BLOCKED verdict)

| # | Item | Level | Pass Condition |
|---|---|---|---|
| 11.1 | All 15 output files exist | CRITICAL | All expected files in research/, script/, visuals/, voice/, seo/ |
| 11.2 | No FAIL in source_report | CRITICAL | source_report.md Overall Status ≠ FAIL |
| 11.3 | Script word count in range | CRITICAL | Within ±10% of target |
| 11.4 | No markdown in voice_script | CRITICAL | voice_script.txt has no markdown characters |
| 11.5 | SRT valid | CRITICAL | Sequential, non-overlapping, correct format |
| 11.6 | No TBD in image_plan | CRITICAL | image_plan.md has no TBD entries |
| 11.7 | All AI beats have prompts | CRITICAL | Every escalated beat has a prompt in ai_image_prompts.md |
| 11.8 | All SEO titles ≤70 chars | CRITICAL | All 3 options confirmed ≤70 characters |

### Content Checks (WARN on failure — does not block)

| # | Item | Level | Pass Condition |
|---|---|---|---|
| 11.9 | Hook ≤65 words | STANDARD | |
| 11.10 | All beats have visuals | STANDARD | |
| 11.11 | Pronunciation guide complete | ADVISORY | |
| 11.12 | Tag count 15-30 | STANDARD | |
| 11.13 | Thumbnail prompt self-contained | STANDARD | |

### Consistency Checks (WARN on failure — does not block)

| # | Item | Level | Pass Condition |
|---|---|---|---|
| 11.14 | Names match story_bible | STANDARD | Spot-check 5 names across all files |
| 11.15 | Dates consistent | STANDARD | Spot-check 3 dates across research_verified, script, storyboard |
| 11.16 | SEO chapters match outline | STANDARD | Chapter count and names match |
| 11.17 | Image count matches storyboard | ADVISORY | Visual count in image_plan matches storyboard beat count |
| 11.18 | Voice script word count matches script | STANDARD | Within ±5% |

---

## Stage 12 — Export Checklist

| # | Item | Level | Pass Condition |
|---|---|---|---|
| 12.1 | QA verdict is READY_FOR_EXPORT | CRITICAL | qa_report.md Overall verdict = READY_FOR_EXPORT |
| 12.2 | export_manifest.json finalized | CRITICAL | All asset statuses = validated, top-level status = ready_for_production |
| 12.3 | project_report.md written | CRITICAL | File exists at `export/project_report.md` |
| 12.4 | director_run_log.md completed | STANDARD | Completion entry added to run log |
| 12.5 | All 17 asset entries in manifest | CRITICAL | No missing asset entries in the manifest |

---

## Checklist Scoring

After each stage, the Director calculates:

```
Stage Score = (CRITICAL passed + STANDARD passed + ADVISORY passed) / (total items) × 100
```

Status assignment:
- All CRITICAL pass, all STANDARD pass → **PASS**
- All CRITICAL pass, some STANDARD fail (with retry) → **PASS** (after retry)
- All CRITICAL pass, some ADVISORY warn → **FLAGGED** (continues, warnings logged)
- Any CRITICAL fail → **FAIL** (pipeline halts)

The Final QA (Stage 11) uses its own separate scoring, reported as:
```
Critical: {N}/{N} ✓
Content: {N}/{N} with {N} warnings
Consistency: {N}/{N} with {N} warnings
Overall verdict: READY_FOR_EXPORT / NEEDS_REVISION / BLOCKED
```
