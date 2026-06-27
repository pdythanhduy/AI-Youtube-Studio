# research/ — Research and Source Verification

This folder contains all research outputs. It is written by Stages 1 and 2.

---

## Files

### `research.md` — Raw research brief (Stage 1)

**Written by:** Director AI running `prompts/01_research.md`

Contains:
- **Summary** — 2-3 sentence overview of the topic
- **Key Facts** — minimum 5 verified facts about the topic
- **Timeline** — chronological events (if applicable)
- **Key People** — people relevant to the story
- **Key Locations** — locations and their significance
- **Sources** — minimum 3 named sources with outlet and year
- **Niche-Specific Research** — additional research per niche (e.g., Reddit post metadata, GPS coordinates)
- **Unresolved Questions** — gaps that could not be confirmed

**Status after stage:** `research.status = complete` in manifest

---

### `source_report.md` — Source audit (Stage 2)

**Written by:** Director AI running `prompts/02_source_verifier.md`

Contains:
- Source quality ratings (PASS / FLAG / FAIL) per claim
- Source type hierarchy assessment
- Overall Status: `PASS` / `NEEDS_REVISION` / `FAIL`
- Reasoning for each rating

**Critical:** If Overall Status = `FAIL`, the pipeline halts here. A human must resolve source failures before resuming.

**Status after stage:** `source_report.status = complete` in manifest

---

### `research_verified.md` — Clean verified research (Stage 2)

**Written by:** Director AI running `prompts/02_source_verifier.md`

This is `research.md` with all `FAIL` claims removed and all `FLAG` claims labeled. This is the authoritative fact source for all subsequent stages. The script writer uses ONLY this file for facts.

**Status after stage:** `research_verified.status = complete` in manifest

---

## Human Review Points

After Stage 1: You may add missing context to `research.md` before Stage 2 runs. If you do, re-run Stage 2.

After Stage 2: If Overall Status = `NEEDS_REVISION`, review the flagged claims in `source_report.md`. You may:
- Accept the flagged claims with a label (continue pipeline)
- Remove flagged claims from `research_verified.md` (continue pipeline)
- Find better sources and update `research.md`, then re-run Stage 2

---

## What Does NOT Belong Here

- Story outlines or scripts (go in `script/`)
- Visual planning (go in `visuals/`)
- SEO content (go in `seo/`)
