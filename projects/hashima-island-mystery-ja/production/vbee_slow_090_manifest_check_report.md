# vbee_slow_090 Manifest Check Report

**Stage:** Voice Pace Fix  
**Date:** 2026-06-28 08:08  
**Speed factor:** 0.9 (atempo=0.9, 90% speed, 1.11x longer)  
**Audio dir:** `audio\vbee_slow_090`  
**Status:** PASS

---

## Summary

| Metric | Value |
|--------|-------|
| Speed factor | 0.9 (atempo=0.9) |
| Files expected | 28 |
| Files found (OK) | 28 |
| Files MISSING | 0 |
| Duration anomalies | 0 |
| Original total duration | 345.12s |
| Expected slowed duration | 383.47s |
| Actual slowed duration | 383.88s |
| Delta vs expected | +0.41s |

---

## File-by-File Results

| Line | In (s) | Exp Out (s) | Act Out (s) | Status |
|------|--------|-------------|-------------|--------|
| L001 | 4.42 | 4.91 | 4.92 | OK |
| L002 | 8.11 | 9.01 | 9.02 | OK |
| L003 | 2.66 | 2.96 | 2.98 | OK |
| L005 | 16.44 | 18.27 | 18.29 | OK |
| L006 | 15.10 | 16.78 | 16.80 | OK |
| L007 | 12.77 | 14.19 | 14.21 | OK |
| L008 | 22.03 | 24.48 | 24.50 | OK |
| L009 | 29.62 | 32.91 | 32.93 | OK |
| L011 | 17.16 | 19.07 | 19.08 | OK |
| L012 | 22.85 | 25.39 | 25.42 | OK |
| L013 | 6.84 | 7.60 | 7.61 | OK |
| L014 | 14.35 | 15.94 | 15.96 | OK |
| L015 | 16.46 | 18.29 | 18.31 | OK |
| L016 | 13.03 | 14.48 | 14.50 | OK |
| L017 | 17.16 | 19.07 | 19.08 | OK |
| L018 | 5.59 | 6.21 | 6.24 | OK |
| L019 | 10.39 | 11.54 | 11.57 | OK |
| L020 | 4.46 | 4.96 | 4.97 | OK |
| L021 | 10.08 | 11.20 | 11.21 | OK |
| L023 | 12.43 | 13.81 | 13.82 | OK |
| L024 | 11.30 | 12.56 | 12.58 | OK |
| L025 | 7.82 | 8.69 | 8.71 | OK |
| L027 | 9.86 | 10.96 | 10.97 | OK |
| L028 | 20.42 | 22.69 | 22.70 | OK |
| L029 | 13.73 | 15.26 | 15.26 | OK |
| L032 | 8.18 | 9.09 | 9.12 | OK |
| L033 | 7.39 | 8.21 | 8.23 | OK |
| L034 | 4.39 | 4.88 | 4.90 | OK |

---

## Next Steps

If all files are present and durations are OK:

1. Use `data/timeline_assembly_plan_v2_090.json` for render
2. Audio source: `audio\vbee_slow_090/`
3. Render: `python tools/render/render_rough_video.py --timeline data/timeline_assembly_plan_v2_090.json --concat-only`
