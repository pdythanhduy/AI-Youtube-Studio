# Batch 2A Image QA Report
## hashima-island-mystery-ja
**Date:** 2026-06-27
**Gate:** Batch 2A AI Image QA
**Reviewer:** batch_2a_image_qa_gate

---

## 1. File Verification

**Note on folder:** Batch 2A images were saved to `batch_1/` instead of `batch_2a/`. The `batch_2a/` subdirectory does not exist. All 5 expected files are present in `batch_1/`. QA proceeds as normal. For future batches, save to the correct named subfolder.

| Expected filename | Found in | Size |
|-------------------|----------|------|
| IMG003_S003_wooden_door_closeup.png | batch_1/ | 2,486 KB |
| IMG010_S011b_mine_rock_texture.png | batch_1/ | 2,752 KB |
| IMG011_S013_heritage_light_ruins.png | batch_1/ | 2,274 KB |
| IMG012_S015_abandoned_dock.png | batch_1/ | 2,169 KB |
| IMG013_S016_personal_items.png | batch_1/ | 2,269 KB |

**All 5 expected files found.**

---

## 2. QA Classification Summary

| image_id | scene | Classification | Approved |
|----------|-------|----------------|----------|
| IMG003 | S003 Hook door close-up | **APPROVED** | YES |
| IMG010 | S011b Mine rock texture | **APPROVED** | YES |
| IMG011 | S013 Heritage light ruins | **APPROVED_WITH_MINOR_NOTES** | YES |
| IMG012 | S015 Abandoned dock | **APPROVED** | YES |
| IMG013 | S016 Personal items | **REGENERATE** | NO — critical gate triggered |

**APPROVED: 3 | APPROVED_WITH_MINOR_NOTES: 1 | REGENERATE: 1 | REJECTED: 0**

---

## 3. Image-by-Image Review

---

### IMG003 — S003 — Weathered Wooden Door
**Classification: APPROVED**

**What is in the image:**
Close-up of a heavily weathered wooden door set into a concrete wall. Paint peeled away in thick layers exposing raw grey wood grain. Ivy and vines creeping across the door surface and surrounding wall. Rusted metal door handle/latch at centre. Dark, atmospheric tones. The door fills almost the entire frame.

**QA checks:** All PASS.

| Check | Result |
|-------|--------|
| Correct scene match | PASS — exact match for S003 close-up door visual |
| Correct subject | PASS — door, peeling paint, vines all present |
| No people | PASS |
| No victims / suffering | PASS |
| No forced labor depiction | PASS |
| No ghost/horror | PASS — dark atmosphere, not sinister |
| No gore/violence | PASS |
| No modern objects | PASS |
| No text/logos/watermarks | PASS |
| 16:9 format | PASS |
| Respectful Hashima tone | PASS |
| Usable for static hold | PASS |

**Post-processing:** Minimal. Add film grain. Color already near target — dark grey-green, deeply desaturated. Static hold 15 seconds.

---

### IMG010 — S011b — Mine Rock Face Texture
**Classification: APPROVED**

**What is in the image:**
Extreme macro close-up of dark coal/shale rock surface. Near-black with wet sheen. Jagged geological crevices and fractured layers. Warm amber mineral highlights in crevices. Raking side light creates surface relief. Very abstract and near-monochrome — purely geological.

**QA checks:** All PASS.

| Check | Result |
|-------|--------|
| Correct scene match | PASS — extreme close-up geological texture matches S011b |
| No human forms / silhouettes | PASS — zero human-coded shapes in shadows |
| No chains, tools, shackles | PASS |
| No forced labor reference | PASS — pure geology |
| No gore/violence | PASS |
| Shadow patterns read as geological | PASS |
| 16:9 format | PASS |
| Usable for slow_zoom_in | PASS — rich detail rewards a slow push |

**Also confirmed:** viable as fallback for IMG009 (mine tunnel) under FIX-M1 gate.

**Post-processing:** Minimal. Film grain. Do not brighten — dark palette is correct. Apply slow_zoom_in at 20-second duration.

---

### IMG011 — S013 — Heritage Light Ruins
**Classification: APPROVED_WITH_MINOR_NOTES**

**What is in the image:**
Wide view of a massively collapsed multi-storey building interior. Three dramatic light shafts (god-rays) cut through collapsed ceiling from upper centre. Brilliant light against very dark surroundings. Structural columns partially standing. Heavy rubble on floor. Through the collapsed back wall, exterior ruins are visible in the background (further destroyed building facades).

**QA checks:** All core checks PASS.

| Check | Result |
|-------|--------|
| Correct scene match | PASS — grand-scale ruin with light shafts, UNESCO tension scene |
| No people | PASS |
| No UNESCO plaque or signage | PASS |
| No text/logos/watermarks | PASS |
| No ghost/horror | PASS — light shafts are contemplative, not sinister |
| No gore/violence | PASS |
| 16:9 format | PASS |
| Usable for slow_pan_left | PASS |

**Minor notes:**

1. **Exterior ruins through collapsed back wall** — same pattern noted in IMG002/Batch 1. The background shows destroyed urban building facades, giving a partial war-zone quality alongside the haikyo aesthetic. For S013 (showing grand-scale ruin for the UNESCO tension moment), this is less problematic than in the Hook — the scale of destruction is intentionally significant here. However, the director should frame the slow_pan_left to favour the interior light shafts rather than lingering on the external ruins.

2. **Visual duplication with IMG014** — both S013 and S017 use light shaft imagery. After IMG014 (Batch 2B) is generated, compare and ensure variety: S013 should feel wide-and-grand, S017 should feel room-scale and intimate.

**Post-processing:** Slight contrast boost (deepen black surrounds to intensify light shafts). Film grain. Slow_pan_left at 30-second duration — begin on primary light shaft, pan to reveal more interior depth.

---

### IMG012 — S015 — Abandoned Dock
**Classification: APPROVED**

**What is in the image:**
Industrial dock/pier extending into calm grey water. Two large rusted mooring bollards dominate the foreground. Crumbling concrete pier surface. Metal railing running along the dock edge. Ruins of an industrial building on the left. Overcast sky with layered clouds. Calm grey-blue water with no vessels. Distant landmass visible on the far horizon (right).

**QA checks:** All PASS.

| Check | Result |
|-------|--------|
| Correct scene match | PASS — abandoned dock, calm water, stillness |
| Correct subject | PASS — bollards, dock, crumbling concrete all present |
| No people | PASS |
| No boats or modern vessels | PASS |
| No text/logos/watermarks | PASS |
| No modern elements | PASS |
| 16:9 format | PASS |
| Usable for slow_zoom_out | PASS — dock recession into water provides perfect pull-back axis |

**Assessment:** Strongest image in Batch 2A. Naturally desaturated, compositionally balanced, authentic industrial dock atmosphere. The dock's perspective line receding into the grey water creates an ideal slow_zoom_out anchor. The distant landmass on the horizon adds geographic realism without being distracting.

**Post-processing:** Minimal. Film grain. Natural desaturation already at target. Slow_zoom_out at 30-second duration — begin on bollards in foreground, pull back to reveal full dock and water.

---

### IMG013 — S016 — Personal Items
**Classification: REGENERATE — CRITICAL GATE TRIGGERED**

**What is in the image:**
Close-up still life on a dusty concrete ledge. Child's leather shoe (centre-left, aged, with buckle strap). Rusted cylindrical metal can (right). Aged photograph lying flat in front of the shoe.

**Critical gate result: FAIL**

The **old photograph prop** shows a **group of people** in a formal posed portrait. Multiple human figures are clearly visible standing together in what appears to be a family or group portrait. The photograph is sepia-toned and aged but the human figures are unmistakably present — multiple adults in a posed group composition.

The mandatory rejection gate specified: *"If ANY human face or figure is visible in the photograph prop: REJECT immediately."*

**Gate triggered. Image rejected for regeneration.**

| Check | Result |
|-------|--------|
| Correct scene match | PASS |
| Child's shoe present | PASS |
| Rusted can present | PASS |
| No people in scene | PASS |
| No forced labor | PASS |
| **Photograph prop check** | **FAIL — human figures visible in photograph** |

**Why the prompt failed:** The positive prompt phrase "too damaged and faded to show any identifiable features" was not sufficient to prevent the AI from generating a recognizable group portrait. The model generated a legible-enough photograph to show human figures clearly.

---

## 4. Corrected Prompt — IMG013 (Regeneration Attempt 1 of 3)

**Strategy:** The photograph is now explicitly **face-down** — only the aged blank paper back is visible. This removes any possibility of photograph content appearing.

### Midjourney command (Attempt 1):
```
/imagine Abandoned personal belongings left behind in ruins, close-up still life: a weathered child's shoe with worn leather buckle strap, a rusted empty metal can lying on dusty crumbling concrete surface, an aged photograph turned face-down so only its yellowed blank paper back is visible with edges curling and yellowed with age, dim atmospheric single light source from one side, warm amber tones against dark concrete background, mood of memory and quiet departure, still life photography aesthetic, symbolic --ar 16:9 --no people, faces, human figures, photographs showing content, photographs facing up, legible photograph content, identifiable subjects in photographs, legible text, modern objects, logos, watermark, bright colors --v 6.1 --q 2
```

**Output filename:** `IMG013_S016_personal_items_v2.png`

### If Attempt 1 also fails (Attempt 2 of 3) — Remove photograph entirely:
```
/imagine Abandoned personal belongings left behind in ruins, close-up still life: a weathered child's shoe with worn leather buckle strap, a rusted empty metal can lying on its side on dusty crumbling concrete surface, scattered dust and small debris, dim atmospheric single light source from one side, warm amber tones against dark concrete background, mood of memory and quiet departure, still life photography aesthetic, symbolic --ar 16:9 --no people, faces, photographs, paper, text, modern objects, logos, watermark, bright colors --v 6.1 --q 2
```

**Output filename:** `IMG013_S016_personal_items_v3.png`

**If both fail (3 attempts total):** Escalate to human review. Consider replacing S016 with a real-photo candidate (stock or CC-licensed photograph of abandoned objects — no people visible) or removing S016 from the timeline.

---

## 5. Data Updates Applied

| File | Change |
|------|--------|
| `data/image_plan.json` | IMG003/IMG010/IMG012 → approved. IMG011 → approved_with_notes. IMG013 → regenerate_required. |
| `data/export.json` | Stage 22 added, next_production_action updated |
| `composition/composition_compliance.json` | batch_2a_qa block added |

---

## 6. Final Output

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BATCH 2A IMAGE QA — RESULT

FILES FOUND:              5 / 5
  (all in batch_1/ folder — note for next batch)

IMAGES APPROVED:          4 of 5
  APPROVED:               3  →  IMG003, IMG010, IMG012
  APPROVED_WITH_MINOR_NOTES: 1 → IMG011
  REGENERATE:             1  →  IMG013
  REJECTED:               0

IMAGES REQUIRING REGENERATION:
  IMG013 — S016 personal items
  REASON: photograph prop shows group of people
           in a legible group portrait
  ATTEMPT: 1 of 3

CORRECTED PROMPT (IMG013 — Attempt 1):
  Key change: photograph is now FACE-DOWN
  Only aged paper back visible — no image content

BATCH 2B MAY BEGIN: YES
  Run IMG013 regeneration in parallel with Batch 2B
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
