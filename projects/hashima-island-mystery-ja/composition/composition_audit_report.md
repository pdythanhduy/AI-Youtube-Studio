# Composition Audit Report
## hashima-island-mystery-ja
**Date:** 2026-06-27
**Audited against:** `japan_mystery_lost_place` composed template
**Manifest:** `CM-2026-japan-mystery-lost-place`
**Auditor:** Phase 3 Migration

---

## Executive Summary

| Metric | Value |
|---|---|
| Overall compliance score | **78 / 100** |
| Composition-ready | **NO** |
| Blockers | **3** |
| High | 6 |
| Medium | 7 |
| Low | 4 |
| Info | 3 |

**Composition-ready requirement:** 0 BLOCKERs, 0 HIGH issues, thumbnail selected, title selected. Current state is 3 BLOCKERs + 6 HIGH issues unresolved.

---

## Dimension Scores

| Dimension | Score | Weight | Weighted |
|---|---|---|---|
| Creator (anh_duy) | 85 | 20% | 17.0 |
| Platform (youtube_long_form) | 60 | 20% | 12.0 |
| Audience (general) | 88 | 10% | 8.8 |
| Documentary (base genre) | 72 | 15% | 10.8 |
| Mystery (primary genre) | 82 | 15% | 12.3 |
| Japan (modifier) | 92 | 10% | 9.2 |
| Lost Place (modifier) | 80 | 10% | 8.0 |
| **Overall** | | | **78.1** |

---

## Section 1 — Creator Profile Compliance (anh_duy)

**Score: 85 / 100**

### ✅ Curiosity over fear

The hook (L001-L003) is atmospheric and curious — "かつて、ここに5,259人が暮らしていました" establishes wonder, not fear. No horror framing present anywhere. L014-L016 handle forced labor with factual restraint ("連行された人々が…働かされました" — calm, documented phrasing). Primary emotional target throughout is curiosity and reflective melancholy.

### ✅ Trust over shock

TITLE_B deleted (FIX-B1) because "一夜で消えた" was factually false. THUMB_B deleted for unverified forced labor death statistics. These deletions demonstrate proactive trust protection. The content_declaration in seo.json acknowledges the dispute and discloses the dual-source methodology to viewers.

### ✅ Fact-based storytelling

13 verified facts (VF001-VF013) covering distance, construction dates, population counts, closure dates, UNESCO designation, and forced labor acknowledgment. Every narration line that makes a factual claim references at least one fact_id. Disputed content (L016) is clearly framed as disputed without asserting a resolution.

### ✅ Respectful tone

Forced labor history handled with measured, restrained language. Ma beat (S022) provides respectful silence after the emotional weight of the UNESCO/dispute section. S016 visual description frames personal items as "evidence of hasty departure" not aesthetic objects. S011a enforced "no people rule."

### ✅ Repeat-viewer goal

L034 ends with an open question: "この島が、あなたに問いかけているものは——何でしょうか" (What is this island asking of you?). This is a philosophically open ending that invites reflection and return, not a resolved conclusion.

### ⚠️ Minor concerns

- AI image usage at 85% concerns fact-image credibility for a factual documentary
- L003 ("すべてが消えました") is dramatic rather than curious — does not explicitly pose the investigative question

---

## Section 2 — Platform Compliance (youtube_long_form)

**Score: 60 / 100**

### ✅ Duration

720 seconds = 12 minutes. Platform sweet spot: 480–1200 seconds. **PASS**

### ✅ Aspect ratio / resolution

dark_documentary style with 16:9 framing implied by image_plan.json global_style. **PASS** (not yet confirmed in timeline)

### ✅ Description and tags

seo.json description is 320 characters. Dispute disclosure included. 25 tags across primary/secondary/international. **PASS**

### ❌ Thumbnail not selected (BLOCKER — COMP-002)

`selected_concept_id = null`. YouTube requires a thumbnail.

### ❌ Thumbnail respect checks not done (BLOCKER — COMP-003)

`respect_check = false` on both THUMB_A and THUMB_C. Blocks thumbnail selection.

### ❌ Title not finalized (HIGH — COMP-005)

`selected_title_id = null`. TITLE_A is approved but not selected. Must be set before publish.

### ❌ Community guidelines review pending (HIGH — COMP-007)

`community_guidelines_review = "pending"`. Sensitive topics include forced_labor, historical_violence, political_dispute. Must be declared and reviewed.

### ⚠️ Chapter markers planned but not assembled (HIGH — COMP-006)

CH001-CH006 exist in timeline data but timeline assembly is not complete. YouTube chapter markers require exact timecodes embedded in the description at publish time. Cannot confirm functionality until timeline assembly is done.

### ⚠️ Subtitles: placeholder only (MEDIUM — COMP-015)

Subtitles are recommended for Japanese historical content. Currently a placeholder entry only. Dependent on voice recording completion.

---

## Section 3 — General Audience Compliance (general)

**Score: 88 / 100**

### ✅ No expert knowledge assumed

ACT_I is entirely cultural context. L005 explains Meiji industrialization. L006 establishes geographic location (15-18km from Nagasaki). L008 explains the significance of Building 30. L009 explains urban development of the island. History and geography are provided before analysis begins.

### ✅ Accessible language

desu/masu register throughout. Vocabulary is conversational Japanese. Technical terms (鉄筋コンクリート, 採掘権) appear but are used in context where meaning is inferable.

### ✅ Cultural context provided

BEAT_JPN_01 (cultural_context) is the entire ACT_I — 120 seconds of historical and geographic framing. Japanese Imperial calendar reference in L008 uses Western year first: "1916年——大正5年". Non-Japanese viewers get the Western year; Japanese viewers get the additional cultural reference.

### ✅ Self-contained

The video does not assume prior knowledge of Hashima. The story is complete from historical origin through abandonment through UNESCO designation through present day.

### ⚠️ Minor vocabulary concern

L008 uses "最古級の鉄筋コンクリート造集合住宅のひとつ" (one of the oldest reinforced concrete apartment buildings). This is architectural terminology but contextually clear. Not a significant barrier for a general Japanese audience.

---

## Section 4 — Documentary Genre Compliance

**Score: 72 / 100**

### ✅ Verified sources

13 verified facts (VF001-VF013). Sources referenced by every factual narration line. Research data includes Japanese-language sources (S004, S005, S007). Dual-source uncertainty on forced labor data explicitly documented and disclosed.

### ✅ No fabricated facts

All factual fixes applied (FIX-M2, FIX-M4, FIX-B1). Disputed facts labeled as disputed. Unverified claims either removed or flagged. The only uncited claim (L011 movie connection, COMP-020) is framed with "とされ" (is said to be) — a hedge marker, not an assertion.

### ✅ Emotional arc

Clear arc through 6 sections: curiosity (HOOK) → context (ACT_I) → moral complexity (ACT_II) → loss (ACT_III) → ambiguity (ACT_IV) → open question (OUTRO). Emotional trajectory is documentary-appropriate: wonder → respect → unresolved complexity.

### ❌ Real footage preference violated (BLOCKER — COMP-001)

Currently 85% AI-generated imagery (610/720 seconds). Composed template hard limit: 75% (540/720 seconds). 5 scenes marked stock_search_required (FIX-H1): S001, S007, S008, S020, S024.

---

## Section 5 — Mystery Genre Compliance

**Score: 82 / 100**

### ⚠️ Hook: curiosity framing present, explicit question absent (HIGH — COMP-009)

Template hook_duration_seconds: 30. Current HOOK: 60 seconds. The atmospheric opening (L001-L003) establishes that people lived here and then it "disappeared" but does not pose an explicit investigative question within the first 30 seconds. BEAT_MYS_01 requires the mystery to be "clearly posed within 30 seconds." The current approach is thematically valid but structurally undershoots the template target.

**Mitigating factor:** The Japan modifier's guiding principle explicitly values atmospheric slow openings and the "very_slow" pacing principle. The 60-second atmospheric HOOK may be an intentional and culturally appropriate design choice that prioritizes the Japan modifier over the Mystery base requirement. Human producer judgment required.

### ✅ Evidence-first structure

ACT_II presents evidence in logical sequence: cultural image (L011-L013) → forced labor fact (L014) → official acknowledgment (L015) → disputed numbers (L016) → UNESCO designation framing (L017). Each piece builds on the last.

### ✅ No fake certainty

L016 explicitly: "現在も、日本と韓国の双方で資料の記述が異なっています。歴史の検証は続いています。" (Records from Japan and Korea still differ. Historical verification continues.) This is the composed template's BEAT_MYS_03 in action.

### ✅ No exaggerated claims

FIX-M2 removed "企業城下島" (a reductive characterization). FIX-B1 removed false departure timing. FIX-M4 corrected the distance figure.

### ✅ Open-loop ending

L034: "この島が、あなたに問いかけているものは——何でしょうか" is a genuine philosophical open question. Not a manufactured cliffhanger — no resolution is promised. BEAT_MYS_04 satisfied.

---

## Section 6 — Japan Modifier Compliance

**Score: 92 / 100**

### ✅ Japanese naturalness

Script is entirely in standard Japanese. Desu/masu register consistent throughout. No anglicization of Japanese terms. Japanese proper nouns used in full canonical form.

### ✅ Cultural respect

FIX-M2 removed "企業城下島" which reduced a complex human story to an economic label. The revised phrasing "ひとつの企業によって管理される、前代未聞の島" is more human and factually precise.

### ✅ Sensitive history handling

L014-L016 handle forced labor with documented, dual-source presentation. L015 references the Japanese government's own UNESCO acknowledgment statement — the strongest possible form of cited evidence. L016 explicitly acknowledges that specific numbers remain disputed between Japan and Korea.

### ✅ Japanese sources

Research.json includes Japanese-language sources: S004 (Nagasaki prefecture), S005 (Mitsubishi), S007 (UNESCO Japanese records). The dual-source approach on disputed data (S006 Korean sources) demonstrates balance.

### ✅ Canonical place names

story_bible.json contains 8 canonical place names. FIX-M2 removed an off_limits expression. No unverified or anglicized names present in the script.

### ✅ No sensational tragedy framing

TITLE_B deleted for false departure timing. TITLE_C "一夜で捨てられた" is flagged in THUMB_C (COMP-004). Narration handles the closure date precisely (L018: 1974年1月15日, L020: 4月20日).

### ✅ Ma beat (S022)

40 seconds, static, no narration, is_ma_beat=true, ambient sound only. Placed in ACT_IV after the UNESCO/dispute synthesis. Correctly implemented per BEAT_JPN_02.

### ✅ Multiple silence moments (BEAT_JPN_03)

6 explicit [PAUSE:2s] cues (L004, L010, L022, L026, L030, L035) plus the 40-second Ma beat. BEAT_JPN_03 satisfied.

---

## Section 7 — Lost Place Modifier Compliance

**Score: 80 / 100**

### ✅ Real location establishing shots

S001 (extreme_wide_shot, HOOK) and S007 (aerial, ACT_I) both establish the island. Both marked stock_search_required=true for real photography. Perspective rule compliance: wide → aerial before interior close-ups.

### ✅ Maps and geography

S006 is an animated_map (MOTION_GRAPHICS) showing Nagasaki port to Hashima Island distance. Distance annotation "約15〜18km" visible per FIX-M4. Geography established before narrative begins.

### ✅ Before/after contrast

L009 describes the peak state: "5,259人——世界最高水準のひとつとされる人口密度" and then ACT_III presents the aftermath of closure. The before/after arc is the structural backbone of the video. BEAT_LP_02 satisfied.

### ✅ Abandonment atmosphere

dark_documentary color grade, film_grain=true, desaturated visual style — all aligned with lost_place modifier. The visual language of the existing image prompts (dark, crumbling, very slow motion) matches the composed template requirements.

### ✅ Respectful handling of former inhabitants

L009 ends: "端島は、彼らにとって、日本そのものでした" (For them, Hashima was Japan itself). L023 describes personal items left behind without aestheticizing them — frames them as historical reality. S016 notes explicitly forbid identifiable faces in photographs.

### ❌ Opening motion mismatch (MEDIUM — COMP-010)

S001 uses slow_pan_right. Template opening_motion and wide_establishing both map to very_slow_pan_right.

### ❌ BEAT_LP_03 gap (MEDIUM — COMP-011)

No dedicated contemplative exterior shot with minimal/no narration distinct from the Ma beat (S022). S020 and S024 are wide exterior shots but both carry active narration.

---

## Section 8 — Beat Compliance Summary

| Beat ID | Beat Name | Section Found | Status |
|---|---|---|---|
| BEAT_DOC_01 | hook | HOOK (L001-L003) | **PASS** |
| BEAT_DOC_02 | context | ACT_I (L005-L009) | **PASS** |
| BEAT_DOC_03 | evidence_presentation | ACT_II (L011-L017) | **PASS** |
| BEAT_DOC_04 | synthesis | ACT_III+IV (L018-L030) | **PASS** |
| BEAT_DOC_05 | takeaway | OUTRO (L032-L034) | **PASS** |
| BEAT_MYS_01 | central_mystery_reveal | HOOK (L001-L003 — atmospheric) | **PARTIAL** |
| BEAT_MYS_02 | evidence_trail | ACT_II (L014-L017) | **PASS** |
| BEAT_MYS_03 | uncertainty_acknowledgment | ACT_II (L016) | **PASS** |
| BEAT_MYS_04 | open_question_ending | OUTRO (L034) | **PASS** |
| BEAT_JPN_01 | cultural_context | ACT_I (full section) | **PASS** |
| BEAT_JPN_02 | ma_beat | ACT_IV (S022, 40s, static) | **PASS** |
| BEAT_JPN_03 | japanese_silence | Multiple sections (6× [PAUSE:2s]) | **PASS** |
| BEAT_LP_01 | location_establishing | HOOK (S001), ACT_I (S007) | **PASS** |
| BEAT_LP_02 | before_after_contrast | ACT_I→ACT_III arc | **PASS** |
| BEAT_LP_03 | contemplative_exterior_shot | Missing distinct from Ma beat | **PARTIAL** |

**Beats passing: 13/15. Partial: 2/15 (BEAT_MYS_01, BEAT_LP_03). Failing: 0/15.**

---

## Section 9 — Issue Register

| ID | Severity | Category | File | Description |
|---|---|---|---|---|
| COMP-001 | **BLOCKER** | visual | image_plan.json | AI images: 85% > 75% limit |
| COMP-002 | **BLOCKER** | platform | thumbnail.json | Thumbnail not selected |
| COMP-003 | **BLOCKER** | creator | thumbnail.json | Respect checks not done |
| COMP-004 | **HIGH** | platform | thumbnail.json | THUMB_C title misleading |
| COMP-005 | **HIGH** | platform | seo.json | No title selected |
| COMP-006 | **HIGH** | platform | timeline.json | Chapters planned, not assembled |
| COMP-007 | **HIGH** | platform | seo.json | Guidelines review pending |
| COMP-008 | **HIGH** | platform | seo.json | TITLE_C all checks pending |
| COMP-009 | **HIGH** | genre | story.json | Hook 60s vs 30s; no explicit mystery question in 30s |
| COMP-010 | MEDIUM | genre | scene.json | S001 slow_pan vs very_slow_pan_right |
| COMP-011 | MEDIUM | genre | scene.json | BEAT_LP_03 gap — no contemplative exterior w/o narration |
| COMP-012 | MEDIUM | production | voice.json | Timed read-through not done |
| COMP-013 | MEDIUM | production | voice.json | Voice recording not started |
| COMP-014 | MEDIUM | safety | scene.json | S011a mandatory human review pending |
| COMP-015 | MEDIUM | platform | subtitle.json | Subtitles placeholder only |
| COMP-016 | MEDIUM | genre | scene.json | S016 personal items — borderline aestheticization |
| COMP-017 | LOW | genre | scene.json | S002/S008 ken_burns_zoom_in not preferred |
| COMP-018 | LOW | structural | story.json | ACT_IV vs ACT_III section naming |
| COMP-019 | LOW | structural | story.json | Legacy 'japan_template' reference |
| COMP-020 | LOW | genre | story.json | L011 movie claim no fact_id |
| COMP-021 | INFO | structural | composed template | _composition_metadata removed ✓ |
| COMP-022 | INFO | structural | scene.json | Ma beat in ACT_IV vs template ACT_III hint |
| COMP-023 | INFO | production | voice.json | TTS speaking_rate not in template constraints |

---

## Section 10 — Priority Action List

### Immediately (no production required):

1. **COMP-003** — Human review and sign-off on THUMB_A respect_check
2. **COMP-002** — Select THUMB_A after respect check passes
3. **COMP-005** — Set selected_title_id = 'TITLE_A' (already approved, 30 seconds of work)
4. **COMP-010** — Change S001 motion_direction from 'slow_pan_right' to 'very_slow_pan_right' (metadata edit)
5. **COMP-019** — Update story.json outline.template to 'japan_mystery_lost_place' (metadata edit)

### Requires external assets (FIX-H1):

6. **COMP-001** — Download and integrate 5 real stock photos (S001, S007, S008, S020, S024)

### Requires human review (safety gate):

7. **COMP-014** — Human review S011a / IMG009 before image generation
8. **COMP-007** — Complete community guidelines review for sensitive content
9. **COMP-016** — Human review of S016 generated image when produced

### Requires production completion:

10. **COMP-012** — Timed read-through → FIX-M3
11. **COMP-013** — Voice recording
12. **COMP-006** — Timeline assembly → chapter confirmation
13. **COMP-015** — Subtitle generation (post-voice)
