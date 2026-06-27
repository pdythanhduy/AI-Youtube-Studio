# Batch 2B Image QA Report + IMG013 Regeneration QA
## hashima-island-mystery-ja
**Date:** 2026-06-27
**Gate:** Batch 2B Image QA + IMG013 Regeneration Verification
**Reviewer:** batch_2b_image_qa_gate

---

## 1. File Verification

### IMG013 Regeneration (batch_2a/)
| Expected filename | Found | Size |
|-------------------|-------|------|
| IMG013_S016_personal_items_v2.png | YES | 2,309 KB |

### Batch 2B (batch_2b/)
| Expected filename | Found | Size |
|-------------------|-------|------|
| IMG008_S009_school_interior.png | YES | 2,417 KB |
| IMG014_S017_light_beams_interior.png | YES | 2,171 KB |
| IMG015_S018_storm_ruins.png | YES | 2,505 KB |
| IMG017_S021_heritage_plaque_ruin.png | YES | 2,680 KB |
| IMG019_S023_tourist_ferry_approach.png | YES | 2,073 KB |

**All 6 expected files found.**

---

## 2. QA Classification Summary

| image_id | scene | Classification | Approved |
|----------|-------|----------------|----------|
| IMG013 v2 | S016 Personal items | **APPROVED** | YES — critical gate cleared |
| IMG008 | S009 School interior | **APPROVED_WITH_MINOR_NOTES** | YES |
| IMG014 | S017 Light beams interior | **REGENERATE** | NO — reads as cave, not room |
| IMG015 | S018 Storm ruins | **APPROVED** | YES |
| IMG017 | S021 Heritage plaque | **APPROVED** | YES — plaque text illegible |
| IMG019 | S023 Tourist ferry | **APPROVED** | YES — vessel deck empty |

**APPROVED: 4 | APPROVED_WITH_MINOR_NOTES: 1 | REGENERATE: 1 | REJECTED: 0**

---

## 3. IMG013 Regeneration QA

### IMG013 v2 — S016 — Personal Items (Attempt 2)
**Classification: APPROVED — Critical gate cleared**

**Regeneration strategy used:** Photograph turned face-down — only yellowed blank paper back visible.

**What is in the image:**
Close-up still life on a dark concrete floor against a concrete corner. Child's leather shoe (centre-left, dark leather, Mary-Jane style with buckle strap, heavily worn and distressed). Rusted metal can lying on its side (right). Aged piece of paper/photograph lying **face-down**, showing only the blank yellowed aged paper back — no photographic content visible.

**Critical gate: PASS**

| Critical check | Result |
|----------------|--------|
| Photograph face-down or blank | **PASS — face-down, blank paper back only** |
| No visible family portrait | PASS |
| No visible faces | PASS |
| No identifiable people | PASS |
| No legible personal information | PASS |
| No modern objects | PASS |
| Tone quiet and respectful | PASS |

**Verdict:** The face-down strategy succeeded. Regeneration closed after attempt 2 (of max 3). All critical checks pass. Image approved for production.

**Post-processing:** Film grain. Dark_documentary palette already correct. Warm paper tones against dark concrete provide the emotional focus. Slow_zoom_in at 30-second duration.

---

## 4. Batch 2B Image-by-Image Review

---

### IMG008 — S009 — Ruined School Classroom
**Classification: APPROVED_WITH_MINOR_NOTES**

**What is in the image:**
Wide view of a heavily decayed school classroom. Multiple wooden desks and chairs scattered throughout, most overturned or tilted at angles. Dark blackboard at the back of the room. Left wall has large windows with light shafts breaking through, vegetation visible outside. Heavy debris, dried leaves on floor. Teacher's desk near the blackboard. Very dark and atmospheric.

**QA checks:** All PASS.

| Check | Result |
|-------|--------|
| Correct scene match | PASS — school classroom, desks, blackboard, light shafts |
| No people | PASS |
| No forced labor depiction | PASS — civilian school context |
| No ghost/horror | PASS — atmospheric not sinister |
| No modern objects | PASS |
| No text/logos/watermarks | PASS — blackboard is dark/blank |
| 16:9 format | PASS |
| Usable for slow_pan_right 40s | PASS |

**Minor notes:**

1. **Destruction level** — The classroom is very heavily destroyed: debris, fallen ceiling material, dried leaves, exposed damage. More extreme than gradual 50-year abandonment alone would suggest (could read as fire or structural collapse). For Hashima specifically, this level is plausible given typhoon access over 50 years. Director should judge whether this level matches the scene's intended "quiet sense of loss" or feels excessively violent.

2. **Blackboard** — No chalk writing discernible. Scene description says "faded chalk writing barely visible." The prompt requested this but the AI rendered a blank/dark board. This is actually safer (no legibility concerns) but is a minor miss against the scene description.

**Post-processing:** Film grain. Slight desaturation from warm sepia toward cooler dark_documentary target. Slow_pan_right at 40-second duration.

---

### IMG014 — S017 — Light Beams Interior
**Classification: REGENERATE — Attempt 1 of 3**

**What is in the image:**
A dark interior space with dramatic light beams converging from a ceiling opening above. However, the space reads clearly as a **natural cave chamber**, not a ruined concrete building interior. The walls are raw natural stone/rock. The ceiling opening has a cave-arch formation, not a collapsed concrete ceiling. The floor has natural rock gravel, not concrete rubble.

**Why regeneration is required:**

1. **Scene mismatch** — S017 requires "ruined room interior of abandoned building." This is a natural cave.

2. **Mine tunnel visual collision** — The cave chamber aesthetic visually overlaps with IMG009 (mine tunnel, ACT_II). Placing two cave-like dark spaces in the same documentary — one for ACT_II forced labor context, one for ACT_III contemplation — creates viewer confusion. Was this the mine again? Did we go underground again?

3. **Architectural narrative break** — ACT_III is about the built community of Hashima (civilians, school, dock, personal items). A natural cave breaks the architectural-ruin visual language established throughout the video.

**What was good:** The light beam quality is excellent — multiple beams converging from above, dramatic chiaroscuro, dust visible in light. If regenerated in a concrete room, this quality should be preserved.

---

### Corrected Prompt — IMG014 (Regeneration Attempt 1 of 3)

**Strategy:** Anchor firmly on concrete/masonry architecture. Explicitly block cave/natural rock/underground cave appearance. Preserve the excellent light beam visual concept from attempt 1.

```
/imagine Ruined concrete room interior of an abandoned building, a single dramatic shaft of natural light entering through a large hole in the collapsed concrete ceiling, dust particles visible in the light beam, concrete walls clearly visible on both sides with cracks and weathering stains, concrete rubble and building debris on the concrete floor, chiaroscuro lighting, beautiful and reflective, cinematic, high contrast, dark concrete surroundings with brilliant entering light, film grain, intimate room-scale of a single abandoned residential or industrial room, former built interior space --ar 16:9 --no people, furniture, text, modern objects, logos, watermark, cave walls, natural stone walls, underground cave, cave ceiling arch, mine tunnel appearance, natural rock floor, bright colors --v 6.1 --q 2
```

**Output filename:** `IMG014_S017_light_beams_interior_v2.png`

**Key changes from attempt 1:**
- "concrete walls clearly visible on both sides" — anchors material
- "collapsed concrete ceiling" — not cave arch
- "concrete rubble and building debris on the concrete floor" — not rock gravel
- Negative: "cave walls, natural stone walls, underground cave, cave ceiling arch, mine tunnel appearance, natural rock floor" added

**If attempt 2 also fails:** Try a different approach — describe a recognizable building element (window frame, doorframe, exposed rebar in wall) to anchor the architecture more definitively.

---

### IMG015 — S018 — Post-Typhoon Storm Ruins
**Classification: APPROVED**

**What is in the image:**
Wide shot of concrete ruin columns and wall frames standing at the ocean edge, heavily eroded. Multiple ruined concrete columns forming a structural silhouette against the stormy sky. Ocean waves crashing dramatically at the base of the ruins. Heavy dark storm clouds filling the sky. Cool blue-grey dawn/storm light. Exposed structural elements including what appears to be rebar.

**QA checks:** All PASS.

| Check | Result |
|-------|--------|
| Correct scene match | PASS — post-typhoon concrete ruins at ocean, waves, dark clouds |
| Collapsed walls / exposed rebar | PASS |
| No people | PASS |
| No boats | PASS |
| No modern elements | PASS |
| Cool dawn/storm light | PASS |
| No text/logos/watermarks | PASS |
| 16:9 format | PASS |
| Usable for slow_pan_right 30s | PASS |

**Assessment:** Strong image. The ruins at ocean edge with crashing waves conveys exactly the "35 years of erosion" narration. The cool blue-grey palette is already at target. No issues.

**Post-processing:** Minimal. Film grain. Palette already correct — do not warm. Slow_pan_right at 30-second duration.

---

### IMG017 — S021 — Heritage Plaque Close-up
**Classification: APPROVED**

**What is in the image:**
Close-up of a rectangular dark metal/bronze plaque mounted on a heavily weathered concrete wall. The plaque surface is heavily tarnished and oxidized — nearly black with corrosion. Any original inscription is worn to near-complete illegibility. The surrounding concrete wall is heavily weathered and stained. In the background (soft focus, depth of field), ruins of a structure are visible.

**Critical gate: PASS — plaque inscription is illegible.**

| Check | Result |
|-------|--------|
| Plaque inscription illegible | **PASS — worn beyond readability** |
| Correct scene match | PASS — heritage plaque on ruin wall |
| No people | PASS |
| No legible text anywhere | PASS |
| No logos/watermarks | PASS |
| No modern/pristine surfaces | PASS |
| 16:9 format | PASS |
| Usable for slow_zoom_in 40s | PASS |

**Director note:** The plaque surface reads entirely as corroded/oxidized metal — the surface texture is corrosion, not legible text. This is exactly correct: the visual says "official recognition exists but is fading into the same decay as the surrounding ruins." This is the exact thematic content of S021.

**Post-processing:** Minimal. Film grain. Consider slight warm toning on plaque surface vs cool concrete to emphasize the material contrast. Slow_zoom_in at 40-second duration.

---

### IMG019 — S023 — Tourist Ferry Approach
**Classification: APPROVED**

**What is in the image:**
Clear view from the bow of a white tourist ferry. The vessel's bow with white railing dominates the lower foreground — deck is empty (no people). Hashima Island's distinctive "battleship" silhouette is clearly visible in the middle distance: multi-storey concrete tower blocks rising from the sea in the distinctive elongated shape. Calm grey water. Overcast grey sky. Distant coastline/mountains visible behind the island.

**Critical gate: PASS — vessel deck completely empty.**

| Check | Result |
|-------|--------|
| No people on vessel deck | **PASS — deck empty, no crew or tourists** |
| No faces | PASS |
| Hashima Island visible | PASS — distinct battleship silhouette |
| Calm ocean | PASS |
| No other boats | PASS |
| No text/logos/watermarks | PASS |
| No dramatic weather | PASS — overcast but calm |
| 16:9 format | PASS |
| Usable for slow_zoom_in 30s | PASS |

**Director note:** The Hashima Island silhouette in this image is exceptionally distinctive — clearly recognizable as the actual Gunkanjima/Battleship Island shape. This is highly appropriate for the OUTRO position: the viewer has spent 11 minutes learning about the island and now sees it fully and recognizably as they exit. Strong finale visual.

**Post-processing:** Film grain. Apply subtle warm color grade (slight amber vs the cold grey of ACT_II/III) — represents contemporary context. Slow_zoom_in at 30-second duration.

---

## 5. Data Updates Applied

| File | Change |
|------|--------|
| `data/image_plan.json` | IMG013 v2 → approved. IMG008/IMG015/IMG017/IMG019 → approved. IMG014 → regenerate attempt 1. |
| `data/export.json` | Stage 24 added, next_production_action updated |
| `composition/composition_compliance.json` | batch_2b_qa block added |

---

## 6. Remaining AI Images (Status Overview)

| image_id | scene | current_status |
|----------|-------|---------------|
| IMG014 | S017 | REGENERATE attempt 1 — corrected prompt ready |
| IMG009 | S011a | FIX-M1 gate (mine tunnel — separate protocol) |
| IMG001 | S001 | HUMAN_REVIEW_REQUIRED (CC BY-SA legal hold) |
| IMG007 | S008 | HUMAN_REVIEW_REQUIRED (CC BY-SA legal hold + structure confirm) |
| IMG016 | S020 | HUMAN_REVIEW_REQUIRED (CC BY-SA legal hold / PIXTA recommended) |
| IMG005 | S009 | SUPPRESSED — do not generate |

**12 of 17 active AI images now approved** (excluding suppressed IMG005).
**2 real photos registered** (IMG006 CC BY 2.0, IMG020 Japan Govt).
**Total confirmed images: 14 of 20.**

---

## 7. Final Output

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BATCH 2B IMAGE QA + IMG013 REGEN — KẾT QUẢ

FILES FOUND:              6 / 6
  IMG013 v2 in batch_2a/
  IMG008/014/015/017/019 in batch_2b/

IMG013 v2 STATUS:         APPROVED
  Critical gate CLEARED — photograph face-down,
  only blank paper back visible.
  Regeneration closed (2 of max 3 attempts used).

BATCH 2B RESULTS:
  APPROVED:               3 → IMG015, IMG017, IMG019
  APPROVED_WITH_MINOR_NOTES: 1 → IMG008
  REGENERATE:             1 → IMG014
  REJECTED:               0

IMAGES REQUIRING REGENERATION:
  IMG014 — S017 light beams interior
  REASON: Reads as natural cave chamber,
          not concrete building room interior.
          Risks visual collision with IMG009
          mine tunnel aesthetic.
  ATTEMPT: 1 of 3

CORRECTED PROMPT KEY CHANGES:
  + "concrete walls clearly visible on both sides"
  + "collapsed concrete ceiling"
  + "concrete rubble and building debris on floor"
  - cave walls, natural stone walls, underground cave,
    cave ceiling arch, mine tunnel appearance, rock floor

REMAINING AI IMAGES NOT YET APPROVED:
  IMG014  REGENERATE attempt 1
  IMG009  FIX-M1 mine gate (separate protocol)
  IMG001  Legal hold (CC BY-SA)
  IMG007  Legal hold (CC BY-SA + structure confirm)
  IMG016  Legal hold / PIXTA recommended

TOTAL CONFIRMED IMAGES: 14 of 20
  (12 AI approved + 2 real photos registered)

IMG009 MINE GATE — MAY IT BE PREPARED NEXT?
  YES — FIX-M1 protocol is fully documented.
  Prompt: PROMPT_008_SAFE in generation_queue.json
  Requirements: human producer reviews EVERY output
  Max 3 attempts. Fallback: IMG010 (already approved)
  Run in parallel with IMG014 regeneration.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
