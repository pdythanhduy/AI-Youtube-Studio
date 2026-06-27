# Regression Tests — AI YouTube Studio OS

Regression test suite to detect when system changes break previously-working behavior. Run the full suite after any change to prompts, templates, configs, or engine logic. Any failure blocks the change from merging.

---

## Test Naming Convention

`RT-[AREA]-[NNN]`

- `RT` = Regression Test
- `AREA` = system area (PIPELINE, PROMPT, CONFIG, TEMPLATE, ENGINE)
- `NNN` = sequential number

---

## What Triggers a Full Regression Run

| Change Type | Regression Scope |
|---|---|
| Any prompt file modified | Full pipeline regression (all RT-PIPELINE tests) |
| Template file modified | Template-specific tests + RT-PIPELINE for that niche |
| Config file modified | Config-specific tests + affected acceptance tests |
| Engine logic changed | All tests for that engine + RT-PIPELINE |
| New language profile added | RT-CONFIG-LANG + full pipeline test with new language |
| New style profile added | RT-CONFIG-STYLE + full pipeline test with new style |

---

## RT-PIPELINE: Full Pipeline Regression Tests

These tests run the full pipeline with a standard fixture and verify that known-good behavior is preserved.

### RT-PIPELINE-001: English Internet Mystery — 12 Minute
**Fixture:** `tests/fixtures/inputs/en_internet_mystery_12min.json`  
**Scope:** Full 10-stage pipeline  
**Expected outcomes:**
- All 15 output files generated
- `script.md` word count between 1,404-1,716
- Hook section ≤65 words
- No [FAIL] items in `source_report.md`
- `voice_script.txt` contains no markdown
- `subtitles.srt` passes SRT validation
- All 3 SEO titles ≤70 chars
- Tag count 15-30
- Export manifest status = `ready_for_production`

**How to run:** Full pipeline execution with fixture. Compare outputs against baseline metrics.

### RT-PIPELINE-002: Japanese Mystery — 8 Minute
**Fixture:** `tests/fixtures/inputs/ja_japanese_mystery_8min.json`  
**Scope:** Full 10-stage pipeline  
**Expected outcomes:**
- All output files in Japanese
- です/ます register maintained throughout script
- Cultural context beat present in story outline
- Legend vs. fact distinction labeled where applicable
- Story bible includes Japanese name format (family-first)
- Word count between 730-1,000 (8min × 100 = 800 ±10% for Japanese equivalent)

### RT-PIPELINE-003: Reddit Mystery — English — 10 Minute
**Fixture:** `tests/fixtures/inputs/en_reddit_mystery_10min.json`  
**Scope:** Full 10-stage pipeline  
**Expected outcomes:**
- Script contains clear first-person post narration section
- Story outline includes platform context, post beat, community reaction, current status
- Screenshot beat present in storyboard (Reddit post)
- Truth status labeled once in script
- SEO tags include at least 3 reddit-specific tags

### RT-PIPELINE-004: Vietnamese Reddit Mystery — 12 Minute
**Fixture:** `tests/fixtures/inputs/vi_reddit_mystery_12min.json`  
**Scope:** Full 10-stage pipeline  
**Expected outcomes:**
- All output files in Vietnamese
- All diacritical marks intact in output files
- Subtitles encoded UTF-8
- SEO package includes English crossover tags

### RT-PIPELINE-005: Google Maps Mystery — English — 8 Minute
**Fixture:** `tests/fixtures/inputs/en_google_maps_mystery_8min.json`  
**Scope:** Full 10-stage pipeline  
**Expected outcomes:**
- Research includes coordinates in canonical format
- Story outline includes progressive reveal structure
- Storyboard includes map/satellite visual beat
- Image plan includes screen recording or map screenshot sourcing strategy

---

## RT-PROMPT: Prompt Regression Tests

Run when any file in `prompts/` is modified.

### RT-PROMPT-001: Output File Name Invariance
**Given:** Any prompt file is modified  
**When:** The stage is run with a standard fixture  
**Then:** The output file name is unchanged (canonical names are sacred)

### RT-PROMPT-002: Word Count Formula Unchanged
**Given:** `04_script_writer.md` modified  
**When:** Stage 04 runs with 10-minute fixture  
**Then:** Generated word count is within ±10% of 1,300 (10 × 130)

### RT-PROMPT-003: Hook Constraint Preserved
**Given:** `04_script_writer.md` modified  
**When:** Stage 04 runs with any fixture  
**Then:** Hook section is always ≤65 words

### RT-PROMPT-004: Pacing Markers Still Present
**Given:** `09_voice_director.md` modified  
**When:** Stage 09 runs with any fixture  
**Then:** `voice_script.txt` still contains `[PAUSE:2s]` and exactly one `[PAUSE:3s]`

### RT-PROMPT-005: No Fabrication Rule Enforced
**Given:** Any prompt file is modified  
**When:** The stage is run and produces research or script content  
**Then:** QA Layer 2 "Facts traceable to research" check still passes

---

## RT-CONFIG: Configuration Regression Tests

### RT-CONFIG-001: QA Threshold Changes Propagate
**Given:** `qa.word_count_tolerance` changed in `configs/configuration_system.md`  
**When:** QA Engine validates a script at the edge of the new tolerance  
**Then:** The new threshold is correctly applied (not the old one)

### RT-CONFIG-002: Model Override Applied
**Given:** `model.overrides.stage_05` changed to a different model  
**When:** Stage 05 executes  
**Then:** The run log shows the new model was used for stage 05

### RT-CONFIG-003: Language Profile Pacing Applied
**Given:** `ja` language profile `words_per_minute_equivalent` changed  
**When:** Script word count target is calculated for Japanese  
**Then:** Target word count reflects the updated profile value

### RT-CONFIG-004: New Config Key Available
**Given:** A new config key is added to `configuration_system.md`  
**When:** The relevant engine reads config  
**Then:** The engine reads the new key without error; falls back to default if not set

---

## RT-TEMPLATE: Template Regression Tests

### RT-TEMPLATE-001: Template Addendum Injected
**Given:** A template file is modified  
**When:** The affected stage runs with a matching niche  
**Then:** The template addendum content appears in the AI context (verifiable in run log)

### RT-TEMPLATE-002: Override Values Applied
**Given:** A template has a `Parameter Overrides` section  
**When:** A stage runs using that template  
**Then:** The override value is used instead of the base prompt default

### RT-TEMPLATE-003: Non-Matching Niche Uses Default Template
**Given:** An `input.json` with a niche that has no matching template  
**When:** Routing Engine resolves template  
**Then:** `mystery_template.md` is used as the fallback and a routing warning is logged

### RT-TEMPLATE-004: Template Version Mismatch Warning
**Given:** A template declares compatibility with `04_script_writer v1.x` but v2 is installed  
**When:** Routing Engine loads the template  
**Then:** A compatibility warning is logged (pipeline does NOT halt for warnings)

---

## RT-ENGINE: Engine Behavior Regression Tests

### RT-ENGINE-001: Director Sequences Stages in Order
**Given:** A new project with valid `input.json`  
**When:** Director Engine runs  
**Then:** Stages execute in order stage_01 → stage_10, with no stage starting before its dependencies are `validated`

### RT-ENGINE-002: QA Failure Triggers Retry
**Given:** Stage output that fails QA for a mechanical reason (word count off by 8%)  
**When:** QA Engine returns `fail`  
**Then:** Director Engine retries the stage automatically (not halts)

### RT-ENGINE-003: Hard Halt on FAIL Source
**Given:** Stage 02 returns overall status = `FAIL`  
**When:** Director Engine reads the verdict  
**Then:** Pipeline halts and `export_manifest.json` shows `status: needs_human_review`

### RT-ENGINE-004: Memory Engine Writes After Completion
**Given:** A project reaches `ready_for_production`  
**When:** Memory Engine is triggered  
**Then:** A new entry appears in `knowledge/memory_database.md` with the correct project_id

### RT-ENGINE-005: Export Bundle Structure Correct
**Given:** A project at `ready_for_production`  
**When:** Export Engine runs  
**Then:** `export_bundle/` contains the expected three subfolder structure and `editor_handoff.md`

---

## RT-REGRESSION: Change Detection Tests

These tests detect unintended side effects when one component is changed.

### RT-REGRESSION-001: Prompt Change Does Not Affect Config
**Given:** A prompt file is modified  
**When:** Config files are read  
**Then:** No config value has changed (config files are untouched)

### RT-REGRESSION-002: Config Change Does Not Affect Prompt Text
**Given:** A config file is modified  
**When:** Prompt files are read  
**Then:** No prompt file content has changed

### RT-REGRESSION-003: Template Change Does Not Break Other Niches
**Given:** `japan_template.md` is modified  
**When:** Pipeline runs with `mystery_template.md` (different niche)  
**Then:** Mystery niche pipeline produces the same results as before the Japan template change

---

## Regression Baseline

The regression baseline is established by running the full test suite after each major version release and recording the expected outcomes. The baseline is stored in `tests/fixtures/expected/`.

When a regression test produces output that differs from the baseline:
1. Determine if the difference is **intentional** (a prompt improvement) or **accidental** (a bug)
2. If intentional: update the baseline after human review
3. If accidental: revert the change and investigate

A regression baseline update requires explicit human approval — it cannot happen automatically.
