# Purpose

Generate a complete YouTube SEO package for the video. This includes: video title options, full description with chapters, tags, hashtags, thumbnail text overlay, and a pinned comment idea. Every element is optimized for the mystery niche and the target language. The goal is maximum discoverability, high click-through rate, and strong retention signals.

# Inputs

| File / Field | Required | Description |
|---|---|---|
| `projects/{project_slug}/script.md` | yes | Full script — for chapters and keyword extraction |
| `projects/{project_slug}/research_verified.md` | yes | Verified facts — for accurate keyword usage |
| `projects/{project_slug}/story_bible.md` | yes | Canonical names and terminology |
| `projects/{project_slug}/story_outline.md` | yes | Scene structure — for chapter timestamps |
| `input.json` → `topic` | yes | Primary subject |
| `input.json` → `language` | yes | Output language |
| `input.json` → `niche` | yes | Affects keyword strategy |
| `input.json` → `channel_name` | no | Used in description footer |
| `input.json` → `video_length_minutes` | yes | Used to generate accurate chapter timestamps |
| `STYLE_GUIDE.md` | yes | Thumbnail style rules |
| `MASTER_RULE.md` | yes | Rule 8 (SEO Compliance), Rule 9 (Subtitle Standards) |

# Outputs

| File | Location |
|---|---|
| `seo.md` | `projects/{project_slug}/seo.md` |

# Rules

1. **Title max 70 characters.** Count every character including spaces. Titles over 70 characters are truncated in YouTube search results.
2. **Description first 150 characters must be a hook.** YouTube shows only the first 150 characters in search results and the "Show more" truncation on mobile. No channel introductions, no "Hi everyone," no topic summaries — open with the most compelling fact or question.
3. **Minimum 15 tags, maximum 30 tags.** Include: specific tags (person name, location), niche tags (true crime, mystery, unsolved), format tags (documentary, narration, storytime), language-specific tags when not English.
4. **At least one tag must be a long-tail search phrase** of 5+ words (e.g., "why did elisa lam go missing").
5. **Chapters (timestamps) must match the scene structure from `story_outline.md`** and be formatted exactly as YouTube requires: `0:00 Title`.
6. **Do not fabricate viewer count claims, view milestones, or engagement statistics** in the description.
7. **Thumbnail text is maximum 4 words.** Short, shocking, or curious. Must work at thumbnail size (small text is unreadable).
8. **Pinned comment must add value**, not repeat the title. Options: a compelling follow-up question, a key fact not in the title, a "what do YOU think?" prompt, or a link to a related video placeholder.
9. **For non-English content (Japanese, Vietnamese):** Write the full SEO package in the target language. Include an additional set of English tags for cross-language discoverability only if the niche has significant English-language search overlap.
10. **Titles must not be clickbait that the video cannot deliver.** If the video does not reveal the answer to a mystery, the title cannot say "The Truth Finally Revealed." Accuracy in the title is required.

# Prompt

```
You are a YouTube SEO specialist for a mystery content channel.

Your task is to write a complete YouTube SEO package for the following video.

---

TOPIC: {topic}
LANGUAGE: {language}
NICHE: {niche}
VIDEO LENGTH: {video_length_minutes} minutes
CHANNEL NAME: {channel_name}
PROJECT SLUG: {project_slug}

---

Read before proceeding:
- MASTER_RULE.md Rule 8 (SEO Compliance) — title length, description hook, tag count
- projects/{project_slug}/story_bible.md — use canonical names in all SEO copy
- projects/{project_slug}/story_outline.md — use scene names and structure for chapters

INPUT FILES:
- projects/{project_slug}/script.md
- projects/{project_slug}/research_verified.md

---

STEP 1 — Keyword Research

From the script and research, identify:
- Primary keyword: the main thing people search for related to this topic
- Secondary keywords (3-5): related searches, alternate phrasings
- Long-tail keywords (2-3): full questions people type into search (5+ words each)
- Niche keywords: mystery / unsolved / true crime / paranormal / etc.
- Name keywords: every named person and location from story_bible.md
- Format keywords: documentary / narration / dark mystery / reddit story / etc.

STEP 2 — Write the full SEO package:

---

# SEO Package: {topic}

## Keyword Map

### Primary Keyword
[The single most searched term for this topic]

### Secondary Keywords
1. [keyword]
2. [keyword]
3. [keyword]

### Long-Tail Keywords
1. [5+ word search phrase]
2. [5+ word search phrase]

### Niche Keywords
[mystery, unsolved, unexplained, true crime, paranormal, etc.]

---

## Title Options

Provide exactly 3 title options. For each:
- Stay under 70 characters (count including spaces)
- Include the primary keyword naturally
- Create curiosity, dread, or urgency — but only promise what the video delivers
- State the character count in brackets after each title

### Option 1 (Primary — best for search)
[Title] [XX characters]

### Option 2 (Emotional — best for CTR)
[Title] [XX characters]

### Option 3 (Question format — best for long-tail)
[Title] [XX characters]

**Recommended:** Option [N] — [one-sentence reason]

---

## Thumbnail Text Overlay

### Primary text (main headline — max 4 words)
[TEXT IN CAPS OR TITLE CASE]

### Sub-text (optional — max 5 words)
[Smaller text below or beside main text, if needed]

### Design note
[One sentence on color, contrast, or placement — reference STYLE_GUIDE.md thumbnail rules]

---

## Description

Write a full YouTube description. Requirements:
- First 150 characters: hook sentence only — most compelling fact or question
- Main body: 200-400 words covering the story summary (no spoilers of the resolution)
- Chapters section: formatted as YouTube timestamp list
- Tags section: #hashtags at the bottom
- Footer: channel name and subscribe line (if channel_name provided)

---

[FIRST 150 CHARS — HOOK]
[Most shocking or mysterious fact or question from the video — one sentence or two very short ones]

[BLANK LINE]

[MAIN BODY — 200-400 words]
[Story summary — what the viewer will learn, without spoiling the ending]
[Include primary keyword naturally in the first paragraph]
[Include 2-3 secondary keywords naturally in the body]

[BLANK LINE]

━━━━━━━━━━━━━━━━━━━━
CHAPTERS
━━━━━━━━━━━━━━━━━━━━
0:00 [Chapter name — from story_outline.md]
[X:XX] [Chapter name]
[X:XX] [Chapter name]
[Continue for all scenes — match story_outline.md structure exactly]

[BLANK LINE]

━━━━━━━━━━━━━━━━━━━━
TAGS
━━━━━━━━━━━━━━━━━━━━
#[Topic] #[Niche] #[Format] [3-5 relevant hashtags only — the rest go in the tags field below]

[BLANK LINE]

[If channel_name is set:]
🔔 Subscribe to {channel_name} for new mysteries every week.

---

## Tags Field (YouTube tag input box)

Provide 15-30 tags, comma-separated, no # symbol:

[tag 1], [tag 2], [tag 3], ... [tag 15-30]

Include in this order:
1. Topic-specific tags (names, locations, events)
2. Long-tail phrase tags (5+ words — at least 2)
3. Niche category tags (mystery, unsolved, true crime, etc.)
4. Format tags (documentary, narration, youtube mystery, etc.)
5. Language-specific tags (if non-English: include 3-5 English crossover tags)

---

## Pinned Comment

Write 2 options for the pinned comment. The pinned comment appears immediately below the video and is the first comment viewers see.

### Option A — Compelling follow-up question
[A question that makes viewers think and encourages replies]

### Option B — Key fact + engagement prompt
[One striking fact from the video that wasn't in the title] + [What do you think?]

**Recommended:** Option [N] — [one-sentence reason]

---

## SEO Notes
- Primary keyword density target: 2-4 mentions naturally in description
- Recommended upload time for mystery niche: [Thursday-Friday, 6-9pm target timezone]
- End screen recommendation: Add at [video_length - 0:20] → link to most related video
- Cards recommendation: Add at [30% of video length] → link to related video or playlist

---

Write all copy in {language}.
For non-English: also include a separate "English Tags Addendum" section with 5-8 English search tags if the niche has English-language audience overlap.
Use canonical names from story_bible.md throughout — no spelling variations.

Save to: projects/{project_slug}/seo.md
```

# Validation Checklist

- [ ] All 3 title options are ≤70 characters (character count stated after each)
- [ ] Description first 150 characters is a hook — no channel greeting, no "Hi everyone"
- [ ] Primary keyword appears naturally in the description's first paragraph
- [ ] Description main body is 200-400 words
- [ ] Chapters section matches scene structure from `story_outline.md`
- [ ] Chapter timestamps are in correct YouTube format: `0:00 Title`
- [ ] Tags field contains 15-30 tags (count them)
- [ ] At least 2 long-tail tags (5+ words each) are present in the tags field
- [ ] Hashtags in the description body are ≤5 (YouTube recommendation)
- [ ] Thumbnail text is ≤4 words for primary text
- [ ] Pinned comment options are present (2 options with recommendation)
- [ ] All names and locations match canonical forms from `story_bible.md`
- [ ] No fabricated statistics or viewer count claims appear
- [ ] Title options do not promise a resolution if the video does not provide one
- [ ] For non-English: English Tags Addendum is present if niche has English audience overlap
- [ ] File saved to `projects/{project_slug}/seo.md`
