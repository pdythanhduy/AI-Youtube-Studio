# Voice Pace Fix v1 Report
## hashima-island-mystery-ja — Stage 41

**Date:** 2026-06-28  
**Status:** SCRIPTS READY — Not yet executed  
**Method:** FFmpeg atempo=0.82

---

## Problem

Vbee TTS API was called with `VBEE_INCLUDE_SPEED=false` (speed field excluded from payload after Stage 34 fix). The intended `speed_rate=0.75–0.85` was never sent. All 28 segments exported at speed_rate=1 (normal speed).

**Result in Rough V1:**
- Actual narration: **345.12s** (5m 45s)
- Planned narration: **~423s** (7m 3s)
- Deficit: **-77.88s** of narration
- Visual silence: **322.88s** (53.8% of video) — too much dead space

---

## Solution

Apply FFmpeg `atempo=0.82` to all 28 narration MP3 files.

- **atempo=0.82** = playback at 82% speed = audio 1.22× longer
- Single-pass valid: 0.82 is within [0.5, 2.0] range — no chaining needed
- Command per file:
  ```
  ffmpeg -i input.mp3 -filter:a "atempo=0.82" -codec:a libmp3lame -q:a 2 output_slow082.mp3
  ```

---

## Expected Results

| Metric | V1 (raw) | V2 (slowed) | Change |
|--------|----------|-------------|--------|
| Total narration | 345.12s | 420.88s | +75.76s |
| Visual silence | 322.88s | 247.12s | -75.76s |
| Ma beat buffer | 7.85s | **0.86s** | -6.99s |
| L008 ends at | 179.03s | 183.87s | +4.84s |
| L028 ends at | 595.42s | 599.90s | +4.48s |

---

## Per-Line Slowed Durations

| Line | Raw (s) | Slowed (s) | Start V1 | Start V2 |
|------|---------|-----------|----------|----------|
| L001 | 4.42 | 5.39 | 0.0 | 0.0 |
| L002 | 8.11 | 9.89 | 10.0 | 10.0 |
| L003 | 2.66 | 3.24 | 25.0 | 25.0 |
| L005 | 16.44 | 20.05 | 61.0 | 61.0 |
| L006 | 15.10 | 18.41 | 100.0 | 100.0 |
| L007 | 12.77 | 15.57 | 131.0 | 131.0 |
| L008 | 22.03 | **26.87** | **157.0** | **157.0 (FIXED)** |
| L009 | 29.62 | 36.12 | 181.0 | 185.0 |
| L011 | 17.16 | 20.93 | 214.0 | 224.0 |
| L012 | 22.85 | 27.87 | 233.0 | 246.0 |
| L013 | 6.84 | 8.34 | 257.0 | 275.5 |
| L014 | 14.35 | 17.50 | 269.0 | 285.0 |
| L015 | 16.46 | 20.07 | 286.0 | 303.0 |
| L016 | 13.03 | 15.89 | 305.0 | 324.0 |
| L017 | 17.16 | 20.93 | 331.0 | 340.5 |
| L018 | 5.59 | 6.82 | 362.0 | 362.5 |
| L019 | 10.39 | 12.67 | 391.0 | 391.0 |
| L020 | 4.46 | 5.44 | 422.0 | 422.0 |
| L021 | 10.08 | 12.29 | 452.0 | 452.0 |
| L023 | 12.43 | 15.16 | 481.0 | 481.0 |
| L024 | 11.30 | 13.78 | 511.0 | 511.0 |
| L025 | 7.82 | 9.54 | 528.0 | 528.0 |
| L027 | 9.86 | 12.02 | 545.0 | 545.0 |
| L028 | 20.42 | **24.90** | **575.0** | **575.0 (FIXED)** |
| L029 | 13.73 | 16.74 | 596.42 | 600.4 |
| L032 | 8.18 | 9.98 | 661.0 | 661.0 |
| L033 | 7.39 | 9.01 | 692.0 | 692.0 |
| L034 | 4.39 | 5.35 | 707.0 | 707.0 |
| **Total** | **345.12** | **420.88** | | |

---

## Critical Timing Analysis

### L008 Anchor (FIXED at 2:37 = 157.0s)
- V1: ends 179.03s (bleeds 14.03s into S009/S008 boundary)
- V2: ends 183.87s (bleeds 3.87s into S009) — SLIGHTLY LONGER BLEED
- **Status: OK** — L009 pushed to 185.0s to accommodate. 1.13s gap.

### L028 Anchor (FIXED at 9:35 = 575.0s)
- V1: ends 595.42s (19.42s into S021)
- V2: ends 599.90s (19.90s into S021)
- **Status: OK** — extends slightly further but Ma beat still intact.

### Ma Beat (10:20–11:00 = 620–660s)
- V2 narration chain end:
  - L028 ends 599.90s
  - Gap 0.5s
  - L029 starts 600.4s, ends 617.14s
  - L030 pause: 617.14s → 619.14s
  - **Narration ends: 619.14s**
  - **Ma beat starts: 620.0s**
  - **Buffer: 0.86s**
- **Status: INTACT but TIGHT**

> **RF-V2-001 [HIGH]:** Ma beat buffer has shrunk from 7.85s (V1) to 0.86s (V2). After running `slow_vbee_audio.py`, verify actual L029 output duration from ffprobe. If actual > 16.74s expected, check `production/vbee_slow_082_manifest_check_report.md` and consider adjusting L029 start from 600.4s → 600.0s (gains 0.4s). Do NOT adjust L028 anchor.

---

## Files Created

| File | Purpose |
|------|---------|
| `tools/audio/slow_vbee_audio.py` | Apply atempo=0.82 to 28 MP3s, write manifest |
| `tools/audio/check_slow_audio_manifest.py` | Verify 28 slowed files, write check report |
| `audio/vbee_slow_082/` | Output directory (empty until script runs) |
| `data/timeline_assembly_plan_v2.json` | Updated timeline with vbee_slow_082 audio paths |
| `timeline/timeline_assembly_plan_v2.md` | Human-readable V2 timeline |
| `tools/render/render_rough_video.py` | Updated: `--timeline` flag added |

---

## Run Commands

```bash
# Step 1: Dry run preview (no files written)
python tools\audio\slow_vbee_audio.py --dry-run

# Step 2: Process single test file
python tools\audio\slow_vbee_audio.py --segment L008

# Step 3: Process all 28 files
python tools\audio\slow_vbee_audio.py

# Step 4: Verify results
python tools\audio\check_slow_audio_manifest.py

# Step 5: Rough V2 render (audio mix only)
python tools\render\render_rough_video.py --timeline data/timeline_assembly_plan_v2.json --concat-only
```

---

## Acceptance Criteria

- [ ] 28 files in `audio/vbee_slow_082/` all ending with `_slow082.mp3`
- [ ] `check_slow_audio_manifest.py` reports: 28/28 OK, STATUS: PASS
- [ ] Total slowed duration: 420.88s ± 5% (≥400s, ≤442s)
- [ ] L029 actual duration ≤ 17.5s (Ma beat buffer ≥ 0.3s)
- [ ] Rough V2 renders to 720.00s
- [ ] Human listen confirms narration no longer sounds rushed

---

## Risks

| Risk | Severity | Probability | Mitigation |
|------|----------|------------|------------|
| Ma beat buffer at 0.86s | HIGH | LOW | Monitor L029 actual output after atempo |
| atempo pitch change noticeable | MEDIUM | LOW | 0.82 is within natural human range. Listen test required |
| FFmpeg audio codec quality | LOW | VERY LOW | -q:a 2 VBR is high quality (≈190kbps) |
| L003 still too short at 3.24s | LOW | CERTAIN | 3.24s vs 6s target — dramatic line, may be intentional. Human listen |

---

## What Did NOT Change

- Script/narration content — unchanged
- Image assets — unchanged
- Scene durations — unchanged
- Total video duration — still 720s
- L008 anchor: 157.0s (2:37) — unchanged
- L028 anchor: 575.0s (9:35) — unchanged
- Ma beat: 620–660s (40s) — unchanged
- Audio architecture (adelay+amix render pipeline) — unchanged
