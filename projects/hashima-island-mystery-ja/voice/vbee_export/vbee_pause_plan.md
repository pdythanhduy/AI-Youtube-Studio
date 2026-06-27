# Vbee Pause Plan
## hashima-island-mystery-ja — Post-Export Editor Instructions
**Date:** 2026-06-27

---

## Critical Rule

**Vbee does not create pauses. The editor creates pauses.**

Do not attempt to generate silence, pauses, or the Ma beat inside Vbee. Export only the spoken narration segments. All pauses and silences are added in the editing timeline (DaVinci Resolve, Premiere, CapCut, or equivalent).

---

## Pause Events — Full List

After exporting all 27 Vbee narration files, insert the following silences in the editing timeline:

| Line | Type | Duration | Insert After | Timeline Position | Action |
|------|------|----------|-------------|-------------------|--------|
| L004 | 2s pause | 2 sec | L003 file ends | 0:26 | Add 2s silent clip |
| L010 | 2s pause | 2 sec | L009 file ends | 3:31 | Add 2s silent clip |
| L022 | 2s pause | 2 sec | L021 file ends | 7:50 | Add 2s silent clip |
| L026 | 2s pause | 2 sec | L025 file ends | 9:02 | Add 2s silent clip |
| L030 | 2s pause | 2 sec | L029 file ends | 10:18 | Add 2s silent clip |
| **L031** | **40s MA BEAT** | **40 sec** | **L030 ends** | **10:20** | **See Section 3 below** |
| L035 | 2s pause | 2 sec | L034 file ends | 11:58 | Add 2s silent clip + video fade |

---

## Standard 2-Second Pauses (L004, L010, L022, L026, L030)

Each of these is a 2-second silent gap between narration lines. In the editor:

1. Place the preceding narration file on the audio track.
2. Leave a 2-second gap before the next narration file begins.
3. Do not fill this gap with music swell, sound effects, or any audio.
4. The ambient music track (if present) continues underneath — only narration is absent.
5. These pauses are intentional breathing moments. Do not shorten them.

**Note:** In some editors, it is easier to place all narration files first with correct gaps, then verify each pause duration with a timecode ruler.

---

## The Ma Beat — L031 (40 Seconds of Silence)

This is the most important silence in the entire video.

### What the Ma beat is

**Scene:** S022 — Wide static shot of Hashima ruins (IMG018)
**Timeline position:** 10:20 to 11:00 (40 seconds)
**Rule (FIX-H3):** Absolutely no narration. Music and ocean waves only.

The Ma beat (間) is a Japanese aesthetic concept: silence as presence, not absence. This 40 seconds is not dead time. It is the most meaningful moment in the documentary — the point where the viewer sits alone with everything they have just heard.

### How to create it in the editor

1. After L029 (ends ~10:16) and L030 pause (ends ~10:20), the narration audio track goes completely silent.
2. In the video timeline, S022 image (IMG018 — wide static ruins) holds from 10:20 to 11:00.
3. On the audio track: **no narration clip**. Only the ambient music and/or ocean wave sound layer.
4. The 40-second silence runs from 10:20 to 11:00.
5. L032 (OUTRO) begins at approximately 11:01 (1 second after S022 ends).

### Audio layers during Ma beat

| Layer | During Ma beat |
|-------|---------------|
| Narration | SILENT — zero output |
| Music | Continues (fade down slightly if needed, but do not cut) |
| Ocean waves / ambient | Should be audible — this is the only sound the viewer hears |
| Sound effects | None |

### Common mistakes to avoid

- Do not trim the Ma beat to "save time" — it is exactly 40 seconds by design (FIX-H3).
- Do not fill it with a music swell or crescendo — the silence is the point.
- Do not add narration. Not even a whisper.
- Do not generate a 40-second "silence.mp3" from Vbee — there is nothing to generate.

---

## Natural Pauses Within Narration Files

Within each exported Vbee file, there will be natural micro-pauses at punctuation (。、——). These are part of the narration flow. They are **not** the L004/L010/L022/L026/L030 pause events listed above.

The pause events in this document are **inter-line** gaps — silence between two separate audio clips.

---

## Recommended Pause Workflow

1. Export all 27 narration segments from Vbee as separate MP3 files.
2. Import all 27 files into the editing timeline.
3. Place them at the intended start times from `data/timing_plan.json`.
4. Insert 2-second silent gaps at L004, L010, L022, L026, L030 positions.
5. Insert 40-second silence at L031 position (10:20-11:00) — narration track empty.
6. Insert 2-second final gap at L035 position (11:58-12:00) with video fade.
7. Verify each gap with timecode: use the line_timecodes array in timing_plan.json as reference.

---

## Special Placement Notes

**L008 start at 2:37** — This narration file starts 8 seconds before S008 begins (S007 image still showing). Place L008 audio at 2:37 in the timeline even though the visual is still S007. The scene cut happens at 2:45 during the narration. This is intentional.

**L028 start at 9:35** — This narration file starts 5 seconds before S021 begins (S020 image still showing). Place L028 audio at 9:35. This ensures the Ma beat (L031) begins at exactly 10:20. This is the critical timing adjustment from TF-002.

---

*See also: data/timing_plan.json → line_timecodes for all intended start/end times.*
*See also: voice/timed_readthrough_plan.md → Section 5 for pause placement map.*
