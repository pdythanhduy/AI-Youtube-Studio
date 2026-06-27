# QA Engine — AI YouTube Studio OS

The QA Engine validates every stage output before the Director Engine advances the pipeline. It runs the validation checklist defined in each prompt file, plus system-level consistency checks. It cannot generate or modify content — it only reads, evaluates, and reports. Its verdict is final: PASS or FAIL (with specific reasons).

---

## Responsibility

The QA Engine is responsible for **confirming that every output file meets its defined quality standard** before the next stage can begin. It catches fabrication, format errors, word count violations, consistency failures, and policy violations.

**Single sentence:** The QA Engine is the gatekeeper — nothing moves forward until it signs off.

---

## Inputs

| Input | Source | Description |
|---|---|---|
| Stage output file | `projects/{slug}/` | The file to validate |
| Prompt file | `prompts/NN_[stage].md` | Contains the Validation Checklist for this stage |
| `MASTER_RULE.md` | System | Global quality rules |
| `story_bible.md` | `projects/{slug}/` | Canonical names for consistency checks |
| `export_manifest.json` | `projects/{slug}/` | Current state, retry count |
| Previous stage files | `projects/{slug}/` | For cross-file consistency checks |

---

## Outputs

| Output | Destination | Description |
|---|---|---|
| Validation signal | Director Engine | PASS or FAIL + summary |
| QA report file | `projects/{slug}/[stage]_qa.md` | Detailed checklist results |
| Updated manifest | `projects/{slug}/export_manifest.json` | Asset status updated |

---

## Dependencies

| Dependency | Type | Purpose |
|---|---|---|
| Director Engine | upstream | Triggers validation; receives result |
| Decision Engine | downstream | Consults for ambiguous failures |
| Memory Engine | downstream | Reports failure patterns |
| `MASTER_RULE.md` | reference | All rule definitions |

---

## Validation Process

For every stage output, the QA Engine runs three layers of checks:

### Layer 1: Format Checks (Mechanical)

These checks are deterministic — pass or fail with no ambiguity.

| Check | Applies To | Failure Condition |
|---|---|---|
| File exists | All | File not found at expected path |
| File is non-empty | All | File size = 0 |
| Word count in range | `script.md`, `voice_script.txt` | Outside ±10% of target |
| No markdown in plain text | `voice_script.txt` | Markdown characters detected |
| Valid SRT format | `subtitles.srt` | Invalid timecode format |
| Timecodes sequential | `subtitles.srt` | Any timecode ≤ previous |
| No timecode overlap | `subtitles.srt` | Any timecode start < previous end |
| Line length ≤42 chars | `subtitles.srt` | Any line exceeds 42 characters |
| Title ≤70 chars | `seo.md` | Any title option exceeds 70 chars |
| Tag count 15-30 | `seo.md` | Count outside range |
| JSON valid | `export_manifest.json`, `input.json` | Invalid JSON syntax |
| Required JSON keys present | `input.json` | Missing `topic`, `language`, `video_length_minutes`, `style` |

### Layer 2: Content Checks (Semantic)

These checks require reading and interpreting content. Some may involve a secondary AI call for evaluation.

| Check | Applies To | Failure Condition |
|---|---|---|
| No fabricated URLs | `research.md`, `research_verified.md` | URL present that cannot be confirmed |
| Facts traceable to research | `script.md` | Fact present not found in `research_verified.md` |
| Speculation properly labeled | `script.md` | Unhedged claim that is not in research |
| Hook ≤65 words | `script.md` | Hook section exceeds 65 words |
| Hook not a channel greeting | `script.md` | Hook begins with "Hi" or "Welcome back" |
| All beats have visuals | `storyboard.md` | Any narration beat without a visual |
| Image type assigned | `storyboard.md` | Any beat with missing image type |
| No TBD entries | `image_plan.md` | Any row with "TBD" in source field |
| All escalated beats have AI prompts | `ai_image_prompts.md` | Any escalated beat from image_plan.md missing a prompt |
| Pacing markers present | `voice_script.txt` | No `[PAUSE:2s]` or `[PAUSE:3s]` in file |
| Description hook ≤150 chars | `seo.md` | First 150 chars of description is not a hook |

### Layer 3: Consistency Checks (Cross-File)

These checks require reading multiple files and comparing them.

| Check | Applies To | Failure Condition |
|---|---|---|
| Names match story_bible | All files | Name in file differs from canonical form |
| Dates match story_bible | All files | Date for same event differs between files |
| Scene count matches | `storyboard.md` vs `script.md` | Different number of scenes |
| Image count matches | `image_plan.md` vs `storyboard.md` | Different number of visual entries |
| Word count matches | `voice_script.txt` vs `script.md` | Difference >5% |
| Chapter timestamps match | `seo.md` vs `story_outline.md` | Different scene names or order |

---

## QA Report Format

A QA report is written for every validation run:

```markdown
# QA Report: stage_04 — script.md
**Project:** 20260627_disappearance-of-elisa-lam
**Validation time:** 2026-06-27T10:50:00Z
**Result:** PASS

## Layer 1: Format Checks
- [PASS] File exists
- [PASS] File non-empty
- [PASS] Word count: 1,547 (target 1,560 ±156) ✓
- [N/A] Markdown in plain text — not applicable to .md file

## Layer 2: Content Checks
- [PASS] Hook word count: 58 words (≤65 ✓)
- [PASS] Hook opening: "In January 2013..." — no greeting ✓
- [PASS] All facts traceable to research_verified.md (14 facts checked)
- [PASS] Speculation labeled — 2 instances found, both correctly hedged
- [PASS] No fabricated URLs in script

## Layer 3: Consistency Checks
- [PASS] All names match story_bible.md
- [PASS] All dates match story_bible.md
- [PASS] Scene count matches story_outline.md (5 scenes)

## Summary
Checklist items: 14
Passed: 14
Flagged: 0
Failed: 0

**Verdict: PASS**
Next stage may proceed.
```

---

## Failure Reporting

When a check fails, the QA report includes:

```markdown
## Failed Check: Facts traceable to research
- **Severity:** HIGH
- **Location:** Scene 3, paragraph 2
- **Issue:** "The hotel had a documented history of 16 suicides" — this claim does not appear in research_verified.md.
- **Action required:** Remove or verify this claim before proceeding.
- **Auto-recoverable:** No — requires human review.
```

---

## Severity Levels

| Severity | Description | Director Action |
|---|---|---|
| `LOW` | Minor formatting issue — does not affect content quality | Auto-fix and revalidate |
| `MEDIUM` | Quality issue — affects output professionalism | Auto-retry (up to 2x) |
| `HIGH` | Policy violation — affects factual accuracy or legal compliance | Human review required |
| `CRITICAL` | Fabrication or source failure | Pipeline halt, human must resolve |

---

## QA Configuration

Thresholds configurable in `configs/configuration_system.md`:

| Config Key | Default | Description |
|---|---|---|
| `qa.word_count_tolerance` | 0.10 | ±10% word count tolerance |
| `qa.voice_script_word_count_tolerance` | 0.05 | ±5% for voice script |
| `qa.max_subtitle_line_chars` | 42 | Maximum characters per subtitle line |
| `qa.max_subtitle_duration_seconds` | 7 | Maximum subtitle segment duration |
| `qa.min_tags` | 15 | Minimum YouTube tags |
| `qa.max_tags` | 30 | Maximum YouTube tags |
| `qa.title_max_chars` | 70 | Maximum title character count |
| `qa.description_hook_chars` | 150 | Characters that must be a hook |

---

## Future Automation Points

| Point | Description |
|---|---|
| AI-assisted content QA | Use a secondary Claude call to evaluate semantic quality (not just format) |
| Automated fact tracing | NLP matching to verify script facts against research — not just string search |
| Real-time QA | Stream output from Workflow Engine and flag issues as they appear |
| QA dashboard | Web interface showing pass/fail history across all projects |
| Regression detection | Alert when QA pass rate for a stage drops below historical average |
