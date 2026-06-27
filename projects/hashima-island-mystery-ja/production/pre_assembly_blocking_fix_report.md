# Pre-Assembly Blocking Fix Report
## hashima-island-mystery-ja
**Date:** 2026-06-28
**Stage:** 39 — Pre-Assembly Image Assignment Fix
**Blocking issue from:** Stage 38 Timeline Assembly Plan

---

## 1. Problem Statement

Stage 38 identified two blocking issues preventing NLE assembly:

| Scene | Duration | Timecode | Problem |
|-------|----------|----------|---------|
| S010 | 30s | 3:40–4:10 | `image_id_ref: null` in scene.json — no image assigned |
| S019 | 30s | 8:30–9:00 | `image_id_ref: null` in scene.json — no image assigned |

Image asset phase was previously declared complete (19 of 20 active images confirmed, IMG005 suppressed). These two null references were not caught during image QA because they had no image_id in image_plan.json — the gap existed at the scene.json level, not the image level.

---

## 2. Scene Inspection

### S010 — ACT_II — 3:40–4:10

| Field | Value |
|-------|-------|
| Duration | 30s |
| Shot type | close_up |
| Motion | slow_zoom_in |
| Section | ACT_II |
| Audio lines | L012 (sole line, spans S010→S011a) |
| PROMPT_ID | PROMPT_009 |
| Visual description | Urban explorer close-up. Grass growing through cracks in concrete. Dialogue between past and nature. Haikyo aesthetic. |
| Narration context | L012 is the ACT_II bridge narration between school interior (S009/IMG008) and mine tunnel (S011a/IMG009). It transitions viewer from civilian-life loss to forced-labor history. |
| Risk level | MEDIUM — no sensitive content; visual fills transitional ACT_II position |
| Why assignment missing | PROMPT_009 existed but no image was generated for this prompt during batch production. Batches were organized around approved prompts (Batch 1–3) and the concrete-crack close-up was deprioritized during queue cleanup. |
| Adjacent scenes | S009 (IMG008 school, 3:00–3:40), S011a (IMG009 mine tunnel, 4:10–4:40) |

### S019 — ACT_III — 8:30–9:00

| Field | Value |
|-------|-------|
| Duration | 30s |
| Shot type | extreme_close_up |
| Motion | static (spec'd in scene.json) |
| Section | ACT_III |
| Audio lines | L024, L025, L026 |
| PROMPT_ID | PROMPT_016 (also shared with S020/IMG016) |
| Visual description | Macro concrete texture. Cracks, moss, rust. Near-abstract composition. Expresses 'slowly, quietly disappearing.' Two [PAUSE:2s] events fall on this scene. |
| Narration context | L024/L025 are reflective late ACT_III lines. L026 is an editor 2s pause. Scene purpose is contemplative transition from S018 storm ruins to S020 dusk island wide. |
| Risk level | LOW — no sensitive content; abstract macro texture scene |
| Why assignment missing | PROMPT_016 is referenced by both S019 and S020. IMG016 (dusk island wide) was generated for S020. S019's distinct "macro texture" visual was never generated — both scenes shared a PROMPT reference but needed different image outputs. The data inconsistency was not flagged during batch QA. |
| Adjacent scenes | S018 (IMG015 storm ruins, 8:00–8:30), S020 (IMG016 dusk island, 9:00–9:40) |

---

## 3. Available Asset Review

| Image | Current Scene | Character | Gap to S010 | Gap to S019 |
|-------|--------------|-----------|-------------|-------------|
| IMG003 | S003 (0:25–0:40) | Close-up wooden door, vines/ivy, decayed texture | 3:00 min | 8:05 min |
| IMG010 | S011b (4:40–5:00) | Extreme close-up coal/shale rock macro, pure texture | 0:30 min before | 3:30 min |
| IMG002 | S002 (0:10–0:25) | Medium concrete corridor, light shafts | 3:15 min | 8:05 min |
| IMG008 | S009 (3:00–3:40) | School interior | 0s (ADJACENT) | N/A |
| IMG015 | S018 (8:00–8:30) | Storm ruins, wide | N/A | 0s (ADJACENT) |
| IMG017 | S021 (9:40–10:20) | Heritage plaque close-up | N/A | opposite end |

**Rule:** Do not reuse if too close or creates obvious repetition. IMG008 is adjacent to S010 (eliminated). IMG015 is adjacent to S019 (eliminated). All others evaluated on gap + visual fit.

---

## 4. Decisions

### S010 — DECISION B: IMG003, alternate crop

**Assigned image:** IMG003  
**File:** `assets/ai_images/generated/batch_1/IMG003_S003_wooden_door_closeup.png`  
**Assignment type:** REUSE — alternate crop, different motion, different color treatment

**Rationale:**
- S010 visual spec: "grass growing through cracks in concrete / haikyo aesthetic" — organic growth on ruins
- IMG003: decayed wooden door with ivy/vines growing on concrete surround — same thematic territory (organic growth on ruins)
- 3-minute gap from S003 (0:25–0:40) is sufficient for reuse without obvious repetition
- Motion differentiation: S003 = static hold; S010 = slow_zoom_in — editor will zoom into the ivy/vine corner rather than centering on door
- Crop instruction: frame toward the concrete wall + vines intersection (upper-left and right edges of the door image where ivy meets raw concrete), NOT the center door panel
- Color: apply slightly more desaturation and +10% contrast to distinguish from S003's warm-neutral treatment
- Contextual fit: S010 sits between school interior (institutional loss) and mine tunnel (forced labor). A vine-through-ruins texture signals the slow, organic erasure of human presence — directly aligned with the haikyo aesthetic
- Risk: ACCEPTABLE — different crop section, different motion, 3-minute gap, same thematic register

**Eliminated alternatives:**
- IMG010: Only 30 seconds after S010 in S011b → visual repetition too close
- IMG008: Directly adjacent (S009) — eliminated
- IMG002: Concrete corridor is medium shot, not close-up; haikyo-specific organic growth not present

---

### S019 — DECISION B: IMG010, alternate crop

**Assigned image:** IMG010  
**File:** `assets/ai_images/generated/batch_1/IMG010_S011b_mine_rock_texture.png`  
**Assignment type:** REUSE — alternate crop, different motion, adjusted color treatment

**Rationale:**
- S019 visual spec: "macro concrete texture, cracks, moss, rust, near-abstract" — the only fully abstract/macro texture image in the library is IMG010
- IMG010: coal/shale macro — pure mineral texture, zero human-coded shapes, extremely close and abstract; QA approved it as "pure coal/shale macro"
- 3:30 gap from S011b (4:40–5:00) to S019 (8:30–9:00) is the largest gap available for any reuse candidate
- Motion differentiation: S011b = slow_zoom_in; S019 = static (per scene.json spec) — visually distinct
- Crop instruction: frame to moss/mineral surface edges — highlight green-grey surface growth and rust-orange oxidation streaks rather than coal-black center. The rock surface has natural color variation that reads as "concrete with moss and rust" under post-processing
- Color: warm +15° color shift to pull orange/rust tones; desaturate the deepest blacks; this transforms the "cold coal mine" read into "aged concrete/rust" read consistent with S019's abstract contemplative intent
- Contextual fit: S019 is the penultimate contemplative scene before ACT IV. The macro texture places the viewer in intimate, abstract relationship with the material of the island. Mineral texture reads as timeless decay — appropriate for "slowly, quietly disappearing"
- The two [PAUSE:2s] events (L026) that land in S019 benefit from a static, near-abstract image that doesn't demand visual decoding
- Risk: ACCEPTABLE — 3:30 minute gap, different motion (static vs. zoom), color shift creates distinct visual character from the dark cold mine use in S011b

**Eliminated alternatives:**
- IMG003: Wooden/vine character doesn't align with "macro concrete/rust" spec
- IMG002: Medium shot (not extreme close-up); too narrative for an abstract texture role
- IMG015: Directly adjacent (S018) — eliminated

---

## 5. New Image Generation Status

**No new image generation required.** Both gaps are resolved with existing approved assets using alternate crop and treatment.

This decision preserves:
- The "no new image generation" constraint
- The image asset phase "complete" status (19 active images remain; dual-use does not add or remove an image)
- The AI% ceiling (75% — unchanged; no new AI images)

---

## 6. AI Percentage Impact

| Metric | Before fix | After fix |
|--------|-----------|-----------|
| Active images | 19 | 19 (unchanged) |
| AI_GENERATE | 15 | 15 (unchanged) |
| REAL_PHOTO_LICENSED | 2 | 2 (unchanged) |
| MOTION_GRAPHICS | 4 | 4 (unchanged) |
| AI% | 75% | 75% (unchanged) |
| New images generated | — | 0 |

---

## 7. Updated Scene Assignments

| Scene | Timecode | Image ID | File | Assignment Type | Motion | Crop Note |
|-------|----------|----------|------|-----------------|--------|-----------|
| S010 | 3:40–4:10 | IMG003 | `batch_1/IMG003_S003_wooden_door_closeup.png` | REUSE — alternate crop | slow_zoom_in | Crop to vines/concrete edge, not door center |
| S019 | 8:30–9:00 | IMG010 | `batch_1/IMG010_S011b_mine_rock_texture.png` | REUSE — alternate crop | static | Crop to moss/rust surface, warm color shift |

---

## 8. Dual-Use Image Registry

### IMG003 — now assigned to S003 AND S010

| Use | Scene | Timecode | Motion | Crop |
|-----|-------|----------|--------|------|
| Primary | S003 | 0:25–0:40 | static | Full door center — peeling paint, vines |
| Secondary | S010 | 3:40–4:10 | slow_zoom_in | Vines/concrete edge crop — de-emphasize door panel |

Gap between uses: 3:00 minutes. Motion and crop differentiate the two appearances.

### IMG010 — now assigned to S011b AND S019

| Use | Scene | Timecode | Motion | Crop/Color |
|-----|-------|----------|--------|-----------|
| Primary | S011b | 4:40–5:00 | slow_zoom_in | Dark coal/shale, cold color grade |
| Secondary | S019 | 8:30–9:00 | static | Moss/rust surface crop, +15° warm shift, +15% rust desaturation |

Gap between uses: 3:30 minutes. Motion, crop, and color treatment differentiate the two appearances.

---

## 9. Timeline Assembly Blocker Status

| Gate | Before | After |
|------|--------|-------|
| S010 image assigned | 🔴 BLOCKED | ✅ RESOLVED — IMG003 |
| S019 image assigned | 🔴 BLOCKED | ✅ RESOLVED — IMG010 |
| All other images confirmed | ✅ PASS | ✅ PASS (unchanged) |

**Timeline assembly blocker: CLEARED.**

Remaining pre-assembly actions (not blocking, proceed in parallel with rough assembly):
- IMG009 human producer review (S011a)
- Post-processing: IMG002, IMG004 (caption), IMG008, IMG011, IMG016
- Human listen: L001, L003, L008, L013, L014, L028
- Sensitive content review: L013–L016 (COMP-007)

---

## 10. Exact Next Action

**Timeline assembly may now BEGIN.**

Editor instructions:
1. Use timecodes in `timeline/timeline_assembly_plan.md` and `data/timeline_assembly_plan.json`
2. For S010 (3:40–4:10): import `IMG003_S003_wooden_door_closeup.png`, apply slow_zoom_in, crop to vine/concrete edge section, darker grade
3. For S019 (8:30–9:00): import `IMG010_S011b_mine_rock_texture.png`, apply static hold, crop to moss/rust surface, warm color shift (+15°), desaturate black
4. L008 clip at sec=157 (2:37) — mark before assembly
5. L028 clip at sec=575 (9:35) — mark before assembly
6. Narration track empty at sec=620–660 (10:20–11:00 Ma beat) — enforce before any render

---

*Pre-Assembly Blocking Fix Report — Stage 39 — hashima-island-mystery-ja — 2026-06-28*
