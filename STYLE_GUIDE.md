# STYLE GUIDE — AI YouTube Studio OS

Visual, narrative, voice, and editing consistency rules for mystery-niche YouTube content.

---

## Defined Styles

Four production styles are available. Each has specific rules for narrative tone, visual treatment, pacing, and music. The `style` field in `input.json` must match one of these exactly.

---

### Style: `dark_documentary`

**Use for:** Real-world cases, disappearances, deaths, historical mysteries, true crime adjacent.

**Examples:** Elisa Lam, Sodder children, Missing 411, Dyatlov Pass.

#### Narrative Tone
- Measured, serious, authoritative
- Third-person narration throughout
- No jokes, no humor, no lightness
- Emotional weight must be earned through facts, not dramatic adjectives
- Present events as documented — label speculation clearly
- Sentence rhythm: slow and deliberate, with short punchy statements at climax moments

**Bad example:** "Nobody EVER expected what happened next — it was ABSOLUTELY SHOCKING!"
**Good example:** "By morning, she was gone. The elevator footage was the last time anyone saw Elisa Lam alive."

#### Visual Treatment
- Dark color grade: desaturated, deep shadows, cool tones (blue, teal, charcoal)
- Real photographs and news footage preferred
- AI images: cinematic, realistic, not stylized
- Avoid bright colors, cartoons, or any playful visual elements
- Text overlays: white or pale gray on dark background, serif or clean sans-serif font
- Transitions: slow fade or cut — no wipes, no flashy effects

#### Pacing
- Slow build in opening (0:00-2:00)
- Steady escalation through middle scenes
- Peak tension 70-80% through the video
- Unresolved ending preferred (most real mysteries are unsolved)

#### Music
- Ambient, dark instrumental
- No lyrics
- Volume: background (under narration), rises at scene transitions
- Suggested tone: low drone, subtle strings, sparse piano
- Silence is a valid tool — use it at dramatic moments

---

### Style: `reddit_narration`

**Use for:** Reddit posts, NoSleep stories, r/UnresolvedMysteries, AskReddit threads, personal accounts.

**Examples:** "I found something in my basement," Reddit ghost stories, "My neighbor does something strange every night."

#### Narrative Tone
- First person when narrating a Reddit post (voice the original poster)
- Third person when providing context or commentary
- Conversational, intimate — like a friend telling a story
- Short, punchy sentences mixed with longer explanatory ones
- Casual language acceptable, but no slang that dates quickly
- Read the original post faithfully — do not editorialize or change the story

**Format:**
```
[Context setting in third person]
"[Direct quote or paraphrase of post — in first person]"
[Transition back to narrator perspective]
[Comments or community reaction if relevant]
[Analysis or follow-up]
```

#### Visual Treatment
- Screenshot of the original Reddit post (pinned, highlighted text)
- Username visible but consider blurring if content is sensitive
- Dark Reddit interface preferred (dark mode screenshot)
- Intercut screenshots with atmospheric imagery
- AI images: stylized, slightly unreal, impressionistic — not photorealistic
- Color palette: slightly warmer than `dark_documentary` — dark but not cold

#### Pacing
- Fast opening — get to the story immediately
- Fast scene cuts in the hook
- Slow down for the creepiest or most confusing moment
- Optional: read comment reactions as a mid-video beat

#### Music
- Lo-fi horror or ambient unease
- Slightly more dynamic than `dark_documentary`
- Can use subtle music with texture (crackling, distant sounds)
- Rise to a stinger at the most frightening moment

---

### Style: `mystery_investigation`

**Use for:** Google Maps mysteries, strange locations, anomalies, puzzles, internet rabbit holes.

**Examples:** Google Maps coordinates with weird structures, mysterious numbers stations, Cicada 3301, abandoned websites.

#### Narrative Tone
- Curious, investigative, analytical — like a detective narrating their own case
- Second person or first person ("What we found," "Follow me down this rabbit hole")
- Ask questions to the viewer — pull them into the investigation
- Present evidence progressively, building the case piece by piece
- Acknowledge when you don't know something — uncertainty is part of the style

**Format:** Each scene is an "evidence beat" — something new is discovered, something deepens the mystery.

#### Visual Treatment
- Heavy use of screen recordings, screenshots, maps, satellite imagery
- Annotated images: circles, arrows, zoom-ins on specific details
- Real imagery strongly preferred — AI images only for atmosphere or concepts
- Text overlays: monospace or technical-feeling font (investigation aesthetic)
- Include coordinate data, timestamps, metadata where relevant
- Color grade: slightly green-tinted for digital investigation feel, or neutral

#### Pacing
- Structured like a reveal: each beat adds a new piece of information
- Build anticipation: "But then we found something we didn't expect."
- Use chapter-style pacing — each scene is a distinct discovery

#### Music
- Electronic, tense, algorithmic texture
- Subtle and non-distracting — this style is more cognitive than emotional
- Can use silence more than other styles

---

### Style: `japanese_mystery`

**Use for:** Japanese urban legends, J-horror cases, strange Japanese internet stories, real Japanese disappearances, Aokigahara, Hachiko-type stories, Japanese paranormal.

**Examples:** The Slit-Mouthed Woman (Kuchisake-onna), the Kyoto abandoned hotel mystery, Takako Konishi.

#### Narrative Tone
- Respectful and measured — Japanese mysteries carry cultural weight
- Formal narration style, not casual
- Acknowledge cultural context — explain Japanese beliefs or practices when relevant
- Do not sensationalize or mock Japanese culture
- When narrating urban legends: distinguish between folklore ("according to legend...") and documented events ("police confirmed...")

#### Visual Treatment
- Atmospheric and evocative: rain, fog, empty streets, traditional architecture
- Strong contrast between old Japan (traditional) and modern Japan (urban, neon)
- Real photos of locations when available
- AI images: East Asian aesthetic, cinematic, slightly painterly
- Color palette: desaturated with occasional deep red accents (culturally resonant for horror/mystery in Japan)
- Text overlays: can include Japanese characters alongside translation

#### Language Rules (for Japanese-language production)
- Write the script in Japanese from scratch — do not translate from English
- Polite register: です/ます throughout narration
- Include furigana in subtitle files for complex kanji where needed
- Cultural references do not need explanation when producing for Japanese audience

#### Pacing
- Slow and deliberate — longer pauses than other styles
- Build dread through atmosphere rather than facts
- The unsaid is as important as the said — leave space

#### Music
- Traditional Japanese instruments with ambient electronic layering
- Or: silence broken by a single musical element (a koto note, a bell)
- Never use Western horror clichés (jump-scare stings)

---

## Cross-Style Rules

These rules apply to every style without exception.

### Thumbnail Style

All thumbnails for this channel share these properties:

| Element | Rule |
|---|---|
| Face/eyes | If a real face is used, eyes must be prominent — looking at the camera or looking to the side with intention |
| Background | Dark, with high contrast between subject and background |
| Text | Max 4 words, bold, high contrast (white/yellow on dark, or black on bright) |
| Color accent | One strong accent color per thumbnail (red, teal, orange, yellow — not all at once) |
| Composition | Subject in left third or center, text in right third or bottom |
| Clickbait markers | Question marks acceptable. Arrows acceptable. Avoid: emoji overload, Comic Sans, MS Paint aesthetic |

### Subtitle Style

| Property | Value |
|---|---|
| Font | Clean sans-serif (YouTube default acceptable) |
| Position | Bottom center |
| Background | Semi-transparent black box (improves readability) |
| Capitalization | Sentence case (first word capitalized only, except proper nouns) |
| Tone | No exclamation marks in subtitles unless it is actual dialogue |

### Voice and Narration Style

| Style | Voice Tone | Speed | Recommended TTS Voice Type |
|---|---|---|---|
| `dark_documentary` | Deep, measured, authoritative | Slow | Male or female, low register |
| `reddit_narration` | Conversational, intimate | Medium | Gender-neutral, warm mid-range |
| `mystery_investigation` | Curious, analytical | Medium | Clear, professional, slight tension |
| `japanese_mystery` | Respectful, atmospheric | Slow | Native or near-native speaker |

**ElevenLabs recommended settings (approximate):**
- Stability: 0.55-0.70
- Similarity Boost: 0.70-0.85
- Style: 0.30-0.50 for documentary styles; 0.50-0.70 for narration styles

---

## Narrative Structure Templates

### Three-Act Mystery Structure

```
Act 1 — Setup (25% of video)
  - Hook: Drop into the most compelling moment
  - Context: Who, where, when
  - Stakes: Why does this matter?

Act 2 — Escalation (50% of video)
  - Scene 1: The ordinary (before everything changed)
  - Scene 2: The anomaly (the first strange thing)
  - Scene 3: The investigation (what was discovered)
  - Scene 4: The dead ends (what couldn't be explained)

Act 3 — Resolution or Void (25% of video)
  - What is known for certain
  - What remains unexplained
  - The open question (preferably unanswered)
  - Call to action (subscribe, comment, next video)
```

### Reddit Narration Structure

```
Setup (15%)
  - Context: where the post appeared, when, basic situation

Main Story (60%)
  - Read/paraphrase the original post faithfully
  - Include the most chilling or confusing details verbatim

Community Reaction (15%)
  - Top comments, theories, responses
  - Did anyone recognize the story?

Status (10%)
  - Update if one exists
  - Or: "The account was deleted. No one heard from OP again."
```

### Investigation Structure

```
Discovery (10%)
  - What were you doing? What did you find?

Evidence Presentation (60%)
  - Present each piece of evidence as a scene
  - Each scene: show the evidence, explain significance, note anomaly

Dead Ends and Theories (20%)
  - What was checked? What was debunked?
  - What theories remain?

Conclusion (10%)
  - What do you believe? (optional — this style allows editorializing)
  - What would solving it require?
```

---

## Visual Tone References

| Style | Comparable Shows/Channels |
|---|---|
| `dark_documentary` | Kendall Rae, Stephanie Harlowe, True Crime Daily |
| `reddit_narration` | MrCreepsPasta, Dr. Creepen, Lazy Masquerade |
| `mystery_investigation` | Nexpo, Nick Crowley, Night Mind |
| `japanese_mystery` | 不思議な話 style channels, Japanese paranormal documentaries |

Use these as tone references only — do not copy content.
