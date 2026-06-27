# Purpose

Transform the narration script into a voice-director-ready document. This means: clean plain text for TTS, precise pacing markers, emotional delivery notes, pronunciation guides for difficult words, and language-specific rhythm adjustments. The output must make the narration sound natural, suspenseful, and human — not robotic.

This prompt produces two outputs: `voice_script.txt` (clean TTS-ready text) and `voice_direction.md` (human or AI voice director notes with emotional beats and delivery instructions).

# Inputs

| File / Field | Required | Description |
|---|---|---|
| `projects/{project_slug}/script.md` | yes | Full narration script |
| `projects/{project_slug}/story_bible.md` | yes | Pronunciation guides for proper nouns |
| `projects/{project_slug}/story_outline.md` | yes | Emotional arc — informs delivery notes |
| `input.json` → `language` | yes | Determines pacing rules and language-specific adjustments |
| `input.json` → `style` | yes | Voice character for this style |
| `STYLE_GUIDE.md` | yes | Voice tone, speed, and register per style |
| `MASTER_RULE.md` | yes | Word count match Rule 6 |

# Outputs

| File | Location | Description |
|---|---|---|
| `voice_script.txt` | `projects/{project_slug}/voice_script.txt` | Clean plain text for TTS or voice actor |
| `voice_direction.md` | `projects/{project_slug}/voice_direction.md` | Delivery notes, emotional beats, pronunciation guide |

# Rules

1. **`voice_script.txt` must be pure plain text.** No markdown, no headers, no brackets except approved pacing markers. Any special character outside pacing markers must be removed.
2. **Approved pacing markers only:**
   - `[PAUSE:0.5s]` — short breath between thoughts
   - `[PAUSE:1s]` — natural sentence end pause
   - `[PAUSE:1.5s]` — scene transition pause
   - `[PAUSE:2s]` — dramatic pause (maximum 3 per video — use sparingly)
   - `[PAUSE:3s]` — dead silence moment (maximum 1 per video — reserve for the most chilling beat)
   - `[SLOW]` — begin slower delivery
   - `[NORMAL]` — return to standard delivery speed
   - `[FAST]` — accelerate pace (for rapid-fire fact sequences)
   - `[WHISPER]` — lower volume/intensity (for intimate or disturbing moments)
3. **Do not add or remove words from the script.** The voice script must contain the same words as the final script. Only formatting is changed.
4. **Pacing must serve the emotional arc.** Slow down for dread and grief. Speed up for cascading revelations. Use silence at the single most disturbing moment.
5. **Pronunciation guides are mandatory for:**
   - All proper nouns not in standard English (Japanese names, place names, etc.)
   - Any term the reader might mispronounce
   - All proper nouns when language is `ja` or `vi`
6. **Language-specific rules:**
   - English: Average pacing ~130 wpm. Vary between 100 (dramatic) and 160 (energetic).
   - Japanese: Write in natural spoken Japanese, not stiff written register. Pacing ~300 morae/min.
   - Vietnamese: Tonal language — note tones on ambiguous words. Pacing ~150 syllables/min.
7. **ElevenLabs optimization (when language = en):**
   - Use commas to create micro-pauses in long sentences
   - Break run-on sentences into shorter segments
   - Avoid parenthetical asides — rewrite as sequential sentences
   - Spell out numbers: "2013" → "two thousand and thirteen" for TTS accuracy
   - Spell out abbreviations: "LAPD" → "L-A-P-D" or "the Los Angeles Police Department"
8. **`voice_direction.md` is for human voice actors or advanced TTS with emotion control.** It is not required for basic TTS use but must always be generated.

# Prompt

```
You are a voice director for an AI YouTube mystery channel.

Your task is to prepare the narration script for voice production. You will produce two outputs: a clean TTS-ready voice script, and a voice direction document with emotional delivery notes.

---

TOPIC: {topic}
LANGUAGE: {language}
STYLE: {style}
PROJECT SLUG: {project_slug}

---

Read before proceeding:
- STYLE_GUIDE.md → {style} voice tone section (speed, register, emotional character)
- projects/{project_slug}/story_bible.md → pronunciation guides for proper nouns
- projects/{project_slug}/story_outline.md → emotional arc — which scenes are high tension vs. low tension

INPUT: projects/{project_slug}/script.md

---

STEP 1 — Read the full script. Identify:
a) Scene transitions (where tone shifts significantly)
b) High-tension moments (where the viewer should feel dread or shock)
c) Slow revelation moments (where pace should drop)
d) Rapid-fire sequences (where facts accumulate quickly)
e) The single most disturbing or chilling moment in the entire script

STEP 2 — Produce voice_script.txt

Strip all markdown from the script:
- Remove all ## scene headers
- Remove all **bold** and *italic* markers
- Remove all timecode annotations
- Remove all parenthetical stage directions
- Remove scene labels

Then format for TTS:
- Add [PAUSE:1s] after every sentence that ends a complete thought
- Add [PAUSE:1.5s] at every scene transition (blank line in original script)
- Add [PAUSE:2s] at the three most dramatically important moments
- Add [PAUSE:3s] at the single most chilling moment in the script
- Add [SLOW] before the most atmospheric passages; [NORMAL] to close them
- Add [FAST] before any rapid-fact sequences; [NORMAL] to close them
- Add [WHISPER] before any particularly intimate or disturbing lines

For English TTS:
- Spell out all numbers (2013 → "two thousand and thirteen")
- Spell out all abbreviations (LAPD → "the Los Angeles Police Department" on first use)
- Break any sentence over 30 words into two sentences

STEP 3 — Verify word count matches script.md ±5%.

STEP 4 — Produce voice_direction.md

---

# Voice Direction: {topic}

## Voice Character
- **Style:** {style}
- **Overall register:** [Deep/measured/conversational/formal — based on STYLE_GUIDE.md]
- **Baseline speaking speed:** [slow/medium/medium-fast] — [approximate WPM or syllables/min]
- **Emotional character:** [What the narration should feel like overall: authoritative, curious, intimate, reverent]

## Scene-by-Scene Delivery Notes

### [Scene Name]
- **Tone:** [What emotion the narrator is conveying]
- **Speed:** [Slower / Standard / Faster than baseline]
- **Key delivery instruction:** [e.g., "Lower your voice slightly here. Don't rush the sentence about the hotel."]
- **Specific lines requiring special delivery:**
  - Line: "[exact line from script]"
    Direction: [How to deliver it: pause before, stress which word, trailing off vs. sharp cut]

[Repeat for each scene]

## Critical Moments
These are the most important moments for delivery. Get these right.

### The Hook (0:00-0:30)
[Delivery instruction — how to open]

### The Climax Beat
[Exact line]: "[text]"
[Direction]: [How to deliver the most chilling moment]

### The Closing Line
[Exact line]: "[text]"
[Direction]: [End strong, end with weight — not rushed]

## Pronunciation Guide
For every proper noun and potentially difficult word in the script:

| Word / Name | Phonetic Guide | Notes |
|---|---|---|
| [Name] | [IPA or simple phonetic] | [Any context — Japanese name, regional accent, etc.] |

## ElevenLabs Settings (English only)
- Recommended voice type: [male/female/neutral, low/mid/high register]
- Stability: [0.55 – 0.70 for documentary / 0.45 – 0.60 for narration]
- Similarity Boost: [0.70 – 0.85]
- Style: [0.30 – 0.50 for {dark_documentary} / 0.50 – 0.70 for {reddit_narration}]

---

Write voice_direction.md in {language}.
Write voice_script.txt in pure plain text, same language as script.md, with only approved pacing markers.

Save both files:
- projects/{project_slug}/voice_script.txt
- projects/{project_slug}/voice_direction.md
```

# Validation Checklist

**voice_script.txt:**
- [ ] No markdown characters remaining (`#`, `*`, `_`, `>`, `-` at line start, `|`)
- [ ] No brackets except approved pacing markers (`[PAUSE:Xs]`, `[SLOW]`, `[NORMAL]`, `[FAST]`, `[WHISPER]`)
- [ ] At least one `[PAUSE:2s]` present (dramatic pause)
- [ ] Exactly one `[PAUSE:3s]` present (the single most chilling moment)
- [ ] `[SLOW]` / `[NORMAL]` pair present around at least one atmospheric passage
- [ ] All `[SLOW]` tags have a corresponding `[NORMAL]` close tag
- [ ] Word count matches `script.md` ±5%
- [ ] For English: numbers spelled out, abbreviations expanded on first use
- [ ] No sentence exceeds 30 words without a natural break
- [ ] File is clean UTF-8 plain text

**voice_direction.md:**
- [ ] Voice character section defines register, speed, and emotional character
- [ ] Every scene has delivery notes
- [ ] Critical Moments section covers: hook, climax beat, and closing line
- [ ] Pronunciation guide covers all proper nouns from `story_bible.md`
- [ ] For English: ElevenLabs settings are present
- [ ] File saved to `projects/{project_slug}/voice_direction.md`
