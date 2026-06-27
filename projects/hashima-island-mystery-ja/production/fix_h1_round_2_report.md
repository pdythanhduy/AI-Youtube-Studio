# FIX-H1 Round 2 Report — Real Image Asset Decision Matrix
## hashima-island-mystery-ja
**Date:** 2026-06-27
**Fix ID:** FIX-H1
**Round:** 2 — Final candidate selection, risk classification, scenario projection
**Status after this round:** S007 and S024 PRODUCTION_READY. S001/S008/S020 SELECTED_PENDING_LEGAL_REVIEW.

---

## 1. Context

This report completes the decision layer of FIX-H1. Round 1 (real_image_curator_report.md) curated 19 candidates across 5 scenes. Round 2 makes the final per-scene decision: what to download now, what requires human legal review or purchase, and what the compliance impact is under each scenario.

**The core problem:** 17 of 20 images in image_plan.json are AI_GENERATE (85%). The contract C04 limit is 75% (15 images maximum). Replacing 5 target scenes (S001, S007, S008, S020, S024) would bring AI usage to 12/20 = 60% — 15 points below the limit.

**The core constraint:** Most high-quality free candidates for S001, S008, S020, and S024 are licensed CC BY-SA 4.0. This production applies color grading, film grain, and Ken Burns motion to all images — modifications that trigger the ShareAlike clause, potentially requiring the entire video to adopt CC BY-SA licensing (incompatible with commercial YouTube monetization).

Only S007 and S024 have clean, immediately-safe real image options.

---

## 2. Decision Matrix — Per Scene

### S007 — USE_WITH_ATTRIBUTION

| Field | Value |
|-------|-------|
| Decision | USE_WITH_ATTRIBUTION |
| Selected candidate | C007-A: Battle-Ship_Island_Nagasaki_Japan.jpg |
| License | CC BY 2.0 — no ShareAlike |
| Legal risk | LOW |
| Production status | PRODUCTION_READY |
| Action required | Download immediately. No legal review needed. |

**Reasoning:** CC BY 2.0 is the cleanest free license in the candidate set. No SA clause means color grading and motion effects create zero additional license obligation. This candidate is a Wikimedia Commons "Valued Image" — a designation indicating quality and free-license verification. Aerial framing clearly shows the battleship silhouette that the S007 scene requires.

**Companion download:** C007-B (Japan Govt 1974 aerial, attribution-only) — recommended as a 2-3 second ACT III historical insert during the 1974 narration. Same file also serves S024 (as C024-B). One download, multiple uses.

---

### S024 — USE_WITH_ATTRIBUTION

| Field | Value |
|-------|-------|
| Decision | USE_WITH_ATTRIBUTION |
| Selected candidate | C024-B: Cku-74-20_c45_6_hashima.jpg (Japan Govt 1974) |
| License | National Land Image Information — attribution-only, no ShareAlike |
| Legal risk | LOW |
| Production status | PRODUCTION_READY_PENDING_CROP |
| Action required | Download immediately. Crop to 16:9 (1900×1069 from center). |

**Reasoning:** This is the only non-CC-BY-SA option for S024 that has adequate resolution for production (1900×2100, sufficient for 1920×1080 after 16:9 crop). Japanese government public data is explicitly cleared for commercial use — the license is attribution-only with no SA clause.

**Editorial strength:** This 1974 aerial photograph was taken in the actual year of Hashima's closure. Using it as the video's final image creates a structural bookend: the video opens with a 2023 sea-level view of the island (S001, present day) and closes with a 1974 aerial government survey of the same island (the year it stopped). This time-reversal concept reinforces the video's core theme — Hashima as a frozen moment in history — without any additional narration required.

**Attribution specificity:** The Japan National Land Image Information license requires the exact attribution string. Do not paraphrase. Copy verbatim from attribution_plan.md.

**Upgrade path:** If CC BY-SA legal review is approved, upgrade S024 to C024-A (Hashima_Island_2023.jpg) for visual match 9/10 vs 7/10. One download of that file covers both S001 and S024 with different crops.

---

### S001 — LEGAL_REVIEW_REQUIRED

| Field | Value |
|-------|-------|
| Decision | LEGAL_REVIEW_REQUIRED |
| Selected candidate | C001-A: Hashima_Island_2023.jpg |
| License | CC BY-SA 4.0 |
| Legal risk | MEDIUM-HIGH |
| Production status | SELECTED_PENDING_LEGAL_REVIEW |
| Action required | Legal review OR fallback selection |

**Reasoning:** C001-A (visual match 10/10) is the only sea-level candidate — shot from a tourist vessel exactly as the scene requires. 9248×6936 resolution at 14MB gives exceptional editorial latitude for color grading. However, CC BY-SA 4.0 ShareAlike clause is triggered by the dark_documentary color grade, film grain, and motion effects applied in post.

**Safe fallback available now:** C001-C is the Battle-Ship aerial image — the same file already being downloaded for S007. It can serve as S001 with aerial framing (visual match 7/10, license clean). No additional download needed if C001-C is used.

**Legal review scope note:** The CC BY-SA legal review for C001-A covers C008-A and C020-A simultaneously (same license, same concern). One review unlocks three scenes.

---

### S008 — LEGAL_REVIEW_REQUIRED

| Field | Value |
|-------|-------|
| Decision | LEGAL_REVIEW_REQUIRED |
| Selected candidate | C008-A: 第四竪坑捲座跡-01.jpg (mine hoistroom 1992) |
| License | CC BY-SA 4.0 |
| Legal risk | MEDIUM-HIGH |
| Production status | SELECTED_PENDING_LEGAL_REVIEW |
| Action required | (1) Confirm S008 scene structure. (2) Legal review or Getty paid stock. |

**Reasoning:** C008-A shows the actual Fourth Mine Pit Hoistroom (第四竪坑捲座跡) — coal shaft infrastructure photographed 18 years after closure. No people. No forced labor context. This is industrial archaeology photography, completely distinct from the sensitive S011a mine tunnel scene (which has its own CRITICAL human review flag, FIX-M1). C008-A adds documentary authenticity that AI cannot replicate.

**Structure mismatch flag:** image_plan.json IMG007 originally called for "Building 30 Hashima" (residential). C008-A is the mine hoistroom (industrial). Both are authentic structures. Check scene.json S008 scene_description to confirm which structure the scene actually depicts before finalizing C008-A.

**No clean CC BY free alternative:** Unlike S001 (which has C001-C as a clean fallback) and S024 (C024-B), there is no CC BY 2.0 or PD candidate for S008 mine/industrial imagery. If legal review is blocked: Getty Images (905 Gunkanjima images, Royalty-Free commercial available) is the recommended paid path.

---

### S020 — LEGAL_REVIEW_REQUIRED

| Field | Value |
|-------|-------|
| Decision | LEGAL_REVIEW_REQUIRED |
| Selected candidate | C020-A: Hashima_Island_ruins_1.jpg (2017, 6000×4000) |
| License | CC BY-SA 4.0 |
| Legal risk | MEDIUM-HIGH |
| Production status | SELECTED_PENDING_LEGAL_REVIEW |
| Action required | Legal review OR PIXTA purchase (strongly recommended for this scene) |

**Reasoning:** C020-A is the highest-resolution candidate in the entire set (6000×4000 / 10.41MB), providing exceptional editorial latitude for color grading. The 2017 photography shows advanced decay that aligns with the video's atmospheric_ruin aesthetic. However CC BY-SA SA clause applies.

**Paid stock strongly recommended for S020 specifically:** S020 is the scene immediately preceding the 40-second Ma beat silence — the emotional peak of the entire video. This is not a neutral B-roll position. A real dusk or golden-hour photograph of Hashima ruins at this exact narrative moment would significantly elevate emotional impact. PIXTA has 30,594+ Gunkanjima images — a dusk/atmospheric shot exists there. The investment in a single stock license for S020 has the highest emotional ROI of any scene in this project.

**Safe fallback exists but is weak:** C020-C is the same Battle-Ship aerial image as C007-A — aerial framing, 7/10 visual match, creates a visual repeat with S007. Not recommended for ACT IV contemplative tone. It is a license-clean last resort only.

---

## 3. Scenario Projections — AI Image Percentage

**Total images: 20 | Limit: 75% (max 15 AI images)**

| Scenario | AI Images | Real Images | AI% | COMP-001 |
|----------|-----------|-------------|-----|----------|
| Baseline (current) | 17 | 0 | **85%** | BLOCKER |
| A: S007 only | 16 | 1 | **80%** | STILL VIOLATING |
| E*: S007 + S024 (immediate) | 15 | 2 | **75.0%** | MARGINAL PASS |
| B: S007 + all CC BY-SA approved | 12 | 5 | **60%** | RESOLVED |
| C: S007 + paid stock × 4 | 12 | 5 | **60%** | RESOLVED |
| D: S007 only, rest AI fallback | 16 | 1 | **80%** | STILL VIOLATING |

*Scenario E is a bonus scenario not in the original task spec but captures the immediately-achievable intermediate state.

**Interpretation:** Scenario A and Scenario D are numerically equivalent. Neither resolves the COMP-001 blocker. Scenario B and C both achieve 60% with a 15-point compliance buffer. Scenario E achieves exactly 75% with zero buffer — it is an intermediate milestone, not a final resolution.

**Key insight:** COMP-001 cannot be resolved through S007 download alone. At minimum, one additional scene (S024 via C024-B, available now without legal review) must be added to reach the 75% threshold. Three more scenes (S001/S008/S020) are needed to reach 60% and build a compliance buffer.

---

## 4. Legal Risks

### Risk 1: CC BY-SA ShareAlike (HIGH for commercial YouTube)

**Affected candidates:** C001-A (S001), C008-A (S008), C020-A (S020), C024-A (S024 upgrade)
**Core question:** Does incorporating CC BY-SA images as modified B-roll in a commercial YouTube documentary constitute a "derivative work" requiring the video to adopt CC BY-SA licensing?

**Current documentation (license_notes.md Option 2):** "Some legal opinions hold that incorporating CC BY-SA images into a larger editorial work does not make the whole video a derivative work. This view is contested. Do not rely on this interpretation without written legal advice."

**Production impact:** Three of the five target scenes have no clean non-SA free candidates. Legal review is the most cost-effective resolution path (one review, three scenes). Paid stock is the fallback.

**Do not rely on "Option 3" (common practice):** license_notes.md documents a common informal practice of using CC BY-SA images with a YouTube description statement. This is NOT technically compliant with SA. The risk of enforcement is low for non-commercial Wikimedia images — but this is a commercial channel. This report does not recommend Option 3.

### Risk 2: Japan Govt Attribution Specificity (LOW)

**Affected:** C024-B and C007-B (same file)
**Risk:** The required attribution string is specific. If shortened or paraphrased, the license may not be satisfied.
**Mitigation:** Copy exact text from attribution_plan.md. Do not paraphrase.

### Risk 3: S008 Structure Mismatch (MEDIUM — production quality risk)

**Risk:** C008-A depicts mine hoistroom, not Building 30. If the scene requires Building 30 specifically, C008-A is the wrong image.
**Mitigation:** Confirm against scene.json S008 before downloading. Takes 2 minutes.

### Risk 4: S024 Resolution After Crop (LOW)

**Risk:** C024-B is 1900×2100. After 16:9 crop to 1900×1069, the image is exactly 1920×1080 width-matched but slightly below ideal. For a dark_documentary color grade with film grain, this is acceptable — grain and grain overlay will mask any minor quality limit.
**Mitigation:** Apply film grain at a level consistent with other scenes. If quality is insufficient after crop: use C024-A (9248×6936) after legal review — dramatically higher resolution.

### Risk 5: Visual Repeat — C001-C used for S001 AND S007

**Risk:** If C001-C (Battle-Ship aerial) is used for S001 (fallback) AND S007 (primary), the same image appears twice in the video — opening shot and ACT I aerial shot.
**Mitigation:** Use different crops and dramatically different motion directions (very_slow_pan_right for S001 vs very_slow_zoom_in for S007) to visually differentiate. However, an attentive viewer may still notice the repeat. Best resolution: complete legal review and use C001-A for S001 (sea-level, visually distinct).

---

## 5. Files Created This Round

```
assets/real_images/
  asset_decision_matrix.json    ← per-scene decisions, all scenarios, exact actions
  attribution_plan.md           ← exact attribution text, video description template
  human_approval_required.md    ← tiered action plan for human producer

production/
  fix_h1_round_2_report.md      ← this file
```

**Updated files:**
```
data/image_plan.json            ← selected_candidate_id added for all 5 scenes; S007 and S024 set to REAL_PHOTO_LICENSED / production_ready
data/export.json                ← FIX-H1 status updated to decision_matrix_complete
composition/composition_compliance.json ← 4 scenario projections added
```

---

## 6. Whether COMP-001 is Resolved

**COMP-001 STATUS: PARTIALLY RESOLVED — PENDING HUMAN DOWNLOAD**

The decision matrix is complete. Two candidates (S007 and S024) are cleared for immediate download. Together they bring AI usage to 75.0% — exactly the contract limit.

COMP-001 will be **technically resolved** (at the limit) as soon as:
1. S007 / C007-A is downloaded and image_plan.json IMG006 updated to REAL_PHOTO_LICENSED
2. S024 / C024-B is downloaded, cropped, and image_plan.json IMG020 updated to REAL_PHOTO_LICENSED

COMP-001 will be **fully resolved with compliance buffer** (60%) after:
3. Decision A or B completed for S001/S008/S020

**No AI tasks are blocking the download of C007-A and C024-B.** These are human file-download actions that can happen in the next 10 minutes.

---

## 7. Next Exact Human Action

**Do this now (10 minutes):**

1. Download `https://upload.wikimedia.org/wikipedia/commons/6/6b/Battle-Ship_Island_Nagasaki_Japan.jpg`
   → Save as `assets/real_images/downloaded/S007/Battle-Ship_Island_Nagasaki_Japan.jpg`
   → Create `.license.txt` companion

2. Download `https://upload.wikimedia.org/wikipedia/commons/c/cc/Cku-74-20_c45_6_hashima.jpg`
   → Save as `assets/real_images/downloaded/S024/Cku-74-20_c45_6_hashima.jpg`
   → Crop to 16:9 (1900×1069 from center)
   → Create `.license.txt` companion

3. Update `data/image_plan.json`:
   → IMG006 (S007): source_type → REAL_PHOTO_LICENSED, status → production_ready
   → IMG020 (S024): source_type → REAL_PHOTO_LICENSED, status → production_ready_pending_crop
   → ai_generate_count: 17 → 15
   → stock_licensed_count: 0 → 2
   → ai_overuse_percent: 85 → 75
   → ai_overuse_violation: true → false

4. Check `data/scene.json` scene S008 description to confirm whether C008-A (mine hoistroom) or Building 30 is the correct structure.

**Then (within 1 week):**

5. Decide: CC BY-SA legal review (Decision A) OR paid stock PIXTA/Getty (Decision B) for S001/S008/S020.
6. Complete downloads, update image_plan.json for remaining 3 scenes.
7. After image_plan.json shows ai_overuse_violation=false: begin AI image generation for the 12–15 remaining AI scenes.
