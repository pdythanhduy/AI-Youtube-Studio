# Purpose

Conduct deep, structured research on the video topic. Produce a factual brief covering all known information: timeline, key people, key locations, verified events, disputed claims, and open questions. This document feeds every downstream component — script, storyboard, SEO — so accuracy is critical.

# Inputs

| File / Field | Required | Description |
|---|---|---|
| `input.json` → `topic` | yes | The subject to research |
| `input.json` → `language` | yes | Output language (en / ja / vi) |
| `input.json` → `niche` | yes | Content category — shapes research angle |
| `input.json` → `notes` | no | Specific angles, sub-topics, or exclusions |
| `MASTER_RULE.md` | yes | No-fabrication rule, source requirements |
| `MASTER_PLAN.md` | yes | research.md output format specification |

# Outputs

| File | Location |
|---|---|
| `research.md` | `projects/{project_slug}/research.md` |

# Rules

1. **No fabrication.** Every fact must be verifiable. If you are not certain a fact is true, label it `[Unverified]`.
2. **No fake URLs.** If you cannot confirm a URL exists, write the source name and description only — never invent a link.
3. **Minimum 5 distinct verified facts.** Trivia does not count as a fact.
4. **Minimum 3 named sources.** Each source must include: title, outlet/platform, and year. URL is required if the source is online and you can confirm it exists.
5. **Disputed claims must be presented as disputed.** Write: "Some sources claim X, while others report Y."
6. **Unresolved questions must be documented.** If the mystery is genuinely unsolved, say so explicitly and list what is unknown.
7. **Research must match the niche angle.** For `reddit_mystery`: include original post metadata and community reaction. For `japanese_mystery`: include cultural context. For `google_maps_mystery`: include coordinates and satellite image details.
8. **Write in the language specified in `input.json`.** If language is `ja`, write the research brief in Japanese. If `vi`, write in Vietnamese.

# Prompt

```
You are a research specialist for an AI YouTube video production system focused on mystery content.

Your task is to research the following topic and produce a structured research brief.

---

TOPIC: {topic}
LANGUAGE: {language}
NICHE: {niche}
SPECIAL NOTES: {notes}

---

Read and follow MASTER_RULE.md before proceeding. Apply the no-fabrication rule strictly.

Produce a research brief in the following format, written in {language}:

---

# Research: {topic}

## Summary
[2-3 sentences. What happened? Why is it a mystery? What makes it compelling?]

## Key Facts
List at minimum 5 verified, distinct facts. Format each as:
- [Fact] — Source: [Source name, year]

Mark any unverified claim with [Unverified].

## Timeline
| Date | Event |
|---|---|
| [Date or approximate period] | [What happened] |

Include at least 3 timeline entries if the topic has a chronological narrative.
If dates are unknown, use approximate periods (e.g., "Early 2012", "Late 19th century").

## Key People
| Name | Role / Connection |
|---|---|
| [Full name] | [Their relationship to the topic] |

Include all named individuals who appear in verified accounts.

## Key Locations
For each significant location:
- **[Location name]** — [City, Country if known] — [Why it matters to the story]
- Include GPS coordinates or addresses if publicly available and relevant.

## Unresolved Questions
List every major question that remains unanswered. Be specific.
- What happened to [person/object]?
- Why did [event] occur?
- Who was responsible for [action]?

## Disputed Claims
List any claims where sources disagree. For each:
- **Claim:** [What is disputed]
- **Version A:** [Source name] says [X]
- **Version B:** [Source name] says [Y]

## Cultural / Platform Context (if applicable)
For niche = japanese_mystery: Explain any cultural practices, folklore, or social context a non-Japanese viewer would need to understand.
For niche = reddit_mystery: Note the subreddit, post date, username (if public), and whether OP ever responded or updated.
For niche = google_maps_mystery: Include the coordinates, what was found, and current satellite image status if known.

## Sources
List all sources used. For each source:
- **[Source title]** — [Outlet / Platform] — [Year]
  - URL: [Full URL if confirmed to exist, or "URL not confirmed — search recommended"]
  - Type: news / documentary / academic / reddit / social media / government record / wiki

---

STRICT RULES:
- Do not fabricate any fact, name, date, quote, or URL.
- If you are uncertain whether a URL exists, write "URL not confirmed" — never invent a link.
- If a fact is unverified, label it [Unverified].
- If a claim is disputed, present both sides.
- Write everything in {language}.
- Save the output to: projects/{project_slug}/research.md
```

# Validation Checklist

Before accepting this output as complete, verify:

- [ ] Summary is 2-3 sentences and accurately describes the topic
- [ ] At least 5 distinct verified facts are listed
- [ ] Every fact has a named source
- [ ] At least 3 sources are listed with title, outlet, and year
- [ ] No URLs appear that the AI cannot confirm exist (check for suspiciously specific or generic fake-looking URLs)
- [ ] Unverified claims are labeled `[Unverified]`
- [ ] Disputed claims list both versions with attributed sources
- [ ] Timeline has at least 3 entries (if topic is chronological)
- [ ] Unresolved Questions section is present and specific
- [ ] Output is written in the correct language (`{language}`)
- [ ] File saved to `projects/{project_slug}/research.md`
