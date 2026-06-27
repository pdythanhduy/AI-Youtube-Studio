# Asset Library — AI YouTube Studio OS

Catalog of all images, audio, and text assets sourced or generated across all production projects. Prevents re-sourcing the same assets, tracks licensing, and enables reuse across multiple videos.

**Schema version:** 1.0
**Last updated:** [Updated automatically by Memory Engine]
**Asset count:** 0 (seed file — no projects completed yet)

---

## Schema Definition

### Image Asset Schema

| Field | Type | Required | Description |
|---|---|---|---|
| `asset_id` | string | yes | `img_YYYYMMDD_NNN` |
| `asset_type` | enum | yes | `real_photo`, `ai_generated`, `screenshot`, `stock`, `map`, `screen_recording` |
| `subject` | string | yes | What is depicted |
| `source_platform` | string | yes | Where it was sourced (for real) or generated (for AI) |
| `source_url` | string | no | Original URL (for real assets) |
| `license` | enum | yes | See License Enum |
| `attribution_required` | boolean | yes | Whether credit is required |
| `attribution_text` | string | no | Required credit text if attribution needed |
| `resolution` | string | no | e.g., `1920x1080` |
| `format` | string | no | `jpg`, `png`, `webp`, etc. |
| `projects_used_in` | string[] | yes | List of project slugs that used this asset |
| `times_used` | integer | yes | Count of project uses |
| `ai_prompt` | string | no | If ai_generated: the prompt used |
| `ai_model` | string | no | If ai_generated: which model/tool |
| `topics_associated` | string[] | yes | Topics this asset visually represents |
| `deprecated` | boolean | no | If true: asset URL is dead or asset no longer suitable |
| `notes` | string | no | Any special handling notes |

### AI Prompt Asset Schema

| Field | Type | Description |
|---|---|---|
| `prompt_id` | string | `prompt_YYYYMMDD_NNN` |
| `prompt_text` | string | Full generation prompt |
| `model_tool` | string | Midjourney / DALL-E / Stable Diffusion / etc. |
| `style` | string | Style profile this prompt was written for |
| `niche` | string | Niche this prompt was written for |
| `subject_concept` | string | What kind of scene this prompt generates |
| `qa_result` | enum | `approved` / `rejected` / `untested` |
| `projects_used_in` | string[] | Projects that used this prompt |
| `times_used` | integer | |
| `notes` | string | What worked, what didn't |

### Audio Asset Schema

| Field | Type | Description |
|---|---|---|
| `asset_id` | string | `aud_YYYYMMDD_NNN` |
| `asset_type` | enum | `music_track`, `sound_effect`, `voice_sample`, `tts_output` |
| `title` | string | Track or file name |
| `source_platform` | string | Where sourced |
| `source_url` | string | |
| `license` | enum | See License Enum |
| `duration_seconds` | integer | |
| `style_suitable_for` | string[] | Which style profiles this audio suits |
| `projects_used_in` | string[] | |
| `times_used` | integer | |
| `loudness_lufs` | float | Measured loudness (for mix consistency) |

### License Enum

| Value | Meaning | Commercial Use | Attribution |
|---|---|---|---|
| `public_domain` | No copyright | Yes | No |
| `cc0` | Creative Commons Zero | Yes | No |
| `cc_by` | CC Attribution | Yes | Yes |
| `cc_by_sa` | CC Attribution ShareAlike | Yes | Yes |
| `cc_by_nc` | CC NonCommercial | No | Yes |
| `stock_standard` | Paid stock license | Yes | No |
| `fair_use` | Editorial/commentary fair use | Limited | Recommended |
| `editorial_only` | News/documentary use only | No | Yes |
| `proprietary` | Custom license | Per agreement | Per agreement |
| `unknown` | License not determined | Do not use | — |

---

## Image Assets

*Populated automatically by Memory Engine.*

### Real Photos

| Asset ID | Subject | Source | License | Used In | Times Used |
|---|---|---|---|---|---|
| *No assets yet* | | | | | |

### AI Generated Images

| Asset ID | Subject Concept | Tool | Style | Prompt ID | Used In |
|---|---|---|---|---|---|
| *No assets yet* | | | | | |

### Screenshots

| Asset ID | Platform | Content | Date Captured | Used In |
|---|---|---|---|---|
| *No assets yet* | | | | |

### Maps and Satellite

| Asset ID | Location | Platform | Zoom Level | Coordinates | Used In |
|---|---|---|---|---|---|
| *No assets yet* | | | | | |

---

## AI Prompt Library

*Approved AI generation prompts that produced good results — catalogued for reuse.*

| Prompt ID | Concept | Style | Niche | Times Used | QA |
|---|---|---|---|---|---|
| *No prompts yet* | | | | | |

---

## Audio Assets

| Asset ID | Type | Title | Source | License | Style | Times Used |
|---|---|---|---|---|---|---|
| *No audio assets yet* | | | | | | |

---

## Reuse Guidelines

### When to Reuse an Asset

An asset from the library may be reused in a new project when:
- The asset depicts a generic concept (not a specific person, event, or date)
- The license permits reuse (public domain, CC0, CC BY, stock standard)
- The asset quality meets the current project's resolution requirements
- The asset has not been used in the immediately preceding 2 videos (avoid visual déjà vu)

### When NOT to Reuse an Asset

- The asset depicts a specific named individual — do not reuse in a different context
- The asset is a screenshot of a specific Reddit post — do not reuse for different topics
- The asset was used under fair use for commentary on a specific work — reuse in a different context may not qualify
- The asset quality is below `1920x1080` and the project requires high resolution

---

## Memory Engine Write Protocol

After every completed project, the Memory Engine:

1. Reads `image_plan.md` from the project
2. For each image in the plan:
   a. Check if asset already exists in the library (match by source URL for real assets)
   b. If match: increment `times_used`, add project to `projects_used_in`
   c. If new: create asset record with new `asset_id`
3. Reads `ai_image_prompts.md` from the project
4. For each AI prompt that was used and produced an approved image:
   a. Catalogue in AI Prompt Library
5. Updates all counts and statistics
6. Updates `last_updated` and `asset_count` in header
