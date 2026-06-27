# Production Go / No-Go — 端島 / 軍艦島：消えた都市の謎
**Reviewer:** Human Review Gate v1
**Date:** 2026-06-27

---

## DECISION: GO WITH FIXES

The content is factually sound. The script is production-ready after targeted edits. The sensitive history is handled correctly. The research is properly sourced and FLAG items are correctly applied.

The project is NOT ready to hand to an editor today. Three HIGH issues must be resolved before edit begins. One BLOCKER must be resolved before the SEO file is used.

---

## Fix Priority Order

### ── BLOCKER — Must fix before using seo/youtube_seo.md ──

**FIX-B1 — Delete Title Option B**
**File:** `seo/youtube_seo.md`

Delete the following block entirely (lines 19–24):

```
### Option B — Alternative
​```
【廃墟の島】端島・軍艦島 なぜ5000人が一夜で消えたのか？
​```
**Characters:** 30 / 100 limit
**Notes:** Question format. 廃墟 (haikyo) is high-search keyword.
```

Reason: Factually false. The island was vacated over a 3-month period (Jan 15 – Apr 20, 1974), not "一夜で" (overnight). Also uses「5000人」instead of the verified 5,259. Cannot be published under any circumstances.

---

### ── HIGH — Must fix before sending to editor ──

**FIX-H1 — Add stock footage sourcing requirement to image_plan.csv**
**File:** `visuals/image_plan.csv`

Add a new column: `stock_footage_fallback`

For the following rows, set this column to: `SEEK REAL PHOTOGRAPHY FIRST — AI fallback only if not found`
- IMG001 (S001) — island exterior wide
- IMG006 (S007) — aerial view
- IMG007 (S008) — Building 30 exterior
- IMG016 (S020) — wide atmosphere
- IMG020 (S024) — final frame

For these rows, also add a note to the `legal_status` cell: `CHECK: Getty Images Japan, アフロ, 時事通信フォト, 朝日新聞フォトアーカイブ, 長崎市観光写真素材`

For all other AI_GENERATE rows: mark `stock_footage_fallback` as `AI preferred (no equivalent real footage exists)`.

**FIX-H2 — Add motion direction column to scene_list.csv**
**File:** `visuals/scene_list.csv`

Add a new column `motion_direction` and populate as follows:

| scene_id | motion_direction |
|---|---|
| S001 | slow_pan_right |
| S002 | ken_burns_zoom_in |
| S003 | static (texture shot — no motion needed) |
| S004 | fade_in_title |
| S005 | slow_pan_left (simulate archive film movement) |
| S006 | animated (inherent) |
| S007 | slow_zoom_out (reveal scale) |
| S008 | ken_burns_zoom_in |
| S009 | slow_pan_right |
| S010 | slow_zoom_in (isolation detail) |
| S011 | slow_zoom_in_then_hold (see FIX-H2a) |
| S012 | animated (inherent) |
| S013 | slow_pan_left |
| S014 | fade_in_text (inherent) |
| S015 | slow_zoom_out |
| S016 | slow_zoom_in |
| S017 | static (light beam is the movement) |
| S018 | slow_pan_right |
| S019 | static (texture — macro, no motion) |
| S020 | very_slow_pan_right |
| S021 | slow_zoom_in |
| S022 | static (Ma beat — intentional) |
| S023 | slow_zoom_in (boat approaching) |
| S024 | slow_pan_right_then_hold_for_fade |

**FIX-H2a — Subdivide S011 to address 50-second duration**
**File:** `visuals/scene_list.csv`

S011 at 50 seconds (4:10–5:00) is too long for a single static mine interior. Subdivide into two scenes:
- S011a: 4:10–4:40 (30s) — Mine tunnel, slow zoom in, dark and atmospheric
- S011b: 4:40–5:00 (20s) — Mine tunnel, different angle or extreme CU of rock surface/light source

Add S011b row with matching prompt reference PROMPT_008b (a variation of PROMPT_008 with different framing: extreme close-up of rock wall with single light source, no tunnel depth, 30-second simpler composition).

**FIX-H3 — Resolve S022 timecode contradiction**
**Files:** `visuals/scene_list.csv`, `voice/voice_script.txt`, `script/script.md`

Decision: Extend Ma beat to 40 seconds. This is the stronger creative choice.

In `visuals/scene_list.csv`, S022 notes field: change "10 seconds of silence" to "40 seconds of silence (Ma beat)"

In `voice/voice_script.txt`, Section 5, change:
```
[NO NARRATION — 10 seconds of music and waves only]
```
to:
```
[NO NARRATION — 40 seconds of music and ocean waves only. Do not speak. Do not breathe audibly.]
```

In `script/script.md`, ACT IV section, change:
```
[B-ROLL: 映像のみ。音楽のみ。波の音。10秒間。]
```
to:
```
[B-ROLL: 映像のみ。音楽のみ。波の音。40秒間。完全な沈黙。]
```

---

### ── MEDIUM — Fix before image generation begins ──

**FIX-M1 — Add mandatory human-review gate to PROMPT_008**
**File:** `visuals/ai_image_prompts.md`

Append to the PROMPT_008 Notes section:

```
**MANDATORY REVIEW GATE:**
Before approving any generated image from this prompt:
1. Inspect for any human form, silhouette, shadow readable as human, or implied human body shape.
2. If found → REJECT. Do not use. Do not modify and use. Regenerate.
3. If rejection occurs 3 consecutive times → substitute PROMPT_013 (concrete texture) for this scene. Do not attempt further mine interior generation.
Negative prompt reinforcement: also add `--no silhouettes, figures, human shadows, implied human presence, people shapes, bodies` to the generation command.
```

**FIX-M2 — Replace 「企業城下島」in script**
**Files:** `script/script.md` (ACT I), `voice/voice_script.txt` (SECTION 2)

Find:
```
以来、島全体が一企業によって管理される、前代未聞の「企業城下島」となりました。
```

Replace with:
```
以来、島全体がひとつの企業によって管理される、前代未聞の島となりました。
```

Apply to both files identically.

**FIX-M3 — Timed read-through required before voice recording**
**Action:** Before booking voice recording, a Japanese native speaker must do a complete timed read of `voice/voice_script.txt` with all [slow] and [PAUSE:2s] instructions applied. If result deviates more than ±45 seconds from 12:00, script must be adjusted.

No file edit required now. Add a note to `voice/voice_direction.md` under Recording Specifications:

```
**MANDATORY PRE-RECORDING CHECK:** Complete timed read-through by native Japanese speaker with all [slow] and [PAUSE:2s] instructions applied. Target: 11:15–12:45 total duration. If outside range, adjust script length before studio booking.
```

**FIX-M4 — Correct distance in script**
**File:** `script/script.md` (ACT I), `voice/voice_script.txt` (SECTION 2)

Find:
```
長崎港から南西に約15キロメートル離れた小さな岩礁で
```

Replace with:
```
長崎港から南西に約15〜18キロメートル離れた小さな岩礁で
```

Apply to both files. This aligns with research_verified.md VF2.

---

### ── LOW — Fix before publishing ──

**FIX-L1 — Update voice direction narrator profile**
**File:** `voice/voice_direction.md`

Find in the Narrator Profile table:
```
| 言語 | ネイティブ日本語話者（標準語 / NHKアナウンサー的発音） |
```

Replace:
```
| 言語 | ネイティブ日本語話者（標準語 / NHKドキュメンタリーナレーター調。ニュースアナウンサー的な硬い発音は避けること） |
```

**FIX-L2 — Replace 「廃島」tag**
**File:** `seo/youtube_seo.md`

In the Tags section, find: `廃島`
Replace with: `廃墟島`

**FIX-L3 — Separate publishing advice from production checklist**
**File:** `seo/youtube_seo.md`

In the Publishing Checklist section, move these two items out of the checklist into a new section "## Channel Strategy Notes (Optional)":
- `Schedule: Publish time 20:00 JST`
- `Premiere mode: Recommended for first 48 hours`

---

## Fix Summary Table

| Fix ID | Severity | File | Type | Blocking? |
|---|---|---|---|---|
| FIX-B1 | BLOCKER | seo/youtube_seo.md | Delete section | Yes — before any title use |
| FIX-H1 | HIGH | visuals/image_plan.csv | Add column, revise 5 rows | Yes — before image sourcing |
| FIX-H2 | HIGH | visuals/scene_list.csv | Add column, 24 entries | Yes — before edit |
| FIX-H2a | HIGH | visuals/scene_list.csv | Split S011 into S011a/S011b | Yes — before edit |
| FIX-H3 | HIGH | scene_list.csv + voice_script.txt + script.md | 3 file edits | Yes — before edit |
| FIX-M1 | MEDIUM | visuals/ai_image_prompts.md | Append to PROMPT_008 notes | Before image generation |
| FIX-M2 | MEDIUM | script.md + voice_script.txt | Text replacement, 2 files | Before voice recording |
| FIX-M3 | MEDIUM | voice/voice_direction.md | Add timed read-through note | Before studio booking |
| FIX-M4 | MEDIUM | script.md + voice_script.txt | Distance figure correction | Before voice recording |
| FIX-L1 | LOW | voice/voice_direction.md | Text replacement | Before voice casting |
| FIX-L2 | LOW | seo/youtube_seo.md | Tag replacement | Before publishing |
| FIX-L3 | LOW | seo/youtube_seo.md | Section reorganization | Before publishing |

**Total fixes: 12**
**BLOCKER fixes: 1**
**HIGH fixes: 4 (across 3 categories)**
**MEDIUM fixes: 4**
**LOW fixes: 3**

---

## What Does NOT Require Fixes

- Script factual accuracy — all FLAG adjustments correctly applied
- Script register (です/ます) — no breaches found
- Japan template compliance — all 4 beats present, 5× [PAUSE:2s] correctly placed
- Story bible consistency — all canonical names/dates/numbers match script
- Sensitive history handling — no breaches, both governments' positions respected
- Research sourcing — no fabricated facts or URLs
- QA report — correctly self-assessed (20/20); the issues found in this review are execution-level, not factual-level
- Skyfall exclusion — correctly dropped
- Hook compliance — under 65 words
- PROMPT_008 intent — correct; gap is in execution gate only

---

## Sign-off

**Decision: GO WITH FIXES**
**BLOCKER items must be resolved before SEO file use.**
**HIGH items must be resolved before handing to editor.**
**MEDIUM items must be resolved before voice recording or image generation.**
**LOW items must be resolved before publishing.**

**Human Review Gate v1 — 2026-06-27**
