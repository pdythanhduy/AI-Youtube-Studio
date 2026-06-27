# Template Inheritance

## Purpose

Template inheritance prevents duplication across Genre Templates. Rules shared by all documentaries should be defined once in the `documentary` base template — not copied into `mystery`, `history`, `science`, and every other subtype.

---

## Folder Structure and Template Types

```
genre_templates/
  base/           ← Root templates. Define the full template surface.
  modifiers/      ← Additive layers. Inherit from a base, override specific fields.
  composed/       ← Auto-generated. The merged output of base + modifiers.
                    Do not author these manually.
```

---

## Template Type Hierarchy

### Level 1: Base Templates (`genre_templates/base/`)

Base templates are the root of the inheritance tree. They must define every field in `genre_template.schema.json`, either with a concrete value or an explicit `null` meaning "undefined, will be specified by modifier or human."

A base template is both the genre root AND a usable template on its own. A video with `primary_genre: "documentary"` and no modifiers uses the `documentary` base template directly.

**Initial base templates to author (Phase 2):**

| template_id | description |
|---|---|
| `documentary` | Cinematic non-fiction. Root for most channel content. |
| `educational` | Explanation-first content with heavy text on screen. |
| `short_form` | Fast-paced vertical video. Root for all Shorts/TikTok content. |

### Level 2: Primary Genre Templates (`genre_templates/base/`)

Primary genre templates also live in `base/` but use `inherits_from: "documentary"` (or whichever root applies). They define genre-specific rules and inherit everything else from their parent.

**Initial primary genre templates to author (Phase 2):**

| template_id | inherits_from | description |
|---|---|---|
| `mystery` | `documentary` | Suspense and curiosity arc. Hook-forward structure. |
| `history` | `documentary` | Historical accuracy and source citation emphasis. |
| `science` | `educational` | Explanation depth, data visualization. |
| `true_crime` | `documentary` | Stricter safety rules, respect standards. |

### Level 3: Modifier Templates (`genre_templates/modifiers/`)

Modifiers are additive layers applied on top of the composed primary genre. A modifier only defines what it changes — everything else inherits.

**Initial modifiers to author (Phase 2):**

| template_id | applicable_to | description |
|---|---|---|
| `japan` | `mystery`, `history`, `documentary` | Ma beat, desu_masu register, Japanese pronunciation rules, slower pacing. |
| `lost_place` | `mystery`, `history` | Abandonment visual language, decay aesthetic, contemplative framing. |
| `historical_period` | `history`, `mystery` | Historical photo integration rules, archival visual grammar. |
| `unsolved` | `mystery`, `true_crime` | Structural open ending, explicit uncertainty language, one unanswered question required. |

---

## Inheritance Resolution Rules

### Rule 1: Null means "inherit from parent"

In a modifier template, a field set to `null` means "take the value from the base template." A field that is explicitly set (even to a non-null value) means "override the parent."

This distinction matters: a modifier that wants to explicitly clear a field must use a sentinel value like `"none"` or `[]` rather than `null`.

**Example:**
```json
// In base template 'documentary':
"pacing": {
  "silence_usage": "deliberate"
}

// In modifier 'japan':
"pacing": {
  "silence_usage": "frequent"   // ← overrides 'deliberate' with 'frequent'
}

// In modifier 'lost_place':
"pacing": {
  "silence_usage": null          // ← inherits 'deliberate' from documentary
}
```

### Rule 2: Additive fields merge, they do not override

Certain fields are always additive regardless of inheritance level:
- `scene_grammar.required_beats` — union of base beats + modifier beats
- `scene_grammar.section_structure.required_sections` — union
- `camera_language.forbidden_shot_types` — union
- `forbidden_elements` — union
- `narrator_guidance.forbidden_delivery_styles` — union

A modifier cannot remove a required beat from the base template. It can only add new required beats.

To remove a base template's required beat, the modifier must escalate to a human conflict (Type C) with a documented editorial reason.

### Rule 3: Modifiers are applied in order

When multiple modifiers are stacked, they are applied sequentially. The last modifier in the list has the highest modifier priority (within the modifier layer).

```
Composition order:
1. Base template ('documentary')      → sets all defaults
2. Primary genre ('mystery')          → overrides genre-specific fields
3. Modifier[0] ('japan')             → overrides japan-specific fields
4. Modifier[1] ('lost_place')        → overrides lost_place-specific fields
```

If `japan` and `lost_place` both define `pacing.silence_usage`, `lost_place` wins (applied later).

### Rule 4: Composed templates are generated, not authored

The `genre_templates/composed/` folder contains the output of the composition engine after merging base + all modifiers. These files are:
- Named: `{primary_genre}+{modifier1}+{modifier2}.json`
- Generated at composition time by `profile_composer`
- Read-only for humans (do not edit manually)
- Cached by `composition_hash` — regenerated when any source template changes

---

## Inheritance Example: `mystery` + `japan` + `lost_place`

```
Input:
  primary_genre: "mystery"
  modifiers: ["japan", "lost_place"]

Step 1 — Start with 'documentary' base:
  pacing.silence_usage = "deliberate"
  pacing.cut_frequency = "moderate"
  visual_style.color_grade = "natural"
  scene_grammar.required_beats = ["hook", "context", "revelation", "resolution"]

Step 2 — Apply 'mystery' (inherits from documentary):
  pacing.hook_style = "question"           ← mystery adds this
  pacing.cut_frequency = "moderate"        ← inherits from documentary (null)
  scene_grammar.required_beats += ["open_question_ending"]   ← mystery adds this

Step 3 — Apply modifier 'japan':
  pacing.silence_usage = "frequent"        ← overrides 'deliberate'
  pacing.cut_frequency = "slow"            ← overrides 'moderate'
  visual_style.color_grade = null          ← inherits from mystery/documentary: 'natural'
  scene_grammar.required_beats += ["cultural_context", "ma_beat"]  ← japan adds these
  narrator_guidance.tonal_modes.history = "respectful and restrained"  ← japan adds

Step 4 — Apply modifier 'lost_place':
  visual_style.color_grade = "dark_documentary"  ← overrides 'natural'
  visual_style.saturation = "desaturated"        ← overrides (documentary default: neutral)
  visual_style.film_grain = true                 ← overrides (documentary default: false)
  scene_grammar.required_beats += ["contemplative_exterior_shot"]  ← lost_place adds

Final composed output:
  pacing.silence_usage = "frequent"        (from japan)
  pacing.cut_frequency = "slow"            (from japan)
  visual_style.color_grade = "dark_documentary"   (from lost_place)
  visual_style.saturation = "desaturated"  (from lost_place)
  visual_style.film_grain = true           (from lost_place)
  scene_grammar.required_beats = [
    "hook",                          (from documentary)
    "context",                       (from documentary)
    "revelation",                    (from documentary)
    "resolution",                    (from documentary)
    "open_question_ending",          (from mystery)
    "cultural_context",              (from japan)
    "ma_beat",                       (from japan)
    "contemplative_exterior_shot"    (from lost_place)
  ]
```

---

## Authoring Guidelines for New Templates

**For a new base template:**
- Define every field. Use `null` only for fields that genuinely have no default.
- Write `description` fields. Humans need to understand these templates.
- Do not embed project-specific values. Base templates are reusable across all projects.

**For a new modifier:**
- Define only what changes. Do not copy fields from the base.
- Specify `inherits_from` and `applicable_primary_genres`.
- If a modifier adds a required beat, document the beat in `scene_grammar.required_beats` with a full description.
- If a modifier needs to restrict something from the base, prefer `forbidden_elements` over removing base fields.

**Naming convention:**
- Use lowercase snake_case: `japan`, `lost_place`, `historical_period`
- Be descriptive but short: a modifier named `slow_reflective_japan_mystery` is too specific — split into `japan` + `slow_reflective` modifiers
