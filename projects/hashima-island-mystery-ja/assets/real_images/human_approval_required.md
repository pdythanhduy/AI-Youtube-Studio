# Human Approval Required
## FIX-H1 Round 2 — hashima-island-mystery-ja
**Date:** 2026-06-27
**Summary:** 2 downloads safe immediately. 3 scenes require legal review OR paid stock decision.

---

## TIER 1: DOWNLOAD NOW — No Approval Needed

These are safe to download immediately. No legal review, no purchase.

---

### ACTION 1 — Download S007 primary image

**File:** Battle-Ship_Island_Nagasaki_Japan.jpg
**URL:** https://upload.wikimedia.org/wikipedia/commons/6/6b/Battle-Ship_Island_Nagasaki_Japan.jpg
**License:** CC BY 2.0 — no ShareAlike, no restrictions beyond attribution
**Save to:** `assets/real_images/downloaded/S007/Battle-Ship_Island_Nagasaki_Japan.jpg`
**Create companion:** `Battle-Ship_Island_Nagasaki_Japan.jpg.license.txt`
**Add to video description:** "Battle-Ship Island Nagasaki Japan (2008) by kntrty / Wikimedia Commons / CC BY 2.0"
**Impact:** S007 changes from AI_GENERATE to REAL_PHOTO_LICENSED. AI% drops from 85% to 80%.

---

### ACTION 2 — Download S024 / ACT III historical image (same file, two uses)

**File:** Cku-74-20_c45_6_hashima.jpg
**URL:** https://upload.wikimedia.org/wikipedia/commons/c/cc/Cku-74-20_c45_6_hashima.jpg
**License:** Japan National Land Image Information — attribution-only, no ShareAlike
**Save to:** `assets/real_images/downloaded/S024/Cku-74-20_c45_6_hashima.jpg`
**Also reference in:** `assets/real_images/downloaded/S007/` (same file serves ACT III insert C007-B)
**Crop required:** Portrait 1900×2100 → 16:9 1900×1069 (crop from center)
**Create companion:** `Cku-74-20_c45_6_hashima.jpg.license.txt`
**Add to video description (exact — do not paraphrase):**
```
Aerial photograph of Hashima Island (1974)
Source: National Land Image Information (Color Aerial Photographs)
Ministry of Land, Infrastructure, Transport and Tourism of Japan
```
**Impact:** S024 changes from AI_GENERATE to REAL_PHOTO_LICENSED. AI% drops to 75% (exactly at limit).

**After completing Actions 1 and 2:**
- AI image usage = 75.0% (limit met, zero buffer)
- COMP-001 is technically resolved but marginal
- 3 remaining scenes (S001, S008, S020) still AI — proceed to Tier 2 to build buffer

---

## TIER 2: LEGAL REVIEW DECISION — Human Choice Required

You must make ONE of the following decisions before S001, S008, S020 can be resolved.

---

### DECISION A — Seek CC BY-SA legal clearance (covers S001 + S008 + S020 simultaneously)

**What to submit:** Forward `assets/real_images/license_notes.md` Section 2 to legal counsel.

**Question to ask:**
> "We are producing a commercial YouTube documentary (monetized). We wish to use 3 photographs licensed under CC BY-SA 4.0 as B-roll footage. Our post-production workflow applies: (1) desaturation color grade, (2) film grain, (3) Ken Burns zoom/pan motion effects. Do these modifications constitute a 'derivative work' that requires the entire video to adopt CC BY-SA licensing? If yes, is there a licensing workaround (e.g., isolated scene licensing, license upgrade request to photographer)?"

**If YES (legally cleared):** Download all three files, use CC BY-SA images with attribution. One review unlocks S001 + S008 + S020. AI% drops to 60%.

**If NO (legally blocked or no legal counsel available):** Proceed to Decision B.

**Estimated time:** 1–5 business days for legal review.

---

### DECISION B — Purchase paid stock licenses (covers S001 + S008 + S020 without legal ambiguity)

**Recommended platform:** PIXTA (best Hashima coverage, Japanese market)
**URL:** https://www.pixtastock.com/c30/c41/c1

**Search terms per scene:**
- S001: `軍艦島 海 全景` or `端島 海 全景` or `Hashima sea exterior` (sea-level wide shot)
- S008: `軍艦島 廃墟 建物` or `端島 炭鉱` or `30号棟 端島` (industrial ruins / Building 30)
- S020: `軍艦島 夕暮れ` or `端島 夕焼け` or `Gunkanjima dusk` (dusk/atmospheric ruin shot)

**License required at purchase:** PIXTA Royalty-Free (covers commercial online video, worldwide, in perpetuity). Confirm at checkout.

**Alternative platform:** Getty Images (https://www.gettyimages.com/photos/gunkanjima)
- Search: Gunkanjima / Hashima Island / Hashima mine
- Filter: "Creative" (not "Editorial" — editorial images cannot be used commercially)
- License: Royalty-Free. Confirm "online video commercial" use at checkout.

**Impact:** AI% drops from 75% to 60%. COMP-001 fully resolved with 15pp buffer.

---

## TIER 3: CONFIRMATION REQUIRED — Before Image Generation Begins

The following non-download decisions must also be confirmed before final image_plan execution.

---

### CONFIRM: S008 scene content (structure mismatch)

**Issue:** image_plan.json IMG007 originally called for "Building 30 Hashima" (residential apartment). The candidate curated by FIX-H1 is C008-A — Fourth Mine Pit Hoistroom (industrial coal shaft infrastructure), a different structure.

**Both are authentic Hashima buildings.** The question is which structure the S008 scene actually depicts.

**Check:** Open `data/scene.json`, find scene_id="S008", read `scene_description`. 

- If scene describes industrial / mining infrastructure → C008-A is correct. Proceed.
- If scene describes residential building / Building 30 → C008-A is wrong candidate. Curate separately from Getty/PIXTA using keyword '30号棟 端島'.

---

### CONFIRM: After legal/paid stock decision, update image_plan.json

After any of the above actions result in confirmed candidates:
1. Change `source_type` from `AI_GENERATE` to `REAL_PHOTO_LICENSED` for affected scenes
2. Update `file_path` to `assets/real_images/downloaded/[scene_id]/[filename]`
3. Update global `ai_generate_count`, `stock_licensed_count`, `ai_overuse_percent`, `ai_overuse_violation`
4. Run this check: (ai_generate_count / total_images) × 100 ≤ 75 → COMP-001 resolved

---

## Impact Summary

| Action | AI% After | COMP-001 | Requires |
|--------|-----------|----------|----------|
| Download S007 only | 80% | BLOCKER | Nothing — do it now |
| Download S007 + S024 | 75% | Marginal pass | Nothing — do it now |
| S007 + S024 + Decision A (CC BY-SA cleared) | 60% | RESOLVED | Legal review |
| S007 + S024 + Decision B (paid stock) | 60% | RESOLVED | Purchase 3 licenses |
| No action | 85% | BLOCKER | — |

---

## Recommended Order of Operations

```
TODAY:
  [1] Download C007-A → S007
  [2] Download C007-B/C024-B → S024 (same file, two uses)
  → AI% = 75.0% (limit met, marginal)

THIS WEEK:
  [3] Choose: Decision A (legal review) OR Decision B (paid stock)
  [4] Confirm S008 structure mismatch (check scene.json)

AFTER DECISION A or B:
  [5] Download / purchase remaining 3 images
  [6] Update image_plan.json source_type for all 5 scenes
  → AI% = 60% (COMP-001 fully resolved with buffer)

THEN:
  [7] Begin AI image generation for remaining 15 scenes
  [8] Complete FIX-M1 (IMG009 human review)
  [9] Complete FIX-M3 (timed read-through)
```
