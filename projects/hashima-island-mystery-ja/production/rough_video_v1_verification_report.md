# Rough Video v1 - Verification Report

**Generated:** 2026-06-27T23:16:18Z
**Video file:** `C:\youtubeAI\AI-Youtube-Studio\projects\hashima-island-mystery-ja\export\rough\hashima_rough_v1.mp4`
**Status:** ALL CHECKS PASSED ✅

---

## Check Results

| Check | Result | Detail |
|-------|--------|--------|
| 1. File exists | ✅ | PASS |
| 2. Duration ~720s | ✅ | PASS - 720.00s  (12:00)  delta=0.00s vs target 720s |
| 3. Video 1920×1080 | ✅ | PASS - h264 1920x1080 |
| 4. Audio stream | ✅ | PASS - aac  44100Hz  2ch |
| 5. Ma beat clear (10:20–11:00) | ✅ | PASS - Ma beat window [620–660s] (10:20–11:00) is narration-free |
| 6. L008 at 2:37 | ✅ | L008 anchor - PASS  placed at 157.0s (2:37)  target 157s  delta=0.0s |
| 7. L028 at 9:35 | ✅ | L028 anchor - PASS  placed at 575.0s (9:35)  target 575s  delta=0.0s |
| 8. 25 scenes | ✅ | PASS - 25 scenes (expected 25) |

---

## Critical Timing Anchors

| Anchor | Target | Status |
|--------|--------|--------|
| L008 (2:37) | sec=157 | L008 anchor - PASS  placed at 157.0s (2:37)  target 157s  delta=0.0s |
| L028 (9:35) | sec=575 | L028 anchor - PASS  placed at 575.0s (9:35)  target 575s  delta=0.0s |
| Ma beat clear | 620–660s | PASS - Ma beat window [620–660s] (10:20–11:00) is narration-free |

---

## Human Review Checklist

Before approving rough v1 for fine cut, verify:

- [ ] **L001** - HOOK opener: delivery has correct emotional weight
- [ ] **L003** - 'すべてが消えました': complete, not truncated (2.66s TTS)
- [ ] **L008** - Anchor placement audible at 2:37 in video playback
- [ ] **L013/L014** - Sensitive content (forced labor): tone appropriate
- [ ] **L028** - Pre-Ma-beat narration: clean ending before 9:35
- [ ] **S022 Ma beat** - 10:20–11:00 panorama silence feels intentional
- [ ] **S010** - IMG003 vine/concrete crop: reads as different scene from S003
- [ ] **S019** - IMG010 warm crop: reads as concrete/rust (not mine shaft)
- [ ] **IMG009 (S011a)** - Producer review completed before fine cut
- [ ] **IMG004 (S005)** - '参考映像' caption overlay added
- [ ] **Overall pacing** - 322.88s visual silence distributed; documentary rhythm acceptable

---

## Post-Processing Pending (before fine cut)

| Scene | Image | Action |
|-------|-------|--------|
| S002  | IMG002 | Desaturate 60–70%, darken −0.5–1 stop, film grain |
| S005  | IMG004 | Add '参考映像 / illustrative archival simulation' caption |
| S011a | IMG009 | Producer review required before import |
| S013  | IMG011 | Pan direction: start on ruins, move toward light shafts |
| S020  | IMG016 | Desaturate sky 15–20%, preserve warm dusk tone |

---

## Known Limitations - Rough v1

1. **Motion graphics**: MG001–MG004 are text placeholders on dark background
2. **Transitions**: Cuts only (no dissolves between scenes, except S022 fade)
3. **No music bed**: Narration-only audio track - no background music/ambience
4. **Post-processing approximated**: Color corrections via eq filter are rough;
   fine-grade in NLE required (especially IMG002 film grain, IMG011 pan framing)
5. **Crop framing (S010/S019)**: Color differentiation applied; exact crop
   framing for vine/concrete edge and moss/rust edge is NLE editor's task
6. **zoompan quality**: Motion at ultrafast/CRF28 may show blocking artifacts;
   re-render at medium/CRF23 for fine cut
7. **L001 file**: Vbee returned 'skipped' status - audio may be silent or missing.
   Verify L001 in playback.
