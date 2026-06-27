# Migration Notes
## hashima-island-mystery-ja → Composable Configuration Architecture
**Date:** 2026-06-27
**Phase:** 3 — Runtime Data Migration + Audit

---

## What Changed in Phase 3

### 1. Composed template `_composition_metadata` removed (Task 1)

The `_composition_metadata` block was removed from `genre_templates/composed/japan_mystery_lost_place.json`. This block would have failed strict `additionalProperties: false` schema validation. Metadata now lives canonically in the manifest file.

**No content impact. No rewrite required.**

### 2. Composition manifest created

`composition/manifests/japan_mystery_lost_place_manifest.json` is now the single source of truth for:
- Which profiles compose this template
- Source file list
- Effective limits
- Conflict summary
- Schema version

All projects using `japan_mystery_lost_place` should reference this manifest.

### 3. project.json updated

Seven new fields added to `projects/hashima-island-mystery-ja/data/project.json`:

```json
"creator_profile_id": "anh_duy",
"platform_profile_id": "youtube_long_form",
"audience_profile_id": "general",
"composition_manifest_id": "CM-2026-japan-mystery-lost-place",
"composed_template_id": "japan_mystery_lost_place",
"primary_genre": "mystery",
"modifiers": ["japan", "lost_place"]
```

No existing fields were modified.

### 4. Project composition/ directory created

Three new files created in `projects/hashima-island-mystery-ja/composition/`:
- `composition_audit_report.md` — full compliance audit
- `composition_compliance.json` — structured compliance data
- `migration_notes.md` (this file)

---

## Structural Alignment Notes

### ACT_IV vs ACT_III section naming

The composed template defines minimum required sections:
```
["HOOK", "ACT_I", "ACT_II", "ACT_III", "OUTRO"]
```

The Hashima project uses 6 sections:
```
["HOOK", "ACT_I", "ACT_II", "ACT_III", "ACT_IV", "OUTRO"]
```

**Mapping:**

| Project section | Template equivalent | Content |
|---|---|---|
| HOOK (0:00-1:00) | arc.hook | Atmospheric opening, title card |
| ACT_I (1:00-3:00) | arc.act_I | Cultural context, geography, Meiji era |
| ACT_II (3:00-6:00) | arc.act_II | Legend vs. reality, forced labor evidence |
| ACT_III (6:00-9:00) | arc.act_III* | Closure narrative, abandonment |
| ACT_IV (9:00-11:00) | arc.act_III (synthesis)** | UNESCO, Ma beat — the emotional synthesis |
| OUTRO (11:00-12:00) | arc.outro | Reflective close, open question |

*Template ACT_III combines what the project splits into ACT_III and ACT_IV.
**The project's ACT_IV contains BEAT_JPN_02 (Ma beat, 40s). The template maps this to ACT_III.

**Decision:** Accept the project's 6-section structure as a valid extension. Having more than the minimum sections is not a compliance violation. Do not rename sections — renaming would require updating all scene.json, story.json, voice.json cross-references.

### Beat compliance alignment

The project's legacy `template_compliance` block in story.json references the old japan_template's 4 beats:
```
["cultural_context", "legend_vs_reality", "japanese_silence", "ma_beat"]
```

The composed template requires 15 beats. All 15 beats are present in the project content — the project's 4-beat system was a subset of the full 15-beat system. The additional beats were always satisfied by the content; they just weren't explicitly tracked.

**COMP-019 (LOW):** story.json should have its `outline.template` field updated to reference the new system. This is bookkeeping only and can be done at any time.

---

## Metadata-Safe Fixes (Can Be Applied Without Content Review)

These fixes are pure metadata changes — they update field values to match what already exists in the visual/audio content. No regeneration required.

| Fix ID | File | Field | From | To |
|---|---|---|---|---|
| COMP-010 | scene.json | scenes[S001].motion_direction | "slow_pan_right" | "very_slow_pan_right" |
| COMP-019 | story.json | outline.template | "japan_template" | "japan_mystery_lost_place" |
| COMP-005 | seo.json | selected_title_id | null | "TITLE_A" |

These three fixes can be applied immediately without any human content review.

---

## Phase 4 Preview

Phase 4 will update the existing contracts (C01-C07) to reference the composition architecture. Key changes anticipated:

- C01 (narration contract) → reference narrator_guidance from composed template
- C03 (ma_beat contract) → reference BEAT_JPN_02 from composed template (already aligned)
- C07 (publish gate contract) → reference composition_manifest for compliance checks

No contracts were modified in Phase 3.

---

## What Was NOT Done in Phase 3

Per task specification:

- ❌ Did not rewrite the full project
- ❌ Did not regenerate research
- ❌ Did not regenerate script
- ❌ Did not regenerate visuals
- ❌ Did not generate images or audio
- ❌ Did not modify prompts or runtime modules
- ❌ Did not create new architecture documents
- ❌ Did not modify contracts (C01-C07)

Phase 3 was migration + audit only. All content fixes identified in the audit are documented as issues and deferred to the appropriate production phase.

---

## Files Created / Modified in Phase 3

| File | Action | Notes |
|---|---|---|
| `genre_templates/composed/japan_mystery_lost_place.json` | Modified | Removed `_composition_metadata` block |
| `composition/manifests/japan_mystery_lost_place_manifest.json` | Created | New manifest canonical file |
| `projects/hashima-island-mystery-ja/data/project.json` | Modified | Added 7 composition reference fields |
| `projects/hashima-island-mystery-ja/composition/composition_audit_report.md` | Created | Full compliance audit |
| `projects/hashima-island-mystery-ja/composition/composition_compliance.json` | Created | Structured compliance data |
| `projects/hashima-island-mystery-ja/composition/migration_notes.md` | Created | This file |
