# Timeline Assembly Plan V2 — Voice Pace Fix
## hashima-island-mystery-ja

**Source timeline:** data/timeline_assembly_plan.json (V1)  
**Audio source:** audio/vbee_slow_082/  
**Speed factor:** atempo=0.82 (1.22× longer, 82% playback speed)  
**Original narration:** 345.12s | **Slowed narration:** 420.88s | **Change:** +75.76s

---

## Key Changes vs V1

| Metric | V1 | V2 | Delta |
|--------|----|----|-------|
| Total narration | 345.12s | 420.88s | +75.76s |
| Visual silence | 322.88s | 247.12s | -75.76s |
| Ma beat buffer | 7.85s | 0.86s | -6.99s |
| L008 ends | 179.03s | 183.87s | +4.84s |
| L028 ends | 595.42s | 599.90s | +4.48s |

**Anchors preserved:** L008 @ 2:37 (157.0s) and L028 @ 9:35 (575.0s) unchanged.

---

## Critical Timing Flags

### RF-V2-001 — Ma beat buffer TIGHT [HIGH]
- Narration ends: **619.14s**
- Ma beat starts: **620.00s**
- Buffer: **0.86s** (was 7.85s in V1)
- Status: TECHNICALLY INTACT
- Action: After running slow_vbee_audio.py, verify actual L029 output duration. If longer than 16.74s expected, adjust L029 start from 600.4 → 600.0.

### RF-003 — L008 bleeds 3.87s into S009 [INFO]
- L008 ends at 183.87s (3.87s past S009 start of 180s)
- L009 starts at 185.0s (gap 1.13s after L008 ends)
- Normal documentary audio practice.

---

## Scene-by-Scene Audio Map (V2)

| Scene | Range | Line IDs | V2 Start(s) | V2 End(s) | Silence in Scene |
|-------|-------|----------|-------------|-----------|-----------------|
| S001 | 0:00–0:10 | L001 | 0.0 | 5.39 | 4.61s |
| S002 | 0:10–0:25 | L002 | 10.0 | 19.89 | 5.11s |
| S003 | 0:25–0:40 | L003 | 25.0 | 28.24 | 11.76s |
| S004 | 0:40–1:00 | — (MG001) | — | — | 20.0s |
| S005 | 1:00–1:40 | L005 | 61.0 | 81.05 | 18.95s |
| S006 | 1:40–2:10 | L006 | 100.0 | 118.41 | 11.59s |
| S007 | 2:10–2:45 | L007, L008↓ | 131.0, **157.0** | 146.57, →S009 | 10.43s (L007→L008) |
| S008 | 2:45–3:00 | L008 (cont.) | **157.0** | →S009 | 0s |
| S009 | 3:00–3:40 | L008 tail, L009 | **157.0**, 185.0 | 183.87, →S010 | 1.13s |
| S010 | 3:40–4:10 | L011, L012↓ | 224.0, 246.0 | 244.93, →S011a | 1.07s |
| S011a | 4:10–4:40 | L012, L013, L014↓ | 246.0, 275.5, 285.0 | 273.87, 283.84, →S012 | 1.63s |
| S011b | 4:40–5:00 | L013, L014 | 275.5, 285.0 | 283.84, →S012 | 0s |
| S012 | 5:00–5:30 | L014, L015, L016↓ | 285.0, 303.0, 324.0 | 302.5, 323.07, →S013 | 0.5s |
| S013 | 5:30–6:00 | L016, L017↓ | 324.0, 340.5 | 339.89, →S014 | 0.61s |
| S014 | 6:00–6:30 | L017, L018 | 340.5, 362.5 | 361.43, 369.32 | 20.68s |
| S015 | 6:30–7:00 | L019 | 391.0 | 403.67 | 16.33s |
| S016 | 7:00–7:30 | L020 | 422.0 | 427.44 | 22.56s |
| S017 | 7:30–8:00 | L021, L022 (pause) | 452.0, 464.29 | 464.29, 466.29 | 13.71s |
| S018 | 8:00–8:30 | L023 | 481.0 | 496.16 | 13.84s |
| S019 | 8:30–9:00 | L024, L025, L026 (pause) | 511.0, 528.0, 537.54 | 524.78, 537.54, 539.54 | 3.22s |
| S020 | 9:00–9:40 | L027, L028↓ | 545.0, **575.0** | 557.02, →S021 | 17.98s |
| S021 | 9:40–10:20 | L028 tail, L029, L030 (pause) | **575.0**, 600.4, 617.14 | 599.90, 617.14, 619.14 | **0.86s** |
| S022 | 10:20–11:00 | — (Ma beat) | — | — | 40.0s |
| S023 | 11:00–11:30 | L032 | 661.0 | 670.98 | 19.02s |
| S024 | 11:30–12:00 | L033, L034 | 692.0, 707.0 | 701.01, 712.35 | 7.65s |

↓ = line bleeds into next scene

---

## Slowed Duration Reference (all ÷ 0.82)

| Line | Raw (s) | Slowed (s) | V1 Start | V2 Start |
|------|---------|-----------|----------|----------|
| L001 | 4.42 | 5.39 | 0.0 | 0.0 |
| L002 | 8.11 | 9.89 | 10.0 | 10.0 |
| L003 | 2.66 | 3.24 | 25.0 | 25.0 |
| L005 | 16.44 | 20.05 | 61.0 | 61.0 |
| L006 | 15.10 | 18.41 | 100.0 | 100.0 |
| L007 | 12.77 | 15.57 | 131.0 | 131.0 |
| L008 | 22.03 | **26.87** | **157.0** | **157.0** (FIXED) |
| L009 | 29.62 | 36.12 | 181.0 | 185.0 (+4.0) |
| L011 | 17.16 | 20.93 | 214.0 | 224.0 (+10.0) |
| L012 | 22.85 | 27.87 | 233.0 | 246.0 (+13.0) |
| L013 | 6.84 | 8.34 | 257.0 | 275.5 (+18.5) |
| L014 | 14.35 | 17.50 | 269.0 | 285.0 (+16.0) |
| L015 | 16.46 | 20.07 | 286.0 | 303.0 (+17.0) |
| L016 | 13.03 | 15.89 | 305.0 | 324.0 (+19.0) |
| L017 | 17.16 | 20.93 | 331.0 | 340.5 (+9.5) |
| L018 | 5.59 | 6.82 | 362.0 | 362.5 (+0.5) |
| L019 | 10.39 | 12.67 | 391.0 | 391.0 |
| L020 | 4.46 | 5.44 | 422.0 | 422.0 |
| L021 | 10.08 | 12.29 | 452.0 | 452.0 |
| L023 | 12.43 | 15.16 | 481.0 | 481.0 |
| L024 | 11.30 | 13.78 | 511.0 | 511.0 |
| L025 | 7.82 | 9.54 | 528.0 | 528.0 |
| L027 | 9.86 | 12.02 | 545.0 | 545.0 |
| L028 | 20.42 | **24.90** | **575.0** | **575.0** (FIXED) |
| L029 | 13.73 | 16.74 | 596.42 | 600.4 (+3.98) |
| L032 | 8.18 | 9.98 | 661.0 | 661.0 |
| L033 | 7.39 | 9.01 | 692.0 | 692.0 |
| L034 | 4.39 | 5.35 | 707.0 | 707.0 |
| **Total** | **345.12** | **420.88** | | |

---

## Run Order

```
# Step 1: Slow the audio
python tools\audio\slow_vbee_audio.py

# Step 2: Verify
python tools\audio\check_slow_audio_manifest.py

# Step 3: Rough V2 render
python tools\render\render_rough_video.py --timeline data/timeline_assembly_plan_v2.json --concat-only

# Dry run preview (no audio processed):
python tools\audio\slow_vbee_audio.py --dry-run

# Single segment test:
python tools\audio\slow_vbee_audio.py --segment L008
```
