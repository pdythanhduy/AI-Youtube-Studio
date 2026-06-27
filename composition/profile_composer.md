# Profile Composer

## Purpose

The Profile Composer is the process that takes four independent profile inputs and produces one `composition_manifest.json` — the single source of truth for all production decisions on a video.

Input:
```
Creator Profile   (profiles/creator/{id}.json)
Primary Genre     (genre_templates/base/{primary_genre}.json)
Modifiers         (genre_templates/modifiers/{modifier}.json × N)
Platform Profile  (profiles/platform/{platform_id}.json)
Audience Profile  (profiles/audience/{audience_id}.json)
```

Output:
```
composition_manifest.json
genre_templates/composed/{primary_genre}+{modifiers}.json
```

---

## Step-by-Step Process

### Step 0 — Validate Inputs

Before composing, verify:

- [ ] Creator Profile exists and `profile_status = "active"`
- [ ] Primary Genre template exists in `genre_templates/base/`
- [ ] Each modifier exists in `genre_templates/modifiers/`
- [ ] Each modifier's `applicable_primary_genres` includes the primary genre (or is empty = compatible with all)
- [ ] Platform Profile exists in `profiles/platform/`
- [ ] Audience Profile exists in `profiles/audience/`
- [ ] All profiles have valid `schema_version` fields

If any input is missing or invalid: stop and report. Do not compose a partial manifest.

---

### Step 1 — Compose the Genre Template

This step produces the composed genre template that represents the merged production language.

**1a. Start with the base template.**

Load `genre_templates/base/{primary_genre}.json`.

If `primary_genre` has an `inherits_from` field (meaning it is itself a secondary genre inheriting from a root), resolve the full inheritance chain first:
```
documentary → mystery
```
Apply inheritance rules from `template_inheritance.md`. The result is the fully resolved primary genre template with all base values populated.

**1b. Apply each modifier in order.**

For each modifier in `genre_modifiers` (left to right):
1. Load `genre_templates/modifiers/{modifier_id}.json`
2. For each field defined (non-null) in the modifier: override the current composed value
3. For additive fields (required_beats, forbidden_elements, forbidden_shot_types): union, do not override
4. Track which modifier last set each field

**1c. Write the composed template.**

Save to `genre_templates/composed/{primary_genre}+{modifier1}+{modifier2}.json`.

This file is the composed genre template used in Step 3.

---

### Step 2 — Extract Safety and Legal Rules

Load all `absolute_rules` from the Creator Profile:
- `safety_rules`
- `legal_rules`
- `ethical_rules`

These are copied verbatim into `effective_rules.absolute_rules`. They do not participate in the override hierarchy — they are applied before it.

Hold this set as the **blocking set**. Any value in any other profile that violates a rule in this set triggers a Type D conflict (see `conflict_resolution.md`).

---

### Step 3 — Build Effective Rules by Field

For each field in the `effective_rules` schema, apply the following resolution process:

```
1. Check if the field violates any Safety/Legal rule → Type D conflict if yes
2. Collect all values defined for this field across:
      creator_profile, platform_profile, composed_genre_template, audience_profile
3. If only one profile defines the field → use that value (no conflict)
4. If multiple profiles define the field with the SAME value → use that value (no conflict)
5. If multiple profiles define the field with DIFFERENT values:
      a. Identify the highest-priority profile per override_hierarchy.md
      b. Check if this is a logical contradiction → Type C conflict if yes
      c. Otherwise → Type A resolution: higher priority wins, log in override_log
6. Apply Stricter Limit Rule for numeric limits (use the most restrictive)
7. Apply Additive Rule for additive fields (union, not override)
```

Repeat for every field. When complete, every field in `effective_rules` must have either:
- A resolved value (from one of the profiles)
- A `null` with a `_source: "undefined"` annotation flagged for human input

---

### Step 4 — Classify and Log Conflicts

After Step 3, categorize all conflicts detected:

**Type A** (higher priority wins) → Add to `override_log`. Continue.

**Type B** (only one profile defines the field) → No log entry. Continue.

**Type C** (logical contradiction) → Add to `unresolved_conflicts`. Set `composition_status: "partial_unresolved_conflicts"`. Continue composing other fields but flag these for human review.

**Type D** (safety/legal violation) → Add to `unresolved_conflicts` with severity `CRITICAL`. Set `composition_status: "blocked"`. Stop composition. Do not proceed to Step 5.

---

### Step 5 — Set Composition Status

After all fields are resolved and all conflicts are classified:

```
If any Type D conflicts exist:
    composition_status = "blocked"
    Do not proceed to production. Require human resolution.

Else if any Type C conflicts (unresolved) exist:
    composition_status = "partial_unresolved_conflicts"
    Surface to human for review. Production may begin on resolved fields
    but blocked fields must be resolved before those production stages.

Else:
    composition_status = "complete"
    Ready for production.
```

---

### Step 6 — Generate the Manifest

Assemble the `composition_manifest.json`:

```json
{
  "manifest_id": "CM{YEAR}-{project_id}",
  "project_id": "{project_id}",
  "creator_profile_id": "{id}",
  "platform_profile_id": "{id}",
  "audience_profile_id": "{id}",
  "primary_genre": "{id}",
  "genre_modifiers": ["{id}", "..."],
  "composed_at": "{ISO timestamp}",
  "profile_versions": { ... },
  "composition_hash": "{hash of all input version strings}",
  "override_log": [ ... ],
  "unresolved_conflicts": [ ... ],
  "effective_rules": { ... },
  "composition_status": "complete | partial_unresolved_conflicts | blocked"
}
```

Save to `projects/{project_id}/composition_manifest.json`.

---

### Step 7 — Deliver to Production

Once `composition_status = "complete"`, the `effective_rules` object in the manifest is the **single source of truth** for:

| Production Stage | References |
|---|---|
| Script writing | `effective_rules.scene_grammar`, `narrator_guidance`, `pacing` |
| Image planning | `effective_rules.visual_style`, `camera_language` |
| Motion assignment | `effective_rules.motion_grammar`, `camera_language.preferred_motion_directions` |
| AI image prompting | `effective_rules.visual_style.color_grade`, `ai_image_max_percent` |
| Voice direction | `effective_rules.narrator_guidance` |
| Music selection | `effective_rules.music_language` |
| Editing | `effective_rules.editing_language`, `pacing` |
| Thumbnail | `effective_rules.thumbnail_strategy` |
| SEO | `effective_rules.platform_constraints` |

The runtime data model documents (`scene.json`, `story.json`, etc.) should reference the manifest via `composition_manifest_id` so any reviewer can trace why a production decision was made.

---

## Recomposition

If any input profile changes after a manifest is generated, the manifest becomes stale. The composition system detects this by comparing the current `composition_hash` against a fresh hash of all input profile versions.

**When to recompose:**
- Creator Profile is updated (new interview data, changed values)
- A Genre Template is revised
- The target platform changes
- The target audience changes
- A new modifier is added to the project

**Recomposition is non-destructive:** the new manifest is saved alongside (or replaces) the old one. The runtime data model documents are not automatically updated — a human reviews the diff between old and new `effective_rules` and decides which production stages need to be revisited.

---

## Example: Hashima Island Project

```
Creator:    profiles/creator/channel-v1.json
Platform:   profiles/platform/youtube_long_form.json
Audience:   profiles/audience/general.json
Genre:      genre_templates/base/mystery.json (inherits: documentary)
Modifiers:  genre_templates/modifiers/japan.json
            genre_templates/modifiers/lost_place.json
            genre_templates/modifiers/historical_period.json

Composed genre: genre_templates/composed/mystery+japan+lost_place+historical_period.json
Manifest:       projects/hashima-island-mystery-ja/composition_manifest.json
```
