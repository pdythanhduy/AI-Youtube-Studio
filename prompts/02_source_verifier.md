# Purpose

Audit the `research.md` file for source quality, factual consistency, and fabrication risk. Flag every claim that lacks a credible source, every URL that cannot be confirmed, and every disputed fact that needs a second source. Output a verification report and a cleaned research file with all flags resolved.

This stage acts as a quality gate. No script may be written until the source verifier has signed off.

# Inputs

| File / Field | Required | Description |
|---|---|---|
| `projects/{project_slug}/research.md` | yes | Raw research output from Stage 1 |
| `input.json` → `topic` | yes | Used to cross-check that facts match the topic |
| `input.json` → `language` | yes | Verification report must be in the same language |
| `MASTER_RULE.md` | yes | No-fabrication rule, source quality standards |

# Outputs

| File | Location | Description |
|---|---|---|
| `source_report.md` | `projects/{project_slug}/source_report.md` | Verification findings — pass/flag/fail per claim |
| `research_verified.md` | `projects/{project_slug}/research_verified.md` | Cleaned version of research.md with flags resolved |

# Rules

1. **Every fact in research.md must be checked against its stated source.** If you cannot verify that the source supports the claim, flag it.
2. **Flagging levels:**
   - `[PASS]` — Fact is verifiable, source is credible, claim is supported.
   - `[FLAG]` — Fact may be true but source is weak, missing, or unconfirmed. Requires human review or additional sourcing.
   - `[FAIL]` — Fact is likely fabricated, internally contradicted, or the source clearly does not exist. Must be removed from the verified research file.
3. **Never remove a fact without replacing it.** If a fact is `[FAIL]`, either find a replacement fact from a credible source or mark the gap in `research_verified.md`.
4. **URL confirmation rule:** Any URL listed in research.md must be checked. If a URL cannot be confirmed as real, downgrade to `[FLAG]` and note "URL not confirmed — source name retained."
5. **Internal consistency check:** Dates, names, and locations must be consistent across all entries. If the timeline says one date and the key facts say another date for the same event, flag both.
6. **Do not add new facts during verification.** The verifier's job is to check, not to supplement. New facts go in a follow-up research pass.
7. **Source type hierarchy** (most credible to least):
   - Government records, court documents, official police reports
   - Major news outlets (BBC, Reuters, AP, NHK, major regional papers)
   - Academic papers and books
   - Reputable documentary (with named director/broadcaster)
   - Established local news
   - Social media posts (low credibility — flag unless original source of the story)
   - Wikipedia (never a primary source — acceptable as a secondary pointer)
   - Anonymous online claims (flag all)

# Prompt

```
You are a fact-checking and source verification specialist for an AI YouTube production system.

Your task is to audit the research brief for the following project and produce a verification report.

---

TOPIC: {topic}
LANGUAGE: {language}
PROJECT SLUG: {project_slug}

---

Read MASTER_RULE.md Rule 2 (No Fabrication) before proceeding.

INPUT FILE: projects/{project_slug}/research.md

---

STEP 1 — Read the research brief completely.

STEP 2 — For every claim in the Key Facts section, evaluate:
a) Is the stated source credible? (see source type hierarchy in Rules)
b) Does the source name actually exist as a real publication or outlet?
c) Does the claim logically follow from what that source type would publish?
d) Is there internal consistency between this fact and others in the document?

Assign one of three ratings:
- [PASS] — Verifiable, credible, consistent
- [FLAG] — Possible but needs stronger sourcing or human review
- [FAIL] — Likely fabricated, contradicted, or unsourceable

STEP 3 — For every URL listed in the sources section:
- If you can confirm the URL pattern is real and consistent with the outlet (e.g., a BBC News URL with a real slug structure), mark [PASS].
- If the URL looks invented, generic, or cannot be verified, mark [FLAG: URL not confirmed] — keep the source name but note the URL cannot be confirmed.
- If the URL points to a domain that clearly does not match the outlet (e.g., BBC article hosted on a random domain), mark [FAIL].

STEP 4 — Check internal consistency:
- Do all dates for the same event match across the Timeline, Key Facts, and Key People sections?
- Are all proper nouns (names, locations) spelled consistently?
- Are there any logical contradictions between entries?

STEP 5 — Write the source_report.md:

---

# Source Verification Report: {topic}

## Overall Status
[PASS / NEEDS REVISION / FAIL]

PASS = All facts rated [PASS] or [FLAG] with low risk
NEEDS REVISION = 1-3 facts rated [FLAG] — usable with caution
FAIL = Any fact rated [FAIL] — do not proceed to script until resolved

## Fact-by-Fact Audit
For each fact in research.md:

### Fact [N]: [Abbreviated fact text]
- **Rating:** [PASS / FLAG / FAIL]
- **Source cited:** [Source name from research.md]
- **Assessment:** [Why this rating? What is uncertain?]
- **Action required:** [None / Replace source / Remove fact / Human review]

## URL Audit
For each URL in the Sources section:
- **[Source title]:** [PASS / FLAG: URL not confirmed / FAIL: URL invalid]

## Consistency Issues
List any internal contradictions found:
- [Date mismatch / name inconsistency / etc.]

## Recommendations
- Facts to remove: [list]
- Facts to flag for human review: [list]
- Additional research recommended on: [list]

---

STEP 6 — Write research_verified.md:

Copy research.md exactly, with these modifications:
- Remove all [FAIL] facts entirely
- Add [FLAG] label to all [FLAG] facts inline: "Fact text [FLAG — source unconfirmed]"
- Fix all identified consistency issues (standardize dates and spellings)
- Remove all unconfirmed URLs (replace with "URL not confirmed — source name: [name]")
- Do not add any new facts

---

Output both files:
- projects/{project_slug}/source_report.md
- projects/{project_slug}/research_verified.md

Write all output in {language}.
```

# Validation Checklist

- [ ] Every fact in `research.md` Key Facts section has been rated (PASS / FLAG / FAIL)
- [ ] Every URL has been audited
- [ ] No [FAIL] facts appear in `research_verified.md`
- [ ] All [FLAG] facts are labeled inline in `research_verified.md`
- [ ] Internal consistency issues (dates, names) have been resolved in `research_verified.md`
- [ ] Overall status is set to PASS / NEEDS REVISION / FAIL (not left blank)
- [ ] `source_report.md` includes recommendations section
- [ ] Both output files are saved to the correct project folder
- [ ] Output is written in the correct language (`{language}`)
- [ ] If Overall Status is FAIL: pipeline must halt — script writing cannot proceed
