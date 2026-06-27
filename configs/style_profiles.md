# Style Profiles — AI YouTube Studio OS

Per-style configuration for narrative tone, visual treatment, pacing, music direction, and voice character. These profiles are the machine-readable version of the style definitions in STYLE_GUIDE.md. The STYLE_GUIDE.md is the human-readable reference — this file is what the engines read.

**Schema version:** 1.0

---

## How Style Profiles Are Used

The Routing Engine reads the `style` field from `input.json` and selects the matching profile. The Workflow Engine injects profile values into prompts at construction time. Every `{style_profile.*}` placeholder in a prompt resolves to a value from this file.

Style profiles augment — they do not replace — the base prompts. A prompt file defines structure; the style profile defines character.

---

## Profile: `dark_documentary`

### Narrative Settings

| Key | Value | Description |
|---|---|---|
| `tone` | `authoritative` | The narrator is a measured, knowledgeable voice |
| `person` | `third` | Third-person narration throughout |
| `humor_allowed` | `false` | No jokes, lightness, or casual asides |
| `speculation_labeling` | `required` | Any non-verified claim must use hedged language |
| `hook_type` | `shocking_fact` or `unanswered_question` | Hook must be one of these types |
| `closing_type` | `open_question` | Most endings are unresolved |
| `sentence_variety` | `mixed_short_medium` | Vary 7-15 word and 15-25 word sentences |
| `climax_sentence_style` | `short_punchy` | At peak moments: sentences under 10 words |

### Visual Settings

| Key | Value | Description |
|---|---|---|
| `color_grade` | `desaturated_cool` | Low saturation, blue-gray tones |
| `primary_colors` | `#1a2530, #2d3f50, #8a9ba8` | Dark navy, steel blue, muted gray |
| `accent_color` | `#b8860b` | Warm amber — archival/aged feel |
| `image_preference` | `real_first` | Strongly prefer real images over AI |
| `ai_image_style` | `cinematic_realistic` | AI images must look photorealistic |
| `text_overlay_style` | `white_serif_on_dark` | White or pale gray serif text |
| `transition_style` | `slow_fade` or `cut` | No wipes, zooms, or flashy effects |
| `b_roll_style` | `slow_pan` | Camera movement is deliberate, never frenetic |

### Pacing Settings

| Key | Value | Description |
|---|---|---|
| `opening_pace` | `slow` | First 2 minutes: slow atmospheric build |
| `middle_pace` | `steady_escalating` | Gradual tension increase |
| `climax_position` | `0.70-0.80` | Peak tension at 70-80% of video |
| `closing_pace` | `slow` | Ending is measured, not rushed |
| `beat_duration_seconds` | `45-90` | Standard visual beat length |
| `dramatic_pause_budget` | `3` | Max [PAUSE:2s] markers in voice script |
| `chilling_pause_budget` | `1` | Max [PAUSE:3s] markers (reserve for singular moment) |

### Music Settings

| Key | Value |
|---|---|
| `music_type` | `dark_ambient_instrumental` |
| `lyrics_allowed` | `false` |
| `volume_under_narration` | `low` — background only |
| `tempo` | `slow` — under 80 BPM |
| `instrumentation` | `low drone, sparse strings, minimal piano` |
| `silence_as_tool` | `true` — silence at peak dramatic moments is intentional |

---

## Profile: `reddit_narration`

### Narrative Settings

| Key | Value | Description |
|---|---|---|
| `tone` | `conversational_intimate` | Like a friend telling a story |
| `person_default` | `third` | Third person for context |
| `person_post_narration` | `first` | First person when voicing the original poster |
| `humor_allowed` | `false` | Mystery content — no comedy |
| `speculation_labeling` | `required` | Any non-verified claim requires hedging |
| `hook_type` | `in_media_res` | Drop into the middle of the most disturbing moment |
| `reddit_post_format` | `faithful_paraphrase` | Voice the post faithfully — do not editorialize |
| `community_reaction_included` | `true` | Top comment reactions are a required beat |

### Visual Settings

| Key | Value | Description |
|---|---|---|
| `color_grade` | `dark_warm` | Slightly warmer than documentary — dark but not cold |
| `primary_colors` | `#1f1a17, #3d2f28, #a08060` | Dark brown tones |
| `image_preference` | `screenshot_first` | Show the original post and platform |
| `ai_image_style` | `stylized_impressionistic` | Not photorealistic — slightly dreamlike |
| `reddit_screenshot_style` | `dark_mode` | Prefer Reddit dark mode interface |
| `text_overlay_style` | `reddit_quote_highlight` | Pull-quote style for key post excerpts |
| `transition_style` | `cut` | Fast cuts in hook; slower in body |

### Pacing Settings

| Key | Value | Description |
|---|---|---|
| `opening_pace` | `fast` | Get to the story immediately |
| `post_read_pace` | `medium` | Slow down during the post read |
| `community_reaction_pace` | `fast` | Quick scan of reactions |
| `closing_pace` | `medium_slow` | End with weight |
| `beat_duration_seconds` | `30-60` | Faster cuts than documentary |

### Music Settings

| Key | Value |
|---|---|
| `music_type` | `lo-fi_horror_ambient` |
| `texture_allowed` | `true` — crackling, distant sounds, tape hiss |
| `dynamic_range` | `medium` — more dynamic than documentary |
| `stinger_allowed` | `true` — subtle stinger at the most frightening moment |

---

## Profile: `mystery_investigation`

### Narrative Settings

| Key | Value | Description |
|---|---|---|
| `tone` | `curious_analytical` | Like a detective narrating their own case |
| `person` | `first` or `second` | "We found..." or "Look at this..." both acceptable |
| `viewer_involvement` | `high` | Pull viewer into the investigation actively |
| `evidence_structure` | `progressive_reveal` | Each scene adds a new piece of evidence |
| `editorial_opinion_allowed` | `true` | Narrator may share their interpretation at the end |
| `uncertainty_as_feature` | `true` | "We don't know" is a valid and honest statement |

### Visual Settings

| Key | Value | Description |
|---|---|---|
| `color_grade` | `neutral_clean` or `green_tinted` | Documentary-clean or digital investigation feel |
| `image_preference` | `screenshot_and_real_first` | Screenshots, maps, and screen recordings preferred |
| `annotation_allowed` | `true` — circles, arrows, zoom-ins | Evidence must be highlighted |
| `ai_image_style` | `documentary_style` | If AI is used, it must look like a real photo |
| `text_overlay_style` | `technical_monospace` | Coordinates, timestamps, metadata feel |
| `metadata_display` | `true` — show coordinates, timestamps, file data | Investigation authenticity |

### Pacing Settings

| Key | Value | Description |
|---|---|---|
| `structure` | `evidence_beats` | Each scene is a distinct discovery |
| `reveal_cadence` | `one_discovery_per_scene` | Do not reveal multiple findings in one scene |
| `opening_pace` | `medium` | Establish the discovery context |
| `investigation_pace` | `steady` | Methodical — not rushed |

### Music Settings

| Key | Value |
|---|---|
| `music_type` | `electronic_tense_ambient` |
| `cognitive_vs_emotional` | `cognitive` — supports thinking, not just feeling |
| `silence_use` | `high` — silence for cognitive moments |

---

## Profile: `japanese_mystery`

### Narrative Settings

| Key | Value | Description |
|---|---|---|
| `tone` | `respectful_atmospheric` | Reverent toward the cultural weight of the subject |
| `person` | `third` | Third-person narration |
| `cultural_context_required` | `true` | Cultural context beat must appear early |
| `legend_vs_fact_distinction` | `required` | Always label: 伝説 (legend) vs 事実 (fact) |
| `pacing_philosophy` | `ma` | 間 (ma) — the Japanese concept of meaningful silence and space |

### Visual Settings

| Key | Value | Description |
|---|---|---|
| `color_grade` | `desaturated_with_red_accent` | Deep shadows, occasional deep crimson |
| `primary_colors` | `#0d0d0d, #1a0a0a, #8b0000` | Near-black, dark red |
| `atmosphere_images` | `rain_fog_empty_streets_traditional` | Core visual vocabulary |
| `ai_image_style` | `east_asian_cinematic_painterly` | Between photorealistic and painted |
| `western_horror_tropes` | `forbidden` — no jump-scare stings, no Western horror clichés | Cultural respect |

### Pacing Settings

| Key | Value | Description |
|---|---|---|
| `opening_pace` | `very_slow` | Longer atmospheric setup than other styles |
| `silence_budget` | `high` | More [PAUSE:2s] and [PAUSE:3s] usage |
| `unsaid_principle` | `active` — what is not said is as important as what is | Japanese aesthetic principle |
| `beat_duration_seconds` | `60-90` | Slower visual changes — longer dwelling |

### Music Settings

| Key | Value |
|---|---|
| `music_type` | `traditional_japanese_ambient_electronic` |
| `instruments` | `koto, shakuhachi, taiko (distant), ambient electronics` |
| `western_stingers` | `forbidden` |
| `silence_as_instrument` | `true` — a single bell note in silence is more powerful than continuous music |

---

## Adding a New Style Profile

To add a new style (e.g., `true_crime_podcast`):

1. Add a new `## Profile: true_crime_podcast` section following the same key structure.
2. Define all required key groups: Narrative, Visual, Pacing, Music.
3. Update STYLE_GUIDE.md with the human-readable description of the new style.
4. Bump `schema_version` in this file.
5. Add the new style ID to `core/naming_conventions.md` style ID table.
6. Add routing support in `engine/routing_engine.md` style selection table.
7. Add a test case in `tests/acceptance_tests.md`.
