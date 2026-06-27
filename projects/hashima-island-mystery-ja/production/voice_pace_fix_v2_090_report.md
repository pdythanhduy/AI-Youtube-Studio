# Voice Pace Fix v2 Report — atempo=0.90
## hashima-island-mystery-ja — Stage 42

**Date:** 2026-06-28  
**Status:** SCRIPTS READY — Not yet executed  
**Method:** FFmpeg atempo=0.90  
**Trigger:** v1 (0.82x) human review found voice too slow / AI-dragging

---

## Background

Voice Pace Fix v1 applied atempo=0.82, which extended narration from 345.12s to 420.88s.  
Human review found this created an unnatural dragging quality.

This report documents v2: atempo=0.90, a lighter adjustment that preserves more natural voice rhythm.

---

## Expected Results

| Metric | Raw (1.00x) | v082 | **v090** |
|--------|------------|------|----------|
| Total narration | 345.12s | 420.88s | **383.47s** |
| Visual silence | 322.88s | 247.12s | **284.53s** |
| Silence % | 44.8% | 34.3% | **39.5%** |
| Ma beat buffer | 7.85s | 0.86s | **4.54s** |
| L008 bleed | +14.03s | +3.87s | **+1.48s** |
| Change vs V1 | — | +75.76s | **+38.35s** |

---

## Per-Line Slowed Durations at 0.90x

| Line | Raw (s) | 0.90x (s) | V1 Start | V090 Start | Shift |
|------|---------|----------|----------|-----------|-------|
| L001 | 4.42 | 4.91 | 0.0 | 0.0 | 0 |
| L002 | 8.11 | 9.01 | 10.0 | 10.0 | 0 |
| L003 | 2.66 | 2.96 | 25.0 | 25.0 | 0 |
| L005 | 16.44 | 18.27 | 61.0 | 61.0 | 0 |
| L006 | 15.10 | 16.78 | 100.0 | 100.0 | 0 |
| L007 | 12.77 | 14.19 | 131.0 | 131.0 | 0 |
| L008 | 22.03 | 24.48 | 157.0 | 157.0 | FIXED |
| L009 | 29.62 | 32.91 | 181.0 | 182.0 | +1.0 |
| L011 | 17.16 | 19.07 | 214.0 | 217.5 | +3.5 |
| L012 | 22.85 | 25.39 | 233.0 | 237.0 | +4.0 |
| L013 | 6.84 | 7.60 | 257.0 | 263.0 | +6.0 |
| L014 | 14.35 | 15.94 | 269.0 | 271.0 | +2.0 |
| L015 | 16.46 | 18.29 | 286.0 | 287.5 | +1.5 |
| L016 | 13.03 | 14.48 | 305.0 | 306.5 | +1.5 |
| L017 | 17.16 | 19.07 | 331.0 | 331.0 | 0 (same as V1) |
| L018 | 5.59 | 6.21 | 362.0 | 362.0 | 0 |
| L019 | 10.39 | 11.54 | 391.0 | 391.0 | 0 |
| L020 | 4.46 | 4.96 | 422.0 | 422.0 | 0 |
| L021 | 10.08 | 11.20 | 452.0 | 452.0 | 0 |
| L023 | 12.43 | 13.81 | 481.0 | 481.0 | 0 |
| L024 | 11.30 | 12.56 | 511.0 | 511.0 | 0 |
| L025 | 7.82 | 8.69 | 528.0 | 528.0 | 0 |
| L027 | 9.86 | 10.96 | 545.0 | 545.0 | 0 |
| L028 | 20.42 | 22.69 | 575.0 | 575.0 | FIXED |
| L029 | 13.73 | 15.26 | 596.42 | 598.2 | +1.78 |
| L032 | 8.18 | 9.09 | 661.0 | 661.0 | 0 |
| L033 | 7.39 | 8.21 | 692.0 | 692.0 | 0 |
| L034 | 4.39 | 4.88 | 707.0 | 707.0 | 0 |
| **Total** | **345.12** | **383.47** | | | |

**Key observation:** From L017 onward, ALL start timecodes are identical to V1. Only early-to-mid Act II lines are shifted, with a maximum shift of +6s (L013).

---

## Critical Timing

### L008 (FIXED 2:37 = 157.0s)
- End: 181.48s (bleed 1.48s into S009)
- V1: ended 179.03s (bleed 14.03s past L009 start — L009 started before L008 ended)
- v082: ended 183.87s (bleed 3.87s)
- **v090: ended 181.48s (bleed 1.48s) — CLEANEST of all three versions**

### L028 (FIXED 9:35 = 575.0s)
- End: 597.69s (extends 17.69s into S021)
- Ma beat starts: 620.0s
- Buffer: **4.54s — comfortable**

### Ma Beat (10:20–11:00 = 620–660s)
- Narration chain: L028 (575–597.69) → gap → L029 (598.2–613.46) → L030 pause (613.46–615.46)
- Narration ends: 615.46s
- **Buffer: 4.54s (COMFORTABLE)**

---

## Visual Silence Analysis

Total visual silence: 284.53s (39.5% of 720s video)

The main silent stretches are concentrated in Act III (S014–S018), which is dramatically intentional for the evacuation/abandonment sequence. These can be filled with:
- Music bed (already planned)
- Ambient sound (wind, waves, structural creaks)
- Subtle motion on still frames (very slow pans already designed in)

A 10:30 or 11:00 cut is **not recommended** at 0.90x — the silence is within acceptable documentary range. If the director still finds too much silence after music+ambience, a 0.92x version can be tested, or selected scenes can be shortened.

---

## Run Commands

```bash
# Dry run — preview commands without processing
python tools\audio\slow_vbee_audio.py --factor 0.90 --dry-run

# Process single test file
python tools\audio\slow_vbee_audio.py --factor 0.90 --segment L008

# Process all 28 files
python tools\audio\slow_vbee_audio.py --factor 0.90

# Verify results
python tools\audio\check_slow_audio_manifest.py --audio-dir audio/vbee_slow_090 --factor 0.90

# Render Rough V2 (090 audio)
python tools\render\render_rough_video.py --timeline data/timeline_assembly_plan_v2_090.json --concat-only
```

---

## Acceptance Criteria

- [ ] 28 files in `audio/vbee_slow_090/` all ending with `_slow090.mp3`
- [ ] `check_slow_audio_manifest.py` reports: 28/28 OK, STATUS: PASS
- [ ] Total slowed duration: 383.47s ± 5% (≥365s, ≤403s)
- [ ] L029 actual end ≤ 615.5s (Ma beat buffer ≥ 4.5s)
- [ ] Rough V2 renders to 720.00s
- [ ] Human listen: narration sounds natural-paced (not rushed, not dragging)

---

## What Did NOT Change

- Script/narration content, images, scene durations, total video 720s
- L008 anchor: 157.0s (2:37)
- L028 anchor: 575.0s (9:35)
- Ma beat: 620–660s (40s)
- All start timecodes from L017 onward
- Audio render architecture (adelay+amix pipeline)
