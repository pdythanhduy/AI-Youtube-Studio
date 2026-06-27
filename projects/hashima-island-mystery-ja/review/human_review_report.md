# Human Review Report — 端島 / 軍艦島：消えた都市の謎
**Reviewer:** Human Review Gate v1
**Date:** 2026-06-27
**Files reviewed:** 13
**Decision: GO WITH FIXES**

---

## Issue Summary

| ID | Severity | Category | Short Description |
|---|---|---|---|
| B1 | BLOCKER | SEO/Accuracy | Title Option B is factually false — 「一夜で消えた」 |
| H1 | HIGH | Visuals | 85% AI images, zero licensed/stock footage fallback |
| H2 | HIGH | Visuals | 15+ scenes missing motion direction — will produce a slideshow |
| H3 | HIGH | Visuals | S022 timecode vs. description contradiction |
| M1 | MEDIUM | Visuals | PROMPT_008 "no people" insufficient for AI generators |
| M2 | MEDIUM | Script | 「企業城下島」— coined term not in standard Japanese use |
| M3 | MEDIUM | Script | Word count self-certified; morae/min not verified |
| M4 | MEDIUM | SEO | 「消えた」framing needs in-video clarification within 30s |
| L1 | LOW | Voice | "NHKアナウンサー的" direction is ambiguous for this tone |
| L2 | LOW | SEO | 「廃島」is not an established Japanese search term |
| L3 | LOW | SEO | Checklist mixes production requirements with advice |

**BLOCKER count: 1**
**HIGH count: 3**
**MEDIUM count: 4**
**LOW count: 3**

---

## BLOCKER Issues

### B1 — Title Option B: Factually False
**File:** `seo/youtube_seo.md`
**Location:** Option B title

```
【廃墟の島】端島・軍艦島 なぜ5000人が一夜で消えたのか？
```

**Problem:** 「一夜で消えた」(disappeared overnight) is factually incorrect.
- Closure announced: 1974年1月15日
- Last residents departed: 1974年4月20日
- This is a 3-month process, not a single night.

The research (VF8) correctly documents this as two separate dates. The script correctly distinguishes them. This title directly contradicts the verified facts produced by Stage 1.

Additionally, 「5000人」rounds down from 5,259 — inconsistent with how every other document treats this number.

**Classification:** BLOCKER — publishing this title creates a verifiable factual error. It also sets up a viewer disappointment loop: they click expecting a mystery about how people vanished overnight; the video correctly explains a planned economic closure.

**Required fix:** Delete Title Option B from `seo/youtube_seo.md` entirely. Do not offer it as an alternative. It cannot be salvaged.

---

## HIGH Issues

### H1 — Visual Asset Strategy: 85% AI Images, No Stock Fallback
**File:** `visuals/image_plan.csv`

17 of 20 images (85%) are AI_GENERATE. Zero are designated as licensed stock footage or real documentary photographs. The notes say "real footage preferred" for only one scene (S023, LOW priority).

**Problem:** Hashima Island is one of the most photographed locations in Japan. Getty, Shutterstock, Aflo, and Japanese news archives have extensive licensed imagery. AI-generated images of this island will look generic compared to real photography — and more importantly, competitor videos already use real drone footage, real interiors, and real historical photographs. A 100% AI-generated visual package will be identifiable as such by the Japanese audience, who is highly familiar with the actual island's appearance.

There is also a transparency obligation: the video presents documentary-style narration. Using 100% AI visuals without disclosure is an increasing ethical and platform-policy risk.

**Required fix:** For at minimum scenes S001, S007, S008, S020, S024 (all HIGH priority wide/establishing shots), the image_plan must add a `stock_footage_source` column listing licensed agencies to check (Getty Images Japan, アフロ, 長崎市観光写真素材) before defaulting to AI generation. AI remains fallback, not primary, for establishing shots of a real location.

### H2 — Scene Motion: Missing Direction on 15+ Scenes
**File:** `visuals/scene_list.csv`

Reviewing each scene's `notes` column for motion direction:
- S001: "Slow pan" — OK
- S002, S003, S005, S007, S008, S009, S010, S011, S012, S013, S015, S016, S017, S018, S019, S021, S023, S024: **No motion direction.**

These scenes range from 10 to 50 seconds long. A static AI-generated still held on screen for 30–50 seconds without any movement is not a video — it is a slideshow. Every professional documentary uses Ken Burns effect, slow zoom, parallax, or actual footage movement on every scene longer than 5 seconds.

S011 is the worst case: a single dark tunnel image held for 50 seconds (4:10–5:00) with no motion direction. This will lose viewer attention at the most important thematic moment in the video.

**Required fix:** Add a `motion_direction` column to `scene_list.csv`. Every scene must have explicit motion instruction: `slow_zoom_in`, `slow_pan_left`, `ken_burns`, `parallax`, `static_with_overlay`, or `actual_footage`. No scene should be `static` unless it is the Ma beat (S022) or a title card (S004, S014).

### H3 — S022 Timecode vs. Description Contradiction
**File:** `visuals/scene_list.csv`, line S022

```
S022,10:20,11:00,ACT4,...,10 seconds of silence.
```

Timecode: 10:20 to 11:00 = **40 seconds**.
Notes say: "10 seconds of silence."
`voice_script.txt` says: "[NO NARRATION — 10 seconds of music and waves only]"
`script.md` says: "波の音。10秒間。"

The scene occupies 40 seconds in the timeline but all other documents describe only 10 seconds of narration-free content. There are 30 unaccounted seconds.

**Possibilities:**
1. The 40-second slot is: 30 seconds of narrated ACT IV + 10-second silence. But the script puts the silence at the END of ACT IV, and S022 is listed as the entire Ma beat sequence.
2. The scene was intended to be 10 seconds but the timecode was incorrectly set.
3. The Ma beat was expanded to 40 seconds at scene level without updating the script.

This inconsistency will cause confusion at edit. The editor will cut 40 seconds to this scene but the voice script only accounts for 10 seconds of silence.

**Required fix:** Decide which is correct — 10 or 40 seconds of silence — and update all three files consistently. If the Ma beat is 40 seconds, update `voice_script.txt` to say "[NO NARRATION — 40 seconds of music and waves only]" and update `script.md` accordingly. If 10 seconds, correct the timecode in `scene_list.csv` to 10:20–10:30 and restructure the surrounding scenes.

---

## MEDIUM Issues

### M1 — PROMPT_008: "No People" Is Not Reliable
**File:** `visuals/ai_image_prompts.md`, PROMPT_008

The prompt uses `--no people` as the only safeguard against human depictions in the mine scene. Current image AI tools (Midjourney v6, DALL-E 3, Stable Diffusion XL) frequently generate silhouettes, partial figures, or implied human presence even with explicit negative prompts. This scene represents the forced labor period (1939–1945). If the generated image contains even a silhouette of a person in a mine tunnel, the visual will imply a depiction of the forced labor itself — the one thing the project explicitly prohibits.

The prompt notes say "CRITICAL — Must be abstract and atmospheric ONLY" but provide no escalation path if the generated output fails this check.

**Required fix:** Add to PROMPT_008 notes a mandatory human-review gate:
- If generated image contains any human form, silhouette, or implied human presence → reject and regenerate.
- If regeneration fails 3 times → replace this scene with concrete texture (PROMPT_013) or a different non-mine visual.
- Under no circumstances approve a mine image with human figures for this project.

### M2 — 「企業城下島」Is a Coined Term
**File:** `script/script.md`, ACT I

```
以来、島全体が一企業によって管理される、前代未聞の「企業城下島」となりました。
```

「企業城下島」is not a common Japanese term. 「城下町」(castle town, company town) is well understood. 「企業城下島」is an invented compound. For a general Japanese YouTube audience, this may cause a comprehension hiccup at a moment when the narration should be delivering clear information.

**Required fix:** Replace with: 「以来、島全体がひとつの企業によって管理される、前代未聞の島となりました。」 
Or alternatively, use the more recognizable framing: 「三菱が、島そのものを所有する形となったのです。」

### M3 — Word Count Self-Certified, Morae Rate Unverified
**File:** `script/script.md`, word count table

The word count table claims 1,201 "words." Japanese narration rate is measured in morae (拍), not words. The pipeline targets 300 morae/min × 12 min = 3,600 morae. The self-reported count of 1,201 "words" cannot be cross-validated against a morae count without actual counting.

Concretely: Japanese has an average of 2–3 morae per written character. The script narration text (estimated ~2,800–3,200 characters including kanji and kana) would yield approximately 2,800–3,200+ morae — potentially too fast if narrated at normal documentary pace, or the word-count methodology is measuring kanji compounds as single "words" while the actual morae count is higher.

**Risk:** Voice recording runs over 12 minutes with the [slow] pacing instructions, or under if the narrator interprets "slow" loosely.

**Required fix:** Before sending to voice recording, have a Japanese native speaker do a timed read-through of `voice/voice_script.txt` with all [slow] and [PAUSE:2s] instructions applied. Adjust script length if the timed read deviates more than ±45 seconds from 12:00.

### M4 — 「消えた」Framing Needs In-Video Clarification
**Files:** `seo/youtube_seo.md` (Title Option A), `visuals/scene_list.csv` (HOOK)

Title Option A: 「5,259人が消えた日」
Thumbnail Concept A: 「5,259人が消えた」

「消えた」(disappeared/vanished) has mystery/supernatural connotations in Japanese media. The video is a dark documentary about an economic closure — not a mystery about missing persons. If the hook does not immediately clarify that "disappeared" means "left voluntarily due to economic closure," viewers who click expecting a supernatural mystery will feel misled.

The current HOOK script does this correctly: 「そして、ある日——すべてが消えました。」immediately transitions into a historical explanation. But the visual sequence (S001–S004) shows only ruins and a title card before any narration context is given. The title card itself says only 「端島 / 軍艦島」without context.

This is acceptable for mystery niche framing, but the risk is that some viewers will interpret the "mystery" as being about the forced labor disappearances rather than the 1974 closure — which is a much more ethically loaded implication.

**Required fix:** In the first 60 seconds of narration, confirm that the economic closure context is clear before the forced labor history section. The current script does achieve this, but the editor must be explicitly briefed that the HOOK title card must NOT sit on screen longer than specified — the economic context narration begins at 1:00 and cannot be delayed.

---

## LOW Issues

### L1 — Voice Direction: "NHKアナウンサー的" Is the Wrong Reference
**File:** `voice/voice_direction.md`

```
標準語 / NHKアナウンサー的発音
```

NHK announcer delivery is crisp, formal, and emotionally neutral — it is news anchor style. This video is dark_documentary style with heavy use of [slow] pacing and Ma beats. An NHK announcer delivery will produce clinical, detached reading that conflicts with the atmospheric tone the script requires.

Better reference: NHKドキュメンタリー (not news), 岩波ドキュメンタリー, or specifically the narrator style of NHKスペシャル — which uses slower, warmer delivery than the news desk.

The direction already mentions "NHKドキュメンタリーや、岩波ドキュメンタリーのようなスタイルを参考にしてください" later in the same document, which is the correct reference. The "NHKアナウンサー的発音" phrase in the profile table should be updated to avoid contradicting this.

**Required fix:** Change `voice_direction.md` narrator profile: 「標準語 / NHKアナウンサー的発音」→「標準語 / NHKドキュメンタリーナレーター的な語り口」

### L2 — Tag 「廃島」Has No Established Search Volume
**File:** `seo/youtube_seo.md`

「廃島」is not an established Japanese compound. YouTube tag searches for this term will return near-zero results. The space should be given to a higher-value alternative such as 「廃墟島」or 「軍艦島 ドキュメンタリー」.

**Required fix:** Replace 「廃島」with 「廃墟島」in the tags list.

### L3 — SEO Publishing Checklist Mixes Requirements with Opinions
**File:** `seo/youtube_seo.md`

```
- [ ] Premiere mode: Recommended for first 48 hours
```

"Premiere mode" is a channel-strategy decision, not a production requirement. It should not appear in a production checklist without a qualification. Similarly, the specific publish time "20:00 JST" is advice, not a requirement, and will vary by channel analytics.

**Required fix:** Move "Premiere mode" and "Publish time" items from the checklist into a separate "Channel Strategy Notes" section to distinguish production requirements from operational recommendations.

---

## What Passed Without Issue

- Factual accuracy: VF1–VF11 correctly handled. All FLAG adjustments properly applied.
- Register: です/ます throughout script. No breaches.
- Japan template: All 4 beats present. 5× [PAUSE:2s] correctly placed. Ma beat present.
- No fabricated URLs anywhere in any file.
- No exaggerated mystery claims in the body content (title is the only risk area).
- PROMPT_008 intent is correct — atmospheric only, no people — risk is in execution, not intent.
- Skyfall (VF12, UNVERIFIED): correctly dropped from script. Not mentioned anywhere.
- Hook word count: ~55 words of narration. Under the 65-word limit.
- Forced labor history: correctly attributed to UNESCO record. Numbers not asserted. Both governments' positions noted.
- Story bible canonical names, dates, and off-limits expressions are all consistent with the script.

---

## Final Decision

**GO WITH FIXES**

The core content — script, research, source verification, story bible, voice direction — is production-ready with minor corrections. The pipeline is blocked only by one SEO item (B1) and three visual execution issues (H1, H2, H3) that must be resolved before the editor begins assembly.

No rewrite required. Targeted edits only.

See `production_go_no_go.md` for the exact fix command list.
