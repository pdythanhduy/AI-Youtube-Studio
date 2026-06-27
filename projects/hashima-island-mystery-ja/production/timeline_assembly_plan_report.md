# Timeline Assembly Plan Report
## hashima-island-mystery-ja
**Date:** 2026-06-28
**Stage:** 38 — Timeline Assembly Plan v1

---

## 1. Inputs Verified

| Input | Status |
|-------|--------|
| `data/scene.json` — 25 scenes, 720s total | ✅ Verified |
| `data/image_plan.json` — 19 active images, 1 suppressed | ✅ Verified |
| `audio/vbee_raw/vbee_full_export_qa.json` — 28 segments, actual durations | ✅ Verified |
| Critical timing (TF-001 L008@2:37, TF-002 L028@9:35) | ✅ Verified (from Stage 37 QA) |
| Ma beat (S022, 10:20–11:00, 40s) | ✅ Verified (scene.json, is_ma_beat=true) |

---

## 2. Planning Summary

| Metric | Value |
|--------|-------|
| Total planned video duration | **12:00 (720s)** |
| Total actual narration audio | **345.12s (5:45)** |
| Total pause events (editor silence) | **12s** |
| Ma beat duration | **40s (10:20–11:00)** |
| Total visual silence (non-Ma, non-pause) | **322.88s** |
| Planned audio duration check | 345.12 + 12 + 40 + 322.88 = **720.00s ✅** |

---

## 3. Critical Timing

| Flag | Check | Result |
|------|-------|--------|
| TF-001 | L008 placed at 2:37, ends 2:59.03 (22.03s) — spans S007/S008 cut | ✅ PASS |
| TF-002 | L028 placed at 9:35. Chain: L028 (20.42s) + gap (1s) + L029 (13.73s) + L030 pause (2s) = completes at 10:12.15 | ✅ PASS |
| Ma beat approach | 7.85s visual silence in S021 after L030 pause (10:12.15–10:20) | ✅ PASS |
| Ma beat | S022 = 10:20–11:00 = exactly 40s, no narration | ✅ PASS |
| OUTRO | L032 begins at 11:01 (1s after Ma beat ends) | ✅ PASS |

---

## 4. Visual Silence Distribution

The 322.88s of visual silence (non-Ma, non-pause) absorbs the 77.88s narration shortfall from speed=1 export.

| Scene | Visual Silence | Notes |
|-------|---------------|-------|
| S001 | 5.58s | Short — music bed covers |
| S002 | 6.89s | Interior wind fills |
| S003 | **12.34s** | ⚠ L003 TOO_SHORT — dramatic or problematic |
| S004 | 20s | Title card — intentional |
| S005 | 22.56s | Meiji industrial slow pan |
| S006 | 14.90s | Map animation covers |
| S007 | 13.23s | Pre-L008 island silence |
| S008 | 0.97s | Near-negligible |
| S009 | 1s | Pre-narration lead |
| S010 | 1.84s | Between L011/L012 |
| S011a | 6.31s | Sensitive scene breathing room |
| S011b | 2.65s | Between L014/L015 |
| S012 | 11.97s | Data graphic holds |
| S013 | 11.84s | Heritage image breathes |
| S014 | 22.41s | Date card contemplation |
| S015 | 18.61s | Dock silence |
| S016 | **23.54s** | Abandoned items — emotionally powerful |
| S017 | 14s | Light beam room |
| S018 | 16.57s | Storm ruins |
| S019 | 5.70s + 4.18s | Between L025/L026 and pre-S020 |
| S020 | **20.14s** | Pre-L028 dusk island |
| S021 | **7.85s** | Pre-Ma-beat approach window |
| S023 | 20.82s | Post-Ma-beat OUTRO ferry |
| S024 | 14.22s | Final narration gaps and fade |

---

## 5. Image Asset Status

| Scene | Image | Source | Status |
|-------|-------|--------|--------|
| S001 | IMG001 | AI | ✅ Approved |
| S002 | IMG002 | AI | ⚠ Post-process required |
| S003 | IMG003 | AI | ✅ Approved |
| S004 | — | MG001 | Motion graphic |
| S005 | IMG004 | AI | ⚠ Caption overlay required |
| S006 | — | MG002 | Motion graphic |
| S007 | IMG006 | REAL CC BY 2.0 | ✅ Production ready |
| S008 | IMG007 | AI | ✅ Approved |
| S009 | IMG008 | AI | ⚠ Post-process required |
| S010 | **NONE** | PENDING | 🔴 Image not assigned |
| S011a | IMG009 | AI | ⚠ Producer review required |
| S011b | IMG010 | AI | ✅ Approved |
| S012 | — | MG003 | Motion graphic |
| S013 | IMG011 | AI | ⚠ Post-process required (pan direction) |
| S014 | — | MG004 | Motion graphic |
| S015 | IMG012 | AI | ✅ Approved |
| S016 | IMG013 | AI | ✅ Approved |
| S017 | IMG014 | AI | ✅ Approved |
| S018 | IMG015 | AI | ✅ Approved |
| S019 | **NONE** | PENDING | 🔴 Image not assigned |
| S020 | IMG016 | AI | ⚠ Post-process required |
| S021 | IMG017 | AI | ✅ Approved |
| S022 | IMG018 | AI | ✅ Approved (Ma beat) |
| S023 | IMG019 | AI | ✅ Approved |
| S024 | IMG020 | REAL Govt 1974 | ✅ Production ready |

**Active images confirmed:** 19 ✅ (1 suppressed: IMG005)
**Image gaps:** 2 (S010, S019) — must be resolved before NLE assembly

---

## 6. Audio Segment Status Summary

| Status | Count | Lines |
|--------|-------|-------|
| OK | 13 | L001, L002, L005–L009, L011, L012, L014, L015, L018, L028 |
| NEEDS_TIMELINE_ADJUSTMENT | 12 | L013, L016, L017, L019, L021, L023–L025, L027, L029, L032, L033 |
| TOO_SHORT | 3 | L003 (44%), L020 (56%), L034 (49%) |
| NEEDS_REEXPORT | 0 | — |

**No files require re-export before assembly.** Director listen to L003/L020/L034 will determine if content is complete at speed=1.

---

## 7. Scenes with Timing Risk

| Scene | Risk | Description |
|-------|------|-------------|
| S003 | MEDIUM | L003 TOO_SHORT (2.66s) — 12.34s silence on door texture. Confirm delivery complete. |
| S010 | HIGH | No image assigned — blocks NLE assembly |
| S011a | HIGH | IMG009 producer review required; L013/L014 sensitive content |
| S012 | HIGH | MG003 must present data neutrally — do not assert death count |
| S019 | HIGH | No image assigned — blocks NLE assembly |
| S016 | LOW | L020 TOO_SHORT — 23.54s silence on personal items. Powerful but confirm complete. |
| S024 | LOW | L034 TOO_SHORT — confirm final narration is not cut off |

---

## 8. Post-Processing Required Before Export

| Image | Scene | Required Action |
|-------|-------|-----------------|
| IMG002 | S002 | Desaturate 60–70%, darken -0.5 to -1 stop, film grain |
| IMG004 | S005 | Add caption overlay: `「illustrative archival simulation / 参考映像」` |
| IMG008 | S009 | Slight desaturation from warm sepia |
| IMG011 | S013 | Frame pan toward interior light shafts; away from war-zone ruins |
| IMG016 | S020 | Desaturate sky 15–20%, preserve warm dusk tone |

---

## 9. Attribution Required in YouTube Description

| Asset | License | Required Attribution |
|-------|---------|---------------------|
| IMG006 (S007) | CC BY 2.0 | "Battle-Ship Island Nagasaki Japan (2008)" by kntrty / Wikimedia Commons / CC BY 2.0 |
| IMG020 (S024) | Japan Govt 1974 | Aerial photograph of Hashima Island (1974) / Source: National Land Image Information (Color Aerial Photographs) / Ministry of Land, Infrastructure, Transport and Tourism of Japan |

---

## 10. Timeline Assembly Gate

| Gate | Status |
|------|--------|
| All 28 audio files present | ✅ PASS |
| Critical timing verified (TF-001, TF-002) | ✅ PASS |
| Ma beat integrity (10:20–11:00, 40s) | ✅ PASS |
| Total duration check (720s) | ✅ PASS |
| S010 image assigned | 🔴 BLOCKED |
| S019 image assigned | 🔴 BLOCKED |
| IMG009 producer review | ⬜ PENDING |
| Human listen (L001, L003, L008, L013, L014, L028) | ⬜ PENDING |
| Sensitive content review L013–L016 (COMP-007) | ⬜ PENDING |
| Post-processing (IMG002, IMG004, IMG008, IMG011, IMG016) | ⬜ PENDING |

**Timeline assembly may BEGIN** once S010 and S019 images are resolved.
Human listening and post-processing may proceed in parallel with rough assembly.

---

## 11. Exact Next Actions

1. **Resolve image gaps** (BLOCKING):
   - S010: Assign IMG003 or IMG010 as placeholder, OR generate from PROMPT_009
   - S019: Assign IMG010 as placeholder, OR generate new macro concrete image

2. **IMG009 producer review** (HIGH — before NLE import of S011a):
   - Review `assets/ai_images/generated/mine_gate/IMG009_S011a_mine_tunnel_approved.png`
   - Confirm: no people, no silhouettes, austere industrial only

3. **Human listening review** (required before final export):
   - L001 (HOOK pacing), L003 (TOO_SHORT — content completeness), L008 (critical placement), L013/L014 (sensitive content), L028 (Ma beat approach)

4. **Post-process images** (before fine assembly):
   - IMG002, IMG004 (caption), IMG008, IMG011, IMG016

5. **Begin NLE rough assembly** when image gaps resolved:
   - Import all 28 audio files per timecodes in `timeline/timeline_assembly_plan.md`
   - Place L008 clip at sec=157 (2:37)
   - Place L028 clip at sec=575 (9:35)
   - Leave narration track empty from sec=620–660 (Ma beat)

6. **NLE export inspection**:
   - Verify narration track empty at Ma beat before any render

---

*Production Report — Stage 38 — hashima-island-mystery-ja — 2026-06-28*
