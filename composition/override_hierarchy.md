# Override Hierarchy

## The Rule

When two profiles define the same field with different values, the higher-priority profile wins. Priority order, highest to lowest:

```
Level 0:  Safety / Legal Rules       ← ABSOLUTE. No exceptions. No override.
Level 1:  Creator Profile            ← Creator's identity and non-negotiables.
Level 2:  Platform Profile           ← Hard technical platform constraints.
Level 3:  Genre Template             ← Production language for this genre.
Level 4:  Audience Profile           ← Soft guidance for this audience tier.
```

---

## Level 0 — Safety and Legal Rules

**Source:** `creator_profile.absolute_rules`

These rules are not part of the override hierarchy — they are above it. No other profile can soften, override, or create an exception to a Safety or Legal rule.

If a Genre Template, Platform Profile, or Audience Profile requires behavior that violates a Safety or Legal rule, the composition system must:

1. Block the composition (set `composition_status: "blocked"`)
2. Log the conflict in `unresolved_conflicts` — not `override_log`
3. Require explicit human resolution before production continues

**Examples of Level 0 rules:**
- "Do not generate graphic imagery of violence, death, or abuse."
- "Do not invent facts, statistics, names, dates, or quotes."
- "Do not use CC BY-SA images in commercial video without legal review."

**`overridable_by` field:** Safety rules with `overridable_by: "nobody"` cannot be overridden even by the creator. Rules with `overridable_by: "creator_only"` may be suspended by the creator via a documented, explicit decision — not by any automated process.

---

## Level 1 — Creator Profile

**Source:** `profiles/creator/{creator_id}.json`

The creator's identity, values, and non-negotiable standards. This is the second authority after Safety/Legal.

Creator Profile fields override matching fields in Platform Profile, Genre Template, and Audience Profile.

**What Creator Profile owns:**
- Emotional goals and prohibited emotions
- Narrator persona and forbidden delivery styles
- Trust standards (trust_over_entertainment = true overrides genre hooks that feel manipulative)
- Quality standards (fact_checking_level, respect_standards)
- AI image maximum percentage (overrides genre_template.visual_style.ai_image_max_percent if stricter)
- Silence philosophy (overrides Genre Template if conflict)
- Music philosophy (overrides Genre Template music role if conflict)
- Signature narrative devices (end-of-video open question, etc.)
- Absolute rejection of specific styles (e.g., "never sensational")

**Example conflict:**
- Genre Template `thriller` specifies `music_language.role: "lead"` (music drives the emotional arc)
- Creator Profile specifies `music_philosophy: "music should never draw attention to itself"`
- **Resolution:** Creator Profile wins. Music role becomes `"support"` or `"ambient"`. Logged as OV001.

---

## Level 2 — Platform Profile

**Source:** `profiles/platform/{platform_id}.json`

Hard technical constraints and algorithmic requirements for the publishing platform. Platform Profile overrides Genre Template and Audience Profile but is overridden by Creator Profile.

**What Platform Profile owns:**
- Technical specs (resolution, aspect ratio, fps, duration limits, file format) — absolute, cannot be softened
- Hook critical window (e.g., YouTube Long Form = 30s, YouTube Shorts = 3s)
- Pacing override for platform-specific algorithm requirements
- Thumbnail dimensions and file constraints
- Metadata limits (title characters, tag count)
- Chapter marker rules
- End screen requirements

**Example conflict:**
- Genre Template `mystery` specifies `pacing.silence_usage: "frequent"` and `pacing.cut_frequency: "slow"`
- Platform Profile `youtube_shorts` specifies `pacing_override.max_silence_duration_seconds: 2` and `cut_frequency_guidance: "very_fast"`
- **Resolution:** Platform Profile wins on pacing. This conflict should also be flagged for human review if the creator is targeting both Long Form and Shorts with the same content.

**Note on technical specs:** Platform technical specs (resolution, aspect ratio, duration range) are never subject to the override hierarchy — they are hard requirements, not preferences. A video cannot be 16:9 AND 9:16 simultaneously. If the same content is targeted at multiple platforms, separate compositions must be generated.

---

## Level 3 — Genre Template

**Source:** `genre_templates/composed/{primary_genre}+{modifiers}.json` (composed output)

The production language for this genre. Defines how the video looks, moves, sounds, and is structured. Genre Template overrides Audience Profile but is overridden by Creator Profile and Platform Profile.

**What Genre Template owns:**
- Pacing arc structure (hook style, section flow, breath points)
- Camera language (shot types, motion directions, perspective rules)
- Editing language (transitions, color grade, motion graphics complexity)
- Music arc (intensity per section, silence ratio)
- Visual style (color tone, saturation, film grain)
- Motion grammar (default motion, emotional motion map)
- Scene grammar (required beats, section structure, scene duration rules)
- Thumbnail strategy
- Narrator guidance (genre-level tonal modes — overridden by Creator Profile persona)
- Forbidden elements

**Example conflict:**
- Audience Profile `beginner` specifies `language_profile.recap_frequency: "frequent"`
- Genre Template `mystery` specifies `scene_grammar.section_structure.required_sections` that doesn't include recap sections
- **Resolution:** Genre Template wins on structure. Recaps may be added within existing scenes but cannot create new required scene types not in the template.

---

## Level 4 — Audience Profile

**Source:** `profiles/audience/{audience_id}.json`

Soft guidance on vocabulary, explanation depth, pacing preference, and engagement strategy. Lowest priority — overridden by everything else. All Audience Profile rules are advisory unless no other profile addresses the same field.

**What Audience Profile owns (when not overridden):**
- Vocabulary level in scripts
- Explanation depth
- Assumed prior knowledge
- Analogy frequency
- Attention span model
- CTA style
- Self-contained video requirement

**Example — Audience Profile applies because no other profile conflicts:**
- Audience Profile `general` specifies `language_profile.vocabulary_level: "conversational"`
- No other profile defines vocabulary level
- **Resolution:** Audience Profile applies. Script should use conversational vocabulary.

---

## Quick Reference Table

| Scenario | Winner |
|---|---|
| Safety rule vs. Genre Template requirement | Safety rule (Level 0) |
| Safety rule vs. Creator Profile | Safety rule (Level 0) |
| Creator "never sensational" vs. Genre "strong hook" | Creator Profile (Level 1) |
| Creator "AI max 60%" vs. Genre "AI max 75%" | Creator Profile (Level 1) — stricter limit applies |
| Platform "max 60s" vs. Genre "12 min documentary" | Platform Profile (Level 2) — technical spec, absolute |
| Platform "very fast cuts" vs. Creator "no fast cuts" | Creator Profile (Level 1) — creator wins over platform |
| Genre "frequent silence" vs. Platform "max 2s silence" | Platform Profile (Level 2) — pacing override applies |
| Genre "slow recap sections" vs. Audience "fast pace" | Genre Template (Level 3) — structure wins over preference |
| No profile defines field X | First profile in hierarchy that defines it wins |
| No profile defines field X at any level | Field is null in effective_rules — flag for human input |
