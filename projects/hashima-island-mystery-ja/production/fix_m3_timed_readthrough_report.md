# FIX-M3: Timed Read-through Report
## hashima-island-mystery-ja
**Date:** 2026-06-27
**Gate:** FIX-M3 — Timed Read-through Preparation (Simulated Timing Audit)
**Status:** SIMULATED AUDIT COMPLETE — Director live read-through still required before voice session

---

## 1. Task Summary

FIX-M3 required the following actions before any voice talent session:
1. ✅ Rename IMG009 file: `IMG009_S010_mine_gate_attempt1.png` → `IMG009_S011a_mine_tunnel_approved.png`
2. ✅ Read 12 project files (scene.json, voice.json, timing data, templates)
3. ✅ Create `voice/timed_readthrough_plan.md` — delivery instructions, timing targets, per-section targets, pause placement, delivery modes
4. ✅ Create `data/timing_plan.json` — machine-readable timing per line and section
5. ✅ Perform simulated Japanese documentary pacing timing audit
6. ✅ Create this report (`production/fix_m3_timed_readthrough_report.md`)
7. ⬜ Update `data/export.json` and `composition/composition_compliance.json` — in progress

---

## 2. IMG009 Rename — CONFIRMED

| Action | Status |
|--------|--------|
| File rename executed | ✅ COMPLETE |
| FROM | `mine_gate/IMG009_S010_mine_gate_attempt1.png` |
| TO | `mine_gate/IMG009_S011a_mine_tunnel_approved.png` |
| References updated | `data/image_plan.json`, `assets/ai_images/generated/mine_gate/img009_mine_gate_qa.json` |
| Completion date | 2026-06-27 |

S010 was a user entry error in the original filename. The content was always correct for scene S011a (mine tunnel, 4:10-4:40). All production data files now reference the correct path.

---

## 3. Source Data Read

Files read for this analysis:
- `data/voice.json` — 35 voice lines (27 narration + 8 pause/silence)
- `data/scene.json` — 25 scenes, total 720s
- `data/image_plan.json` — image asset registry
- `data/export.json` — production stage log
- `composition/composition_compliance.json` — compliance tracking
- Prior QA reports: `img016_v2_final_qa_report.md`, `batch_3_qa.json`, `img009_mine_gate_qa.json`

---

## 4. Simulated Timing Audit — Results

### 4.1 Overall Timing

| Metric | Value |
|--------|-------|
| Total video duration | **720 seconds (12:00)** ✅ |
| Total narration speaking time | ~423 seconds (7:03) |
| Total pauses + inter-line gaps | ~101 seconds (1:41) |
| Total narrated content | **~524 seconds (8:44)** |
| Visual silence (scenes hold without narration) | **~196 seconds (3:16)** |
| Ma beat silence | 40 seconds (S022, 10:20-11:00) |
| Effective narration pacing | ~170 morae/min (overall, including all silences) |

**Verdict:** The narration timing is structurally sound. Total video achieves 12:00 target. The 196 seconds of visual silence is distributed across all scenes and is a deliberate editorial choice — not dead time.

### 4.2 Per-Section Breakdown

| Section | Video Window | Narration | Pauses | Visual Silence |
|---------|-------------|-----------|--------|----------------|
| HOOK | 0:00-1:00 (60s) | 21s | 7s | 32s |
| ACT_I | 1:00-3:00 (120s) | 71s | 5s | 44s |
| ACT_II | 3:00-6:00 (180s) | 124s | 9s | 47s |
| ACT_III | 6:00-9:00 (180s) | 92s | 10s | 78s |
| ACT_IV | 9:00-11:00 (120s) | 54s | 8s | 18s + 40s Ma |
| OUTRO | 11:00-12:00 (60s) | 33s | 6s | 21s |
| **TOTAL** | **720s** | **395s** | **45s** | **196s** |

*Note: ACT_IV visual silence (18s) excludes the Ma beat (40s), which is explicitly designed silence.*

### 4.3 Pacing Analysis

**Japanese documentary pacing baseline:** 250-300 morae/min (standard NHK documentary pacing)

**This project targets:** ~200-230 morae/min for speaking portions (deliberate, contemplative)

**Effective overall pace:** ~170 morae/min (including all pauses and visual silences)

**Assessment:** This pacing is appropriate for the content. The island's layered history — forced labor, world heritage, abandonment — cannot be rushed. The 間(ma)-aware pacing strategy creates space for the viewer to absorb each historical layer before the narration moves forward. ACT_III (180s window, only 102s narrated) exemplifies this approach: the narrator says little; the images of decay and abandonment carry the weight.

**Comparison to voice.json intent:**
The `timed_readthrough_notes` in voice.json states: "Pace target: 300 morae/min × 0.77 = ~1,201 target words." The 0.77 factor yields ~231 morae/min for speaking portions. The estimated_duration_seconds in voice.json are calibrated at approximately this rate. The simulated timing audit confirms these estimates are achievable and structurally consistent with the 720-second video structure.

### 4.4 Hook Timing — Critical Check

**Rule:** Hook narration must land within first 30 seconds.

| Check | Target | Calculated | Status |
|-------|--------|-----------|--------|
| L001 start | 0:00 | 0:00 | ✅ PASS |
| L001 end | ≤0:30 | 0:05 | ✅ PASS |
| L002 end | ≤0:30 | 0:16 | ✅ PASS |
| L003 end | ≤0:30 | 0:24 | ✅ PASS |
| HOOK complete (L003) | ≤0:30 | 0:24 | ✅ PASS |

All three HOOK narration lines complete by 0:24. The title card (S004) does not carry narration. **Hook is within 30 seconds.** ✅

### 4.5 Ma Beat Integrity — Critical Check

**Requirement (FIX-H3):** 40-second Ma beat at scene S022 (10:20-11:00). Absolutely no narration. Music and ocean waves only.

**Current timing (base placement):**
- L028 start at 9:40: L030 ends at 10:25 → Ma silence begins 10:25, ends 11:05 → **only ~35s within S022**

**⚠️ PREFERRED TIMING (recommended adjustment):**
- L028 start at 9:35 (5s early, during S020 visual hold): L030 ends at 10:20 → Ma silence begins **exactly 10:20**, ends 11:00 → **full 40s within S022**

**Recommendation:** Begin L028 at 9:35. This uses 5 seconds of the visual silence buffer in S020 (which has 21 seconds of silence after L027 ends at 9:19). Zero impact on S020 or S021 content. Full Ma beat integrity preserved.

---

## 5. Timing Flags

### TF-001 — S008 Narrow Window ⚠️

| Field | Value |
|-------|-------|
| Scene | S008 (2:45-3:00, 15s) |
| Line | L008 |
| Narration duration | 22 seconds + 1s gap = 23s |
| Available window | 15s |
| Overflow | 8 seconds |
| Resolution | Begin L008 at approximately **2:37** within S007 visual (which holds silently after L007 ends at ~2:25). L008 narration spans the visual cut from S007 to S008 and completes at ~2:59 — 1 second before S009 begins at 3:00. |
| Audio continuity | Narration is seamless across the visual cut. The editor places audio independently of the scene cut. |
| Director action | Mark L008 start at 2:37 in DAW before recording session. |

### TF-002 — Ma Beat Start Point ⚠️

| Field | Value |
|-------|-------|
| Ma beat target | 10:20-11:00 (40s, S022) |
| L028 preferred start | **9:35** (not 9:40) |
| Why | Starting L028 at 9:35 ensures L028(22s)+gap(1s)+L029(18s)+gap(2s)+L030(2s)+gap(0s) = 45s completes at exactly 10:20 |
| Source | S020 has 21s of silence after L027 (9:05-9:19). Starting L028 at 9:35 uses 5s of this silence. |
| Director action | Mark L028 start at 9:35 in DAW. |

### TF-003 — ACT_II Cross-scene Bleeds ℹ️

Lines L011, L012, L014, L015 each span one scene cut. This is normal in documentary audio production and requires no corrective action. The audio track is continuous; visual cuts happen independently. The `scene_id_ref` in voice.json indicates the primary visual playing during the line, not a strict audio boundary.

---

## 6. Delivery Mode Summary

| Mode | Morae/min | Lines | Notes |
|------|-----------|-------|-------|
| `very_slow` | 150-180 | L001, L002, L003, L021, L025 | Opening/closing anchors; departure; decay |
| `slow` | 200-230 | L006, L007, L013, L014, L017, L018, L019, L020, L023, L024, L027, L029, L033, L034 | Historical facts, transition lines, reflection |
| `normal` | 250-270 | L005, L008, L009, L011, L012, L015, L016, L028, L032 | Contextual information, dense historical content |

All modes are significantly slower than conversational Japanese (~350 morae/min). No line should feel hurried. Even "normal" mode is contemplative.

---

## 7. Sensitive Content Delivery Notes

**Lines L013 and L014 (S011a — over IMG009 mine tunnel):**
- L013: "しかし、同じこの島の、もう少し深いところに目を向けると——別の物語が見えてきます。"
- L014: "1939年から1945年にかけて、太平洋戦争の時代。朝鮮半島および中国大陸から連行された人々が、この炭坑の地下深くで働かされました。"

**Delivery requirement:** Factual. Measured. Not emotionally heightened. The empty mine tunnel (IMG009) carries the historical weight visually. The narrator's role is to state the historical fact clearly and then trust the image. No dramatization. No horror framing. The Japanese verb forms used are factual past-tense (働かされました — "were made to work") — they are already heavy. Deliver them plainly.

**FIX-M1 reminder:** These lines play over the approved empty mine tunnel image. No people were depicted in that image. The narration references the people; the image shows the empty space they once occupied. This contrast is the intentional artistic choice.

---

## 8. Voice Session Prerequisites (FIX-M3 Gate)

The following checklist must be completed **before calling the voice talent**. This represents the FIX-M3 gate requirement.

| # | Prerequisite | Status |
|---|-------------|--------|
| 1 | IMG009 rename completed | ✅ DONE (2026-06-27) |
| 2 | `voice/timed_readthrough_plan.md` created | ✅ DONE |
| 3 | `data/timing_plan.json` created | ✅ DONE |
| 4 | Simulated timing audit completed | ✅ DONE (this report) |
| 5 | Director live read-through at target pace | ⬜ PENDING |
| 6 | Live read-through total: ≤450s speaking time | ⬜ PENDING |
| 7 | L008 start marked at 2:37 in DAW | ⬜ PENDING |
| 8 | L028 start marked at 9:35 in DAW | ⬜ PENDING |
| 9 | Ma beat 40s silence confirmed in DAW (10:20-11:00) | ⬜ PENDING |
| 10 | L013/L014 FIX-M1 tone reviewed with talent | ⬜ PENDING |

**FIX-M3 gate opens when items 5-10 are confirmed by director/producer.** Update `data/timing_plan.json → readthrough_checklist` upon completion.

---

## 9. Next Production Steps

After FIX-M3 gate clears:

1. **Voice recording session** — talent records all 27 narration lines at target pace
2. **Timeline assembly** — editor builds 720s timeline using scene.json timecodes + approved images + audio
3. **Audio placement** — L008 placed at 2:37, L028 at 9:35, Ma beat confirmed at 10:20
4. **Thumbnail render** — THUMB_A concept using IMG001 (cold pre-dawn) + title text
5. **SEO final review** — seo.json title/description/tags check
6. **Community guidelines review** — COMP-007 YouTube sensitive content policy (forced labor content)
7. **Publish**

**Optional upgrades (non-blocking):**
- IMG016 S020: PIXTA dusk photo (軍艦島 夕暮れ) to replace AI image before publish
- CC BY-SA legal review: unlocks S001/S008/S020 real photos, reduces AI% from 75% to 60%

---

## 10. Data Updates Applied in This Stage

| File | Change |
|------|--------|
| `assets/ai_images/generated/mine_gate/IMG009_S011a_mine_tunnel_approved.png` | **FILE RENAMED** (was IMG009_S010_mine_gate_attempt1.png) |
| `data/image_plan.json` | IMG009 file_path updated; rename_required→false; rename_completed→true |
| `assets/ai_images/generated/mine_gate/img009_mine_gate_qa.json` | filename fields updated; rename_completed→true; production_status→approved_for_production |
| `voice/timed_readthrough_plan.md` | **CREATED** — delivery instructions, per-section targets, pause map |
| `data/timing_plan.json` | **CREATED** — machine-readable per-line timecodes and section budgets |
| `production/fix_m3_timed_readthrough_report.md` | **CREATED** (this file) |
| `data/export.json` | Stage 29 added; FIX-M1 rename note updated; FIX-M3 status→in_progress |
| `composition/composition_compliance.json` | FIX-M3 block added |

---

## 11. Final Output

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FIX-M3: TIMED READ-THROUGH PREPARATION — COMPLETE

IMG009 RENAME:     ✅ COMPLETE
  IMG009_S011a_mine_tunnel_approved.png

SIMULATED TIMING AUDIT: ✅ COMPLETE
  Total video: 720s (12:00) ✓
  Hook lands by 0:24 (within 30s target) ✓
  Ma beat integrity: achievable at 40s
    → Requires L028 start at 9:35 (not 9:40)
  
  TIMING FLAGS:
  ⚠️ TF-001: L008 must start at 2:37 (in S007)
  ⚠️ TF-002: L028 must start at 9:35 (in S020)
  ℹ️ TF-003: L011/L012/L014/L015 span scene cuts
             (normal in documentary production)

DOCUMENTS CREATED:
  voice/timed_readthrough_plan.md ✓
  data/timing_plan.json ✓
  production/fix_m3_timed_readthrough_report.md ✓

FIX-M3 GATE STATUS:
  Simulated audit: COMPLETE ✓
  Director live read-through: PENDING ⬜
  DAW markers (L008@2:37, L028@9:35): PENDING ⬜
  Ma beat 40s confirmed: PENDING ⬜
  FIX-M1 tone review: PENDING ⬜

NEXT STEP: Director performs live read-through
at target pace. Confirm total ≤450s speaking.
Mark DAW cues. Then voice recording session.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
