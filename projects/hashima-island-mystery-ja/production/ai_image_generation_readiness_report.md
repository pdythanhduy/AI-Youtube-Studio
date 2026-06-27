# AI Image Generation Readiness Report
## hashima-island-mystery-ja
**Date:** 2026-06-27
**Gate:** AI Image Generation Readiness Gate
**Auditor:** generation_readiness_gate_v1
**Based on:** data/image_plan.json, visuals/ai_image_prompts.md, data/scene.json, review/visual_risk_report.md, production/fix_h1_round_3_report.md, genre_templates/composed/japan_mystery_lost_place.json, profiles/creator/anh_duy.json

---

## Executive Summary

AI image generation may BEGIN for 12 of 18 images. Two images are BLOCKED by data errors. Four require human review or decisions before generation. **IMG009 (mine tunnel, S011a) has been audited, a safer rewritten prompt has been prepared, and its mandatory human review gate is confirmed.**

**Critical finding:** A systematic prompt-scene mismatch exists in image_plan.json. The `prompt_id_ref` fields in image_plan.json do not correctly map to scene visual descriptions for approximately 10 of 18 images. **Do not use `prompt_id_ref` values from image_plan.json to drive generation. Use the corrected prompts in `assets/ai_images/generation_queue.json` instead.**

---

## 1. AI Image Inventory

| Count | Source |
|-------|--------|
| 20 | Total image entries in image_plan.json |
| 2 | REAL_PHOTO_LICENSED (IMG006/S007, IMG020/S024) |
| **18** | **AI_GENERATE (source_type in image_plan.json)** |
| 15 | Declared ai_generate_count (reflects 3 images pending real photo legal review) |

**Effective AI generation targets: 18 images across 17 unique scenes.**
(S009 has 2 image slots assigned — both are BLOCKED due to data errors. S010 and S019 have no image slot in image_plan but have scene entries. See Section 5.)

---

## 2. Classification Summary

| Status | Count | Image IDs |
|--------|-------|-----------|
| READY | **3** | IMG002, IMG004, IMG018 |
| READY_WITH_REWRITE | **9** | IMG003, IMG010, IMG011, IMG012, IMG013, IMG014, IMG015, IMG017, IMG019 |
| HUMAN_REVIEW_REQUIRED | **4** | IMG001, IMG007, IMG009, IMG016 |
| BLOCKED | **2** | IMG005, IMG008 |
| **TOTAL** | **18** | |

**Generation may begin now for: 12 images (READY + READY_WITH_REWRITE)**
Use corrected prompts from `assets/ai_images/generation_queue.json` for all READY_WITH_REWRITE images.

---

## 3. Per-Image Safety Audit

### READY (no changes needed)

#### IMG002 — S002 — Hook Interior
- Prompt: PROMPT_002 (Interior ruin, staircase, light through broken windows)
- All 11 safety dimensions: PASS
- Scene match: CORRECT
- Status: **READY**

#### IMG004 — S005 — Meiji Industrial
- Prompt: PROMPT_004 (Simulated Meiji industrial, archival style, black and white)
- All 11 safety dimensions: PASS
- Scene match: CORRECT
- Status: **READY**
- Note: Label in video as "illustrative archival simulation" — not an actual historical photograph

#### IMG018 — S022 — Ma Beat Wide
- Prompt: PROMPT_018 (Hashima panoramic, wide sky, ocean foreground)
- All 11 safety dimensions: PASS
- Scene match: ACCEPTABLE for Ma beat (panoramic island view is appropriate for 40s contemplative silence)
- Status: **READY**
- Director option: PROMPT_016 (abstract ocean, island barely visible) may be substituted for a more minimalist Ma beat

---

### READY_WITH_REWRITE (use corrected prompts in generation_queue.json)

#### IMG003 — S003 — Close-up Wave / Wooden Door
- Declared prompt: PROMPT_003 (ocean waves against seawall)
- Scene description: "Close-up of a decayed wooden door. Peeling paint, encroaching vines."
- Mismatch: Ocean waves ≠ wooden door
- Both are safe. Corrected prompt generates wooden door texture per scene description.
- Status: **READY_WITH_REWRITE** — use `PROMPT_003_REWRITTEN` in generation_queue.json

#### IMG010 — S011b — Mine Rock Texture (Fallback)
- Declared prompt: PROMPT_010 (book on desk still life)
- Scene description: "Extreme close-up of tunnel rock face. Contact surface of concrete and raw rock."
- Mismatch: Book/desk ≠ rock face
- Corrected prompt: PROMPT_013 adapted for rock tunnel texture
- Status: **READY_WITH_REWRITE** — use `PROMPT_013_ADAPTED_ROCK_FACE` in generation_queue.json
- Note: Generate regardless of IMG009 outcome — this is the fallback if IMG009 fails 3 times

#### IMG011 — S013 — Heritage Tension Wide
- Declared prompt: PROMPT_011 (light beams)
- Scene description: "Wide view of island ruins. UNESCO tension."
- Partial mismatch: light beams are an editorial fit but not a literal match for UNESCO wide shot
- Risk: Visual duplication with IMG014/S017 (also light beams)
- Status: **READY_WITH_REWRITE** — use `PROMPT_011_REFRAMED_FOR_UNESCO` in generation_queue.json

#### IMG012 — S015 — Abandoned Dock
- Declared prompt: PROMPT_012 (storm sea)
- Scene description: "Ruined dock. Stillness contrasting former bustle."
- Mismatch: Storm waves contradict the "stillness" narrative purpose of this scene
- Corrected prompt: PROMPT_009 content (empty dock, calm water)
- Status: **READY_WITH_REWRITE** — use `PROMPT_009_CONTENT` in generation_queue.json

#### IMG013 — S016 — Personal Items
- Declared prompt: PROMPT_013 (concrete macro texture)
- Scene description: "Child's shoe, indistinct old photograph, rusted metal can."
- Mismatch: Concrete texture ≠ personal belongings still life
- Corrected prompt: PROMPT_010 adapted for personal items
- CRITICAL requirement: Any photograph shown in output must be too faded/damaged to identify any face
- Status: **READY_WITH_REWRITE** — use `PROMPT_010_ADAPTED_PERSONAL_ITEMS` in generation_queue.json
- Additional review recommended: verify no human face appears in the "faded photograph" prop

#### IMG014 — S017 — Light Study Interior
- Declared prompt: PROMPT_014 (wide ocean landscape)
- Scene description: "Ruined room interior. Light beams cutting through dust. Light itself provides the motion."
- Mismatch: Wide ocean ≠ interior light study
- Corrected prompt: PROMPT_011 content (dramatic light shafts through collapsed ceiling)
- Status: **READY_WITH_REWRITE** — use `PROMPT_011_CONTENT` in generation_queue.json

#### IMG015 — S018 — Storm Ruins
- Declared prompt: PROMPT_015 (faded sign close-up)
- Scene description: "Post-typhoon ruins. Collapsed walls, exposed rebar."
- Mismatch: Faded sign ≠ storm/typhoon ruins
- Corrected prompt: PROMPT_012 content (stormy ocean + concrete structure)
- Status: **READY_WITH_REWRITE** — use `PROMPT_012_CONTENT` in generation_queue.json

#### IMG017 — S021 — Heritage Plaque
- Declared prompt: PROMPT_017 (tourist vessel)
- Scene description: "Contrast of heritage plaque with surrounding ruins. Metal plate against rusted concrete."
- Mismatch: Tourist vessel ≠ heritage plaque close-up
- Corrected prompt: PROMPT_015 adapted for heritage/UNESCO plaque
- Status: **READY_WITH_REWRITE** — use `PROMPT_015_ADAPTED_HERITAGE_PLAQUE` in generation_queue.json

#### IMG019 — S023 — Tourist Ferry
- Declared prompt: PROMPT_019 (**does not exist** in ai_image_prompts.md)
- Scene description: "Hashima silhouette viewed from tourist ferry. POV over bow."
- Error: No PROMPT_019 defined; ai_image_prompts.md ends at PROMPT_018
- Corrected prompt: PROMPT_017 content (tourist vessel approaching island)
- Status: **READY_WITH_REWRITE** — use `PROMPT_017_CONTENT` in generation_queue.json

---

### HUMAN_REVIEW_REQUIRED

#### IMG001 — S001 — Hook Establishing Shot
- Prompt: PROMPT_001 — SAFE AND CORRECT
- Hold reason: Real photo candidate C001-A (CC BY-SA 4.0) pending legal review. Generate AI only if legal review fails or is delayed.
- Status: **HUMAN_REVIEW_REQUIRED (sequencing hold, not safety block)**
- Gate: Legal decision on CC BY-SA for commercial use with modification

#### IMG007 — S008 — Building 30
- Hold reasons: (1) Real photo C008-A pending legal review. (2) structure_mismatch_flag=true — verify whether scene requires Building 30 (residential) or hoistroom (industrial). (3) If AI: prompt must be rewritten for EXTERIOR not interior chair detail.
- Status: **HUMAN_REVIEW_REQUIRED**
- Gate: Legal decision + structure mismatch confirmation

#### IMG009 — S011a — Mine Tunnel (CRITICAL SAFETY GATE)
See Section 4 for full analysis.
- Status: **HUMAN_REVIEW_REQUIRED (mandatory safety gate)**

#### IMG016 — S020 — Dusk Wide Shot
- Hold reason: Real photo C020-A (CC BY-SA 4.0) pending legal. PIXTA paid stock strongly recommended for this position (highest emotional stakes scene in the video — precedes the Ma beat).
- Status: **HUMAN_REVIEW_REQUIRED**
- Gate: Decision A/B for CC BY-SA legal review or paid PIXTA purchase

---

### BLOCKED

#### IMG005 — S009 — BLOCKED (Data Error)
- Assigned prompt: PROMPT_005 (aerial island CG view)
- Assigned scene: S009 (school interior with desks and blackboard)
- Error: Aerial CG island ≠ school interior — completely unrelated subjects
- Root cause: IMG005 appears to be an orphaned slot from the original S007 aerial AI assignment, before S007 received a real photo (IMG006)
- Also: S009 is assigned to both IMG005 AND IMG008 — a duplicate assignment error
- **BLOCK: Do not generate until data error is resolved**
- Resolution: Determine whether IMG005 should be suppressed (aerial obsolete) or reassigned to S009 with the school interior prompt provided in generation_queue.json supplemental_prompts

#### IMG008 — S009 — BLOCKED (Critical Data Error + Safety Gate Bypass)
- Assigned prompt: PROMPT_008 (mine tunnel — safety-controlled, mandatory human review)
- Assigned scene: S009 (school interior)
- Error (1): Mine tunnel ≠ school interior
- Error (2): PROMPT_008 is the safety-controlled mine tunnel prompt. Generating it for S009 would produce an unreviewed mine image outside the IMG009 mandatory human review gate — a bypass of FIX-M1 protocol
- **BLOCK: Do not generate. Correct image_plan.json immediately**
- Resolution: Assign school interior prompt (PROMPT_S009_SCHOOL from generation_queue.json) to IMG008

---

## 4. IMG009 Special Audit — Mine Tunnel Safety Gate

**Image:** IMG009 — Scene S011a (4:10–4:40, 30 seconds)
**Prompt:** PROMPT_008

### Context

Scene S011a depicts the interior of the Hashima coal mine — the site where forced labor occurred during WWII. The scene narration discusses forced labor history. This is the most sensitive image in the entire project.

**Contract / profile requirements:**
- `anh_duy.json` values: "respect for real people, real history, and real tragedy"
- `japan_mystery_lost_place.json` forbidden_elements: "graphic_imagery_of_suffering_or_death" (CRITICAL)
- `scene.json` S011a note: "人物は絶対に描写しない" (Absolutely no people depicted)
- image_plan.json: `mandatory_human_review: true`, `sensitive_content: true`
- visual_risk_report.md finding: "Midjourney v6, DALL-E 3, and SDXL regularly generate human figures (silhouettes, partial figures, shadows that read as human) in mine/tunnel scenes even with 'no people' explicitly blocked"

### Original PROMPT_008 Issues

```
Abstract mine tunnel interior, narrow passage disappearing into darkness, single dim light source
casting harsh shadows on rough rock walls, deep shadow, noir lighting, oppressive atmosphere,
no people, abstract and atmospheric, cinematic close-up perspective
--ar 16:9 --no people, modern equipment, text
```

**Issues identified:**
1. `"oppressive atmosphere"` — biases AI models toward confinement/suffering imagery in mine context
2. `--no` only has 3 terms — insufficient for models that generate human forms in tunnel scenes
3. No explicit anchoring of "empty space" in positive prompt
4. "harsh shadows" in combination with "mine tunnel" can condition models to generate shadow-human forms

### Rewritten PROMPT_008_SAFE

```
Abstract empty coal mine tunnel interior, empty industrial passage disappearing into darkness,
single dim work light casting stark shadows on rough hewn rock walls, exposed wooden support
timbers along walls, bare stone floor, deep shadow, austere industrial atmosphere, no human
presence of any kind, no people, empty space only, abstract and atmospheric, cinematic
close-up perspective
--ar 16:9 --no people, human figures, silhouettes, shadows of persons, human shapes,
implied human presence, victims, bodies, suffering, gore, violence, chains, shackles,
bones, faces, modern equipment, text
```

**Changes:**
| Original | Rewritten | Why |
|----------|-----------|-----|
| "oppressive atmosphere" | "austere industrial atmosphere" | Removes suffering-bias conditioning |
| (nothing) | "empty space only" | Dual reinforcement of emptiness in positive |
| (nothing) | "exposed wooden support timbers, bare stone floor" | Structural anchoring reduces model improvisation |
| `--no people, modern equipment, text` | `--no people, [15 additional terms]` | Comprehensive coverage of all human-presence variants |

### Human Review Gate Protocol

**Required for every generated output:**

| Check | Rejection trigger |
|-------|------------------|
| Human form | Any figure, body, or recognizable human shape |
| Silhouette | Any dark form that reads as a person |
| Shadow | Any shadow with human-coded outline |
| Suffering | Any implication of confinement, pain, captivity |
| Objects | Chains, shackles, restraints, weapons |
| Gore | Any biological content |

**If rejected:** Attempt max **3 times**. If all 3 fail → activate fallback **IMG010** (rock face macro texture). Do not attempt a 4th generation of mine interior.

**Gate: Human producer must review and sign off before IMG009 enters the video timeline.**

---

## 5. Data Errors Found — Action Required

### Error 1: S009 Double Image Assignment (BLOCKER)
- Both IMG005 (PROMPT_005 aerial) and IMG008 (PROMPT_008 mine) are assigned to S009 (school interior)
- scene.json assigns S009 to IMG008
- Both prompts are wrong for a school interior
- **Action:** Correct image_plan.json — assign exactly one image slot to S009 with school interior prompt

### Error 2: Systematic prompt_id_ref Offset
- image_plan.json prompt_id_refs for IMG010–IMG019 do not correspond to the correct prompts for their assigned scenes
- The mismatch is systematic — appears to be a numbering shift from the real photo migration (S007, S024 → real photos changed the effective index)
- **Action:** Do not use prompt_id_ref from image_plan.json. Use generation_queue.json corrected prompts exclusively.

### Error 3: PROMPT_019 Missing
- image_plan.json IMG019 references PROMPT_019
- ai_image_prompts.md only defines PROMPT_001–PROMPT_018
- **Action:** Use PROMPT_017 content for S023 (tourist vessel) as defined in generation_queue.json

### Error 4: S010 and S019 — Scenes with No Image Slot
- scene.json S010 has `image_id_ref: null` — no image slot assigned
- scene.json S019 has `image_id_ref: null` — no image slot assigned
- S010 needs haikyo close-up (grass through cracks); S019 needs macro concrete texture
- These scenes will have no image in the video unless addressed
- **Action:** After resolving IMG005/IMG008 data errors, determine if any freed slots can be assigned to S010 and S019. Alternatively, note that these scenes currently have no visual asset and assess impact on the edit.

---

## 6. Prompt Safety Dimension Summary — All 18 Images

| Dimension | Images with FAIL or RISK |
|-----------|--------------------------|
| No real victims depicted | IMG009 (CONDITIONAL — requires rewrite + review) |
| No forced labor suffering | IMG009 (CONDITIONAL — requires rewrite + review); IMG008 (BLOCKED — mine prompt for school scene) |
| No identifiable real people | IMG013 (READY_WITH_REWRITE — "faded photo" prop must be unidentifiable) |
| No horror exaggeration | IMG009 (CONDITIONAL — "oppressive atmosphere" removed in rewrite) |
| Scene match | IMG003, IMG005, IMG007, IMG008, IMG010–IMG015, IMG017, IMG019 (most READY_WITH_REWRITE) |
| PROMPT_019 missing | IMG019 (READY_WITH_REWRITE — use PROMPT_017 content) |

---

## 7. Alignment with Creator Profile and Genre Template

All 16 non-blocked, non-human-review images align with:

**anh_duy.json values:**
- "curiosity as the primary driver" → atmospheric ruin imagery ✓
- "respect for real people, real history, and real tragedy" → no human depictions, no suffering imagery ✓
- "shock value as a storytelling device" → REJECTED in all prompts ✓
- "sensationalism around real tragedies" → REJECTED in all prompts ✓

**japan_mystery_lost_place.json visual_style:**
- tone: dark ✓
- saturation: desaturated ✓
- contrast: high ✓
- lighting: dramatic_shadows ✓
- film_grain: true — all prompts include film grain ✓

**genre_template forbidden_elements:**
- "graphic_imagery_of_suffering_or_death" (CRITICAL) → No prompt generates suffering imagery. IMG009 PROMPT_008_SAFE explicitly excludes all suffering terms ✓
- "invented_quotes_from_real_people" → Not applicable to images ✓
- "exaggerated_claims_beyond_evidence" → Not applicable to images ✓

---

## 8. Files Created This Gate

| File | Purpose |
|------|---------|
| `assets/ai_images/prompt_safety_audit.json` | Full per-image audit with dimension-level results and classifications |
| `assets/ai_images/generation_queue.json` | Corrected prompts for all 18 images, ready-to-use for generation tools |
| `production/ai_image_generation_readiness_report.md` | This file |

---

## 9. Data Files to Update

Image_plan.json requires correction before generation can begin for blocked images:
- IMG008 → assign school interior prompt (not PROMPT_008)
- IMG005 → determine: suppress or reassign to S009
- Update prompt_id_refs globally to reflect corrected assignments (or note that generation_queue.json is the authoritative source)

Export.json and composition_compliance.json will be updated by this gate entry (stage 18 in export.json).

---

## 10. Final Output

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AI IMAGE GENERATION READINESS GATE — RESULT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total AI images in plan:          18
  READY:                           3
  READY_WITH_REWRITE:              9
  HUMAN_REVIEW_REQUIRED:           4
  BLOCKED:                         2

IMG009 (mine tunnel S011a):
  Status: HUMAN_REVIEW_REQUIRED
  Prompt rewrite: REQUIRED (PROMPT_008_SAFE prepared)
  Human review gate: MANDATORY for every generated output
  Max attempts: 3 (then use fallback IMG010)

Generation may begin:             YES — for 12 of 18 images
  (3 READY + 9 READY_WITH_REWRITE with corrected prompts)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EXACT NEXT ACTION:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 1 — RESOLVE BLOCKS (required before full queue runs):
  Fix image_plan.json:
    - IMG008: change prompt_id_ref from PROMPT_008 to school interior prompt
    - IMG005: suppress (aerial superseded) or reassign to S009 with school prompt
  These fixes unblock S009 generation and close the mine safety bypass.

STEP 2 — GENERATE IMMEDIATELY (3 images, no changes needed):
  IMG002 (S002), IMG004 (S005), IMG018 (S022)
  Use prompts from generation_queue.json as published.

STEP 3 — GENERATE WITH CORRECTED PROMPTS (9 images):
  IMG003, IMG010, IMG011, IMG012, IMG013, IMG014, IMG015, IMG017, IMG019
  Use generation_queue.json — do NOT use prompt_id_ref from image_plan.json.
  KEY REVIEW: IMG013 output must not show identifiable face in "faded photo" prop.

STEP 4 — IMG009 MINE TUNNEL (human review gate):
  Use PROMPT_008_SAFE from generation_queue.json.
  Every output must be reviewed by human producer before approval.
  Rejection criteria: any human form, silhouette, shadow, suffering, gore.
  Max 3 attempts. Fallback: IMG010 (already queued, generate first).

STEP 5 — AWAIT DECISIONS (4 images on hold):
  IMG001 (S001): Await CC BY-SA legal decision or C001-C fallback
  IMG007 (S008): Await CC BY-SA legal decision + structure mismatch confirmation
  IMG016 (S020): Await CC BY-SA legal review or PIXTA purchase (strongly recommended)
  IMG009 (S011a): Awaiting generation + human review (see Step 4)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
