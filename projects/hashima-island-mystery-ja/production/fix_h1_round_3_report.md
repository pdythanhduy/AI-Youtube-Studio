# FIX-H1 Round 3 Report — Real Image Download and Metadata Update
## hashima-island-mystery-ja
**Date:** 2026-06-27
**Fix ID:** FIX-H1
**Round:** 3 — Download, crop, and register approved attribution-safe real images
**Status after this round:** S007 and S024 DOWNLOADED AND REGISTERED. COMP-001 RESOLVED. AI% = 75%.

---

## 1. Downloads

### S007 — Battle-Ship_Island_Nagasaki_Japan.jpg

| Field | Value |
|-------|-------|
| Candidate ID | C007-A |
| Source | Wikimedia Commons |
| Download URL | https://upload.wikimedia.org/wikipedia/commons/6/6b/Battle-Ship_Island_Nagasaki_Japan.jpg |
| Download result | SUCCESS |
| Saved to | `assets/real_images/downloaded/S007_IMG006_Battle-Ship_Island_Nagasaki_Japan.jpg` |
| File size | 991.7 KB (1,015,463 bytes) |
| Dimensions | 1600 × 1200 |
| License | CC BY 2.0 — no ShareAlike |
| License companion | `S007_IMG006_Battle-Ship_Island_Nagasaki_Japan.jpg.license.txt` |

**Technical note:** First download attempt returned HTTP 429 (Wikimedia rate limit). Resolved by adding proper User-Agent header (`Mozilla/5.0 (compatible; VideoProduction/1.0; mailto:thanhduy8vn@gmail.com)`) on second attempt. Download succeeded.

---

### S024 — Cku-74-20_c45_6_hashima.jpg

| Field | Value |
|-------|-------|
| Candidate ID | C024-B |
| Source | Wikimedia Commons (Japan National Land Image Archive) |
| Download URL | https://upload.wikimedia.org/wikipedia/commons/c/cc/Cku-74-20_c45_6_hashima.jpg |
| Download result | SUCCESS |
| Original saved to | `assets/real_images/downloaded/S024_IMG020_Cku-74-20_c45_6_hashima_original.jpg` |
| Original file size | 1,790.6 KB (1,833,575 bytes) |
| Original dimensions | 1900 × 2100 (portrait) |
| License | National Land Image Information — attribution-only, no ShareAlike |
| License companion | `S024_IMG020_Cku-74-20_c45_6_hashima_original.jpg.license.txt` |

---

## 2. Processing — S024 16:9 Crop

| Field | Value |
|-------|-------|
| Method | System.Drawing.Graphics.DrawImage (HighQualityBicubic) |
| JPEG quality | 95 |
| Crop type | Center crop |
| Source dimensions | 1900 × 2100 |
| Crop rectangle | x=0, y=516, w=1900, h=1069 |
| Output dimensions | 1900 × 1069 |
| Aspect ratio | 1900/1069 = 1.778 ≈ 16/9 = 1.778 ✓ |
| Output file size | 422.9 KB |
| Saved to | `assets/real_images/processed/S024_IMG020_Cku-74-20_c45_6_hashima_16x9.jpg` |
| Result | SUCCESS |

**Crop arithmetic:** Target 16:9 from 1900-wide portrait: height = 1900 ÷ (16/9) = 1068.75 → rounded to 1069. Center Y offset: (2100 − 1069) / 2 = 515.5 → 516 (integer floor). Crop is centered, preserving island shape with equal sky and sea margin.

---

## 3. Attribution Text

### S007 — required in YouTube description

```
Battle-Ship Island Nagasaki Japan (2008) by kntrty / Wikimedia Commons
CC BY 2.0 — https://creativecommons.org/licenses/by/2.0/
```

### S024 — required in YouTube description (verbatim — do not paraphrase)

```
Aerial photograph of Hashima Island (1974)
Source: National Land Image Information (Color Aerial Photographs)
Ministry of Land, Infrastructure, Transport and Tourism of Japan
```

**Note on S024:** The Japan National Land Image Information license requires this specific attribution string. Do not shorten, paraphrase, or substitute. Copy verbatim into the YouTube description "IMAGE CREDITS" section before publish.

---

## 4. Files Created / Downloaded This Round

| File | Size | Action |
|------|------|--------|
| `downloaded/S007_IMG006_Battle-Ship_Island_Nagasaki_Japan.jpg` | 991.7 KB | Downloaded |
| `downloaded/S007_IMG006_Battle-Ship_Island_Nagasaki_Japan.jpg.license.txt` | <1 KB | Created |
| `downloaded/S024_IMG020_Cku-74-20_c45_6_hashima_original.jpg` | 1790.6 KB | Downloaded |
| `downloaded/S024_IMG020_Cku-74-20_c45_6_hashima_original.jpg.license.txt` | <1 KB | Created |
| `processed/S024_IMG020_Cku-74-20_c45_6_hashima_16x9.jpg` | 422.9 KB | Cropped |

---

## 5. Data Files Updated

| File | Change |
|------|--------|
| `data/image_plan.json` | IMG006: source_type→REAL_PHOTO_LICENSED, status→production_ready, local_path set, dimensions added |
| `data/image_plan.json` | IMG020: source_type→REAL_PHOTO_LICENSED, status→production_ready, crop fields set, local_path→processed/ |
| `data/image_plan.json` | Global: ai_generate_count 17→15, stock_licensed_count 0→2, ai_overuse_percent 85→75, ai_overuse_violation false |
| `data/export.json` | W001 fix_status updated, FIX-H1 description updated, metrics updated (ai_image_count 15, stock_image_count 2, ai_overuse_percent 75), stage 17 added, next_production_action updated |
| `composition/composition_compliance.json` | COMP-001: status→resolved_at_limit, actual_value 85→75, resolution documented |
| `composition/composition_compliance.json` | overall_compliance_score 82→85, BLOCKER count 1→0, creator score 85→88, documentary score 72→80 |
| `assets/real_images/attribution_plan.md` | S007 and S024 sections marked DOWNLOADED |

---

## 6. Updated AI Image Percentage

| Metric | Before Round 3 | After Round 3 |
|--------|----------------|---------------|
| AI images | 17 | 15 |
| Real images | 0 | 2 |
| Total images | 20 | 20 |
| AI% | 85% | **75%** |
| Contract limit | 75% | 75% |
| Violation | YES | **NO** |
| Buffer | −10pp (violation) | 0pp (at limit) |

**At limit with zero buffer.** Three additional scenes (S001/S008/S020) remain AI-generated. Completing Decision A or Decision B for those scenes brings AI% to 60% — providing a 15pp compliance buffer.

---

## 7. COMP-001 Status

**RESOLVED** ✓

- Previous status: BLOCKER (AI% 85% > 75% limit)
- Current status: `resolved_at_limit`
- Resolution: S007 and S024 real images downloaded and registered. AI% = 75.0% — at contract limit.
- Blocker count: 3 → 0 (over all rounds: COMP-002/003 in Round 1, COMP-001 in Round 3)

**Note:** "Resolved at limit" means the BLOCKER condition is cleared (≤75%), but no compliance buffer exists. This is sufficient to unblock AI image generation for the remaining 15 AI scenes. However, completing Decision A or Decision B for S001/S008/S020 is still recommended to build margin and bring the documentary's visual authenticity to its full potential.

---

## 8. Remaining Legal Risks

### Risk 1: CC BY-SA ShareAlike — S001, S008, S020 (MEDIUM-HIGH)
Three scenes remain AI-generated. Their curated real-image candidates (C001-A, C008-A, C020-A) are CC BY-SA 4.0. This production's color grade and motion effects likely trigger the SA clause. See `assets/real_images/license_notes.md` Section 2. One legal review resolves all three simultaneously.

**This risk is inherited from Round 2. It does not affect production readiness of the current two downloads.**

### Risk 2: S008 Structure Mismatch (MEDIUM)
Curated candidate C008-A is the mine hoistroom (industrial), but image_plan originally specified Building 30 (residential). The S008 scene content must be confirmed in `scene.json` before C008-A is finalized for that scene. This does not affect COMP-001 resolution.

### Risk 3: Zero Compliance Buffer (LOW)
At exactly 75%, any future decision to add a sixth AI image to the project would re-trigger the COMP-001 violation. Track `ai_generate_count` carefully. Completing S001/S008/S020 to 60% eliminates this risk.

### Risk 4: S024 Attribution Verbatim Requirement (LOW)
The Japan National Land Image Information attribution string must be copied verbatim. This is documented in both the license.txt file and attribution_plan.md.

---

## 9. Next Production Action

**COMP-001 is resolved. All BLOCKERs cleared. Image generation may now begin.**

### Immediate parallel actions (no dependencies between them):

1. **Decision A or B for S001/S008/S020** — choose CC BY-SA legal review (covers all 3) or paid PIXTA/Getty. See `assets/real_images/human_approval_required.md` Tier 2. This brings AI% to 60%.

2. **FIX-M1 (IMG009 review gate)** — human review of the mine tunnel scene (S011a) before AI generation. Confirm: no people, no suffering imagery. If rejected 3×: use fallback IMG010. CRITICAL safety gate.

3. **FIX-M3 (timed read-through)** — complete before voice talent session. 1201 words, target 12 minutes. Log timing at paragraph level.

4. **COMP-007 (community guidelines review)** — human review of video content for YouTube sensitive content policy. Topics: forced labor, historical violence, political dispute. Approve or flag required edits.

### After all pending fixes resolved:
```
→ AI image generation for 15 remaining AI scenes
→ Voice recording (requires FIX-M3 timed read-through first)
→ Timeline assembly (requires voice + images complete)
→ Thumbnail design render (THUMB_A concept, pending IMG001 real photo or AI generation)
→ SEO final review
→ Publish
```
