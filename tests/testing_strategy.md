# Testing Strategy — AI YouTube Studio OS

Testing philosophy, test types, coverage expectations, and the overall approach to quality assurance across the system. This document defines how the system is validated — not what specific tests exist (see `acceptance_tests.md` and `regression_tests.md` for that).

---

## Testing Philosophy

### The System Has Two Failure Modes

**Mode 1: Mechanical failure** — a file is malformatted, a word count is wrong, a JSON key is missing. These are deterministic and fully testable.

**Mode 2: Quality failure** — a script is factually accurate but narratively weak, a thumbnail prompt is technically valid but visually unappealing, a voice script has correct pacing markers but the emotional flow is wrong. These are non-deterministic and require human judgment.

The testing system is designed to catch all mechanical failures automatically. Quality failures are flagged for human review — they cannot be fully automated.

### Test Pyramid

```
                    ┌──────────────┐
                    │   Human QA   │  ← Narrative quality, cultural accuracy
                    │  (manual)    │
                ┌───┴──────────────┴───┐
                │  Acceptance Tests    │  ← End-to-end pipeline validation
                │   (semi-automated)   │
            ┌───┴──────────────────────┴───┐
            │     Regression Tests          │  ← Detect changes that break existing behavior
            │     (automated)               │
        ┌───┴──────────────────────────────┴───┐
        │         Unit / Component Tests        │  ← Individual engine and config validation
        │         (automated)                   │
    ┌───┴──────────────────────────────────────┴───┐
    │              Schema Validation               │  ← File format, JSON, SRT, encoding
    │              (automated)                     │
    └──────────────────────────────────────────────┘
```

Most test coverage lives at the bottom (schema validation and regression tests). Human QA is expensive and reserved for final output review.

---

## Test Types

### 1. Schema Validation Tests

**What:** Validate that all files conform to their output profiles (`configs/output_profiles.md`).

**How:** Automated checks run on every output file after it is generated.

**Coverage:**
- Encoding (UTF-8, BOM presence/absence)
- File format (SRT timecodes, JSON syntax, Markdown structure)
- Required fields present (JSON manifests)
- Line length limits (SRT subtitles)
- Timecode sequencing (SRT subtitles)
- No forbidden characters (voice_script.txt)

**Pass/fail:** Binary. No schema errors = pass.

**Automated by:** QA Engine (Layer 1 checks).

---

### 2. Content Validation Tests

**What:** Validate that output content meets defined quality thresholds.

**How:** Automated checks run on content metrics and structure.

**Coverage:**
- Word count within target range
- Hook ≤65 words
- Minimum verified facts in research
- Minimum sources in research
- All scenes in storyboard have visual beats
- All AI escalated beats have corresponding prompts
- Tag counts in SEO package
- Title character counts

**Pass/fail:** Per-check. Failures generate QA reports with severity ratings.

**Automated by:** QA Engine (Layer 2 checks).

---

### 3. Consistency Tests

**What:** Validate cross-file consistency within a project.

**How:** Automated comparison of canonical names, dates, and counts across files.

**Coverage:**
- Names in script match story_bible canonical forms
- Dates in script match story_bible dates
- Scene count in storyboard matches story_outline
- Image count in image_plan matches storyboard
- Word count in voice_script matches script ±5%
- Chapter timestamps in SEO match story_outline scenes

**Pass/fail:** Per-check.

**Automated by:** QA Engine (Layer 3 checks).

---

### 4. Acceptance Tests

**What:** End-to-end validation that the full pipeline produces a complete, production-ready project for a given input.

**How:** A defined set of test inputs (`input.json` fixtures) are run through the pipeline. The output is validated against expected characteristics.

**Coverage:** See `acceptance_tests.md` for the full test suite.

**Pass/fail:** Per test case. A project is "accepted" if it passes all schema, content, and consistency checks AND a human reviewer confirms narrative quality.

**Automated by:** Partially automated — mechanical checks are automated, human quality review is manual.

---

### 5. Regression Tests

**What:** Detect when a change to prompts, templates, or configs causes previously-passing tests to fail.

**How:** A fixed set of test inputs and expected outputs. After any system change, run regressions to confirm nothing broke.

**Coverage:** See `regression_tests.md` for the regression suite.

**Pass/fail:** Binary per test case. Any regression failure blocks the change from merging.

**Automated by:** Fully automated for mechanical checks; manually reviewed for quality metrics.

---

### 6. Human QA Review

**What:** A trained human reviews a sample of completed projects for overall narrative quality, cultural accuracy, and audience fit.

**How:** After every 5 completed projects, a random project is selected for human QA review using the Human QA Rubric (below).

**Not automated.** Results are recorded in `memory_database.md`.

---

## Human QA Rubric

| Dimension | Score 1 (Fail) | Score 3 (Pass) | Score 5 (Excellent) |
|---|---|---|---|
| Narrative arc | No clear structure | Three acts present, functional | Emotionally compelling from hook to close |
| Factual accuracy | Errors or fabrication found | All facts verified | Facts well-sourced and well-contextualized |
| Style consistency | Tone breaks throughout | Generally consistent | Perfectly consistent with style guide |
| Hook quality | Generic, weak, or greeting | Attention-grabbing | Immediately compelling, memorable |
| Cultural accuracy | Errors or stereotypes | Accurate | Nuanced and respectful |
| Voice suitability | Robotic, or wrong register | Natural enough | Sounds like a real narrator |
| Image plan quality | Vague or many TBDs | All slots filled | Strategic and visually compelling choices |
| SEO quality | Generic or inaccurate | Functional | Optimized and distinctive |

**Minimum score to pass human QA:** Average of 3.0 across all dimensions, with no dimension below 2.

---

## Test Coverage Targets

| Test Type | Target Coverage | Current Coverage |
|---|---|---|
| Schema validation | 100% of all output file types | Defined in acceptance_tests.md |
| Content validation | 100% of QA checklist items | Defined in acceptance_tests.md |
| Consistency checks | 100% of cross-file relationships | Defined in acceptance_tests.md |
| Acceptance tests | 1 test per niche × language combination | 0 / 12 (see roadmap) |
| Regression tests | Core pipeline + all major config variations | Defined in regression_tests.md |
| Human QA | Every 5 completed projects (20% sample) | Manual |

---

## When Tests Run

| Event | Tests Triggered |
|---|---|
| After each pipeline stage | Schema + content validation for that stage's output |
| After final stage | Full consistency check across all files |
| Before export | Full export readiness checklist |
| After any prompt change | Full regression suite |
| After any config change | Affected component regression tests |
| After any template change | Template-specific acceptance test |
| Every 5 completed projects | Human QA review (manual) |
| On scheduled learning cycle | Learning Engine reads test outcomes for pattern analysis |

---

## Test Fixtures

Test fixtures live in `tests/fixtures/` (to be created when test automation is implemented):

```
tests/
├── fixtures/
│   ├── inputs/
│   │   ├── en_internet_mystery_12min.json
│   │   ├── ja_japanese_mystery_8min.json
│   │   ├── en_reddit_mystery_10min.json
│   │   ├── en_google_maps_mystery_8min.json
│   │   └── vi_reddit_mystery_12min.json
│   └── expected/
│       ├── en_internet_mystery_12min/
│       │   ├── expected_word_count_range.json
│       │   ├── expected_qa_pass.json
│       │   └── expected_structure.json
│       └── ...
├── testing_strategy.md
├── acceptance_tests.md
└── regression_tests.md
```
