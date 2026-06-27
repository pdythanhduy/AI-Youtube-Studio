# Language Profiles — AI YouTube Studio OS

Per-language configuration for narration pacing, register, formatting conventions, subtitle rules, TTS settings, and SEO considerations. Every supported language has a complete profile. Adding a new language means adding a new profile section here — no engine code changes required.

**Schema version:** 1.0

---

## How Language Profiles Are Used

The Routing Engine reads the `language` field from `input.json` and selects the matching profile section. The Workflow Engine injects the profile into every stage that produces language-specific output. Prompts reference the profile via `{language_profile.*}` placeholders.

---

## Profile: English (`en`)

### Narration Settings

| Key | Value | Description |
|---|---|---|
| `words_per_minute` | `130` | Target narration speed for TTS/voice |
| `words_per_minute_slow` | `100` | Speed for atmospheric/dramatic passages |
| `words_per_minute_fast` | `160` | Speed for rapid-fact sequences |
| `sentence_max_words` | `30` | Max words per sentence before breaking |
| `paragraph_max_sentences` | `4` | Max sentences per narration paragraph |

### Register and Tone

| Key | Value |
|---|---|
| `default_register` | `standard` — neither formal nor casual |
| `number_format` | Spell out in narration: "two thousand and thirteen" |
| `abbreviation_format` | Expand on first use: "LAPD → the Los Angeles Police Department" |
| `date_format_narration` | "January 26, 2013" (Month DD, YYYY) |
| `date_format_subtitles` | "Jan. 26, 2013" (abbreviated for line length) |
| `currency_format` | Spell out: "five hundred dollars" |

### Subtitle Rules

| Key | Value |
|---|---|
| `max_chars_per_line` | `42` |
| `max_lines_per_segment` | `2` |
| `max_segment_duration_seconds` | `7` |
| `target_segment_duration_seconds` | `3.5` |
| `encoding` | `UTF-8` |
| `word_wrap_rule` | Do not break noun phrases — break at prepositions or conjunctions |

### TTS Settings (ElevenLabs)

| Key | Value |
|---|---|
| `recommended_stability` | `0.60` |
| `recommended_similarity_boost` | `0.75` |
| `recommended_style` | `0.35` (documentary) / `0.55` (narration) |
| `pause_short_ms` | `500` |
| `pause_standard_ms` | `1000` |
| `pause_scene_ms` | `1500` |
| `pause_dramatic_ms` | `2000` |
| `pause_chilling_ms` | `3000` |

### SEO Considerations

| Key | Value |
|---|---|
| `primary_search_market` | `US, UK, AU, CA` |
| `title_character_limit` | `70` |
| `description_hook_chars` | `150` |
| `recommended_hashtag_count` | `3-5` |
| `long_tail_min_words` | `5` |

---

## Profile: Japanese (`ja`)

### Narration Settings

| Key | Value | Description |
|---|---|---|
| `morae_per_minute` | `300` | Japanese speech measured in morae (mora = unit of sound) |
| `words_per_minute_equivalent` | `~100` | Approximate English word equivalent for script planning |
| `script_planning_multiplier` | `0.77` | Multiply English target word count by this for Japanese (130 × 0.77 ≈ 100) |
| `sentence_max_morae` | `60` | Break sentences beyond this for readability |

### Register and Tone

| Key | Value |
|---|---|
| `default_register` | `polite_formal` — です/ます throughout narration |
| `number_format` | Kanji numerals for historical/formal context: 一九一三年 / Arabic for modern: 2013年 |
| `name_order` | Family name first for Japanese names: 山田 太郎 (Yamada Taro) |
| `foreign_name_format` | Katakana transcription required: エリザ・ラム |
| `date_format_narration` | 2013年1月26日 |
| `date_format_subtitles` | 2013/1/26 |
| `honorifics` | Omit honorifics in narration for documentary register |

### Subtitle Rules

| Key | Value |
|---|---|
| `max_chars_per_line` | `20` (Japanese characters are wider) |
| `max_lines_per_segment` | `2` |
| `max_segment_duration_seconds` | `5` |
| `target_segment_duration_seconds` | `3.0` |
| `encoding` | `UTF-8` |
| `furigana_policy` | Include furigana in `voice_direction.md` for uncommon kanji; omit from subtitle SRT |
| `word_wrap_rule` | Break after particles (は, が, を, に, で) when possible |

### TTS Settings

| Key | Value |
|---|---|
| `recommended_voice_type` | Native Japanese speaker voice |
| `pause_short_ms` | `600` (Japanese narration uses longer pauses than English) |
| `pause_standard_ms` | `1200` |
| `pause_scene_ms` | `2000` |
| `pause_dramatic_ms` | `3000` |
| `pacing_marker_format` | Same markers as English — they are language-agnostic |

### Cultural Context Rules

| Key | Value |
|---|---|
| `cultural_sensitivity` | HIGH — Japanese mysteries carry significant cultural weight |
| `suicide_topic_handling` | Follow Japanese media guidelines: do not describe methods, use respectful framing |
| `folklore_labeling` | Always distinguish legend (伝説) from documented fact (事実) |
| `location_format` | Prefecture → City → District order: 東京都渋谷区 |

### SEO Considerations

| Key | Value |
|---|---|
| `primary_search_market` | `JP` |
| `title_character_limit` | `60` characters recommended for Japanese YouTube (kanji are wider) |
| `recommended_hashtag_count` | `3-5` |
| `crossover_english_tags` | Include 3-5 English tags for international mystery audience overlap |

---

## Profile: Vietnamese (`vi`)

### Narration Settings

| Key | Value | Description |
|---|---|---|
| `syllables_per_minute` | `150` | Vietnamese narration speed |
| `words_per_minute_equivalent` | `~120` | Approximate equivalent for script planning |
| `script_planning_multiplier` | `0.92` | Multiply English target word count by this for Vietnamese |
| `sentence_max_words` | `25` | Vietnamese sentences tend shorter than English |

### Register and Tone

| Key | Value |
|---|---|
| `default_register` | `formal_standard` — standard educated Vietnamese |
| `number_format` | Arabic numerals in narration (2013), spell out when dramatic emphasis needed |
| `date_format_narration` | ngày 26 tháng 1 năm 2013 |
| `date_format_subtitles` | 26/1/2013 |
| `pronoun_system` | Use `tôi` for narrator; use appropriate kinship terms when discussing subjects |
| `tone_marking` | All Vietnamese text must include full diacritical marks — no stripped tone marks |

### Subtitle Rules

| Key | Value |
|---|---|
| `max_chars_per_line` | `48` (Vietnamese with diacritics reads slightly narrower than CJK but wider than English) |
| `max_lines_per_segment` | `2` |
| `max_segment_duration_seconds` | `6` |
| `target_segment_duration_seconds` | `3.5` |
| `encoding` | `UTF-8` (diacritical marks require UTF-8, not Latin-1) |
| `word_wrap_rule` | Break at clause boundaries; do not break compound nouns |

### TTS Settings

| Key | Value |
|---|---|
| `recommended_voice_type` | Native Vietnamese speaker voice; Southern or Northern accent per audience target |
| `pause_short_ms` | `500` |
| `pause_standard_ms` | `1000` |
| `pause_scene_ms` | `1500` |
| `pause_dramatic_ms` | `2000` |

### SEO Considerations

| Key | Value |
|---|---|
| `primary_search_market` | `VN` |
| `title_character_limit` | `70` |
| `recommended_hashtag_count` | `3-5` |
| `crossover_english_tags` | Include 2-3 English tags for overseas Vietnamese community |

---

## Adding a New Language Profile

To add support for a new language (e.g., Korean `ko`):

1. Add a new `## Profile: Korean (ko)` section to this file following the same structure.
2. Define all required keys: narration settings, register, subtitle rules, TTS settings, SEO considerations.
3. Bump `schema_version` in this file.
4. Add a test case in `tests/acceptance_tests.md` for the new language.
5. Add `ko` to the Routing Engine's supported language list in `engine/routing_engine.md`.
6. No engine code changes are required — the Routing Engine reads the profile from this file.
