# Legal-Hold Image Decision Round
## hashima-island-mystery-ja
**Date:** 2026-06-27
**Gate:** Legal-Hold Image Decision — IMG001 / IMG007 / IMG016
**Policy:** Prefer completing the production pipeline safely over perfect real-photo coverage.

---

## Background

After FIX-H1 Rounds 2 and 3, two images were downloaded and registered (IMG006 S007 CC BY 2.0; IMG020 S024 Japan Govt), bringing AI% to exactly 75% — the contract limit. Three scene slots remained on legal hold because their preferred real-photo candidates all carry CC BY-SA 4.0 licenses, and this production's color grade + motion effects likely trigger the ShareAlike clause.

No CC BY-SA legal review has been completed. Per the production policy for this first test pipeline, the decision is to complete the pipeline without legal risk rather than wait for external review.

---

## The Legal-Hold Problem — Why CC BY-SA is Blocked

All three candidates (C001-A, C008-A, C020-A) are CC BY-SA 4.0. This production applies:
- Dark_documentary color grade (significant saturation and contrast modification)
- Film grain overlay (texture layer added to every image)
- Ken Burns motion effects (transformation of still photo into dynamic video)

Under CC BY-SA, these modifications likely constitute derivative works. Incorporating a CC BY-SA derivative into a commercial YouTube video would technically require the entire video to adopt CC BY-SA licensing — incompatible with standard commercial monetization. Until written legal clearance is obtained confirming these modifications do not trigger the SA clause, CC BY-SA images cannot be used.

---

## Decision Summary

| image_id | scene | scene description | decision | rationale |
|----------|-------|-------------------|----------|-----------|
| IMG001 | S001 | Pre-dawn island extreme wide (HOOK) | **C — AI fallback** | C001-A CC BY-SA blocked. C001-C (CC BY 2.0 aerial) creates visual repeat with IMG006 (S007). AI produces unique sea-level pre-dawn image. |
| IMG007 | S008 | Building 30 exterior, 9-story (ACT_I) | **C — AI fallback** | C008-A CC BY-SA blocked AND wrong structure (mine hoistroom ≠ Building 30). AI resolves both simultaneously. |
| IMG016 | S020 | Island at dusk, extreme wide (ACT_IV) | **C — AI fallback** | C020-A CC BY-SA blocked. C020-C creates visual repeat. AI produces unique warm-palette dusk image. Upgrade to paid stock recommended before publish. |

**AI% impact: none.** All three slots were already source_type=AI_GENERATE in image_plan.json metrics. Generating AI images for these slots does not change the AI count (15) or the 75% compliance position.

---

## Decision Detail — IMG001 / S001 — HOOK Establishing Shot

**Why it's on legal hold:** C001-A (Hashima_Island_2023.jpg) is CC BY-SA 4.0. Color grade + motion = derivative. Legal risk: MEDIUM-HIGH.

**Why not C001-C (aerial CC BY 2.0):** C001-C is the same file as IMG006 (S007). Both S001 (0:00) and S007 (~2:35) would use the same source photograph, creating a visible visual repeat in the first three minutes of the video. The aerial framing (top-down) also conflicts with S001's description: "Full silhouette of ruined island in pre-dawn mist. Extreme wide. Dark and still." — the scene calls for a sea-level perspective, not aerial.

**AI fallback:** Safe documentary extreme wide of island ruins at sea level, pre-dawn, dark blue-black palette, cold and still. Narration ("かつて、ここに5,259人が暮らしていました。") delivers maximum weight over a totally still, dark, desolate image.

**Visual differentiation confirmed:**
- vs IMG006 (S007): aerial daylight real photo vs sea-level pre-dawn AI — opposite in altitude, palette, time of day
- vs IMG019 (S023): ferry bow in foreground vs no vessel — different composition entirely
- vs IMG016 (S020): cold blue-black vs warm amber — narrative arc contrast reinforced

**Midjourney command:**
```
/imagine Extreme wide shot of a ruined uninhabited island at pre-dawn, dark silhouette of large concrete tower blocks and ruin structures rising from calm black sea water, faint deep blue predawn light on the horizon behind the island, low mist drifting at water surface level, island fills the center of frame as a dark architectural mass, no vessels, no people, bare desolate seascape, documentary wide establishing shot, deeply desaturated cold blue-black palette, 35mm film, film grain, cinematic --ar 16:9 --no people, human figures, boats, vessels, tourists, modern structures, text, logos, watermark, warm tones, bright colors, sunlight, orange, red, golden hour, color saturation --v 6.1 --q 2
```

**Output filename:** `IMG001_S001_island_establishing_predawn.png`
**Folder:** `assets/ai_images/generated/batch_3/`
**Post-process:** slow_pan_right, 10 seconds, no color warming.

---

## Decision Detail — IMG007 / S008 — Building 30 Exterior

**Why it's on legal hold:** C008-A (第四竪坑捲座跡-01.jpg) is CC BY-SA 4.0. Same SA clause risk. Legal risk: MEDIUM-HIGH.

**Critical structural mismatch — CONFIRMED:** Scene.json S008 specifies: "Exterior of Building 30 (30-go-to). 9-story concrete apartment complex. Rust and moss. Crumbling window frames." The curated candidate C008-A shows the Fourth Mine Pit Hoistroom (第四竪坑捲座跡) — industrial mining infrastructure, a different building and purpose. The narration (L008) explicitly mentions "コンクリートの集合住宅「30号棟」が建設されます。当時の日本における最古級の鉄筋コンクリート造集合住宅のひとつとされる建物です。" — Building 30 as a landmark residential concrete construction. Showing a mine hoistroom here would create a factual mismatch between image and narration.

**AI fallback resolves both problems:** The prompt specifies the Building 30 character directly: 9-story concrete residential block, rust staining, moss, crumbling window frames. No legal exposure. Architecturally correct.

**Note on paid alternative (Getty):** Getty RF (900+ Gunkanjima images) is the correct paid fallback for Building 30 specifically. Search: 30号棟 端島 / Hashima Building 30. This is the upgrade path if Building 30 real photography is required before publish.

**Midjourney command:**
```
/imagine Exterior facade of a massive abandoned 9-story concrete residential apartment block, looking slightly upward at the weathered concrete facade with rows of empty window frames across all floors, heavy rust staining cascading down the grey concrete surface, moss and small vegetation colonizing cracks in the walls, several window frames crumbling and partially collapsed, scale is immense against the overcast sky, medium-wide angle shot, abandoned and desolate, no people, early 20th century reinforced concrete construction in advanced decay, dark documentary style, deeply desaturated grey-green palette, film grain, cinematic --ar 16:9 --no people, human figures, modern signage, modern buildings, text, logos, watermark, bright colors, glass windows intact, scaffolding, construction equipment, vehicles, cars, colorful facades --v 6.1 --q 2
```

**Output filename:** `IMG007_S008_building30_exterior.png`
**Folder:** `assets/ai_images/generated/batch_3/`
**Post-process:** ken_burns_zoom_in, 15 seconds, slow zoom toward upper floors to convey monumental scale.

---

## Decision Detail — IMG016 / S020 — ACT_IV Contemplative Dusk Wide

**Why it's on legal hold:** C020-A (Hashima_Island_ruins_1.jpg) is CC BY-SA 4.0. Same SA concern. Legal risk: MEDIUM-HIGH.

**Why not C020-C (aerial CC BY 2.0):** C020-C is the same aerial as IMG006 (S007) — using it for S020 creates a visual repeat. Asset_decision_matrix classified C020-C as "last resort before paid stock." S020 is the final image before the 40-second Ma beat silence — the highest emotional position in the video. An aerial repeat at this position would significantly undercut the contemplative resolve of ACT_IV.

**AI fallback:** Warm dusk extreme wide. Island at golden hour, amber palette, calm sea with sky reflection. Narration covers the 2015 UNESCO inscription — a formal recognition of permanence. The warm palette provides visual counterpoint to S001's cold darkness: the video opens in mystery and closes in something closer to acceptance. Very_slow_pan_right over 40 seconds.

**Upgrade flag:** This slot is the strongest case for paid stock in the entire project. PIXTA dusk photography of Hashima (軍艦島 夕暮れ) at ~¥5,000-¥15,000 would produce a significantly stronger result than AI for a 40-second contemplative scene. AI fallback COMPLETES the pipeline. Paid stock IMPROVES the result. Recommend the upgrade before final publish, not as a production blocker.

**Visual differentiation confirmed:**
- vs IMG001 (S001): cold blue-black pre-dawn vs warm amber dusk — opposite color temperature, 9-minute narrative gap
- vs IMG006 (S007): real aerial daytime vs warm-light sea-level AI — opposite palette and perspective

**Midjourney command:**
```
/imagine Extreme wide panoramic shot of a ruined uninhabited island at dusk, golden amber light of late afternoon casting warm tones across weathered concrete ruin structures, large concrete tower blocks and collapsed buildings reflected in calm still sea water, wide sky with soft clouds catching the golden light, island occupies center-to-left of the wide frame with expanse of calm sea visible, serene and vast, no vessels, no people, quiet reflective atmosphere, documentary wide shot, warm desaturated amber and grey palette, film grain, 35mm cinematic --ar 16:9 --no people, human figures, boats, vessels, tourists, text, logos, watermark, bright saturated colors, rain, dark storm clouds, neon, modern structures, cold blue tones, nighttime --v 6.1 --q 2
```

**Output filename:** `IMG016_S020_island_dusk_wide.png`
**Folder:** `assets/ai_images/generated/batch_3/`
**Post-process:** very_slow_pan_right, 40 seconds. Ensure image is wide enough to pan without running out of horizontal content.

---

## Flag Word Audit — All Three Prompts

| image_id | haunting | oppressive | terrifying | horror | ghostly | nightmare | cursed | melancholic |
|----------|----------|------------|------------|--------|---------|-----------|--------|-------------|
| IMG001 | NO | NO | NO | NO | NO | NO | NO | NO |
| IMG007 | NO | NO | NO | NO | NO | NO | NO | NO |
| IMG016 | NO | NO | NO | NO | NO | NO | NO | NO |

**All prompts: CLEAN. Generation may begin.**

---

## AI% Impact

| Metric | Before | After |
|--------|--------|-------|
| AI images | 15 | 15 (no change) |
| Real images | 2 | 2 (no change) |
| AI% | 75.0% | 75.0% |
| COMP-001 | resolved_at_limit | resolved_at_limit |

These three slots were already counted as AI (source_type: AI_GENERATE) in image_plan.json global metrics. Generating AI images for them does not change the compliance count. AI% stays at 75%.

---

## Confirmed Image Status — After Decisions

| image_id | scene | status |
|----------|-------|--------|
| IMG001 | S001 | AI fallback approved — generation ready ← **THIS DECISION** |
| IMG002 | S002 | APPROVED_WITH_MINOR_NOTES ✓ |
| IMG003 | S003 | APPROVED ✓ |
| IMG004 | S005 | APPROVED_WITH_MINOR_NOTES ✓ |
| IMG006 | S007 | REAL_PHOTO_LICENSED (CC BY 2.0) ✓ |
| IMG007 | S008 | AI fallback approved — generation ready ← **THIS DECISION** |
| IMG008 | S009 | APPROVED_WITH_MINOR_NOTES ✓ |
| IMG009 | S011a | APPROVED — FIX-M1 cleared ✓ |
| IMG010 | S011b | APPROVED ✓ |
| IMG011 | S013 | APPROVED_WITH_MINOR_NOTES ✓ |
| IMG012 | S015 | APPROVED ✓ |
| IMG013 | S016 | APPROVED ✓ |
| IMG014 | S017 | APPROVED ✓ |
| IMG015 | S018 | APPROVED ✓ |
| IMG016 | S020 | AI fallback approved — generation ready ← **THIS DECISION** |
| IMG017 | S021 | APPROVED ✓ |
| IMG018 | S022 | APPROVED ✓ |
| IMG019 | S023 | APPROVED ✓ |
| IMG020 | S024 | REAL_PHOTO_LICENSED (Japan Govt 1974) ✓ |
| IMG005 | S009 | SUPPRESSED |

**16 of 20 images confirmed/approved.** 3 slots need new AI generation (Batch 3). 1 suppressed.

---

## Can the Image Asset Phase Complete After Batch 3?

**YES — if Batch 3 generates and passes QA, the image asset phase is complete.**

Required steps:
1. Generate IMG001, IMG007, IMG016 (Batch 3) using the Midjourney commands in this report
2. Save to `assets/ai_images/generated/batch_3/`
3. Run standard QA on all 3:
   - IMG001: no people, no vessels, cold dark blue-black palette, extreme wide
   - IMG007: exterior 9-story residential block, no people, rust and moss, correct scale
   - IMG016: dusk warm palette, no people, no vessels, wide enough for 40s pan
4. If any fail: up to 3 attempts each. Fallbacks documented in generation plan.
5. Upon QA pass: update image_plan.json → approved_for_production

**After image asset phase complete:** Voice recording (requires FIX-M3 timed read-through first) → Timeline assembly → Thumbnail render → SEO final → Publish.

---

## Remaining Open Items (Non-Image)

| item | priority | description |
|------|----------|-------------|
| FIX-M3 | HIGH | Timed read-through before talent session. 1,201 words, target 12 minutes. |
| IMG009 rename | ACTION | Rename IMG009_S010_mine_gate_attempt1.png → IMG009_S011a_mine_tunnel_approved.png |
| S020 paid stock upgrade | RECOMMENDED | Before final publish: consider PIXTA dusk shot for S020 (highest emotional position). Not a blocker. |
| CC BY-SA legal review | DEFERRED | One review would unlock S001/S008/S020 for real-photo upgrade. Not blocking pipeline. |

---

## Final Output

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LEGAL-HOLD IMAGE DECISION — COMPLETE

DECISION:
  IMG001  S001  → C: AI fallback (pre-dawn island wide)
  IMG007  S008  → C: AI fallback (Building 30 exterior)
  IMG016  S020  → C: AI fallback (dusk island wide)
                   ⚑ upgrade recommended before publish

WHY NOT CC BY-SA:
  Color grade + film grain + Ken Burns motion
  likely trigger ShareAlike clause. No legal
  review completed. Zero CC BY-SA in any prompt.

WHY NOT REUSE AERIAL (C001-C / C020-C):
  Both reuse the same file as IMG006/S007.
  Visual repeat within first 3 minutes (S001)
  and at emotional climax (S020). Rejected.

IMG007 STRUCTURE MISMATCH RESOLVED:
  C008-A was the wrong candidate (mine hoistroom
  vs Building 30 residential). AI fallback writes
  directly to scene spec: 9-story concrete
  apartment block, rust, moss, crumbling windows.

FLAG WORD SCAN:
  All 3 prompts CLEAN (8 words checked per prompt)

AI% IMPACT:
  Before: 75.0%  |  After: 75.0%  |  No change
  (slots were already counted as AI in metrics)

NEW BATCH 3 — GENERATION NEEDED:
  YES — 3 images to generate

OUTPUT FILENAMES:
  IMG001_S001_island_establishing_predawn.png
  IMG007_S008_building30_exterior.png
  IMG016_S020_island_dusk_wide.png
  → Folder: assets/ai_images/generated/batch_3/

CONFIRMED IMAGES AFTER DECISIONS:
  16 of 20 confirmed (approved or legally registered)
   3 of 20 pending Batch 3 generation + QA
   1 of 20 suppressed (IMG005)

CAN IMAGE ASSET PHASE COMPLETE?
  YES — after Batch 3 generation + QA passes.
  No other image work remains.

NEXT STEPS AFTER BATCH 3:
  → Voice recording (FIX-M3 read-through first)
  → Timeline assembly
  → Thumbnail render
  → SEO final
  → Publish
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
