# Purpose

Write the full narration script for the video. The script is a complete, word-for-word narration ready to be handed to a voice actor or TTS system. It must match the story outline exactly, hit the target word count, follow the style guide, and contain zero fabricated facts.

This is the core creative output of the entire pipeline. Every downstream component — storyboard, voice script, subtitles — derives from this file.

# Inputs

| File / Field | Required | Description |
|---|---|---|
| `projects/{project_slug}/story_outline.md` | yes | Approved narrative blueprint |
| `projects/{project_slug}/research_verified.md` | yes | Verified facts — only source of truth for factual claims |
| `input.json` → `topic` | yes | Video subject |
| `input.json` → `language` | yes | Script language |
| `input.json` → `video_length_minutes` | yes | Target duration |
| `input.json` → `style` | yes | Narrative style |
| `input.json` → `niche` | yes | Content category |
| `STYLE_GUIDE.md` | yes | Tone, sentence rhythm, language rules per style |
| `MASTER_RULE.md` | yes | Word count targets, hook standard, no fabrication |

# Outputs

| File | Location |
|---|---|
| `script.md` | `projects/{project_slug}/script.md` |

# Rules

1. **Facts only from `research_verified.md`.** Do not introduce any fact, name, date, or claim not present in the verified research. If the outline calls for a scene that has insufficient research, flag it in the script with `[RESEARCH GAP — verify before production]`.
2. **Speculation must be labeled.** Any statement that is not a verified fact must use hedged language: "Some believe...", "According to witnesses...", "One theory suggests...", "It has never been confirmed, but..."
3. **Word count within ±10% of target.** Target = `video_length_minutes × 130`. See MASTER_RULE.md Rule 3.
4. **Hook is ≤65 words.** It must not open with a channel greeting, a cliché question, or presenter introduction. See MASTER_RULE.md Rule 4.
5. **Follow the tone and sentence rhythm rules for `{style}` exactly.** See STYLE_GUIDE.md.
   - `dark_documentary`: measured, authoritative, no humor, short punchy statements at climax
   - `reddit_narration`: first-person for the post, third-person for context, conversational
   - `mystery_investigation`: curious, analytical, progressive reveal, second person acceptable
   - `japanese_mystery`: formal register, respectful tone, cultural context acknowledged
6. **Every scene must be labeled with a timecode estimate.** Use: `## Scene Name (X:XX - X:XX)`
7. **No editorial commentary about the channel or the creator.** The script is narration only.
8. **Call to action appears only in the conclusion.** One sentence maximum. No begging.
9. **Write in `{language}`.** For Japanese: use です/ます register throughout.

# Prompt

```
You are a professional script writer for a mystery YouTube channel.

Your task is to write the full narration script for this video.

---

TOPIC: {topic}
LANGUAGE: {language}
VIDEO LENGTH: {video_length_minutes} minutes
STYLE: {style}
NICHE: {niche}

TARGET WORD COUNT: {video_length_minutes * 130} words (±10% acceptable)
MINIMUM WORDS: {video_length_minutes * 117}
MAXIMUM WORDS: {video_length_minutes * 143}

---

Read before writing:
- STYLE_GUIDE.md → section for {style} — apply tone, rhythm, and language rules exactly
- MASTER_RULE.md → Rule 2 (No Fabrication), Rule 3 (Word Count), Rule 4 (Hook Standard)

INPUT FILES:
- projects/{project_slug}/story_outline.md → follow this structure exactly
- projects/{project_slug}/research_verified.md → only source of factual content

---

Write the full script in this format:

---

# Script: {topic}

**Style:** {style}
**Language:** {language}
**Target length:** {video_length_minutes} min
**Word count:** [fill in after writing]

---

## Hook (0:00 – 0:30)

[Write the hook. Max 65 words. Drop the viewer immediately into the most compelling moment.
No channel greeting. No presenter introduction. No clichés.
End with either a shocking statement or a specific unanswered question.]

---

## Introduction (0:30 – ~1:30)

[Establish: Who? Where? When? What made this strange?
Give the viewer the context they need to follow the story.
End this section with a statement that pulls them into Scene 1.]

---

## Scene 1: [Name from outline] (~1:30 – ~X:XX)

[Write narration for this scene. Follow the emotional arc from the outline.
Use only facts from research_verified.md.
Label any speculation: "Some accounts suggest..." or "According to [source]..."]

---

[Continue for all scenes as defined in the story outline]

---

## Conclusion (~X:XX – End)

[Summarize what is known. State clearly what remains unsolved.
End with a thought-provoking final line — the question the viewer will still be thinking about tomorrow.
Call to action (one sentence only): e.g., "If you want more stories like this, subscribe — a new mystery drops every week."]

---

**Final word count:** [count]
**Estimated runtime:** [word_count / 130] minutes

---

STRICT RULES:
- Every factual claim must be traceable to research_verified.md.
- If a fact is not in research_verified.md, do not write it. Flag the gap instead.
- Speculation uses hedged language — never presented as fact.
- Word count must be within the specified range.
- Hook must be ≤65 words.
- Write in {language}.
- For {style} = japanese_mystery: use です/ます register throughout.
- For {style} = reddit_narration: switch to first person when voicing the original post.

Save output to: projects/{project_slug}/script.md
```

# Validation Checklist

- [ ] Script follows scene structure from `story_outline.md` exactly (same scenes, same order)
- [ ] Hook is ≤65 words
- [ ] Hook does not open with channel greeting, presenter intro, or generic cliché
- [ ] Final word count is within ±10% of target (`video_length_minutes × 130`)
- [ ] Every scene has a timecode estimate label
- [ ] No factual claim appears that is not in `research_verified.md`
- [ ] All speculation uses hedged language (not presented as confirmed fact)
- [ ] Any research gaps are flagged with `[RESEARCH GAP]`
- [ ] Tone and sentence rhythm match the `{style}` rules in STYLE_GUIDE.md
- [ ] Call to action appears once only, in the conclusion, ≤1 sentence
- [ ] For `japanese_mystery`: です/ます register used throughout
- [ ] For `reddit_narration`: first person used when voicing the original post
- [ ] Script is written in the correct language (`{language}`)
- [ ] File saved to `projects/{project_slug}/script.md`
