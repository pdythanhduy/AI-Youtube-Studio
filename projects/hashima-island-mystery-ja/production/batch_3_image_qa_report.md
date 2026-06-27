# Batch 3 Image QA Report
## hashima-island-mystery-ja
**Date:** 2026-06-27
**Gate:** Batch 3 Legal-Hold Fallback QA

---

## 1. File Verification

| Expected filename | Found | Size |
|-------------------|-------|------|
| IMG001_S001_island_establishing_predawn.png | YES | 2,165 KB |
| IMG007_S008_building30_exterior.png | YES | 2,552 KB |
| IMG016_S020_island_dusk_wide.png | YES | 2,382 KB |

**All 3 expected files found.**

---

## 2. QA Classification Summary

| image_id | scene | Classification |
|----------|-------|---------------|
| IMG001 | S001 — HOOK establishing shot | **APPROVED** ✓ |
| IMG007 | S008 — Building 30 exterior | **APPROVED** ✓ |
| IMG016 | S020 — Island dusk wide | **REGENERATE** — attempt 1 of 3 |

**APPROVED: 2 | REGENERATE: 1 | REJECTED: 0**

---

## 3. IMG001 — S001 — Pre-dawn Island Establishing Shot

**Classification: APPROVED**

**What is in the image:**
Sea-level view looking across calm dark water toward the island. The island occupies the center of the frame as a dense dark mass of ruin structures and multi-story buildings. The sky is deep blue-grey with a faint glow of approaching dawn visible on the horizon behind the island. Low mist drifts at the water surface around the island's base. The water is calm and dark. The Hashima silhouette is distinctive and immediately recognizable.

**QA checks:**

| Check | Result |
|-------|--------|
| Pre-dawn palette — cold dark blue-black | PASS — deep blue-grey, desaturated, cold |
| Island establishing shot | PASS — island mass fills center, extreme wide |
| Sea-level perspective | PASS — viewer is at water level |
| No people | PASS |
| No vessels | PASS |
| Visual differentiation from IMG006 (S007 aerial real photo) | PASS — aerial daytime vs sea-level pre-dawn |
| Visual differentiation from IMG020 (S024 1974 govt aerial) | PASS — 1974 crop vs contemporary sea-level |
| Visual differentiation from IMG019 (ferry approach) | PASS — IMG019 has ferry bow; this has no foreground object |
| Suitable as HOOK image | PASS — exceptional cinematic impact |
| Documentary tone, not horror | PASS — atmospheric, documentary. Mist reads as natural, not supernatural |
| No logos / text / watermarks | PASS |
| Slow_pan_right 10s compatible | PASS — wide horizontal composition |

**Director note:** This is an outstanding HOOK image. The distinctive Hashima silhouette against the pre-dawn sky immediately establishes the documentary's subject without narration. The mist at water level adds cinematic depth. The narration "かつて、ここに5,259人が暮らしていました。" (Once, 5,259 people lived here) lands with maximum weight over this still, dark image. The cold palette sets the visual register for the entire film.

**Post-processing:** Film grain in prompt. Dark and cold palette — do not warm. slow_pan_right at 10-second duration (0:00–0:10).

---

## 4. IMG007 — S008 — Building 30 Exterior

**Classification: APPROVED**

**What is in the image:**
A large abandoned multi-story concrete residential building viewed from below at a low upward angle. The facade spans the full width of the frame. Multiple floors of open empty window frames are arranged in a regular grid pattern — consistent with residential apartment block architecture. Heavy rust staining cascades down the grey concrete surface. Moss and vines have colonized window sills and facade cracks. Several window frames are crumbling at their edges. The sky above is overcast grey. The scale is monumental.

**QA checks:**

| Check | Result |
|-------|--------|
| 9-story concrete residential facade | PASS — large multi-story block, 7-8 floors visible, more above crop |
| Resembles Building 30 / residential block | PASS — grid of window openings = residential apartment character. NOT industrial. |
| Not a mine hoistroom (C008-A mismatch resolved) | PASS — above-ground residential facade, no industrial equipment |
| No people | PASS |
| No victims or suffering | PASS — empty facade, no human content |
| No horror or ghost framing | PASS — moss/vegetation gives "nature reclaims" quality. Documentary. |
| Respectful documentary tone | PASS — factual architectural decay |
| No logos / text / watermarks | PASS |
| Visual differentiation from IMG009 (mine tunnel) | PASS — underground narrow passage vs above-ground residential facade |
| Visual differentiation from IMG008 (school interior) | PASS — exterior vs interior, different building type |
| ken_burns_zoom_in 15s compatible | PASS — building fills frame, slow zoom into upper floors works well |

**Director note:** The low-angle shot emphasizes monumental scale — critical for L008 narration establishing Building 30 as "one of Japan's oldest reinforced concrete apartment buildings." The moss and vines read as 50+ years of abandonment, not active decay. The image is correct for the ACT_I historical beat about Hashima's residential construction.

**Note on IMG016 visual collision:** The current IMG016 (REGENERATE) has a similar building facade character. Once IMG016 is correctly regenerated as an island wide dusk shot, this visual collision is eliminated.

**Post-processing:** Film grain in prompt. Desaturated grey-green palette confirmed. ken_burns_zoom_in at 15-second duration (2:45–3:00). Slow zoom toward upper floors.

---

## 5. IMG016 — S020 — Island Dusk Wide — REGENERATE

**Classification: REGENERATE — Attempt 1 of 3**

**What is in the image (attempt 1):**
A large abandoned concrete building facade, viewed from below. Multiple floors of empty window frames, moss and weathering on concrete, overcast cool-grey sky. No sea visible. No island-wide view. Cool grey palette throughout — no warm or amber tones.

**Why regeneration is required:**

| Problem | Severity |
|---------|----------|
| Wrong scene type: building close-up instead of island extreme wide | CRITICAL |
| Wrong palette: cool grey throughout, no warm/amber dusk tones | CRITICAL |
| No sea or water visible | CRITICAL |
| Shot type wrong: medium-wide building facade vs extreme_wide island | CRITICAL |
| Visual collision with IMG007 (same building facade character) | HIGH |
| Not suitable for 40s Ma silence precursor | HIGH |

Scene S020 requires: "Hashima Island at dusk or dawn. Current state after UNESCO inscription. Sky, sea, and ruins. Quiet and majestic. Extreme wide with very slow pan."

The generated image shows none of these elements.

**What caused the failure:** The original prompt led with "Extreme wide panoramic shot of a ruined uninhabited island" but the AI instead anchored on the concrete ruin structures detail and generated a building facade. The word "island" was not sufficient to force the AI to pull back to the full island view with sea visible.

**Corrected prompt strategy:** Force the three-band composition explicitly: sky / island / sea. Add "small island completely surrounded by sea" to anchor that the island must be seen from the water. Add "large expanse of calm water in the foreground" and "wide sky fills upper third of frame" to force the compositional structure. Block "building close-up, facade only, cold grey sky" in the negative prompt.

---

### Corrected Prompt — IMG016 (Regeneration Attempt 2 of 3)

```
/imagine Extreme wide panoramic view looking across calm ocean toward a small island completely surrounded by sea, the island topped with large clusters of abandoned concrete ruin structures and multi-story block buildings, warm amber and golden dusk light illuminating the ruins against a glowing gradient sunset sky of orange and deep amber, the calm sea surface reflects the warm sky colors in soft golden tones, island sits in center-to-left of the wide frame, large expanse of calm water in the foreground, wide sky fills upper third of frame, serene and vast, no vessels, no people, quiet majestic atmosphere, 35mm wide angle cinematic, warm desaturated amber and sienna and grey palette, film grain --ar 16:9 --no people, human figures, boats, vessels, tourists, text, logos, watermark, cool blue tones, cold grey sky, building close-up, interior, facade only, nighttime darkness, rain, storm, neon, modern structures, bright saturated orange, harsh sunlight --v 6.1 --q 2
```

**Output filename:** `IMG016_S020_island_dusk_wide_v2.png`
**Folder:** `assets/ai_images/generated/batch_3/`

**Key changes from attempt 1:**

| Before | After |
|--------|-------|
| "Extreme wide panoramic shot of a ruined uninhabited island at dusk" | "Extreme wide panoramic view looking across calm ocean toward a small island completely surrounded by sea" |
| No compositional anchor | "large expanse of calm water in the foreground / wide sky fills upper third of frame" |
| "golden amber light" only | "warm amber and golden dusk light illuminating the ruins against a glowing gradient sunset sky of orange and deep amber" |
| No sea reflection | "calm sea surface reflects the warm sky colors in soft golden tones" |
| No negative for building close-up | Added: "building close-up, interior, facade only, cold grey sky, cool blue tones" |

**QA requirements for attempt 2:**
- Island must be visible as a DISTANT object, seen from across the water
- Sea/ocean must be visible in foreground
- Sky must have visible warm dusk / sunset tones (amber/orange gradient)
- Palette must be warm amber and grey — NOT cool grey
- No people, no vessels
- Wide enough horizontally for 40s very_slow_pan_right
- Quiet and majestic — suitable for the last image before 40s silence

**If attempt 2 also fails:** PIXTA paid dusk photograph (軍艦島 夕暮れ / Gunkanjima dusk, Royalty-Free, ~¥5,000–¥15,000) is the natural fallback — and an aesthetic upgrade. Three failed AI attempts for this specific slot constitutes a justified purchase. Confirm "online video commercial" use at checkout.

---

## 6. Data Updates Applied

| File | Change |
|------|--------|
| `data/image_plan.json` | IMG001 → approved_for_production. IMG007 → approved_for_production. IMG016 → regenerate_required (attempt 1). |
| `data/export.json` | Stage 27 added, next_production_action updated |
| `composition/composition_compliance.json` | batch_3_image_qa block added |

---

## 7. Full Image Status — After Batch 3 QA

| image_id | scene | status |
|----------|-------|--------|
| IMG001 | S001 | **APPROVED ✓** (Batch 3, this gate) |
| IMG002 | S002 | APPROVED_WITH_MINOR_NOTES ✓ |
| IMG003 | S003 | APPROVED ✓ |
| IMG004 | S005 | APPROVED_WITH_MINOR_NOTES ✓ |
| IMG006 | S007 | REAL_PHOTO_LICENSED (CC BY 2.0) ✓ |
| IMG007 | S008 | **APPROVED ✓** (Batch 3, this gate) |
| IMG008 | S009 | APPROVED_WITH_MINOR_NOTES ✓ |
| IMG009 | S011a | APPROVED — FIX-M1 cleared ✓ |
| IMG010 | S011b | APPROVED ✓ |
| IMG011 | S013 | APPROVED_WITH_MINOR_NOTES ✓ |
| IMG012 | S015 | APPROVED ✓ |
| IMG013 | S016 | APPROVED ✓ |
| IMG014 | S017 | APPROVED ✓ |
| IMG015 | S018 | APPROVED ✓ |
| IMG016 | S020 | **REGENERATE — attempt 1 of 3** |
| IMG017 | S021 | APPROVED ✓ |
| IMG018 | S022 | APPROVED ✓ |
| IMG019 | S023 | APPROVED ✓ |
| IMG020 | S024 | REAL_PHOTO_LICENSED (Japan Govt 1974) ✓ |
| IMG005 | S009 | SUPPRESSED |

**Confirmed images: 18 of 20** (16 AI/real approved + IMG001 + IMG007)
**Pending regeneration: 1** (IMG016 — attempt 1 of 3)
**Suppressed: 1** (IMG005)

---

## 8. Final Output

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BATCH 3 IMAGE QA — RESULT

FILES FOUND:        3 / 3 ✓

IMG001  S001  HOOK ESTABLISHING SHOT
  APPROVED ✓
  Pre-dawn island silhouette — exceptional hook.
  Cold blue-black palette, sea-level, mist at water.
  Hashima silhouette distinctively recognizable.
  No people, no vessels. slow_pan_right ready.

IMG007  S008  BUILDING 30 EXTERIOR
  APPROVED ✓
  9-story residential concrete facade — correct.
  Structure mismatch with C008-A RESOLVED via AI.
  Rust staining, moss, crumbling windows visible.
  No people. ken_burns_zoom_in ready.

IMG016  S020  ISLAND DUSK WIDE
  REGENERATE — attempt 1 of 3
  REASON: AI generated a building facade close-up
  instead of an island-wide dusk shot.
  PROBLEMS:
    - No sea or ocean visible
    - No warm/amber dusk palette (cool grey only)
    - Medium-wide facade, not extreme wide
    - Nearly identical character to IMG007 (S008)
    - Not suitable for 40s Ma silence precursor

CONFIRMED IMAGES: 18 of 20
  (16 prior + IMG001 + IMG007)

PENDING: IMG016 regeneration attempt 2

IS IMAGE ASSET PHASE COMPLETE?
  NOT YET — pending IMG016 v2 generation and QA.
  After IMG016 passes: image asset phase complete.

NEXT EXACT PRODUCTION STEP:
  Generate IMG016 v2 using corrected Midjourney
  command below. Save as:
  IMG016_S020_island_dusk_wide_v2.png
  in assets/ai_images/generated/batch_3/

CORRECTED COMMAND:
  /imagine Extreme wide panoramic view looking
  across calm ocean toward a small island
  completely surrounded by sea, the island topped
  with large clusters of abandoned concrete ruin
  structures and multi-story block buildings, warm
  amber and golden dusk light illuminating the
  ruins against a glowing gradient sunset sky of
  orange and deep amber, the calm sea surface
  reflects the warm sky colors in soft golden
  tones, island sits in center-to-left of the
  wide frame, large expanse of calm water in the
  foreground, wide sky fills upper third of frame,
  serene and vast, no vessels, no people, quiet
  majestic atmosphere, 35mm wide angle cinematic,
  warm desaturated amber and sienna and grey
  palette, film grain --ar 16:9 --no people,
  human figures, boats, vessels, tourists, text,
  logos, watermark, cool blue tones, cold grey
  sky, building close-up, interior, facade only,
  nighttime darkness, rain, storm, neon, modern
  structures, bright saturated orange, harsh
  sunlight --v 6.1 --q 2
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
