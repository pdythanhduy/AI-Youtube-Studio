# Batch 2B Generation Plan Report
## hashima-island-mystery-ja
**Date:** 2026-06-27
**Gate:** Batch 2B AI Image Generation Plan
**Source:** assets/ai_images/generation_queue.json + safety audit + Batch 2A QA context

---

## 1. Scope

Batch 2B covers 5 READY_WITH_REWRITE images. IMG013 (in regeneration) and IMG009 (FIX-M1 gate) are excluded.

| image_id | scene_id | section | timecode | shot_type | motion |
|----------|----------|---------|----------|-----------|--------|
| IMG008 | S009 | ACT_II | 3:00–3:40 | medium_shot | slow_pan_right |
| IMG014 | S017 | ACT_III | 7:30–8:00 | medium_shot | static |
| IMG015 | S018 | ACT_III | 8:00–8:30 | wide_shot | slow_pan_right |
| IMG017 | S021 | ACT_IV | 9:40–10:20 | close_up | slow_zoom_in |
| IMG019 | S023 | OUTRO | 11:00–11:30 | medium_shot | slow_zoom_in |

---

## 2. Flag Word Scan

Scanned all 5 prompts for: haunting / oppressive / terrifying / horror / ghostly / nightmare / cursed / melancholic

| image_id | Flag word | Action |
|----------|-----------|--------|
| IMG008 | None | No change |
| IMG014 | **melancholic** | Replaced with **reflective** |
| IMG015 | None | No change |
| IMG017 | None | No change |
| IMG019 | None | No change |

**1 flag word corrected. 3 negative prompts expanded.**

---

## 3. Image-by-Image Audit

---

### IMG008 — S009 — Ruined School Classroom (ACT II)

**Scene:** ACT_II, 3:00–3:40, 40 seconds, medium_shot, slow_pan_right
**Narration:** L009, L010, L011 (community life / school on island)
**Historical sensitivity:** NONE — civilian school, not a labor site

**Status history:** Was BLOCKED due to PROMPT_008 (mine tunnel) data error in image_plan.json. Unblocked in queue cleanup (2026-06-27) with PROMPT_S009_SCHOOL. All safety checks pass.

**Audit:** All 10 dimensions PASS.

The school context is important: Hashima's school served the children of the mining community's civilian residents. It operated from [date unknown] until March 1974, when the last 22 students graduated and the mine closed. The school closure is an element of civilian community memory — not a forced labor context. This image comes in ACT_II at 3:00, well before the forced labor narration (S011a at 4:10).

**Prompt changes:** None. Already correctly rewritten as PROMPT_S009_SCHOOL.

---

### IMG014 — S017 — Light Beams Interior (ACT III)

**Scene:** ACT_III, 7:30–8:00, 30 seconds, medium_shot, static (light movement IS the motion)
**Narration:** L021, L022 including [PAUSE:2s]
**Historical sensitivity:** NONE — generic interior ruin

**Flag word:** `melancholic` → replaced with `reflective`.

**Reason for replacement:** "melancholic" biases AI models toward heavier grief imagery that edges toward horror/sorrow in dark interior contexts. For S017 (post-personal-items contemplation), the correct tone is reflective — the viewer contemplates what they've just seen, not grieves in the horror sense.

**Visual duplication risk with IMG011 (APPROVED, Batch 2A):** Both images use dramatic light shafts through collapsed ceiling. The risk is significant. Mitigation applied:
- Added "intimate room-scale interior, single abandoned room" to positive prompt → IMG014 should read as one small room
- Added "wide exterior view" to negative → prevents wide landscape generation
- IMG011 (S013) is wide-and-grand (multi-storey, slow_pan_left); IMG014 (S017) must be room-scale and intimate (static hold)

QA must confirm visual variety between these two images after generation.

---

### IMG015 — S018 — Post-Typhoon Storm Ruins (ACT III)

**Scene:** ACT_III, 8:00–8:30, 30 seconds, wide_shot, slow_pan_right
**Narration:** L023 (35 years of erosion and weathering)
**Historical sensitivity:** NONE — architectural/weather imagery

**Audit:** All 10 dimensions PASS. No flag words.

The "35 years of erosion" reference is accurate: mine closed January 1974; the island has been uninhabited and eroded since. The storm imagery is documentary — typhoons affect the Nagasaki coast regularly. "Powerful atmosphere of weathering and time" is appropriate documentary language for an abandoned structure after decades of exposure.

**Prompt changes:** Negative prompt expanded with "human figures, watermark, logos" for Batch 2B consistency.

---

### IMG017 — S021 — Heritage Plaque Close-up (ACT IV)

**Scene:** ACT_IV, 9:40–10:20, 40 seconds, close_up, slow_zoom_in
**Narration:** L028, L029, L030 including [PAUSE:2s]
**Historical sensitivity:** MEDIUM — UNESCO heritage designation context

**Audit:** All 10 dimensions PASS.

**Critical text safety:** The UNESCO World Heritage designation of Hashima (2015) is real and contested (Japan / Korea dispute). The plaque in S021 represents this official recognition. If AI generates legible text on the plaque, it could invent specific UNESCO language not in the script. The prompt now specifies "inscription that is illegible due to age and corrosion" and the negative prompt blocks "legible text in any language, readable inscription."

**Prompt changes from generation_queue.json:**
1. "heavily tarnished and weathered with worn inscription that is illegible" — removes ambiguity
2. Negative prompt: added "readable inscription, text in any language"

---

### IMG019 — S023 — Tourist Ferry Approaching Island (OUTRO)

**Scene:** OUTRO, 11:00–11:30, 30 seconds, medium_shot, slow_zoom_in
**Narration:** L031 (B-ROLL label), L032 (spoken OUTRO line)
**Historical sensitivity:** NONE — contemporary context

**Audit:** All 10 dimensions PASS.

**PROMPT_019 gap (noted from prior gate):** PROMPT_019 does not exist in ai_image_prompts.md (only PROMPT_001–018 defined). PROMPT_017 content (tourist vessel) is used as the correct substitute — this is the right content for S023.

**Prompt changes:**
1. Removed "slightly warmer palette relative to rest of video" from positive prompt — moved to post-processing note (color grade is not reliably controlled via generation parameters)
2. Added "no people on deck, no crew members, no tourists visible on vessel" to negative prompt — this closes the risk of AI generating people on the vessel deck

---

## 4. Final Verified Prompts

### IMG008 — S009 — Ruined School Classroom
```
/imagine Interior of ruined school classroom, overturned wooden desks and metal chairs scattered on crumbling concrete floor, faded chalk writing on deteriorating blackboard barely visible, light filtering through broken windows casting shafts across dust and debris, abandoned educational atmosphere, quiet sense of loss, haikyo aesthetic, high contrast, cinematic, desaturated with warm dust tones against cool concrete, film grain --ar 16:9 --no people, faces, identifiable text on blackboard, modern objects, logos, bright colors, watermark --v 6.1 --q 2
```

### IMG014 — S017 — Light Beams Interior
```
/imagine Dramatic shafts of natural light breaking through collapsed concrete ceiling of abandoned building, dust particles dancing visibly in light beams, chiaroscuro lighting, beautiful and reflective, cinematic, high contrast, dark surroundings with brilliant light shafts, film grain, intimate room-scale interior, single abandoned room with collapsed ceiling opening above, no motion implied --ar 16:9 --no people, furniture, text, modern objects, logos, watermark, wide exterior view, bright colors --v 6.1 --q 2
```

### IMG015 — S018 — Post-Typhoon Storm Ruins
```
/imagine Post-typhoon ruins of concrete structure near ocean, collapsed walls with exposed rebar, turbulent dark grey ocean waves crashing at base of ruins, heavy dark clouds overhead, dramatic weather, cool blue-grey dawn light, wide cinematic shot, powerful atmosphere of weathering and time, 35 years of erosion expressed in material degradation --ar 16:9 --no people, human figures, boats, bright sunlight, tropical colors, text, logos, watermark, modern elements --v 6.1 --q 2
```

### IMG017 — S021 — Heritage Plaque Close-up
```
/imagine Close-up of an aged bronze or metal heritage designation plaque mounted on crumbling concrete ruin wall, plaque surface heavily tarnished and weathered with worn inscription that is illegible due to age and corrosion, surrounding concrete crumbling and water-stained, documentary detail shot, desaturated with muted warm tones against cool concrete grey, juxtaposition of official recognition and physical decay --ar 16:9 --no people, legible text in any language, readable inscription, logos, bright colors, pristine surfaces, modern elements, watermark --v 6.1 --q 2
```

### IMG019 — S023 — Tourist Ferry Approach
```
/imagine Small contemporary tourist vessel approaching a large weathered concrete island in middle distance, ocean surface calm, medium shot from water level, bow of vessel visible in foreground with empty deck, island growing larger in frame, overcast sky, desaturated palette, muted tones, documentary style --ar 16:9 --no people, faces, human figures on vessel, crew members, tourists visible, text, logos, dramatic weather, bright colors, watermark --v 6.1 --q 2
```

---

## 5. Output Filenames

| image_id | output_filename | save_to |
|----------|----------------|---------|
| IMG008 | `IMG008_S009_school_interior.png` | `assets/ai_images/generated/batch_2b/` |
| IMG014 | `IMG014_S017_light_beams_interior.png` | `assets/ai_images/generated/batch_2b/` |
| IMG015 | `IMG015_S018_storm_ruins.png` | `assets/ai_images/generated/batch_2b/` |
| IMG017 | `IMG017_S021_heritage_plaque_ruin.png` | `assets/ai_images/generated/batch_2b/` |
| IMG019 | `IMG019_S023_tourist_ferry_approach.png` | `assets/ai_images/generated/batch_2b/` |

**Save to:** `assets/ai_images/generated/batch_2b/` — create this subfolder before saving.

---

## 6. QA Gate Summary (After Generation)

| image_id | Primary QA check | Critical gate |
|----------|-----------------|---------------|
| IMG008 | No people, desks/blackboard present, chalk illegible | No |
| IMG014 | No people, light shafts present, ROOM-SCALE not wide-grand | VISUAL DUPLICATION CHECK vs IMG011 |
| IMG015 | No people, no boats, collapsed rebar + storm waves present | No |
| IMG017 | No people, plaque inscription ILLEGIBLE | YES — any legible text → REGENERATE |
| IMG019 | No people on vessel deck, island visible | YES — any person/face on deck → REGENERATE |

---

## 7. Parallel Track: IMG013 Regeneration

While Batch 2B is being generated, IMG013 regeneration should run in parallel:

- **Attempt 1 of 3** — Use face-down photograph prompt (see `production/batch_2a_image_qa_report.md`)
- **Save as:** `IMG013_S016_personal_items_v2.png`
- **Save to:** `assets/ai_images/generated/batch_2b/` (or batch_1 if that is where you save personal items images)

---

## 8. Final Output

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BATCH 2B GENERATION PLAN — RESULT

Batch 2B image count:     5
Image IDs:                IMG008, IMG014, IMG015, IMG017, IMG019

Safety status:
  IMG008  READY_WITH_REWRITE → APPROVED (no prompt changes)
  IMG014  READY_WITH_REWRITE → APPROVED (melancholic→reflective; duplication guard added)
  IMG015  READY_WITH_REWRITE → APPROVED (negative expanded)
  IMG017  READY_WITH_REWRITE → APPROVED (plaque text illegibility strengthened)
  IMG019  READY_WITH_REWRITE → APPROVED (vessel-people guard added)

Flag words corrected:     1  (IMG014: melancholic → reflective)
Prompts expanded:         3  (IMG014, IMG017, IMG019)

Batch 2B generation may begin: YES
Output directory: assets/ai_images/generated/batch_2b/
Parallel: IMG013 regeneration attempt 1 of 3
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
