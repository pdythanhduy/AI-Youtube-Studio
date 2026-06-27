# Acceptance Tests — AI YouTube Studio OS

Feature-level acceptance criteria. A pipeline run is "accepted" when all tests in this document pass. These tests define what "done" means for the system, not just for individual files.

---

## Test Naming Convention

`AT-[COMPONENT]-[NNN]`

- `AT` = Acceptance Test
- `COMPONENT` = which subsystem or stage is being tested
- `NNN` = sequential number

Example: `AT-STAGE01-001` = Acceptance test for Stage 01, test #1.

---

## AT-INPUT: Input Validation Tests

### AT-INPUT-001: Required Fields Present
**Given:** An `input.json` file  
**When:** The Director Engine reads it  
**Then:** All four required fields (`topic`, `language`, `video_length_minutes`, `style`) are present  
**Fail behavior:** Pipeline halts immediately with specific error naming the missing field  
**Test data:** `inputs/missing_topic.json`, `inputs/missing_language.json`, etc.

### AT-INPUT-002: Language Code Valid
**Given:** `input.json` with `language` field  
**When:** Routing Engine attempts to load language profile  
**Then:** The language code matches a profile in `configs/language_profiles.md`  
**Fail behavior:** Pipeline halts with error: "Language `{code}` has no defined profile"  
**Test data:** `inputs/invalid_language.json` (e.g., `"language": "zz"`)

### AT-INPUT-003: Style ID Valid
**Given:** `input.json` with `style` field  
**When:** Routing Engine attempts to load style profile  
**Then:** The style ID matches a profile in `configs/style_profiles.md`  
**Fail behavior:** Pipeline halts with error: "Style `{id}` has no defined profile"  
**Test data:** `inputs/invalid_style.json`

### AT-INPUT-004: Video Length in Range
**Given:** `input.json` with `video_length_minutes` field  
**When:** Workflow Engine calculates target word count  
**Then:** `video_length_minutes` is an integer between 5 and 60  
**Fail behavior:** Pipeline halts with error  
**Test data:** `inputs/length_4.json`, `inputs/length_61.json`, `inputs/length_string.json`

---

## AT-STAGE01: Research Tests

### AT-STAGE01-001: Research Output Exists
**Given:** Valid `input.json`  
**When:** Stage 01 completes  
**Then:** `research.md` exists in the project folder and is non-empty  

### AT-STAGE01-002: Minimum Fact Count
**Given:** Completed `research.md`  
**When:** QA Engine validates  
**Then:** At least 5 distinct verified facts are present in the Key Facts section  

### AT-STAGE01-003: Minimum Source Count
**Given:** Completed `research.md`  
**When:** QA Engine validates  
**Then:** At least 3 sources are listed in the Sources section, each with name, outlet, and year  

### AT-STAGE01-004: No Fabricated URLs
**Given:** Completed `research.md`  
**When:** QA Engine validates  
**Then:** Any URL present can be confirmed to exist, or is marked "URL not confirmed"  

### AT-STAGE01-005: Language Correct
**Given:** `input.json` with `language: "ja"`  
**When:** Stage 01 completes  
**Then:** `research.md` content is written in Japanese  

---

## AT-STAGE02: Source Verifier Tests

### AT-STAGE02-001: Source Report Exists
**Given:** Completed `research.md`  
**When:** Stage 02 completes  
**Then:** Both `source_report.md` and `research_verified.md` exist  

### AT-STAGE02-002: Overall Status Assigned
**Given:** Completed `source_report.md`  
**When:** QA Engine validates  
**Then:** Overall status is one of: `PASS`, `NEEDS_REVISION`, or `FAIL` (not blank)  

### AT-STAGE02-003: FAIL Status Halts Pipeline
**Given:** `source_report.md` with Overall Status = `FAIL`  
**When:** Director Engine reads the verdict  
**Then:** Pipeline halts and human review is requested before proceeding to Stage 03  

### AT-STAGE02-004: FAIL Facts Removed
**Given:** `source_report.md` with one or more `[FAIL]` ratings  
**When:** `research_verified.md` is generated  
**Then:** No `[FAIL]` facts appear in `research_verified.md`  

---

## AT-STAGE04: Script Writer Tests

### AT-STAGE04-001: Word Count in Range
**Given:** `input.json` with `video_length_minutes: 12`  
**When:** `script.md` is generated and validated  
**Then:** Word count is between 1,404 and 1,716 (1,560 ±10%)  

### AT-STAGE04-002: Hook Length
**Given:** Completed `script.md`  
**When:** QA Engine validates  
**Then:** The Hook section is ≤65 words  

### AT-STAGE04-003: No Channel Greeting in Hook
**Given:** Completed `script.md`  
**When:** QA Engine validates  
**Then:** The Hook section does not begin with "Hi", "Hello", "Welcome", or "Hey"  

### AT-STAGE04-004: Facts Only from Research
**Given:** Completed `script.md` and `research_verified.md`  
**When:** QA Engine validates  
**Then:** Every factual claim in the script is traceable to `research_verified.md` or labeled as speculation  

### AT-STAGE04-005: Scene Structure Matches Outline
**Given:** Completed `script.md` and `story_outline.md`  
**When:** QA Engine validates  
**Then:** Scene count and names in `script.md` match `story_outline.md`  

---

## AT-STAGE09: Voice Director Tests

### AT-STAGE09-001: Voice Script Is Plain Text
**Given:** Completed `voice_script.txt`  
**When:** QA Engine validates  
**Then:** File contains no markdown characters (`#`, `*`, `_`, `|`, `>`) outside of approved pacing markers  

### AT-STAGE09-002: Required Pacing Markers Present
**Given:** Completed `voice_script.txt`  
**When:** QA Engine validates  
**Then:** File contains at least one `[PAUSE:2s]` and exactly one `[PAUSE:3s]`  

### AT-STAGE09-003: Pacing Marker Syntax Valid
**Given:** Completed `voice_script.txt`  
**When:** QA Engine validates  
**Then:** All pacing markers exactly match the approved list from `configs/output_profiles.md`  

### AT-STAGE09-004: Word Count Matches Script
**Given:** `voice_script.txt` and `script.md`  
**When:** QA Engine validates  
**Then:** Word count of `voice_script.txt` is within 5% of `script.md` word count  

---

## AT-STAGE06: Storyboard Tests

### AT-STAGE06-001: Every Scene Has a Visual
**Given:** Completed `storyboard.md`  
**When:** QA Engine validates  
**Then:** Every scene from `script.md` has at least one visual beat  

### AT-STAGE06-002: Image Type Assigned
**Given:** Completed `storyboard.md`  
**When:** QA Engine validates  
**Then:** Every visual beat has an assigned image type (`real`, `ai-generated`, `stock`, `screenshot`, `text-overlay`, `b-roll`, `map`, `screen-recording`)  

### AT-STAGE06-003: No Beat Exceeds 90 Seconds
**Given:** Completed `storyboard.md`  
**When:** QA Engine validates  
**Then:** No single visual beat's timecode range exceeds 90 seconds  

---

## AT-STAGE10: SEO Tests

### AT-STAGE10-001: Title Length
**Given:** Completed `seo.md`  
**When:** QA Engine validates  
**Then:** All 3 title options are ≤70 characters (counted including spaces)  

### AT-STAGE10-002: Tag Count
**Given:** Completed `seo.md`  
**When:** QA Engine validates  
**Then:** Tag count is between 15 and 30  

### AT-STAGE10-003: Description Hook
**Given:** Completed `seo.md`  
**When:** QA Engine validates  
**Then:** The first 150 characters of the description do not contain "Hi", "Hello", "Welcome", or the channel name  

### AT-STAGE10-004: Chapters Present
**Given:** Completed `seo.md`  
**When:** QA Engine validates  
**Then:** A CHAPTERS section is present with at least 3 timestamp entries  

### AT-STAGE10-005: Long-Tail Tag Present
**Given:** Tags field in `seo.md`  
**When:** QA Engine validates  
**Then:** At least 2 tags are 5+ words (long-tail search phrases)  

---

## AT-EXPORT: Export Tests

### AT-EXPORT-001: All Required Files Exist
**Given:** A completed pipeline run  
**When:** Export Engine validates  
**Then:** All 15 required project output files exist and are non-empty  

### AT-EXPORT-002: No TBD in Image Plan
**Given:** Completed `image_plan.md`  
**When:** Export Engine validates  
**Then:** No occurrence of "TBD" or "tbd" in the source strategy field of any row  

### AT-EXPORT-003: Manifest Status Accurate
**Given:** All validation passed  
**When:** `export_manifest.json` is finalized  
**Then:** Top-level `status` is `ready_for_production` and all asset statuses are `validated`  

### AT-EXPORT-004: Export Bundle Created
**Given:** `ready_for_production` status  
**When:** Export Engine completes  
**Then:** `export_bundle/` directory exists with the correct subfolder structure and `editor_handoff.md`  

---

## AT-CONSISTENCY: Cross-File Tests

### AT-CONSISTENCY-001: Names Match Story Bible
**Given:** All project output files + `story_bible.md`  
**When:** QA Engine runs consistency layer  
**Then:** Every named entity in all files matches the canonical form in `story_bible.md`  

### AT-CONSISTENCY-002: Dates Consistent
**Given:** All project output files + `story_bible.md`  
**When:** QA Engine validates  
**Then:** No event has different dates in different files  

### AT-CONSISTENCY-003: SEO Chapters Match Outline
**Given:** `seo.md` chapters + `story_outline.md`  
**When:** QA Engine validates  
**Then:** Chapter names in `seo.md` match scene names in `story_outline.md`  
