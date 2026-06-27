# Purpose

Create a story bible — a compact reference document that locks in all character names, locations, dates, terminology, and key facts for this specific video. Every downstream component (storyboard, image plan, subtitles, SEO) must reference this file to stay consistent. The story bible is the single source of truth for how names, places, and events are written.

This prevents the most common consistency failure: a person's name spelled three different ways across five files.

# Inputs

| File / Field | Required | Description |
|---|---|---|
| `projects/{project_slug}/script.md` | yes | Finalized script — names/dates sourced from here |
| `projects/{project_slug}/research_verified.md` | yes | Cross-reference for correct spellings and dates |
| `input.json` → `topic` | yes | Video subject |
| `input.json` → `language` | yes | Output language |
| `input.json` → `style` | yes | Style context (affects terminology choices) |
| `MASTER_RULE.md` | yes | Rule 6 — Consistency Across Components |

# Outputs

| File | Location |
|---|---|
| `story_bible.md` | `projects/{project_slug}/story_bible.md` |

# Rules

1. **Extract, do not invent.** Every entry in the story bible must come directly from `script.md` or `research_verified.md`. Do not add new facts or names not present in those files.
2. **One canonical form per entity.** Choose the single correct spelling/format for every name, location, and date. Once locked in the bible, it cannot vary across files.
3. **Flag any inconsistency found between script.md and research_verified.md.** If the script calls a person "Elisa Lam" but the research file says "Eliza Lam," flag it and choose the correct form from the primary source.
4. **Dates must be in ISO format.** Use YYYY-MM-DD for specific dates, YYYY-MM for month-level, YYYY for year-level. Human-readable form is added alongside: `2013-01-26 (January 26, 2013)`.
5. **Include pronunciation guides for non-English names** in the language of the script. This feeds the voice director.
6. **The terminology section must define all niche-specific or culture-specific terms used in the script.** A non-specialist reader must be able to understand the script after reading the bible.
7. **This document is read-only once finalized.** Downstream agents reference it but do not modify it. If a correction is needed, it must be made in the script first, then the bible is regenerated.

# Prompt

```
You are a continuity editor for an AI YouTube video production system.

Your task is to create a story bible for the following project by extracting and canonicalizing all key entities from the script and verified research.

---

TOPIC: {topic}
LANGUAGE: {language}
STYLE: {style}
PROJECT SLUG: {project_slug}

---

Read before proceeding:
- MASTER_RULE.md Rule 6 (Consistency Across Components)

INPUT FILES:
- projects/{project_slug}/script.md
- projects/{project_slug}/research_verified.md

---

STEP 1 — Read script.md fully. Extract every:
- Person's name (full name as used in the script)
- Location name (city, building, address, region, country)
- Date or time reference
- Organization, agency, or institution name
- Document, object, or artifact with a proper name
- Technical term, cultural term, or niche-specific phrase

STEP 2 — Cross-reference against research_verified.md. If any name or date differs between the two files, flag it and choose the correct form (prefer the source with higher credibility — government records > news > Wikipedia).

STEP 3 — Write the story bible in this format:

---

# Story Bible: {topic}

## Project Reference
- **Topic:** {topic}
- **Style:** {style}
- **Language:** {language}
- **Project slug:** {project_slug}

## People
For each person mentioned in the script:

### [Full canonical name]
- **Role:** [Their role in the story]
- **First mentioned:** [Scene name where they appear]
- **Canonical spelling:** [Exactly as it must appear in all files]
- **Alternate spellings found (if any):** [List variants — all are now incorrect except the canonical form]
- **Pronunciation guide:** [For non-English names, phonetic guide in {language}]
- **Key fact:** [One sentence — who are they and why do they matter to this story]

## Locations
For each location mentioned in the script:

### [Full canonical location name]
- **Type:** [Building / City / Country / Coordinate / Website / etc.]
- **Canonical name:** [Exactly as it must appear in all files]
- **First mentioned:** [Scene name]
- **Address or coordinates:** [If publicly available and relevant]
- **Key fact:** [One sentence — why does this place matter?]

## Dates and Timeline
| Date (ISO) | Human-Readable | Event |
|---|---|---|
| YYYY-MM-DD | Month DD, YYYY | What happened |

List every date that appears in the script. If two files disagree on a date, flag it:
`[DATE CONFLICT: script says X, research says Y — research_verified.md used as authority]`

## Organizations and Institutions
| Canonical Name | Abbreviation (if used) | Role in Story |
|---|---|---|
| [Full name] | [e.g., LAPD] | [What they did] |

## Key Objects and Documents
| Canonical Name | Type | Significance |
|---|---|---|
| [Name] | [Document / Photo / Video / Object] | [Why it matters] |

## Terminology
For each technical, cultural, or niche-specific term used in the script:

### [Term]
- **Definition:** [Plain-language explanation]
- **Used in scene:** [Scene name]
- **Language note:** [If the term is from another language, include original and romanization]

## Consistency Flags
List every inconsistency found between script.md and research_verified.md:
- **Flag [N]:** [What was inconsistent] → **Resolved as:** [canonical form chosen]

## Canonical Name Index (Quick Reference)
A flat alphabetical list for fast lookup by downstream agents:

| Entity | Canonical Form | Type |
|---|---|---|
| [Elisa Lam] | Elisa Lam | Person |
| [Cecil Hotel] | Cecil Hotel, Los Angeles | Location |
| ... | ... | ... |

---

Write the story bible in {language}.
Save to: projects/{project_slug}/story_bible.md
```

# Validation Checklist

- [ ] Every person named in `script.md` has an entry in the People section
- [ ] Every location named in `script.md` has an entry in the Locations section
- [ ] Every date in `script.md` is listed in the timeline table in ISO format
- [ ] All canonical spellings are single, unambiguous, chosen forms
- [ ] All alternate/inconsistent spellings found are listed and marked as incorrect
- [ ] Pronunciation guide present for all non-English proper nouns
- [ ] Terminology section defines all niche-specific or culture-specific terms
- [ ] Consistency Flags section lists every conflict found, with resolution
- [ ] Canonical Name Index (quick reference) is present and complete
- [ ] No new facts, names, or events were added that are not in `script.md` or `research_verified.md`
- [ ] File saved to `projects/{project_slug}/story_bible.md`
- [ ] Written in the correct language (`{language}`)
