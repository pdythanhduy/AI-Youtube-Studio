# Rough Video v1 — Assembly Report

**Stage:** 40  
**Date:** 2026-06-28  
**Project:** hashima-island-mystery-ja  
**Status:** SCRIPTS READY — awaiting render execution

---

## Input Assets Summary

| Category | Count | Status |
|----------|-------|--------|
| Scenes total | 25 | Defined in timeline_assembly_plan.json |
| Image scenes (AI-generated) | 17 | All files verified present |
| Image scenes (real/licensed) | 2 | S007 (IMG006 CC BY 2.0), S024 (IMG020 Govt 1974) |
| Motion graphics scenes | 4 | S004 MG001, S006 MG002, S012 MG003, S014 MG004 |
| Narration audio files | 28 | All verified in audio/vbee_raw/ |
| Unique audio placements | 28 | Deduped by filename (cross-cut files counted once) |
| Total audio duration | 345.12s | Per vbee_full_export_qa.json |
| Total video target | 720.0s | 12:00 exactly |

### Missing Assets

None. All 21 image files and 28 audio files verified present on disk before render.

---

## Render Method

**Pipeline:** Python-generated ffmpeg commands (subprocess)  
**Engine:** ffmpeg 7.1.1-essentials (C:\ffmpeg\...)  
**Script:** `tools/render/render_rough_video.py`

### Per-Scene Approach

| Scene type | ffmpeg command | Motion filter |
|------------|----------------|---------------|
| Image — static | `-loop 1 -i IMG ... -vf scale=1920:1080,crop` | Crop to fill |
| Image — zoom in | `-loop 1 -i IMG ... -vf scale+crop,zoompan` | zoompan z=1.0->1.1 |
| Image — zoom out | `-loop 1 -i IMG ... -vf scale+crop,zoompan` | zoompan z=1.1->1.0 |
| Image — pan right | `-loop 1 -i IMG ... -vf scale+crop,crop:x='t/D*px'` | Animated crop |
| Image — pan left | `-loop 1 -i IMG ... -vf scale+crop,crop:x='px-t/D*px'` | Animated crop |
| MG placeholder | `-f lavfi -i color=0x0a0a18 -vf drawtext` | Fade in/out only |

### Audio Mix Approach

- 28 MP3 narration files placed at absolute timecodes using `adelay` filter
- `filter_complex_script` written to file to avoid Windows CLI length limits
- Output: 720s PCM WAV (`audio_mix.wav`) → re-encoded to AAC 192k in final mux

### Scene-Level Post-Processing (applied in rough render)

| Scene | Image | Applied filter |
|-------|-------|----------------|
| S010 | IMG003 (dual-use) | `eq=saturation=0.80:gamma_r=0.95:gamma_b=1.02` (cooler) |
| S019 | IMG010 (dual-use) | `eq=saturation=0.88:gamma_r=1.08:gamma_b=0.92` (warmer) |
| S002 | IMG002 | `eq=saturation=0.35:brightness=-0.07` (heavy desaturate) |
| S009 | IMG008 | `eq=saturation=0.72` (reduce sepia) |
| S020 | IMG016 | `eq=saturation=0.83` (sky desaturate) |
| S001 | — | `fade=in:st=0:d=1.0` |
| S022 | — | `fade=in:st=0:d=1.0` + `fade=out:st=38.5:d=1.5` |
| S024 | — | `fade=out:st=28:d=2.0` |

---

## Render Commands

### Full render (with motion effects, ~30-60 min)

```
cd C:\youtubeAI\AI-Youtube-Studio\projects\hashima-island-mystery-ja
python tools\render\render_rough_video.py
```

### Fast render (no motion / static only, ~8-15 min)

```
python tools\render\render_rough_video.py --no-motion
```

### Resume interrupted render (skip existing clips)

```
python tools\render\render_rough_video.py --skip-existing
```

### Dry run (print commands, no execution)

```
python tools\render\render_rough_video.py --dry-run
```

### Verify after render

```
python tools\render\verify_rough_timeline.py
```

---

## Output Path

```
export/rough/hashima_rough_v1.mp4
```

Expected size: ~400-800 MB (720s at CRF 28, ultrafast)

---

## Render Time Estimate

| Mode | Estimated time |
|------|----------------|
| `--no-motion` (static all) | 8-15 min |
| With motion (pan scenes only) | 15-25 min |
| Full motion (zoom scenes via zoompan) | 30-60 min |
| `--fps 12` (half-rate rough) | 40-60% of above |

Render speed depends on CPU. zoompan is single-threaded in ffmpeg.

---

## Render Cache

Scene clips are written to: `timeline/render_cache/`

| File | Purpose |
|------|---------|
| `s001.mp4` ... `s024.mp4` | Individual scene clips (25 total) |
| `concat.txt` | ffmpeg concat list |
| `video_raw.mp4` | Concatenated video (no audio) |
| `audio_filter.txt` | ffmpeg filter_complex script for audio mix |
| `audio_mix.wav` | 720s PCM audio (all narration placed) |

Intermediate files are reused if `--skip-existing` flag is used.

---

## Timeline Compliance

| Constraint | Target | Implementation |
|-----------|--------|----------------|
| Total duration | 720.0s | Scene durations sum to 720.0s per timeline plan |
| L008 placement | sec=157 (2:37) | Audio placed via `adelay=157000ms` |
| L028 placement | sec=575 (9:35) | Audio placed via `adelay=575000ms` |
| Ma beat (10:20-11:00) | No narration sec=620-660 | No audio files placed in this window |
| Resolution | 1920x1080 | All scenes output `-s 1920x1080` |
| Frame rate | 24fps | All scenes at `-r 24` |
| Scene count | 25 | 25 scenes in timeline plan |

---

## Known Limitations of Rough v1

1. **Motion graphics (MG001-MG004)**: Black background with ASCII text placeholder. No actual animated title/map/data graphics. These must be replaced in fine cut.

2. **Transitions**: Hard cuts between all scenes except S001 (fade in), S022 (fade in/out), S024 (fade out). No cross-dissolves implemented.

3. **No music bed / no ambience**: Narration-only audio. Music and ambient sound must be added in fine cut NLE session.

4. **Post-processing approximated**:
   - IMG002 film grain: not applied (eq filter only, no grain overlay)
   - IMG004 caption overlay: not applied (must add in NLE)
   - IMG011 pan direction: approximate (slow_pan_left applied)
   - All color grades are rough eq approximations, not final LUT-based grades

5. **Crop framing for S010/S019**: Color differentiation applied. Exact crop offset to vine/concrete edge (S010) and moss/rust surface (S019) must be refined in NLE frame-by-frame.

6. **zoompan quality**: At ultrafast/CRF28, zoom scenes may show compression artifacts. Re-render at `medium`/CRF23 for fine cut.

7. **L001 audio**: Vbee manifest shows L001 as `status: "skipped"` — verify in playback. File may be silent or short.

8. **No closed captions / subtitles**: Japanese subtitle track not included in rough.

---

## Human Review Checklist

After rendering, verify the following before proceeding to fine cut:

### Critical
- [ ] Video file exists at `export/rough/hashima_rough_v1.mp4`
- [ ] Duration ~720s (12:00) confirmed in media player
- [ ] L008 audible at 2:37 timestamp
- [ ] L028 audible at 9:35 timestamp
- [ ] Ma beat (10:20-11:00) is completely silent on narration track
- [ ] Run `python tools/render/verify_rough_timeline.py` — all 8 checks pass

### Audio
- [ ] L001 (HOOK opener): plays correctly, not silent
- [ ] L003 ('すべてが消えました'): 2.66s line is complete, not truncated
- [ ] L013/L014 (sensitive content): tone is appropriate, not clinical
- [ ] Overall narration pacing: 322.88s visual silence acceptable as documentary breathing

### Visual
- [ ] S010 color reads differently from S003 (cooler, vine-edge focus)
- [ ] S019 color reads as warm concrete/rust, not mine shaft cold
- [ ] S022 Ma beat panorama: feels like intentional silence, not dead air
- [ ] MG placeholder clips are clearly identified for replacement
- [ ] No obvious render artifacts or ffmpeg errors visible

### Compliance
- [ ] IMG009 (S011a): Producer review scheduled before fine cut
- [ ] IMG004 (S005): Note to add '参考映像' caption overlay in fine cut
- [ ] Attribution text ready for YouTube description (IMG006, IMG020)

---

## Next Actions After Rough Review

1. Human review of rough v1 (checklist above)
2. Fine cut session: replace MG placeholders, add music/ambience, refine crop framing
3. Final color grade (LUT-based, not eq approximation)
4. Add closed captions (Japanese)
5. Community guidelines review (COMP-007 gate)
6. Thumbnail design
7. YouTube description with attribution
8. Publish
