# Visual Risk Report — 端島 / 軍艦島：消えた都市の謎
**Reviewer:** Human Review Gate v1
**Files reviewed:** visuals/scene_list.csv, visuals/image_plan.csv, visuals/ai_image_prompts.md
**Date:** 2026-06-27

---

## Scene Count and Coverage: Adequate?

**24 scenes for 12 minutes.**

Average scene duration: 30 seconds.

Verdict: Scene COUNT is sufficient. A 12-minute video at 30-second average per scene is industry standard. The problem is not count — it is execution. See motion direction issues below.

---

## Scene Duration Analysis

| Scene | Duration | Shot Type | Motion Direction | Risk |
|---|---|---|---|---|
| S001 | 10s | EWS | "Slow pan" noted | OK |
| S002 | 15s | Medium | None specified | MEDIUM |
| S003 | 15s | CU | None specified | MEDIUM |
| S004 | 20s | Title card | N/A | OK |
| S005 | 40s | Archival | None specified | HIGH — 40s static archival still |
| S006 | 30s | Animated map | Motion inherent | OK |
| S007 | 35s | Aerial/CG | None specified | HIGH — 35s for an "aerial" still |
| S008 | 15s | Med wide | None specified | LOW — short duration |
| S009 | 40s | Medium | None specified | HIGH — 40s tourist boat shot |
| S010 | 30s | CU | None specified | MEDIUM |
| S011 | 50s | CU/Atmos | None specified | **BLOCKER-LEVEL for editor** — 50s dark tunnel still |
| S012 | 30s | Graphic | Motion inherent | OK |
| S013 | 30s | Wide | None specified | MEDIUM |
| S014 | 30s | Text overlay | Motion inherent | OK |
| S015 | 30s | Medium | None specified | MEDIUM |
| S016 | 30s | CU | None specified | MEDIUM |
| S017 | 30s | Medium | None specified | MEDIUM |
| S018 | 30s | Wide | None specified | MEDIUM |
| S019 | 30s | ECU | None specified | LOW — texture shot works static |
| S020 | 40s | EWS | "Very slow movement" noted | MEDIUM — needs explicit direction |
| S021 | 40s | CU | None specified | HIGH — 40s faded sign static |
| S022 | 40s | Wide | N/A (Ma beat) | INTENTIONAL — acceptable |
| S023 | 30s | Medium | None specified | MEDIUM |
| S024 | 30s | EWS | None specified | MEDIUM — final frame needs motion |

**Scenes with HIGH motion risk:** S005, S007, S009, S011, S021
**Scenes with MEDIUM motion risk:** S002, S003, S010, S013, S015, S016, S017, S018, S020, S023, S024

S011 is the critical failure: 50 seconds, single dark tunnel image, no motion instruction, during the most emotionally significant section (forced labor history). This will fail in the edit suite and must be addressed before the editor begins.

---

## AI Image Overuse Assessment

| Category | Count | % |
|---|---|---|
| AI_GENERATE | 17 | 85% |
| MOTION_GRAPHICS | 3 | 15% |
| Real licensed photography | 0 | 0% |
| Real stock footage | 0 | 0% |

**Assessment: HIGH RISK**

Hashima Island has been photographed extensively. The following image categories have real photography available through Japanese licensing agencies (Getty Images, アフロ, 時事通信フォト, 朝日新聞フォトアーカイブ):
- Island exterior (S001, S020, S024)
- Building 30 exterior (S008)
- Historical photographs of the island during operation
- Current ruin exterior shots from permitted tourist zones
- UNESCO registration ceremony photographs

Using AI-generated images for well-documented real locations creates a credibility gap. Japanese viewers who have seen the island in person or in other documentaries will recognize that the images do not look like the real Hashima Island. AI island images will not match the actual distinctive shape of the island.

**Specific risk by scene:**

| Scene | Risk | Reason |
|---|---|---|
| S007 (aerial) | HIGH | The actual aerial shape of Hashima is extremely well-known. AI will generate a plausible-looking island, not the real one. Viewers will notice. |
| S001, S020, S024 (exterior wide) | HIGH | Same reason. The silhouette of Hashima is iconic. AI cannot reproduce the actual building layout. |
| S005 (Meiji era archival) | MEDIUM | Real Meiji industrial photographs exist through historical archives. AI simulation is acceptable as labeled "illustrative" but real archival material is better. |
| S011 (mine) | LOW | Real coal mine interiors from Hashima are not publicly available; AI is appropriate here. |
| S009 (tourist boat) | MEDIUM | Tourist footage of the island approach is readily available from tour operators and existing YouTube channels. This could be licensed. |

**Verdict:** The image_plan must be revised to classify images as AI_GENERATE ONLY when no licensable real photography exists for that angle/subject. At minimum, S001, S007, S020, S024 should be marked as "SEEK REAL PHOTOGRAPHY FIRST — AI as fallback only."

---

## PROMPT_008 — Human Depiction Risk (Mine Scene)

**Scene:** S011 (4:10–5:00, 50 seconds)
**Subject:** Coal mine interior, forced labor era

**Current prompt:**
```
Abstract mine tunnel interior, narrow passage disappearing into darkness, single dim light source casting harsh shadows on rough rock walls, deep shadow, noir lighting, oppressive atmosphere, no people, abstract and atmospheric, cinematic close-up perspective --ar 16:9 --no people, modern equipment, text
```

**Risk analysis:**
1. "no people" appears in the negative prompts (`--no people`) — this is correct.
2. However, Midjourney v6, DALL-E 3, and SDXL regularly generate human figures (silhouettes, partial figures, shadows that read as human) in mine/tunnel scenes even with "no people" explicitly blocked. Tunnel imagery strongly conditions these models toward human presence.
3. The prompt uses "oppressive atmosphere" — this is descriptive of the emotional content but also biases the model toward generating confinement/suffering imagery, which increases the likelihood of human-coded outputs (shadows, silhouettes, implied bodies).
4. The 50-second duration means this single image will carry significant visual weight. If it fails — if any silhouette appears — it creates a documentary depiction of forced labor victims that was explicitly prohibited.

**Verdict:** MEDIUM risk. The intent is correct. The execution requires a mandatory human-review gate that is not currently specified in any project file.

**Required additions to PROMPT_008:**
- Add in Notes: "If any human form, silhouette, or shadow readable as human is present in generated output → reject immediately. Do not use."
- Add fallback: "If rejection occurs 3+ times → substitute with PROMPT_013 (concrete texture) for this scene. Do not attempt to generate a mine interior with people in it."
- Consider strengthening negative prompt: `--no people, silhouettes, figures, shadows of people, human shapes, implied human presence, bodies`

---

## S022 Timecode Contradiction

**Scene S022:** 10:20–11:00 = 40 seconds
**Script description:** "10秒の完全な沈黙区間"
**Voice script:** "[NO NARRATION — 10 seconds of music and waves only]"

This is a 30-second discrepancy. The scene occupies 40 seconds in the timeline but only 10 are accounted for by the Ma beat silence specification.

**Options:**
1. Correct the scene to 10:20–10:30 (10 seconds) and add a new scene S022b for the remaining 30 seconds with appropriate visuals/narration.
2. Expand the Ma beat to 40 seconds and update voice_script.txt and script.md accordingly.

**Recommendation:** Option 2 — extend the Ma beat to 40 seconds. The Japan template allows this. A 40-second silence with ocean visuals is a stronger Ma beat than 10 seconds. Update voice_script.txt to read: "[NO NARRATION — 40 seconds of music and ocean waves only]"

---

## Title / Thumbnail Disrespect Assessment

### Title Option A: 「軍艦島の真実：5,259人が消えた日【端島の謎】」
**Assessment:** "消えた日" refers to the 1974 departure. "真実" (the truth) is standard mystery-niche framing. No disrespect to forced labor victims as the phrasing refers to the 1974 economic closure. Acceptable.

### Title Option B: 「なぜ5000人が一夜で消えたのか？」
**Assessment:** FACTUALLY FALSE (not overnight), BLOCKED. Additionally potentially disrespectful by trivializing a documented historical process into sensational "one night" framing. DELETE.

### Title Option C: 「端島（軍艦島）完全解説…」
**Assessment:** Neutral and descriptive. No disrespect risk. Acceptable.

### Thumbnail Concept A: 「5,259人が消えた」
**Assessment:** The phrase "消えた" applied to residents leaving in 1974 is not inherently disrespectful. It is mystery-niche vocabulary. The thumbnail does not reference the forced labor victims specifically. Acceptable.

### Thumbnail Concept C: 「誰が消えたのか」
**Assessment:** "Who disappeared?" as applied to a 1974 economic closure is borderline. The "who" framing could imply ambiguity about whether people died or vanished mysteriously. However, the video content corrects this immediately. Risk is LOW but real.

**Disrespect verdict:** The only disrespect risk is using the forced labor era as a mystery hook — which this project avoids. The titles/thumbnails are all keyed to the 1974 departure, not to wartime atrocities. No disrespect flag on the approved title options (A or C).

---

## Visual Risk Summary

| Issue | Severity | Action |
|---|---|---|
| No motion direction on 15+ scenes | HIGH | Add motion direction column to scene_list.csv |
| S011: 50s static tunnel, no motion | HIGH | Subdivide scene or add Ken Burns/animation direction |
| 85% AI images for a well-photographed real location | HIGH | Revise image_plan to seek real licensed photography for S001, S007, S008, S020, S024 first |
| S022 timecode vs script contradiction | HIGH | Standardize to 40s and update voice_script.txt and script.md |
| PROMPT_008 lacks mandatory human-review gate | MEDIUM | Add explicit reject/fallback instructions to prompt notes |
| Title Option B factually false | BLOCKER | Delete from seo/youtube_seo.md |
