# Batch 1 Image QA Report
## hashima-island-mystery-ja
**Date:** 2026-06-27
**Gate:** Batch 1 AI Image QA
**Reviewer:** batch_1_image_qa_gate
**Source plan:** assets/ai_images/batch_1_generation_plan.json

---

## 1. File Verification

| Expected filename | Found | Size |
|-------------------|-------|------|
| IMG002_S002_interior_ruin.png | YES | 2,727 KB |
| IMG004_S005_meiji_industrial.png | YES | 2,681 KB |
| IMG018_S022_hashima_panorama.png | YES | 2,014 KB |

**All 3 expected files found.**

---

## 2. QA Classification Summary

| image_id | scene | Classification | Approved |
|----------|-------|----------------|----------|
| IMG002 | S002 Hook interior | APPROVED_WITH_MINOR_NOTES | YES |
| IMG004 | S005 Meiji industrial | APPROVED_WITH_MINOR_NOTES | YES |
| IMG018 | S022 Ma beat panoramic | APPROVED | YES |

**APPROVED: 1 | APPROVED_WITH_MINOR_NOTES: 2 | REGENERATE: 0 | REJECTED: 0**

No regeneration required. Batch 2 may begin.

---

## 3. Image-by-Image Review

---

### IMG002 — S002 — Hook Interior Ruin
**Classification: APPROVED_WITH_MINOR_NOTES**

**What is in the image:**
A heavily damaged multi-story concrete building interior. A broken concrete staircase is centered in the frame, ascending to a partially collapsed upper floor. Peeling walls with exposed concrete and rebar. Heavy debris on the floor. Natural daylight floods the space from multiple collapse openings. The far right of the image opens through a demolished wall to an extensive exterior view of similarly destroyed buildings and rubble.

**QA checks:**

| Check | Result |
|-------|--------|
| Correct scene match | PASS — interior ruin, staircase, light through openings |
| Correct subject | PASS — all required elements present |
| No people | PASS — zero human forms |
| No victims / suffering | PASS |
| No forced labor depiction | PASS |
| No ghost/horror | PASS |
| No gore/violence | PASS |
| No modern objects | PASS |
| No text/logos/watermarks | PASS |
| 16:9 format | PASS |
| Respectful Hashima tone | PASS |
| Usable for ken_burns_zoom_in | PASS WITH NOTE (see below) |

**Approval: YES**

**Minor notes:**

1. **Post-processing required — desaturation.** The AI output is warm daylight (bright, slightly yellowish tones). The target dark documentary palette requires significant desaturation (-60–70%) and exposure reduction (-0.5 to -1 stop). This is routine post work.

2. **Director framing note — ken_burns_zoom_in motion.** The right-side of the image shows a large opening through which extensive exterior ruins are visible — a wide field of destroyed building facades. This exterior view has a visual quality closer to Middle Eastern urban conflict destruction than Japanese haikyo abandonment. With the ken_burns_zoom_in framing: the motion should begin wide on the staircase (center/left frame) and push in toward the staircase landing, de-emphasizing the right-side exterior opening. The staircase itself is exactly right for S002.

3. **Not a rejection trigger.** The exterior view through the opening is a framing concern, not a content safety issue. The image is usable with careful crop and motion direction.

**Post-processing instructions:**
- Desaturate to 60–70% of AI output
- Reduce exposure -0.5 to -1.0 stop
- Add film grain (dark_documentary preset)
- Ken_burns_zoom_in: push toward staircase landing, frame left-of-center
- Optional: vignette to de-emphasize peripheral areas

---

### IMG004 — S005 — Meiji Industrial Archival
**Classification: APPROVED_WITH_MINOR_NOTES**

**What is in the image:**
A black and white industrial landscape in a mountain valley setting. A tall smokestack at center-left emits smoke. A prominent coal mine shaft headframe (pit-head tower) rises on the right. Various period-appropriate wooden and metal industrial buildings fill the foreground. Additional smokestacks and smoke at center and right. Mountain ridges form the background. The image is rendered in the aesthetic of a genuine period photograph — highly convincing grain, tonal range, and compositional style of late Meiji/Taisho industrial photography.

**QA checks:**

| Check | Result |
|-------|--------|
| Correct scene match | PASS — Meiji industrial era establishing visual |
| Correct subject | PASS — all required elements present |
| No identifiable people | PASS WITH NOTE — extremely small, non-identifiable shapes in far mid-ground only |
| No victims / suffering | PASS — Meiji era predates wartime forced labor (1939–1945) |
| No forced labor depiction | PASS |
| No ghost/horror | PASS |
| No gore/violence | PASS |
| No modern objects | PASS — all structures consistent with pre-1920 era |
| No text/logos/watermarks | PASS |
| 16:9 format | PASS |
| Respectful Hashima tone | PASS |
| Usable for slow_pan_left | PASS |

**Approval: YES**

**Minor notes:**

1. **MANDATORY PRODUCTION LABEL.** This image looks exactly like a real Meiji-era historical photograph. Before using in the video, the editor must add an "illustrative archival simulation" caption. Presenting this as an actual historical photograph would be factually misleading. Suggested caption: `明治時代のイラスト（AI生成）` or `Illustrative archival simulation / Not an actual historical photograph`. This label should appear as a small, non-intrusive subtitle when the image is on screen.

2. **Mine headframe specificity.** The dominant element on the right is a coal mine headframe (a pit-head winding tower), making this image specifically a coal mine rather than a general "Meiji factory." This is thematically correct for a Hashima coal mine documentary, and the S005 narration covers the island's industrial origins. The director should ensure the narration at this point explicitly references coal mining so the image connects logically.

3. **Distant figures.** Extremely small human-scale shapes appear in the far mid-ground near the mine buildings. They are not identifiable at any viewing scale and are consistent with the "no identifiable individuals" constraint. No action needed — noted for awareness.

4. **Slow_pan_left direction.** Begin on the smokestacks (left-center), pan right to reveal the mine headframe. This creates a natural narrative reveal matching the Meiji coal mine context.

**Post-processing instructions:**
- Image is already true B&W — no desaturation needed
- Slight contrast boost to deepen blacks (optional)
- Apply film grain if AI output lacks sufficient period grain
- Apply slow_pan_left at 40-second duration
- **ADD REQUIRED LABEL: 'illustrative archival simulation'**

---

### IMG018 — S022 — Ma Beat Hashima Panoramic
**Classification: APPROVED**

**What is in the image:**
A wide panoramic view of Hashima Island (Gunkanjima) taken from the ocean. The island's distinctive battleship silhouette is clearly visible — the mass of concrete apartment blocks, seawall, and industrial structures rise from the flat calm grey-blue water. An overcast sky with layered clouds occupies the upper half of the frame. The color palette is naturally desaturated grey-blue, matching the dark documentary target without any post-processing. Faint coastline is visible in the far distant right background, anchoring the Nagasaki geography.

**QA checks:**

| Check | Result |
|-------|--------|
| Correct scene match | PASS — Hashima panoramic wide view, exactly matches S022 |
| Correct subject | PASS — island, ocean, sky in correct proportions |
| No people | PASS — zero human forms |
| No boats/vehicles | PASS — open ocean only |
| No text/logos/watermarks | PASS |
| 16:9 format | PASS |
| Respectful Hashima tone | PASS — haunting and beautiful without sensationalism |
| Usable as 40-second static hold | PASS — composition is restful and contemplative |
| Balanced horizon | PASS — level, centered |

**Approval: YES — no notes required**

**Ma beat compliance confirmed:**
- Motion = STATIC ✓
- Duration = 40 seconds ✓
- Narration = NONE ✓
- Audio = ocean ambient only ✓

**Post-processing instructions:**
- Minimal. Image is already naturally desaturated and at correct tonal target.
- Optional: very slight film grain to match visual language of other images
- Hold STATIC for 40 seconds — no motion
- Dissolve in from S021, dissolve out to S023
- Fade to black at end of hold

**One observation — provenance note:**
This image is highly photorealistic and closely resembles actual photographs of Hashima Island taken from tour vessels. If the production team has any uncertainty about whether this image was AI-generated vs. sourced externally, the file provenance should be confirmed before finalizing. If it is an actual photograph, a separate license check is required. Assuming AI-generated as filed.

---

## 4. Corrected Prompts

**None required.** All three images are approved. No regeneration needed for Batch 1.

---

## 5. Data Updates Applied

| File | Change |
|------|--------|
| `data/image_plan.json` | IMG002, IMG004, IMG018: status → approved, file_path set |
| `data/export.json` | Stage 20 added (batch_1_image_qa), next_production_action updated |
| `composition/composition_compliance.json` | batch_1_qa block added |
| `assets/ai_images/generated/batch_1/batch_1_qa.json` | Created |

---

## 6. Post-Production Priorities (Before Edit Assembly)

| Priority | Image | Action |
|----------|-------|--------|
| HIGH | IMG004 | Add "illustrative archival simulation" label in edit — MANDATORY |
| HIGH | IMG002 | Post-process: desaturate + darken; frame ken_burns_zoom_in toward staircase |
| LOW | IMG018 | Confirm file provenance; minimal post-processing needed |

---

## 7. Final Output

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BATCH 1 IMAGE QA — RESULT

FILES FOUND:                      3 / 3
  IMG002_S002_interior_ruin.png   ✓
  IMG004_S005_meiji_industrial.png ✓
  IMG018_S022_hashima_panorama.png ✓

IMAGES APPROVED:                  3 of 3
  APPROVED:                       1 (IMG018)
  APPROVED_WITH_MINOR_NOTES:      2 (IMG002, IMG004)
  REGENERATE:                     0
  REJECTED:                       0

CORRECTED PROMPTS NEEDED:         0

NOTES:
  IMG002 — desaturate in post; frame ken_burns away
            from right-side exterior view
  IMG004 — MANDATORY 'illustrative archival simulation'
            label required before use
  IMG018 — confirm AI provenance; minimal post needed

BATCH 2 MAY BEGIN:                YES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
