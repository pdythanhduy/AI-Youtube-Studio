# Naming Conventions — AI YouTube Studio OS

All naming rules for files, folders, variables, identifiers, and schema keys across the entire system. Consistency here prevents the most common class of bugs in multi-agent systems: one agent writes a file with one name, another agent looks for it with a different name.

---

## Governing Principle

**One name. One place. No exceptions.**

If two things could be confused by a machine reading their names, they must have different names. If one thing could be referred to in two different ways, choose one and deprecate the other immediately.

---

## Project Slug

The project slug is the unique identifier for a video production run. It is used as the folder name, as a key in databases, and as a reference in all generated files.

### Format
```
YYYYMMDD_[topic-slug]
```

### Topic Slug Rules
- Lowercase only
- Replace spaces with hyphens `-`
- Replace underscores with hyphens `-`
- Remove all special characters: `! @ # $ % ^ & * ( ) , . ? " : { } | < > ' / \`
- Remove leading articles: "the", "a", "an" (English); "the" equivalents in other languages
- Maximum 40 characters for the topic portion
- No consecutive hyphens `--`
- No trailing hyphen

### Examples

| Input Topic | Topic Slug | Full Project Slug |
|---|---|---|
| The Disappearance of Elisa Lam | disappearance-of-elisa-lam | 20260627_disappearance-of-elisa-lam |
| 青木ヶ原の謎 (Aokigahara Mystery) | aokigahara-mystery | 20260627_aokigahara-mystery |
| r/NoSleep: I Found Something in My Basement | r-nosleep-found-something-basement | 20260627_r-nosleep-found-something-basement |
| Google Maps: Coordinates 37°N 116°W | google-maps-37n-116w | 20260627_google-maps-37n-116w |

---

## File Naming

### System Files (core/, engine/, configs/, etc.)
- Format: `snake_case.md` or `snake_case.json`
- All lowercase
- Words separated by underscores
- Descriptive, not abbreviated
- Correct: `director_engine.md`, `language_profiles.md`
- Incorrect: `dirEng.md`, `lang-prof.md`, `lp.md`

### Prompt Files (prompts/)
- Format: `NN_descriptive_name.md` (two-digit index prefix)
- Index is zero-padded: `01`, `02`, ..., `10`, `11`
- Index reflects pipeline execution order
- Correct: `01_research.md`, `10_youtube_seo.md`
- Incorrect: `research.md`, `1_research.md`, `Research_Prompt.md`

### Template Files (templates/)
- Format: `[niche]_template.md`
- Niche matches the `niche` field values from `input.json`
- Correct: `mystery_template.md`, `japan_template.md`, `reddit_template.md`
- Incorrect: `MysteryTemplate.md`, `template_mystery.md`

### Config Files (configs/)
- Format: `[domain]_profiles.md` for profile collections, `[name]_system.md` for system documents
- Correct: `language_profiles.md`, `style_profiles.md`, `configuration_system.md`

### Knowledge Files (knowledge/)
- Format: `[domain]_database.md` for databases, `[domain]_architecture.md` for structural docs
- Correct: `source_database.md`, `memory_database.md`, `asset_library.md`

### Project Output Files (projects/{slug}/)
- File names are **fixed and canonical** — agents must use exactly these names:

| File | Canonical Name |
|---|---|
| User inputs | `input.json` |
| Raw research | `research.md` |
| Source audit report | `source_report.md` |
| Verified research | `research_verified.md` |
| Narrative outline | `story_outline.md` |
| Narration script | `script.md` |
| Continuity reference | `story_bible.md` |
| Visual storyboard | `storyboard.md` |
| Image sourcing plan | `image_plan.md` |
| AI image prompts | `ai_image_prompts.md` |
| TTS-ready voice script | `voice_script.txt` |
| Delivery notes | `voice_direction.md` |
| Subtitle file | `subtitles.srt` |
| Thumbnail brief | `thumbnail_prompt.md` |
| YouTube SEO package | `seo.md` |
| Production manifest | `export_manifest.json` |

---

## Field and Key Naming (JSON / Config)

### JSON Keys
- Format: `snake_case`
- All lowercase
- No abbreviations unless the abbreviation is a known standard (e.g., `url`, `id`, `srt`)
- Correct: `video_length_minutes`, `project_slug`, `source_url`
- Incorrect: `videoLengthMinutes`, `projSlug`, `srcUrl`

### Boolean Fields
- Prefix with `is_` or `has_` to make boolean nature explicit
- Correct: `is_verified`, `has_sources`, `is_complete`
- Incorrect: `verified`, `sources`, `complete`

### Status Fields
- Use a `status` key with an enumerated string value
- Status values are `snake_case` strings
- Correct: `"status": "ready_for_production"`, `"status": "needs_revision"`
- Status enum for project assets: `pending` → `in_progress` → `complete` → `needs_revision` → `archived`

### Count Fields
- Suffix with `_count`: `word_count`, `image_count`, `scene_count`
- Never: `words`, `images`, `numScenes`

### Reference Fields (pointing to another entity)
- Suffix with `_id` for unique identifiers: `project_id`, `source_id`
- Suffix with `_slug` for human-readable identifiers: `project_slug`, `style_slug`

---

## Identifier Naming (Niche, Style, Language)

### Niche IDs

| Display Name | Canonical ID |
|---|---|
| Internet Mystery | `internet_mystery` |
| Japanese Mystery | `japanese_mystery` |
| Reddit Mystery | `reddit_mystery` |
| Google Maps Mystery | `google_maps_mystery` |
| Lost Places | `lost_places` |
| Unexplained Events | `unexplained_events` |

### Style IDs

| Display Name | Canonical ID |
|---|---|
| Dark Documentary | `dark_documentary` |
| Reddit Narration | `reddit_narration` |
| Mystery Investigation | `mystery_investigation` |
| Japanese Mystery | `japanese_mystery` |

### Language Codes
- Use ISO 639-1 two-letter codes exclusively
- Correct: `en`, `ja`, `vi`
- Incorrect: `english`, `Japanese`, `ENG`, `jpn`

---

## Engine and Component Naming

### Engine Identifiers (for logging, analytics, routing)
- Format: `[name]_engine`
- Matches the file name without `.md`
- Correct: `director_engine`, `qa_engine`, `memory_engine`

### Pipeline Stage IDs
- Format: `stage_NN` where NN is the zero-padded stage number
- Correct: `stage_01`, `stage_02`, `stage_10`
- Stage IDs correspond to prompt file indices

### Event Names (for logging and analytics)
- Format: `[engine].[action].[result]`
- All lowercase, dot-separated
- Correct: `qa_engine.validate.pass`, `workflow_engine.stage.complete`, `routing_engine.select.template`
- Incorrect: `QAPass`, `stageComplete`, `templateSelected`

---

## Version Naming

### System Version
- Format: `vMAJOR.MINOR`
- MAJOR: breaking change (new engine, removed component, schema change)
- MINOR: additive change (new template, new prompt, new config option)
- Correct: `v1.0`, `v1.3`, `v2.0`

### Prompt and Template Versions
- When a prompt is substantially revised, archive the old version:
  - Old: `01_research.md` → Rename to `01_research_v1.md`
  - New: `01_research.md` (always the active version)
- Version history is tracked in the file's own version history section, not by filename proliferation.

### Config Versions
- Config files include a `schema_version` field
- Bump on any structural change to the config schema

---

## Anti-Patterns (Explicitly Forbidden)

| Anti-Pattern | Why Forbidden |
|---|---|
| CamelCase file names (`ResearchPrompt.md`) | Inconsistent across OS filesystems; breaks agent lookups |
| Spaces in file names (`research prompt.md`) | Breaks shell commands and URL references |
| Numbered files without zero-padding (`1_research.md`) | Breaks alphabetical sort order at 10+ files |
| Abbreviations in keys (`vid_len_min`) | Unreadable for new agents with no context |
| Generic names (`output.md`, `data.json`) | Ambiguous — impossible to identify purpose without reading |
| Duplicate concepts with different names | Leads to agents using the wrong file |
| Status values as booleans (`"complete": true`) | Cannot express intermediate states |
