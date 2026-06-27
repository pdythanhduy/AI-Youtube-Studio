# Rough V3 Tight Cut Plan Report
## hashima-island-mystery-ja — Stage 43

**Date:** 2026-06-28  
**Status:** PLAN COMPLETE — render pending  
**Audio:** `audio/vbee_slow_090/` (atempo=0.90)

---

## Problem Statement

Rough V1/V2 (both at 12:00 / 720s) feel too slow:
- Narration ends. Image holds. Nothing changes. Viewer disengages.
- Total visual silence: 284s = 39.5% of video time.
- Ma beat (40s, 10:20-11:00): felt frozen, not intentional.
- Key offenders: S014 (30s scene, 6s narration = 24s dead air), S016 (30s / 5s / 25s dead air), S022 (40s static = 40s dead air).

Rough V3 fixes this by designing each scene duration proportionally to its narration content.

---

## V3 Design

### Duration Comparison

| Version | Duration | Narration | Pauses | Ma Beat | Organic Silence | Silence % |
|---------|----------|-----------|--------|---------|----------------|-----------|
| V1 raw  | 720s     | 345.12s   | 12s    | 40s     | 322.88s        | 44.8%     |
| V2_090  | 720s     | 383.88s   | 12s    | 40s     | 284.12s        | 39.5%     |
| **V3**  | **556s** | **383.88s**| **12s**| **17s** | **143.12s**   | **25.7%** |

V3 = 9:16. Saves 164s (2 min 44s) from V2. Narration unchanged — same 28 lines, same 0.90x audio.

### Silence Reduction Detail

Total silence reduction V2 → V3: **141s (50% less organic silence)**

By source:
| Source | V2 | V3 | Saved |
|--------|----|----|-------|
| S022 Ma beat | 40s | 17s | 23s |
| S014 date card | ~24s | ~4s | 20s |
| S016 personal items | ~25s | ~6s | 19s |
| S020 establishing | ~29s | ~10s | 19s |
| S005 Meiji | ~22s | ~7s | 15s |
| S023 OUTRO | ~21s | ~7s | 14s |
| S015 dock | ~19s | ~4s | 15s |
| Other (18 scenes) | ~104s | ~70s | 34s |
| **Total** | **284s** | **143s** | **141s** |

---

## Ma Beat Analysis

| Metric | V1/V2 | V3 |
|--------|-------|----|
| Duration | 40s | **17s** |
| Position | 10:20-11:00 (620-660s) | **8:22-8:39 (502-519s)** |
| Narration ends before Ma | 615.46s (4.54s before) | **485.76s (16.24s before)** |
| Pre-Ma silence origin | end of S021 buffer | **intentional quiet in S021** |
| Visual treatment | static 40s hold | **static + 1s fade in + 1.5s dissolve out** |

The 17s Ma beat at 8:22 is INTENTIONAL — not a freeze:
1. Pre-Ma silence (16.24s) in S021 creates emotional build before S022 starts
2. Fade-in at S022 start signals "this is on purpose"
3. 17s of silence + ocean waves = breathing room, not technical failure
4. Dissolve-out before S023 signals the beat has ended

Risk: 17s may feel short if music/ambience has not been added. If human review of rough V3 finds Ma beat too brief, can extend to 20-22s by adding 3-5s to S022 and adjusting S022 end_sec in JSON.

---

## Architecture Changes

### L008 Anchor Removed

| Version | L008 start | Scene | Notes |
|---------|-----------|-------|-------|
| V1/V2 | 157.0s (2:37) | S007 (bridge to S008) | Fixed anchor maintained across all versions |
| **V3** | **107.0s (1:47)** | **S008 (clean start)** | No bridge needed. S008 = 28s to contain L008 fully. |

V1 held L008 at 157s because the director marked it as a critical timing point. In V3, that constraint is released — L008 now starts exactly when S008 begins. S007 is simplified (20s, L007 only, 5.29s buffer).

### L028 Anchor Removed

| Version | L028 start | Scene | Notes |
|---------|-----------|-------|-------|
| V1/V2 | 575.0s (9:35) | S020 dead air area | 19s of S020 was padding to reach the anchor |
| **V3** | **445.5s (7:25)** | **S021 entry** | L028 starts at S021. S020 compressed to 21s. |

In V3, S021 is the narrative and emotional pivot — it carries L028 (22.70s) + L029 (15.26s) + L030 pause (2s) + 16.24s pre-Ma silence. Total S021 duration: 57s. This is V3's "weight" scene.

### Only Audio Bridge in V3

**L012** spans S010→S011a (starts 195.0s, scene cut at 207.0s, ends 220.42s).  
L012 = 25.42s. Begins in S010 (12s of it plays in S010), continues 13.42s into S011a.  
This bridge is preserved from V2 and is intentional — the narration about the mine shaft connects the two mine scenes.

---

## Audio Recommendation

**USE `audio/vbee_slow_090/` (atempo=0.90) — confirmed for V3.**

| Audio Option | Total | V3 Silence % | Assessment |
|-------------|-------|--------------|------------|
| Raw 1.00x (345.12s) | 345.12s in 556s | 35.0% | Better than V2 raw, but scene-level gaps return |
| **0.90x (383.88s)** | **383.88s in 556s** | **25.7%** | **RECOMMENDED** |
| 0.82x (420.88s) | 420.88s in 556s | 22.3% | Voice sounds AI-dragging (human review rejected) |

The 0.90x audio's 38.76s of extra narration time fills V3's scene buffers cleanly. Raw 1.00x in V3 would still leave short scenes feeling empty (e.g., S008's 28s window with 22s raw audio = 6s dead air vs 3.5s with 0.90x).

---

## Files Created (Stage 43)

| File | Type | Description |
|------|------|-------------|
| `data/timeline_assembly_plan_v3_tight.json` | JSON | Full 25-scene V3 timeline, 556s |
| `timeline/timeline_assembly_plan_v3_tight.md` | Markdown | Human-readable timeline table |
| `production/rough_v3_tight_cut_plan_report.md` | Markdown | This report |
| `tools/render/render_rough_video.py` | Script | Added `--output` flag + dynamic TOTAL_DURATION from meta |
| `tools/render/verify_rough_timeline.py` | Script | Added `--timeline` flag, dynamic Ma beat/duration, audio file check, no-overflow check |

---

## Render Commands

```powershell
# Step 1: Render V3 tight
python tools\render\render_rough_video.py `
    --timeline data/timeline_assembly_plan_v3_tight.json `
    --output export/rough/hashima_rough_v3_tight.mp4 `
    --concat-only

# Step 2: Verify V3 tight
python tools\render\verify_rough_timeline.py `
    --timeline data/timeline_assembly_plan_v3_tight.json `
    --video export/rough/hashima_rough_v3_tight.mp4
```

### Pre-render check

Confirm all audio files exist before render:
```powershell
python tools\render\verify_rough_timeline.py `
    --timeline data/timeline_assembly_plan_v3_tight.json `
    --video export/rough/hashima_rough_v3_tight.mp4
```
Check 6 (Audio files present) will fail if files are missing without needing the video to exist.

---

## Verification Targets (V3)

| Check | Target | Tolerance |
|-------|--------|-----------|
| Duration | 556s (9:16) | ±3s |
| Ma beat window | 502-519s narration-free | exact |
| Ma beat duration | 17s | reference |
| Ma beat position | 8:22-8:39 | reference |
| Audio files | 28 files in audio/vbee_slow_090/ | all present |
| Scene count | 25 | exact |
| Video stream | 1920x1080 h264 | exact |
| Audio stream | aac 44100Hz 2ch | present |

---

## Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| Ma beat at 17s feels too brief without music/ambience | MEDIUM | Extend S022 to 20-22s in JSON if needed |
| S014 (11s) feels rushed for an emotional date reveal | LOW | S014 has 4.26s post-narration hold; if still rushed, extend to 14s |
| S016 (11s) personal items close-up | LOW | 2s pre-silence + 4s post gives weight; human review required |
| Scene clips in render_cache/ are from V1 (720s) | HIGH | Must re-render clips for V3 (different durations); use --concat-only ONLY after re-rendering |
| V3 has no music/ambience yet | HIGH | All render-stage assessment is narration-only; add music bed before final human review |

---

## Next Steps

1. **Render V3**: Run render command above (full render, not --concat-only, since scene durations changed)
2. **Verify V3**: Run verify command — target 556s ±3s, Ma beat clear
3. **Human review V3**: Watch at 1x speed — confirm pacing feels documentary, not rushed
4. **Ma beat eval**: If 17s feels too short at rough stage, extend S022 to 20-22s
5. **Compare V2 vs V3**: Watch the same 5-minute segment in both; confirm V3 feels tighter
6. **Fine cut prep**: Resolve MG001-MG004 placeholders, add music bed, add ambience
