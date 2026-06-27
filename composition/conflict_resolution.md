# Conflict Resolution

## Definition

A conflict occurs when two or more profiles define the same effective_rules field with incompatible values.

There are four conflict types. Each requires a different resolution approach.

---

## Conflict Type A — Same Field, Different Values (Resolvable)

**Definition:** Two profiles define the same field, and one has higher priority than the other.

**Resolution process:**
1. Apply the override hierarchy from `override_hierarchy.md`
2. The higher-priority profile's value becomes the effective value
3. Log the conflict in `override_log`
4. Continue composition

**Log entry format:**
```json
{
  "conflict_id": "OV001",
  "field": "music_language.role",
  "winner": "creator_profile",
  "winner_value": "support",
  "loser": "genre_template",
  "loser_value": "lead",
  "resolution": "higher_priority_wins"
}
```

**Common Type A conflicts:**

| Field | Likely Winner | Notes |
|---|---|---|
| `pacing.cut_frequency` | Platform or Creator | Platform wins if Shorts; Creator wins if philosophical |
| `visual_style.ai_image_max_percent` | Creator Profile | Always apply the stricter (lower) limit |
| `music_language.role` | Creator Profile | Creator music philosophy overrides genre default |
| `pacing.silence_usage` | Creator Profile | Silence as storytelling tool = creator core value |
| `narrator_guidance.tonal_modes` | Creator Profile | Narrator persona is a creator identity decision |
| `editing_language.color_grade` | Genre Template | Creator may not have specified; genre wins |
| `scene_grammar.required_beats` | Genre Template | Structural grammar is genre-owned |
| `language_profile.vocabulary_level` | Audience Profile | No other profile typically owns vocabulary |

---

## Conflict Type B — One Profile Defines a Field, Another Does Not

**Definition:** Only one profile in the hierarchy defines a field. No conflict — that profile wins by default.

**Resolution process:**
1. The defining profile's value is used
2. No log entry required — this is not a conflict

**Example:**
- `visual_style.film_grain` is defined in Genre Template as `true`
- Creator Profile, Platform Profile, and Audience Profile do not define `film_grain`
- Effective value: `true` (from Genre Template)
- No override log entry

**Edge case — field not defined by any profile:**
- Effective value: `null`
- Flag in `effective_rules` with a comment: `"_source": "undefined — requires human input"`
- Production system should surface these nulls to the human before starting

---

## Conflict Type C — Logical Contradiction (Requires Human Review)

**Definition:** Two profiles define the same field with values that cannot be merged by priority alone — because the conflict implies a fundamental production decision the composition system cannot make.

**Examples:**

| Conflict | Why Unresolvable by Priority |
|---|---|
| Creator "must feel cinematic and slow" + Platform "YouTube Shorts, max 60s, very fast cuts" | Even if Creator wins on cut frequency, the 60s limit transforms the entire production model. Human must decide: skip Shorts, make a special Shorts version, or accept the tradeoff. |
| Genre Template "requires 40-second Ma beat" + Platform "max silence: 2s" | Platform pacing override vs. genre structural requirement. 40s silence violates platform constraint. Cannot apply both. |
| Genre "real footage strongly preferred" + Creator "AI max 60%" + Platform Shorts "requires 15+ cuts/min at high visual variety" | The combination makes real footage impractical at Shorts pace. |

**Resolution process:**
1. Do not attempt to auto-resolve
2. Add entry to `unresolved_conflicts` (not `override_log`)
3. Set `composition_status: "partial_unresolved_conflicts"`
4. Block production until human resolves
5. Provide `resolution_options` array with concrete options the human can choose

**Unresolved conflict entry format:**
```json
{
  "conflict_id": "UC001",
  "field": "pacing.silence_usage + platform.pacing_override.max_silence_duration_seconds",
  "profile_a": "genre_template",
  "value_a": "40-second Ma beat (required beat)",
  "profile_b": "platform_profile",
  "value_b": "max_silence_duration_seconds: 2",
  "reason_unresolvable": "Genre requires 40s silence beat. Platform algorithm penalizes silence over 2s. These cannot coexist in the same cut.",
  "resolution_options": [
    "Exclude this video from YouTube Shorts distribution",
    "Create a separate Shorts version without the Ma beat",
    "Override platform pacing rule for this specific genre (accept algorithmic penalty)"
  ]
}
```

---

## Conflict Type D — Safety or Legal Violation (Blocks Composition)

**Definition:** A Genre Template, Platform Profile, or Audience Profile requires behavior that violates a Safety or Legal rule from the Creator Profile.

**Examples:**

| Violation | Triggered By |
|---|---|
| Genre Template requires AI-generated image of a real historical person | SR001 (no graphic content) + ER001 (no speculation about real individuals) |
| Platform requires a 3-second "shock" opening with violence | SR002 (no graphic violence) |
| Genre modifier requires claiming unverified death statistics as fact | SR003 (do not invent statistics) |

**Resolution process:**
1. Immediately halt composition
2. Set `composition_status: "blocked"`
3. Add to `unresolved_conflicts` with severity `CRITICAL`
4. Do not generate a partial `effective_rules`
5. Require explicit human decision + documented exception before resuming

**A blocked composition must NEVER proceed to production automatically.**

---

## Special Resolution Rules

### The Stricter Limit Rule
When two profiles define a numeric limit (maximum or minimum) for the same field, always apply the stricter value regardless of hierarchy. This applies specifically to:
- `ai_image_max_percent` — use the lower of Creator Profile vs. Genre Template
- `duration_range_seconds` — use the intersection of Creator and Platform ranges
- `text_complexity_max` — use the simpler of Creator and Audience

Rationale: a limit exists to protect a constraint. The constraint is not protected if a lower-priority profile can relax it.

### The Additive Rule
Some fields are not in conflict even when defined by multiple profiles — they are additive. These should be merged (union), not overridden:
- `absolute_rules.safety_rules` + any modifier safety rules → union of all
- `scene_grammar.required_beats` from base template + modifier beats → union (duplicates removed)
- `camera_language.forbidden_shot_types` from Creator + Genre → union (both apply)
- `forbidden_elements` from any profile → union (all apply)

### The Precedence Note Rule
When a high-priority profile overrides a Genre Template field that carries editorial meaning (e.g., Creator overrides a required scene type), add a human-readable note to the `override_log` entry explaining what production implication this has. Do not silently remove required beats.
