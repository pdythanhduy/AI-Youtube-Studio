# IMG016 v2 Final QA Report
## hashima-island-mystery-ja
**Date:** 2026-06-27
**Gate:** IMG016 Regeneration v2 — Final QA + Image Asset Phase Gate

---

## 1. File Verification

| File | Found | Size |
|------|-------|------|
| IMG016_S020_island_dusk_wide_v2.png | YES | 1,848 KB |

---

## 2. Classification

**APPROVED ✓**

Regeneration closed — attempt 2 of 3 used.

---

## 3. What Is in the Image

A small island completely surrounded by calm ocean water, viewed from sea level at a wide angle. The island is covered with a dense cluster of large multi-story abandoned concrete ruin structures. The distinctive elongated "battleship" island profile is clearly recognizable. A warm amber and deep orange dusk sky fills the upper two-thirds of the frame, with a horizon glow suggesting the sun is near or just below the horizon. The calm sea surface reflects the warm dusk sky in soft golden tones. Water is visible in the foreground and on both sides of the island. No people, no vessels, no modern elements.

**Three-band composition confirmed:**
```
┌──────────────────────────────────────────────────────┐
│  Warm amber / deep orange gradient sky               │
│  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   │
│           [  ISLAND RUINS  ]                        │
│  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   │
│  Calm reflective sea water                          │
└──────────────────────────────────────────────────────┘
```

---

## 4. QA Checklist

| Check | Result |
|-------|--------|
| Extreme wide island view | PASS — island at middle distance, not a close-up |
| Ocean clearly visible | PASS — sea in foreground and flanking both sides |
| Island completely surrounded by sea | PASS — island is a distinct landmass in open ocean |
| Warm restrained dusk palette | PASS — amber and orange-gold tones. See minor note MN-01 below. |
| Calm reflective water | PASS — calm surface with soft golden sky reflection |
| No people | PASS |
| No vessels | PASS — no boats, ships, or ferries |
| Not a building close-up | PASS — attempt 1 failure fully corrected |
| Not visually identical to IMG007 (S008) | PASS — IMG007 is a close-up cool-grey building facade; this is a warm-dusk island wide. No overlap. |
| Visually distinct from IMG001 (S001 HOOK) | PASS — IMG001 is cold dark blue-black pre-dawn. This is warm amber dusk. Opposite color temperature. |
| Visually distinct from IMG020 (S024 aerial) | PASS — IMG020 is a 1974 aerial govt photo. This is sea-level warm-color contemporary. |
| Visually distinct from IMG019 (S023 ferry) | PASS — IMG019 has ferry bow foreground, cool grey. This is open sea, warm dusk, no vessel. |
| Suitable before 40s Ma silence | PASS — serene and vast. Holds visual interest across 40s very_slow_pan_right. |
| Respectful documentary tone | PASS — reverent, cinematic. No sensationalism, no horror. |
| No logos / text / watermarks | PASS |
| 16:9 suitable | PASS |
| very_slow_pan_right 40s compatible | PASS — wide horizontal composition, open sea on both sides of island |

**All 16 checks: PASS**

---

## 5. Minor Note

**MN-01 — Sky saturation:** The warm amber/orange sky is slightly more vivid than "warm desaturated" may imply. The colors are rich and cinematic but not neon or exaggerated. This is within the acceptable range for a documentary dusk shot.

**Post-processing action:** Apply slight desaturation (~15-20%) to align with the dark_documentary grade. Preserve the warm amber character relative to the cold blue scenes in ACT_I and ACT_II — the warm vs cold contrast between S020 and earlier scenes is a deliberate narrative device. Do not flatten the image to neutral grey.

---

## 6. Narrative Function — Why This Image Works

The film opens with IMG001 (S001): cold dark pre-dawn, the island as a silent dark mass, first narration "once, 5,259 people lived here." 

The film approaches its close with IMG016 (S020): warm amber dusk, the island illuminated and whole, narration announces the 2015 UNESCO inscription. 

These two images are visual bookends. The cold/warm contrast — blue-black pre-dawn vs amber dusk — mirrors the documentary's narrative arc: mystery and loss in the HOOK, recognition and memory in ACT_IV. The viewer who sees both images subconsciously understands: the island has been recognized, it will be remembered.

The very_slow_pan_right over 40 seconds that follows the UNESCO narration (L027) then enters the Ma beat — 40 seconds of silence over this image. The warm, calm, still dusk serves that silence exactly. It is not beautiful in a way that trivializes what happened there. It is beautiful in the way that time and distance make heavy things bearable.

---

## 7. Upgrade Flag — Status

**Flag is valid but is NOT a production blocker.**

PIXTA paid dusk photography of Hashima (軍艦島 夕暮れ, Royalty-Free, ~¥5,000–¥15,000) would provide real photographic depth of field and authentic Hashima atmospheric texture at this position. The AI image is production-ready. The upgrade, if pursued, should happen before final publish rather than blocking the pipeline now.

---

## 8. Data Updates Applied

| File | Change |
|------|--------|
| `data/image_plan.json` | IMG016 → approved_for_production, regeneration_closed, file_path set |
| `data/export.json` | Stage 28 added, image_asset_phase_complete set, next_production_action updated |
| `composition/composition_compliance.json` | img016_v2_final_qa block added, image_asset_phase_complete: true |

---

## 9. Complete Image Asset Inventory — FINAL

| image_id | scene | classification |
|----------|-------|---------------|
| IMG001 | S001 HOOK | APPROVED ✓ |
| IMG002 | S002 | APPROVED_WITH_MINOR_NOTES ✓ |
| IMG003 | S003 | APPROVED ✓ |
| IMG004 | S005 | APPROVED_WITH_MINOR_NOTES ✓ |
| IMG006 | S007 | REAL_PHOTO_LICENSED (CC BY 2.0) ✓ |
| IMG007 | S008 | APPROVED ✓ |
| IMG008 | S009 | APPROVED_WITH_MINOR_NOTES ✓ |
| IMG009 | S011a | APPROVED — FIX-M1 cleared ✓ |
| IMG010 | S011b | APPROVED ✓ |
| IMG011 | S013 | APPROVED_WITH_MINOR_NOTES ✓ |
| IMG012 | S015 | APPROVED ✓ |
| IMG013 | S016 | APPROVED ✓ |
| IMG014 | S017 | APPROVED ✓ |
| IMG015 | S018 | APPROVED ✓ |
| IMG016 | S020 | **APPROVED ✓ (v2, this gate)** |
| IMG017 | S021 | APPROVED ✓ |
| IMG018 | S022 | APPROVED ✓ |
| IMG019 | S023 | APPROVED ✓ |
| IMG020 | S024 | REAL_PHOTO_LICENSED (Japan Govt 1974) ✓ |
| IMG005 | — | SUPPRESSED |

**19 of 20 images: CONFIRMED**
**1 of 20: SUPPRESSED (IMG005 — orphaned aerial CG slot)**

**IMAGE ASSET PHASE: COMPLETE ✓**

---

## 10. Final Output

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
IMG016 v2 FINAL QA — COMPLETE

FILE FOUND:   YES ✓  (1,848 KB)

IMG016 v2 STATUS:   APPROVED ✓
  Regeneration closed — attempt 2 of 3 used.

  What is in the image:
  Small island completely surrounded by calm ocean.
  Dense cluster of multi-story abandoned concrete
  ruins on the island. Warm amber and deep orange
  dusk sky (top 60% of frame). Calm golden sea
  water (bottom). Three-band composition confirmed.
  Hashima 'battleship' profile recognizable.

  All 16 QA checks: PASS
  Minor note MN-01: sky slightly vivid — apply
  slight desaturation in post. Preserve warm tone.

  Narrative: warm amber dusk bookends the cold
  pre-dawn of IMG001/S001 — visual arc complete.
  Suitable for 40s Ma silence precursor.
  very_slow_pan_right 40s compatible.

  Upgrade flag still valid — PIXTA dusk photo
  recommended before publish. Not a blocker.

TOTAL CONFIRMED IMAGES: 19 of 20
  All 19 non-suppressed images CONFIRMED.
  IMG005 SUPPRESSED.
  AI% = 75.0% (unchanged, at limit).

IMAGE ASSET PHASE:   COMPLETE ✓

NEXT EXACT PRODUCTION STEP:
  FIX-M3 — Timed read-through of the full script
  before voice talent session.
  1,201 words, target: 12 minutes total.
  Log timing at paragraph level.
  Required before any voice recording begins.

  Also action before assembly:
  Rename IMG009 file:
    FROM: IMG009_S010_mine_gate_attempt1.png
    TO:   IMG009_S011a_mine_tunnel_approved.png
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
