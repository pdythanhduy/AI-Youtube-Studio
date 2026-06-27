# MASTER RULE — AI YouTube Studio OS

Core operating rules, quality standards, image policy, and consistency requirements. All agents and all humans must follow these rules.

---

## Rule 1: The Four Required Inputs

No production begins without all four required fields in `input.json`:

1. `topic` — must be specific and researchable
2. `language` — must be a valid ISO 639-1 code
3. `video_length_minutes` — must be a positive integer between 5 and 60
4. `style` — must match a defined style in STYLE_GUIDE.md

**If any required field is missing or invalid, stop. Do not guess. Return an error and request the missing input.**

---

## Rule 2: No Fabrication

- Do not invent facts, statistics, names, dates, or quotes.
- Do not generate fake URLs or fabricated source links.
- If a fact cannot be verified, label it: `[Unverified — include with caution]`.
- If a claim is disputed, present both sides: `[Disputed — some sources say X, others say Y]`.
- Real events must be described accurately. Dramatization is allowed in tone, not in fact.

---

## Rule 3: Script Length Discipline

Scripts must hit their target word count within ±10%.

| Video Length | Min Words | Target Words | Max Words |
|---|---|---|---|
| 5 min | 580 | 650 | 720 |
| 8 min | 940 | 1,040 | 1,150 |
| 10 min | 1,170 | 1,300 | 1,430 |
| 12 min | 1,400 | 1,560 | 1,720 |
| 15 min | 1,750 | 1,950 | 2,150 |
| 20 min | 2,340 | 2,600 | 2,860 |

Basis: 130 words per minute for English narration at measured pace.

If a script exceeds maximum word count, cut filler — never cut facts or key narrative beats.
If a script is under minimum word count, deepen the research or add missing context — never pad with empty sentences.

---

## Rule 4: Hook Standard

The first 30 seconds (hook) must do exactly one of the following:
- Present a shocking or unexplained fact
- Pose a specific unanswered question
- Drop the viewer into the middle of the most dramatic moment

The hook must not:
- Begin with "Hi everyone, welcome back to my channel"
- Introduce the presenter
- Start with a question so vague it could apply to any video ("Have you ever wondered...")
- Use clichés like "What you're about to hear will change everything"

**The hook is the most important 30 seconds of the video. Write it last. Edit it most.**

---

## Rule 5: Image Policy

### When to Use Real Internet Images

Use real photos, screenshots, news images, or documentary footage when:

| Situation | Reason |
|---|---|
| The person, place, or event actually exists | Authenticity builds credibility |
| News coverage exists | Use screenshotted headlines or clips |
| The Reddit post or forum thread is the subject | Screenshot the original content |
| The Google Maps location is the focus | Use a direct screenshot from Google Maps/Earth |
| A document, letter, or police report is referenced | Show the real document if publicly available |
| The location is a known place (city, building, landmark) | Real images have higher trust value |

**Sources for real images:**
- News archives (BBC, Reuters, AP, local papers)
- Reddit / Twitter / social media screenshots (original content)
- Google Maps / Google Earth screenshots
- Wikimedia Commons (check license)
- Internet Archive / Wayback Machine
- Documentary screenshots (cite source)
- YouTube stills (cite source)

### When to Use AI-Generated Images

Use AI-generated images when:

| Situation | Reason |
|---|---|
| No real photo exists of the described scene | e.g., a historical event, an imagined location |
| The scene is a dramatization or reconstruction | Label it: "Dramatization" |
| The atmosphere needs to be set (fog, darkness, dread) | Mood imagery that supplements real content |
| The location is fictional or described in a story | Reddit NoSleep, creepypasta, etc. |
| A person's identity must be obscured | Generate a non-real face |
| A scene is too disturbing to show realistically | Safe, stylized alternative |

**Label all AI-generated images in the storyboard:** `[AI-GENERATED]`

**Label all dramatization images:** `[DRAMATIZATION — NOT REAL]`

### Never Use

- Copyrighted images without explicit permission or fair use justification
- Images sourced from unclear origins (watermarked without source)
- AI images presented as real photographs
- Fake "evidence" presented as genuine documentation

---

## Rule 6: Consistency Across Components

Every output file in a project must be internally consistent:

| Consistency Check | Rule |
|---|---|
| Names | A person named in `research.md` must be spelled identically in `script.md`, `storyboard.md`, and `seo.md` |
| Dates | Dates in `research.md` must match `script.md` exactly |
| Timeline | Scene order in `storyboard.md` must match scene order in `script.md` |
| Word count | `voice_script.txt` word count must match `script.md` word count ±5% |
| Image count | Image count in `image_plan.md` must match visual count in `storyboard.md` |
| Timecodes | `subtitles.srt` timecodes must be sequential and non-overlapping |

Run a consistency check before generating `export_manifest.json`. If any check fails, fix it before marking status as `complete`.

---

## Rule 7: Language and Tone Standards

**For English content:**
- Use active voice wherever possible
- Sentence length: vary between short (7-10 words) and medium (15-20 words). Avoid long sentences in narration.
- Avoid passive constructions in the hook and climax scenes
- Present tense for current mystery status: "The case remains unsolved."
- Past tense for historical events: "She checked in on January 26, 2013."

**For non-English content (Japanese, Vietnamese, etc.):**
- The script must be written by the AI in the target language from the start
- Do not translate from English — write natively in the target language
- Cultural references must be appropriate for the target audience
- For Japanese content: use polite register (です/ます form) for narration

---

## Rule 8: SEO Compliance

- Video title: max 70 characters, including spaces
- Description: first 150 characters must be a hook — not a channel intro
- Tags: minimum 15, maximum 30
- At least one tag must be a long-tail search phrase (5+ words)
- Chapters (timestamps) must be included in every description

---

## Rule 9: Subtitle Standards

- Max 42 characters per subtitle line
- Max 2 lines per subtitle segment
- Max 7 seconds per segment (3-4 seconds is ideal)
- Minimum 1 second per segment
- No segment may overlap with the next
- Do not break noun phrases across lines when avoidable
  - Bad: `The disappear-` / `ance of Elisa Lam`
  - Good: `The disappearance` / `of Elisa Lam`

---

## Rule 10: File Naming and Structure

All project files live in: `projects/YYYYMMDD_topic-slug/`

Topic slug rules:
- Lowercase only
- Replace spaces with hyphens
- Remove special characters
- Max 40 characters
- Example: `20260626_elisa-lam-cecil-hotel`

File names are fixed — never rename output files. Automation agents rely on predictable file names.

---

## Rule 11: Sensitive Content

- Do not show, describe, or generate graphic imagery of violence, death, or abuse
- Do not include names or faces of minors in cases involving children without confirmed public availability
- Do not speculate about the guilt of living individuals as if speculation were fact
- Paranormal claims must be labeled as such: "Some believe...", "According to witnesses...", "One theory suggests..."
- Present unsolved cases as unsolved — do not fabricate a conclusion

---

## Rule 12: Export Readiness Checklist

Before generating `export_manifest.json`, verify all of the following:

- [ ] `research.md` — at least 5 facts, at least 3 sources, no fabricated URLs
- [ ] `script.md` — word count within target range, hook under 30 seconds
- [ ] `storyboard.md` — every scene has a visual, every visual has an image type
- [ ] `image_plan.md` — every image slot has a source strategy (no TBDs)
- [ ] `voice_script.txt` — clean plain text, pacing markers present, no markdown
- [ ] `subtitles.srt` — valid SRT format, timecodes sequential, line length ≤42 chars
- [ ] `thumbnail_prompt.md` — self-contained prompt, text overlay specified
- [ ] `seo.md` — title ≤70 chars, ≥15 tags, description hook in first 150 chars
- [ ] Consistency check passed (names, dates, timeline, word count, image count)

Only when all checkboxes are satisfied may status be set to `"ready_for_production"`.
