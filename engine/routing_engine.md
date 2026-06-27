# Routing Engine — AI YouTube Studio OS

The Routing Engine selects the correct combination of prompt file, niche template, language profile, and style profile for each pipeline stage. It translates the parameters in `input.json` into a specific set of assets the Workflow Engine should use. No logic about what to produce lives here — only decisions about which tools to use to produce it.

---

## Responsibility

The Routing Engine answers a single question for every stage: **"Given this project's parameters, which exact files should the Workflow Engine use?"**

**Single sentence:** The Routing Engine is the dispatcher — it reads the request and selects the right team, tools, and instructions.

---

## Inputs

| Input | Source | Description |
|---|---|---|
| `input.json` | `projects/{slug}/` | `niche`, `style`, `language`, `video_length_minutes` |
| Stage ID | Director Engine | Which pipeline stage is being routed |
| `templates/` directory | `templates/` | Available niche templates |
| `configs/language_profiles.md` | `configs/` | Available language configurations |
| `configs/style_profiles.md` | `configs/` | Available style configurations |
| `configs/output_profiles.md` | `configs/` | Available output format configurations |

---

## Outputs

| Output | Destination | Description |
|---|---|---|
| Route resolution | Workflow Engine | Exact files to load for this stage + project |
| Route log entry | `projects/{slug}/run.log` | Which files were selected and why |

---

## Dependencies

| Dependency | Type | Purpose |
|---|---|---|
| Director Engine | upstream | Receives routing request from Director |
| Workflow Engine | downstream | Delivers route resolution to Workflow |
| `configs/` | reference | All configuration profiles |
| `templates/` | reference | All niche templates |

---

## Routing Resolution Process

For every stage dispatch, the Routing Engine resolves a **Route Object**:

```json
{
  "stage_id": "stage_04",
  "prompt_file": "prompts/04_script_writer.md",
  "template_file": "templates/mystery_template.md",
  "language_profile": "configs/language_profiles.md#en",
  "style_profile": "configs/style_profiles.md#dark_documentary",
  "output_profile": "configs/output_profiles.md#markdown_standard",
  "model_override": null,
  "context_files": [
    "projects/{slug}/input.json",
    "projects/{slug}/story_bible.md",
    "projects/{slug}/research_verified.md",
    "projects/{slug}/story_outline.md"
  ]
}
```

---

## Prompt File Selection

Prompt files are always selected by stage number. Stage-to-prompt mapping is fixed:

| Stage ID | Prompt File |
|---|---|
| stage_01 | `prompts/01_research.md` |
| stage_02 | `prompts/02_source_verifier.md` |
| stage_03 | `prompts/03_story_outline.md` |
| stage_04 | `prompts/04_script_writer.md` |
| stage_05 | `prompts/05_story_bible.md` |
| stage_06 | `prompts/06_scene_splitter.md` |
| stage_07 | `prompts/07_image_finder.md` |
| stage_08 | `prompts/08_image_prompt_generator.md` |
| stage_09 | `prompts/09_voice_director.md` |
| stage_10 | `prompts/10_youtube_seo.md` |

---

## Template Selection

Template is selected by `niche` from `input.json`:

| Niche ID | Template File |
|---|---|
| `internet_mystery` | `templates/mystery_template.md` |
| `unexplained_events` | `templates/mystery_template.md` |
| `lost_places` | `templates/mystery_template.md` |
| `japanese_mystery` | `templates/japan_template.md` |
| `reddit_mystery` | `templates/reddit_template.md` |
| `google_maps_mystery` | `templates/mystery_template.md` (+ map_addendum) |

**Fallback:** If no template matches the niche, use `templates/mystery_template.md` and log a routing warning.

**Map addendum:** For `google_maps_mystery`, inject an additional context block from `templates/mystery_template.md#map_section` regardless of which base template is selected.

---

## Language Profile Selection

Language profile is selected by ISO code from `input.json → language`:

| Language Code | Profile Section |
|---|---|
| `en` | `configs/language_profiles.md#en` |
| `ja` | `configs/language_profiles.md#ja` |
| `vi` | `configs/language_profiles.md#vi` |

**Fallback:** If language code is not in the supported list, halt with error: "Language `{code}` has no defined profile. Add a profile to configs/language_profiles.md before proceeding."

---

## Style Profile Selection

Style profile is selected by style ID from `input.json → style`:

| Style ID | Profile Section |
|---|---|
| `dark_documentary` | `configs/style_profiles.md#dark_documentary` |
| `reddit_narration` | `configs/style_profiles.md#reddit_narration` |
| `mystery_investigation` | `configs/style_profiles.md#mystery_investigation` |
| `japanese_mystery` | `configs/style_profiles.md#japanese_mystery` |

---

## Context File Selection (Per Stage)

The Routing Engine selects which project files to inject as context for each stage:

| Stage | Context Files (always) | Context Files (if exists) |
|---|---|---|
| stage_01 | `input.json` | — |
| stage_02 | `input.json`, `research.md` | — |
| stage_03 | `input.json`, `research_verified.md` | — |
| stage_04 | `input.json`, `research_verified.md`, `story_outline.md` | `story_bible.md` |
| stage_05 | `input.json`, `script.md`, `research_verified.md` | — |
| stage_06 | `input.json`, `script.md`, `story_bible.md` | — |
| stage_07 | `input.json`, `storyboard.md`, `story_bible.md` | — |
| stage_08 | `input.json`, `storyboard.md`, `image_plan.md`, `story_bible.md` | — |
| stage_09 | `input.json`, `script.md`, `story_bible.md`, `story_outline.md` | — |
| stage_10 | `input.json`, `script.md`, `research_verified.md`, `story_bible.md`, `story_outline.md` | — |

---

## Model Routing (Cost Optimization)

Different stages warrant different model capabilities. The Routing Engine applies this policy:

| Stage | Recommended Model | Reason |
|---|---|---|
| stage_01 (Research) | `claude-opus-4-8` | Requires deep knowledge retrieval |
| stage_02 (Source Verifier) | `claude-opus-4-8` | Requires critical judgment |
| stage_03 (Story Outline) | `claude-opus-4-8` | Requires narrative intelligence |
| stage_04 (Script Writer) | `claude-opus-4-8` | Core creative output |
| stage_05 (Story Bible) | `claude-sonnet-4-6` | Extraction task — less creative judgment needed |
| stage_06 (Scene Splitter) | `claude-sonnet-4-6` | Structured formatting task |
| stage_07 (Image Finder) | `claude-sonnet-4-6` | Lookup and categorization |
| stage_08 (Image Prompts) | `claude-opus-4-8` | Creative prompt writing |
| stage_09 (Voice Director) | `claude-opus-4-8` | Nuanced emotional direction |
| stage_10 (SEO) | `claude-sonnet-4-6` | Structured output, lower creativity required |

Model selection can be overridden via `configs/configuration_system.md → model_overrides`.

---

## Future Automation Points

| Point | Description |
|---|---|
| Dynamic template loading | New niche templates auto-discovered from `templates/` directory |
| A/B prompt routing | Route 50% of runs to prompt v1, 50% to prompt v2 — compare QA outcomes |
| User-defined routing rules | Config file allowing custom niche-to-template mappings without code changes |
| MCP tool integration | Routing Engine queries an MCP tool registry to include external tools |
| Cost-optimized routing | Routing Engine estimates cost per route and selects cheapest valid option |
