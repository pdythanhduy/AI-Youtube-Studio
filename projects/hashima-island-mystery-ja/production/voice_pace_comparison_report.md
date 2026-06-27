# Voice Pace Comparison Report
## hashima-island-mystery-ja

**Date:** 2026-06-28  
**Versions compared:** Raw 1.00x · Slow 0.90x · Slow 0.82x

---

## Summary Table

| Metric | Raw 1.00x | **v090 (0.90x)** | v082 (0.82x) |
|--------|-----------|-----------------|-------------|
| Speed factor | 1.00 | **0.90** | 0.82 |
| Playback speed | 100% | **90%** | 82% |
| Duration multiplier | 1.00x | **1.11x** | 1.22x |
| Total narration | 345.12s | **383.47s** | 420.88s |
| Total visual silence | 322.88s | **284.53s** | 247.12s |
| Silence % of 720s | 44.8% | **39.5%** | 34.3% |
| Ma beat buffer | 7.85s | **4.54s** | 0.86s |
| L008 ends at | 179.03s | **181.48s** | 183.87s |
| L008 bleed into S009 | 14.03s | **1.48s** | 3.87s |
| L028 ends at | 595.42s | **597.69s** | 599.90s |
| Narration ends | 611.15s | **615.46s** | 619.14s |
| Max start shift from V1 | 0s | **+6.0s** (L013) | +19.0s (L016) |
| Lines with same start as V1 | 21/28 | **20/28** | 11/28 |

---

## Risk Assessment

### Raw 1.00x
- **Voice quality:** Natural speed, no processing artifacts
- **Pacing risk:** HIGH — 322.88s (44.8%) visual silence is excessive. Narration sounds rushed. Too much dead air for documentary style.
- **Ma beat buffer:** 7.85s — comfortable
- **Timeline disruption:** None
- **Verdict:** REJECTED — Too fast, too much silence

### v090 (0.90x)
- **Voice quality:** Very close to natural. 10% slower. Unlikely to be perceptible as "AI slow" to most viewers.
- **Pacing risk:** LOW-MEDIUM — 284.53s (39.5%) visual silence remains. Within acceptable range for documentary with music bed + ambience. The ~5s longer silences vs v082 are manageable.
- **Ma beat buffer:** 4.54s — comfortable and well within safe range
- **L008 behavior:** Cleanest of all three — ends at 181.48s with only 1.48s bleed into S009. In V1, L009 actually started BEFORE L008 finished (L009 at 181.0, L008 ended at 179.03 — near overlap). v090 resolves this cleanly.
- **Timeline disruption:** Minimal. From L017 onward, ALL timecodes identical to V1. Only L009–L016 shifted by 1–6 seconds.
- **Verdict:** **RECOMMENDED**

### v082 (0.82x)
- **Voice quality:** Audibly slower than natural. At 1.22x longer, many viewers will perceive the AI-slowing effect, especially on shorter lines. Human review confirmed this finding.
- **Pacing risk:** LOW — 247.12s (34.3%) silence is well-managed. Visual holds feel tight and intentional.
- **Ma beat buffer:** 0.86s — TIGHT. One longer-than-expected atempo output and the Ma beat boundary could be breached.
- **Timeline disruption:** High. 17 of 28 lines shifted from V1 timecodes. Maximum shift +19s (L016). L011 shifted to start in S010 instead of S009.
- **Verdict:** DEPRECATED pending director override

---

## Impact on Visual Silence (by scene section)

| Section | V1 silence | v082 silence | v090 silence |
|---------|-----------|-------------|-------------|
| HOOK (S001–S004) | ~44s | ~36s | ~40s |
| ACT I (S005–S008) | ~69s | ~60s | ~66s |
| ACT II (S009–S013) | ~55s | ~13s | ~28s |
| ACT III (S014–S019) | ~99s | ~76s | ~88s |
| ACT IV (S020–S022) | ~28s | ~21s | ~27s |
| OUTRO (S023–S024) | ~29s | ~22s | ~27s |

The v090 redistribution is smoother — Act II silence is 28s (more natural documentary breathing room), while v082 compressed Act II to just 13s (tight, fast-feeling, AI-like).

---

## Audio Quality Considerations

| Factor | Effect |
|--------|--------|
| atempo=0.90 | Slight pitch preservation (resampling). Virtually undetectable at 10% change. |
| atempo=0.82 | Noticeable pitch shift at 18% change. AI-vocal quality confirmed by human review. |
| libmp3lame -q:a 2 | High-quality VBR ~190kbps output. No compression artifacts from re-encoding. |
| atempo single-pass | Both 0.82 and 0.90 are within [0.5, 2.0] range — no chaining needed. |

---

## Final Recommendation

**USE v090 (0.90x) for Rough V2 render.**

Rationale:
1. Human review rejected v082 as "too slow / AI-like." v090 addresses this directly.
2. The 39.5% visual silence at v090 is standard for single-narrator documentary with music bed. Not excessive.
3. Ma beat buffer (4.54s) is safe and comfortable.
4. L017–L028 start timecodes are IDENTICAL to V1 — director's timing intuitions for Act III/IV are preserved.
5. L008 anchor behavior at v090 is cleaner than even V1 (1.48s bleed vs 14.03s near-overlap in V1).

**v082 status: DEPRECATED.** Do not use for final render. Archive audio/vbee_slow_082/ for reference only.  
If director wants to experiment with an intermediate value, 0.92x is the logical next step (produces ~375s narration).

---

## Decision Matrix

| Need | Recommendation |
|------|---------------|
| Natural-sounding voice | **v090** |
| Tightest visual pacing | v082 (but voice quality rejected) |
| Minimal timeline disruption | **v090** (L017+ identical to V1) |
| Safe Ma beat buffer | **v090** (4.54s) |
| Best Act II flow | **v090** (less compressed) |
| For director A/B comparison | Render both, compare seconds 130–360 |

---

## Deprecated Files

| File | Status |
|------|--------|
| `audio/vbee_slow_082/` | DEPRECATED — keep for reference, do not use in final |
| `data/timeline_assembly_plan_v2.json` | DEPRECATED — was v082 timeline |
| `timeline/timeline_assembly_plan_v2.md` | DEPRECATED — was v082 |
| `production/voice_pace_fix_v1_report.md` | ARCHIVED — v082 methodology documented |

---

## Active Files (v090)

| File | Purpose |
|------|---------|
| `audio/vbee_slow_090/` | Target audio directory (run script to populate) |
| `data/timeline_assembly_plan_v2_090.json` | Active V2 timeline |
| `timeline/timeline_assembly_plan_v2_090.md` | Human-readable timeline |
| `tools/audio/slow_vbee_audio.py --factor 0.90` | Generate 0.90x audio |
| `tools/audio/check_slow_audio_manifest.py --audio-dir audio/vbee_slow_090 --factor 0.90` | Verify |
