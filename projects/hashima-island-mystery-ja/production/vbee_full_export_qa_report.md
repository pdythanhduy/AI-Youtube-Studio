# Vbee Full Export QA Report
## hashima-island-mystery-ja
**Date:** 2026-06-28
**Stage:** 37 — Voice Asset QA
**QA Method:** File presence check + ffprobe duration measurement + timing plan cross-reference
**Gate:** FIX-M3 human listening still required before final timeline lock

---

## 1. File Presence — PASS ✅

| Metric | Value |
|--------|-------|
| Expected files | 28 |
| Files found | 28 |
| Missing files | 0 |
| Extra/unexpected files | 0 |

All 28 Vbee narration segments are present in `audio/vbee_raw/`.

---

## 2. Per-Segment Audit

> **Speed note:** All segments exported with `VBEE_INCLUDE_SPEED=false` → Vbee rendered at `speed_rate=1` (default).
> Duration targets in `timing_plan.json` were estimated for slow/very_slow pace (0.75–0.85x).
> Shorter actual durations reflect normal-speed rendering, NOT content truncation.
> All content is assumed complete. Human listening required to confirm pacing.

### Status Legend
| Code | Meaning |
|------|---------|
| `OK` | Within 80%+ of target. Fits window. |
| `NEEDS_TIMELINE_ADJUSTMENT` | 60–79% of target. Extra visual silence needed. |
| `TOO_SHORT` | <60% of target. Director listen required before decision. |
| `HUMAN_LISTENING_REQUIRED` | Critical line, sensitive content, or pacing concern. |

---

### HOOK (0:00–1:00)

| line_id | filename | actual_sec | target_sec | ratio | status |
|---------|----------|-----------|-----------|-------|--------|
| L001 | hashima_L001_hook_01.mp3 | 4.42 | 5 | 88% | OK — HUMAN_LISTENING_REQUIRED |
| L002 | hashima_L002_hook_02.mp3 | 8.11 | 10 | 81% | OK |
| L003 | hashima_L003_hook_03.mp3 | 2.66 | 6 | 44% | TOO_SHORT — HUMAN_LISTENING_REQUIRED |

**L001 note:** HOOK opening line. Very slow delivery intended. Listen to confirm "かつて" receives proper weight.
**L003 note:** "そして、ある日——すべてが消えました。" is the dramatic pivot of the HOOK. 2.66s is very brief for a very_slow line with a dash-pause. Director must confirm emotional delivery before timeline lock.

---

### ACT I (1:00–3:00)

| line_id | filename | actual_sec | target_sec | ratio | status |
|---------|----------|-----------|-----------|-------|--------|
| L005 | hashima_L005_act1_01.mp3 | 16.44 | 20 | 82% | OK |
| L006 | hashima_L006_act1_02.mp3 | 15.10 | 15 | 101% | OK |
| L007 | hashima_L007_act1_03.mp3 | 12.77 | 14 | 91% | OK |
| L008 | hashima_L008_act1_04.mp3 | 22.03 | 22 | 100% | OK — HUMAN_LISTENING_REQUIRED |

**L008 critical timing:** Starts at 2:37, duration 22.03s → ends at ~2:59. Spans S007/S008 visual cut (TF-001). Duration matches target almost exactly. ✅ CRITICAL TIMING PASS.

---

### ACT II (3:00–6:00)

| line_id | filename | actual_sec | target_sec | ratio | status | sensitive |
|---------|----------|-----------|-----------|-------|--------|----------|
| L009 | hashima_L009_act1_05.mp3 | 29.62 | 28 | 106% | OK | — |
| L011 | hashima_L011_act2_01.mp3 | 17.16 | 18 | 95% | OK | — |
| L012 | hashima_L012_act2_02.mp3 | 22.85 | 22 | 104% | OK | — |
| L013 | hashima_L013_act2_03.mp3 | 6.84 | 10 | 68% | NEEDS_TIMELINE_ADJUSTMENT — HUMAN_LISTENING_REQUIRED | ✅ SENSITIVE |
| L014 | hashima_L014_act2_04.mp3 | 14.35 | 16 | 90% | OK — HUMAN_LISTENING_REQUIRED | ✅ SENSITIVE |
| L015 | hashima_L015_act2_05.mp3 | 16.46 | 18 | 91% | OK | ✅ SENSITIVE |
| L016 | hashima_L016_act2_06.mp3 | 13.03 | 18 | 72% | NEEDS_TIMELINE_ADJUSTMENT | ✅ SENSITIVE |
| L017 | hashima_L017_act2_07.mp3 | 17.16 | 22 | 78% | NEEDS_TIMELINE_ADJUSTMENT | — |

**L013/L014 note:** Sensitive content. Mandatory tone review — verify factual, respectful delivery. No emotional manipulation or sensationalism.
**L015/L016 note:** Sensitive content. L016 contains disputed historical framing. Verify accuracy and measured tone.

---

### ACT III (6:00–9:00)

| line_id | filename | actual_sec | target_sec | ratio | status |
|---------|----------|-----------|-----------|-------|--------|
| L018 | hashima_L018_act3_01.mp3 | 5.59 | 7 | 80% | OK |
| L019 | hashima_L019_act3_02.mp3 | 10.39 | 15 | 69% | NEEDS_TIMELINE_ADJUSTMENT |
| L020 | hashima_L020_act3_03.mp3 | 4.46 | 8 | 56% | TOO_SHORT |
| L021 | hashima_L021_act3_04.mp3 | 10.08 | 16 | 63% | NEEDS_TIMELINE_ADJUSTMENT |
| L023 | hashima_L023_act3_05.mp3 | 12.43 | 18 | 69% | NEEDS_TIMELINE_ADJUSTMENT |
| L024 | hashima_L024_act3_06.mp3 | 11.30 | 16 | 71% | NEEDS_TIMELINE_ADJUSTMENT |
| L025 | hashima_L025_act3_07.mp3 | 7.82 | 12 | 65% | NEEDS_TIMELINE_ADJUSTMENT |

**ACT III note:** Most spacious section. Shorter audio means more visual silence per scene — this is aesthetically acceptable and allows the images to breathe. L018 (7s window, 5.59s audio) and L020 (30s window, 4.46s audio) provide ample visual breathing room.

---

### ACT IV (9:00–11:00)

| line_id | filename | actual_sec | target_sec | ratio | status |
|---------|----------|-----------|-----------|-------|--------|
| L027 | hashima_L027_act4_01.mp3 | 9.86 | 14 | 70% | NEEDS_TIMELINE_ADJUSTMENT |
| L028 | hashima_L028_act4_02.mp3 | 20.42 | 22 | 93% | OK — HUMAN_LISTENING_REQUIRED |
| L029 | hashima_L029_act4_03.mp3 | 13.73 | 18 | 76% | NEEDS_TIMELINE_ADJUSTMENT |

**L028 note:** HUMAN_LISTENING_REQUIRED — critical pre-Ma beat line. Must begin at 9:35 in timeline.
**Ma beat chain (TF-002):**
- L028 starts 9:35 → ends 9:55.42
- L029 starts ~9:56.42 → ends 10:10.15
- L030 pause (2s) → narration complete at 10:12.15
- Buffer to Ma beat: 7.85s additional visual silence in S021 ✅
- Ma beat: 10:20–11:00 (exactly 40s) ✅ INTACT

---

### OUTRO (11:00–12:00)

| line_id | filename | actual_sec | target_sec | ratio | status |
|---------|----------|-----------|-----------|-------|--------|
| L032 | hashima_L032_outro_01.mp3 | 8.18 | 12 | 68% | NEEDS_TIMELINE_ADJUSTMENT |
| L033 | hashima_L033_outro_02.mp3 | 7.39 | 12 | 62% | NEEDS_TIMELINE_ADJUSTMENT |
| L034 | hashima_L034_outro_03.mp3 | 4.39 | 9 | 49% | TOO_SHORT |

**L034 note:** Final narration line. At 4.39s vs 9s target (49%), content may feel cut short. Director listen required. L035 pause (2s) + video fade follows at ~11:58.

---

## 3. Summary by Status

| Status | Count | Lines |
|--------|-------|-------|
| OK | 13 | L001, L002, L005, L006, L007, L008, L009, L011, L012, L014, L015, L018, L028 |
| NEEDS_TIMELINE_ADJUSTMENT | 12 | L013, L016, L017, L019, L021, L023, L024, L025, L027, L029, L032, L033 |
| TOO_SHORT | 3 | L003, L020, L034 |
| NEEDS_REEXPORT | 0 | — |

**No files require immediate re-export.** Director listen will determine whether TOO_SHORT lines need re-generation with speed adjustment.

---

## 4. Critical Timing — PASS ✅

| Flag | Check | Result |
|------|-------|--------|
| TF-001 | L008 starts at 2:37, 22s target | ✅ PASS — actual 22.03s |
| TF-002 | L028+L029+L030 complete before 10:20 | ✅ PASS — completes at ~10:12 (8s buffer) |
| Ma beat | 10:20–11:00 exactly 40s | ✅ INTACT |
| OUTRO | L032 begins at 11:01 after Ma beat | ✅ PASS |
| L028 start | Must begin at 9:35 in timeline | ✅ 20.42s fits window |

---

## 5. Human Listening Checklist

These segments must be reviewed by a human listener before timeline lock:

| line_id | Reason | Status |
|---------|--------|--------|
| L001 | HOOK opening line — very_slow delivery, emotional weight on "かつて" | HUMAN_LISTENING_REQUIRED |
| L003 | Dramatic pivot ("そして、ある日——") — 2.66s may be too brief | HUMAN_LISTENING_REQUIRED |
| L008 | Critical timing line spanning S007/S008 cut, 22.03s | HUMAN_LISTENING_REQUIRED |
| L013 | Sensitive content — forced labor topic, tone must be factual/respectful | HUMAN_LISTENING_REQUIRED |
| L014 | Sensitive content — forced labor conditions | HUMAN_LISTENING_REQUIRED |
| L028 | Critical pre-Ma-beat line, must start at 9:35 | HUMAN_LISTENING_REQUIRED |

---

## 6. Sensitive Content Tone Review

Lines L013–L016 describe forced labor during WWII. Verify before publishing:

| line_id | Section | Issue |
|---------|---------|-------|
| L013 | S011a | Forced labor introduction — confirm factual, no emotion-amplification |
| L014 | S011a | Labor conditions — confirm measured tone, historical accuracy |
| L015 | S011b | Consequence framing — confirm no nationalistic bias |
| L016 | S012 | Disputed historical framing flagged — double-check wording |

These must pass COMP-007 (community guidelines review) before YouTube publication.

---

## 7. Speed/Pacing Assessment

**Root cause:** `VBEE_INCLUDE_SPEED=false` in production config. All 28 segments rendered at Vbee default `speed_rate=1.0`.

**Intended pacing:**
- `very_slow` lines: 0.75x (L001, L002, L003, L021, L025)
- `slow` lines: 0.80x (L006, L007, L013, L014, L017, L018, L019, L020, L023, L024, L027, L029, L033, L034)
- `normal` lines: 0.85x (L005, L008, L009, L011, L012, L015, L016, L028, L032)

**Impact on total narration:** 345s actual vs 423s planned (−78s, −18%).
**Impact on timeline:** Narration finishes earlier per window. Visual silence gaps increase by average 2.8s per segment. The documentary feel may be less contemplative at speed=1.

**Director options after listening:**
1. **Accept as-is** — documentary pacing achieved by visual silence alone (shorter narration = more image breathing room)
2. **Re-export slow/very_slow lines with speed** — set `VBEE_INCLUDE_SPEED=true`, re-submit affected segments

**Recommendation:** Listen to L001, L003, L008, L028 first. If contemplative tone is sufficient, accept. If too fast for NHK-style documentary feel, re-export with `VBEE_SPEED=0.80` and `INCLUDE_SPEED=true`.

---

## 8. Total Audio Duration

| Metric | Value |
|--------|-------|
| Files measured | 28 |
| Total narration audio | 345.1s (~5m 45s) |
| Planned narration total | 423s |
| Difference | −78s (−18%) |
| Cause | speed_rate=1 (default), not 0.75–0.85 |
| Timeline impact | More visual silence — video length remains 12:00 |

---

## 9. Timeline Assembly Readiness

| Gate | Status |
|------|--------|
| All 28 files present | ✅ PASS |
| Zero missing files | ✅ PASS |
| Critical timing (TF-001, TF-002) | ✅ PASS |
| Ma beat integrity (10:20–11:00) | ✅ PASS |
| Human listening checklist | ⬜ PENDING (L001, L003, L008, L013, L014, L028) |
| Sensitive content tone review | ⬜ PENDING (L013–L016) |
| Director pacing decision | ⬜ PENDING (accept speed=1 or re-export) |

**Voice asset phase may proceed to timeline assembly WITH CONDITIONS:**
- Critical timing is confirmed safe ✅
- Editor must use actual durations (from `vbee_full_export_qa.json`), not timing_plan targets
- L028 must be placed at 9:35 in the timeline regardless of surrounding gaps
- Human listening review must be completed before final export (not before rough assembly)
- Sensitive content (L013–L016) must pass COMP-007 review before YouTube publication

---

*Production report — Stage 37 — hashima-island-mystery-ja — 2026-06-28*
