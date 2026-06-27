# Timeline Assembly Plan — hashima-island-mystery-ja
**Stage 38 | 2026-06-28**

---

## Summary

| Metric | Value |
|--------|-------|
| Total video duration | 12:00 (720s) |
| Total narration audio | 345.12s (5:45) |
| Pause events (editor silence) | 12s |
| Ma beat (inviolable) | 40s |
| Visual silence (non-Ma) | 322.88s |
| Scene count | 25 (FIXED — do not modify) |
| L008 placement | 2:37 (CRITICAL ANCHOR) |
| L028 placement | 9:35 (CRITICAL ANCHOR) |
| Ma beat | 10:20–11:00 (40s INVIOLABLE) |
| Image gaps | 2 (S010, S019 — no image assigned) |
| Assembly readiness | CONDITIONAL PASS |

**Blocked on:** S010 and S019 require image assignment before NLE assembly. All other assets are confirmed.

---

## Audio Placement Notes

All timecodes use actual Vbee export durations from `audio/vbee_raw/vbee_full_export_qa.json`.
Do NOT use timing_plan.json targets — all 28 segments were exported at `speed_rate=1`.

**Critical anchors (FIXED — do not adjust):**
- L008 must begin at `2:37` (sec=157) — spans S007/S008 visual cut
- L028 must begin at `9:35` (sec=575) — spans S020/S021 visual cut

---

## Color Key

| Symbol | Meaning |
|--------|---------|
| ⚠ | Risk flag |
| 🔴 | Critical / inviolable |
| 🟡 | Human review required |
| 🔵 | Post-processing required |
| 📍 | Critical audio anchor |

---

## HOOK — 0:00–1:00

### S001 | 0:00–0:10 | IMG001
- **Image:** `assets/ai_images/generated/batch_3/IMG001_S001_island_establishing_predawn.png`
- **Motion:** slow_pan_right
- **Post-process:** minimal — cold blue-black, already dark_documentary
- **Audio:**
  - L001 `hashima_L001_hook_01.mp3` → 0:00.00–0:04.42 (4.42s)
  - Visual silence: 0:04.42–0:10 (5.58s)
- **Music/Ambience:** Music bed very soft fade-in. Ocean waves from frame 0.
- **Transition in:** fade_from_black
- **Transition out:** cut
- 🟡 Human listen — L001 is HOOK opener, confirm delivery of かつて

---

### S002 | 0:10–0:25 | IMG002
- **Image:** `assets/ai_images/generated/batch_1/IMG002_S002_interior_ruin.png`
- **Motion:** ken_burns_zoom_in
- 🔵 **Post-process REQUIRED:** desaturate 60–70%, darken -0.5 to -1 stop, film grain. Frame zoom toward staircase; away from right-side exterior opening.
- **Audio:**
  - L002 `hashima_L002_hook_02.mp3` → 0:10.00–0:18.11 (8.11s)
  - Visual silence: 0:18.11–0:25 (6.89s)
- **Music/Ambience:** Wind through corridor.
- **Transition:** cut / cut

---

### S003 | 0:25–0:40 | IMG003
- **Image:** `assets/ai_images/generated/batch_1/IMG003_S003_wooden_door_closeup.png`
- **Motion:** static
- **Post-process:** minimal
- **Audio:**
  - L003 `hashima_L003_hook_03.mp3` → 0:25.00–0:27.66 (2.66s)
  - Visual silence: 0:27.66–0:40 (12.34s)
- **Music:** Very gentle swell after L003 ends — hold the dramatic silence.
- **Transition:** cut / cut
- ⚠ **RF-001 MEDIUM:** L003 is TOO_SHORT (2.66s vs 6s target). 12.34s of door texture silence. Dramatically powerful if delivery is complete.
- 🟡 Human listen — confirm そして、ある日——すべてが消えました。 is complete (not truncated)

---

### S004 | 0:40–1:00 | MG001 (Title Card)
- **Motion graphic:** Title card — 端島 / 軍艦島 fade-in on black
- **Audio:** L004 is a 2s editor pause (0:40–0:42). No Vbee file.
- **Silence:** 20s (full scene)
- **Music:** Very subtle rise under title card.
- **Transition:** cut / cut

---

## ACT I — 1:00–3:00

### S005 | 1:00–1:40 | IMG004
- **Image:** `assets/ai_images/generated/batch_1/IMG004_S005_meiji_industrial.png`
- **Motion:** slow_pan_left
- 🔵 **Post-process REQUIRED:** Add caption overlay `「illustrative archival simulation / 参考映像」` — image is convincingly realistic and must not be presented as an actual historical photograph.
- **Audio:**
  - L005 `hashima_L005_act1_01.mp3` → 1:01–1:17.44 (16.44s)
  - Visual silence: 1:17.44–1:40 (22.56s)
- **Music:** Slightly more informational — industrial-era tone.
- **Ambience:** Steam, distant machinery.
- **Transition:** cut / cut
- ⚠ **RF-002 LOW:** 22.56s visual silence on Meiji industrial image. Ensure slow_pan covers the full 40s.

---

### S006 | 1:40–2:10 | MG002 (Animated Map)
- **Motion graphic:** MG002 — Nagasaki Port → Hashima, distance overlay 約15〜18km
- **Audio:**
  - L006 `hashima_L006_act1_02.mp3` → 1:40–1:55.10 (15.10s)
  - Map animation continues: 1:55.10–2:10 (14.90s)
- **Music:** Slightly brighter — geographic reveal.
- **Transition:** cut / cut

---

### S007 | 2:10–2:45 | IMG006 ★ REAL PHOTO
- **Image:** `assets/real_images/downloaded/S007_IMG006_Battle-Ship_Island_Nagasaki_Japan.jpg`
- **License:** CC BY 2.0 — kntrty / Wikimedia Commons
- **Attribution required in YouTube description**
- **Motion:** slow_zoom_out
- **Post-process:** Grade to dark_documentary — cool tones. Do not remove the ocean horizon.
- **Audio:**
  - L007 `hashima_L007_act1_03.mp3` → 2:11–2:23.77 (12.77s)
  - Visual silence: 2:23.77–2:37 (13.23s)
  - 📍 **L008 begins at EXACTLY 2:37** — audio clips mid-S007 and continues across cut
- **Music:** Swell as island is revealed — wide, not dramatic.
- **Ambience:** Ocean wind, waves — grow as island appears.
- **Transition in:** cut | **Transition out:** cut (L008 bridges)
- 📍 **RF-003 INFO — CRITICAL AUDIO ANCHOR:** L008 must begin at sec=157 (2:37) in NLE. Mark clip exactly.
- 🟡 Human listen L008 — critical placement line

---

### S008 | 2:45–3:00 | IMG007
- **Image:** `assets/ai_images/generated/batch_3/IMG007_S008_building30_exterior.png`
- **Motion:** ken_burns_zoom_in
- **Post-process:** Standard dark_documentary
- **Audio:**
  - L008 continues: 2:45–2:59.03 (L008 started at 2:37, ends at 2:59.03)
  - Silence: 2:59.03–3:00 (0.97s)
- **Transition in:** cut (L008 audio bridges this cut) | **Transition out:** cut

---

## ACT II — 3:00–6:00

### S009 | 3:00–3:40 | IMG008
- **Image:** `assets/ai_images/generated/batch_2b/IMG008_S009_school_interior.png`
- **Motion:** slow_pan_right
- 🔵 **Post-process REQUIRED:** Slight desaturation from warm sepia — align to dark_documentary. Preserve light shafts.
- **Audio:**
  - Lead silence: 3:00–3:01 (1s)
  - L009 `hashima_L009_act1_05.mp3` → 3:01–3:30.62 (29.62s)
  - L010 pause (2s): 3:31–3:33
  - L011 `hashima_L011_act2_01.mp3` → starts 3:34, bleeds into S010
- **Music:** Heavier, more contemplative — ACT II tone shift.
- **Ambience:** Classroom echoes, wind through broken windows.
- **Transition:** cut (L011 bridges) / cut

---

### S010 | 3:40–4:10 | ⚠ IMAGE PENDING
- ⚠ **RF-004 HIGH — IMAGE NOT ASSIGNED:** `image_id_ref=null` in scene.json. PROMPT_009 (concrete crack, grass, haikyo) exists but no image generated.
- **Fallback options:** IMG003 (door texture crop) or IMG010 (mine rock macro) as placeholder.
- **Motion:** slow_zoom_in
- **Audio:**
  - L011 continues: 3:40–3:51.16 (from S009 start at 3:34)
  - Gap: 3:51.16–3:53 (1.84s)
  - L012 `hashima_L012_act2_02.mp3` → 3:53–4:10+ (bleeds into S011a)
- **Transition:** cut (L011 bridges) / cut (L012 bridges)

---

### S011a | 4:10–4:40 | IMG009 🔴 HUMAN PRODUCER REVIEW
- **Image:** `assets/ai_images/generated/mine_gate/IMG009_S011a_mine_tunnel_approved.png`
- **Motion:** slow_zoom_in
- **Post-process:** Standard dark_documentary — do NOT add warmth. Cold, austere.
- **Audio:**
  - L012 continues: 4:10–4:15.85
  - Gap: 4:15.85–4:17 (1.15s)
  - L013 `hashima_L013_act2_03.mp3` → 4:17–4:23.84 (6.84s)
  - Sensitive silence: 4:23.84–4:29 (5.16s) — intentional pause after labor reference
  - L014 `hashima_L014_act2_04.mp3` → 4:29–4:40+ (bleeds into S011b)
- **Music:** Very quiet — no dramatic cues during sensitive content.
- **Ambience:** Mine tunnel — deep earth, dripping water.
- **Transition:** cut (L012 bridges) / cut (L014 bridges)
- 🔴 **RF-005 HIGH:** IMG009 requires human producer final review before importing into NLE. FIX-M1 cleared safety but producer signoff outstanding.
- 🟡 **RF-006 HIGH:** L013 and L014 are SENSITIVE CONTENT. Human listen — verify factual, respectful tone. No emotional amplification.

---

### S011b | 4:40–5:00 | IMG010
- **Image:** `assets/ai_images/generated/batch_1/IMG010_S011b_mine_rock_texture.png`
- **Motion:** slow_zoom_in
- **Post-process:** Do not brighten — maintain dark, textural quality.
- **Audio:**
  - L014 continues: 4:40–4:43.35
  - Gap: 4:43.35–4:46 (2.65s)
  - L015 `hashima_L015_act2_05.mp3` → 4:46–5:00+ (bleeds into S012)
- **Transition:** cut (L014 bridges) / cut (L015 bridges)
- ⚠ **RF-007 MEDIUM:** L015 is SENSITIVE CONTENT (consequence framing). Part of COMP-007 review.

---

### S012 | 5:00–5:30 | MG003 (Data Graphic)
- **Motion graphic:** Disputed labor statistics — dual-source display. MUST NOT assert a specific death count.
- **Audio:**
  - L015 continues: 5:00–5:02.46
  - Gap: 5:02.46–5:05 (2.54s)
  - L016 `hashima_L016_act2_06.mp3` → 5:05–5:18.03 (13.03s)
  - MG holds: 5:18.03–5:30 (11.97s)
- **MG design note:** Present numbers as "Source A / Source B" — never as settled fact.
- **Music:** Restrained — no dramatic swells during data presentation.
- **Transition:** cut (L015 bridges) / cut
- ⚠ **RF-008 HIGH:** L016 is SENSITIVE (disputed historical framing). MG must present data neutrally.

---

### S013 | 5:30–6:00 | IMG011
- **Image:** `assets/ai_images/generated/batch_1/IMG011_S013_heritage_light_ruins.png`
- **Motion:** slow_pan_left
- 🔵 **Post-process REQUIRED:** Frame pan to START toward interior light shafts. Avoid lingering on war-zone-like background ruins.
- **Audio:**
  - L017 `hashima_L017_act2_07.mp3` → 5:31–5:48.16 (17.16s)
  - Visual silence: 5:48.16–6:00 (11.84s)
- **Music:** Builds very slightly — transitioning toward ACT III.
- **Transition:** cut / cut

---

## ACT III — 6:00–9:00

### S014 | 6:00–6:30 | MG004 (Date Text)
- **Motion graphic:** Text overlay — `1974年1月15日` — fade in on dark background
- **Audio:**
  - Lead: 6:00–6:02 (2s pre-text silence)
  - L018 `hashima_L018_act3_01.mp3` → 6:02–6:07.59 (5.59s)
  - Date holds: 6:07.59–6:30 (22.41s) — contemplate in silence
- **Music:** Drops to near-silence after L018 — let the date breathe.
- **Ambience:** Near-silence. Very faint ocean.
- **Transition:** cut / cut

---

### S015 | 6:30–7:00 | IMG012
- **Image:** `assets/ai_images/generated/batch_1/IMG012_S015_abandoned_dock.png`
- **Motion:** slow_zoom_out
- **Post-process:** Minimal — already naturalistic desaturated.
- **Audio:**
  - L019 `hashima_L019_act3_02.mp3` → 6:31–6:41.39 (10.39s)
  - Visual silence: 6:41.39–7:00 (18.61s)
- **Music:** Quiet — pier desertion is visual.
- **Ambience:** Water, distant seagulls, rope creak.
- **Transition:** cut / cut

---

### S016 | 7:00–7:30 | IMG013
- **Image:** `assets/ai_images/generated/batch_2a/IMG013_S016_personal_items_v2.png`
- **Motion:** slow_zoom_in
- **Post-process:** Confirm no identifiable faces in photograph prop.
- **Audio:**
  - L020 `hashima_L020_act3_03.mp3` → 7:02–7:06.46 (4.46s)
  - Visual silence: 7:06.46–7:30 (23.54s)
- **Music:** Very quiet. 23.54s of silence on abandoned items IS the emotional beat. Do not fill.
- **Ambience:** Single distant wave.
- **Transition:** cut / cut
- ⚠ **RF-009 LOW:** L020 TOO_SHORT (4.46s vs 8s). Content likely complete at speed=1. Director confirm.

---

### S017 | 7:30–8:00 | IMG014
- **Image:** `assets/ai_images/generated/batch_2b/IMG014_S017_light_beams_interior_v2.png`
- **Motion:** static
- **Post-process:** Do not add camera movement. Light shaft is the motion.
- **Audio:**
  - L021 `hashima_L021_act3_04.mp3` → 7:32–7:42.08 (10.08s)
  - L022 pause (2s): 7:44–7:46
  - Visual silence: 7:46–8:00 (14s)
- **Music:** Quiet, contemplative — breathing space before ACT IV.
- **Ambience:** Dust particles, faint structural sound.
- **Transition:** cut / cut

---

### S018 | 8:00–8:30 | IMG015
- **Image:** `assets/ai_images/generated/batch_2b/IMG015_S018_storm_ruins.png`
- **Motion:** slow_pan_right
- **Post-process:** Standard — cool blue-grey already present.
- **Audio:**
  - L023 `hashima_L023_act3_05.mp3` → 8:01–8:13.43 (12.43s)
  - Visual silence: 8:13.43–8:30 (16.57s)
- **Music:** Slight build toward ACT IV.
- **Ambience:** Ocean waves, intensifying wind.
- **Transition:** cut / cut

---

### S019 | 8:30–9:00 | ⚠ IMAGE PENDING
- ⚠ **RF-010 HIGH — IMAGE NOT ASSIGNED:** `image_id_ref=null` in scene.json. Macro concrete texture visual (PROMPT_016 shared with S020) but S019 is a different scene.
- **Fallback:** IMG010 (mine rock macro) is visually compatible.
- **Motion:** static
- **Audio:**
  - L024 `hashima_L024_act3_06.mp3` → 8:31–8:42.30 (11.30s)
  - Gap: 8:42.30–8:48 (5.70s)
  - L025 `hashima_L025_act3_07.mp3` → 8:48–8:55.82 (7.82s)
  - L026 pause (2s): 8:58–9:00 (straddles S019/S020 boundary)
- **Music:** Very slight fade — approaching ACT IV.
- **Transition:** cut / cut

---

## ACT IV — 9:00–11:00

### S020 | 9:00–9:40 | IMG016
- **Image:** `assets/ai_images/generated/batch_3/IMG016_S020_island_dusk_wide_v2.png`
- **Motion:** very_slow_pan_right
- 🔵 **Post-process REQUIRED:** Desaturate sky 15–20%. Preserve warm dusk tone. This is the most emotionally important image before the Ma beat.
- **Audio:**
  - L026 pause: 9:00–9:02 (starts within S020 boundary)
  - L027 `hashima_L027_act4_01.mp3` → 9:05–9:14.86 (9.86s)
  - Visual silence: 9:14.86–9:35 (20.14s) — wide island in dusk, no narration
  - 📍 **L028 begins at EXACTLY 9:35** — clips into S020, continues across cut into S021
- **Music:** Broad, contemplative swell. Not dramatic — wide.
- **Ambience:** Ocean waves more prominent. Wind. Acoustic approach to Ma beat world.
- **Transition in:** cut | **Transition out:** cut (L028 bridges)
- 📍 **RF-011 INFO — CRITICAL AUDIO ANCHOR:** L028 must begin at sec=575 (9:35). Do not adjust.

---

### S021 | 9:40–10:20 | IMG017
- **Image:** `assets/ai_images/generated/batch_2b/IMG017_S021_heritage_plaque_ruin.png`
- **Motion:** slow_zoom_in
- **Post-process:** Standard — maintain desaturated warm-cool contrast.
- **Audio:**
  - L028 `hashima_L028_act4_02.mp3` continues from S020: 9:40–9:55.42 (started at 9:35)
  - Gap: 9:55.42–9:56.42 (1s)
  - L029 `hashima_L029_act4_03.mp3` → 9:56.42–10:10.15 (13.73s)
  - L030 pause (2s): 10:10.15–10:12.15
  - Visual silence: 10:12.15–10:20 (7.85s) — heritage plaque zoom in, silence before Ma beat
- **Music:** Gradual fade to silence. Must reach ZERO by 10:20. Ocean waves take over.
- **Transition in:** cut (L028 bridges) | **Transition out:** cut — Ma beat begins EXACTLY at 10:20
- ⚠ **RF-012 INFO:** 7.85s visual silence on heritage plaque is pre-Ma-beat window. Music crossfade to silence must complete here.
- 🟡 Human listen L028 — critical pre-Ma-beat line

---

### 🔴 S022 | 10:20–11:00 | IMG018 — MA BEAT (40s INVIOLABLE)

**⬛ ABSOLUTE SILENCE — NO NARRATION TRACK — NO MUSIC SWELL ⬛**

- **Image:** `assets/ai_images/generated/batch_1/IMG018_S022_hashima_panorama.png`
- **Motion:** static
- **Post-process:** Minimal. Dissolve in at 10:20, dissolve out at 11:00.
- **Audio:** NARRATION TRACK MUST BE EMPTY from sec=620 to sec=660.
- **Ambience ONLY:** Ocean waves + wind. Authentic natural sound. No synthetic effects.
- **Music:** Zero or held at barely-audible. No swells, no dramatic cues.
- **Duration:** Exactly 40 seconds. FIX-H3. Contract requirement.
- **Transition in:** dissolve (soft entry) | **Transition out:** dissolve into OUTRO
- 🔴 **RF-013 CRITICAL — MA BEAT INVIOLABLE:** NLE inspector must confirm narration track empty 620s–660s before export.

---

## OUTRO — 11:00–12:00

### S023 | 11:00–11:30 | IMG019
- **Image:** `assets/ai_images/generated/batch_2b/IMG019_S023_tourist_ferry_approach.png`
- **Motion:** slow_zoom_in
- **Post-process:** Subtle warm grade — contemporary context contrast with ruins.
- **Audio:**
  - Lead: 11:00–11:01 (1s post-Ma-beat breath)
  - L032 `hashima_L032_outro_01.mp3` → 11:01–11:09.18 (8.18s)
  - Visual silence: 11:09.18–11:30 (20.82s)
- **Music:** Resumes gently — warm, contemplative OUTRO tone.
- **Ambience:** Ferry engine (distant), sea breeze.
- **Transition in:** dissolve (from S022 Ma beat) | **Transition out:** cut

---

### S024 | 11:30–12:00 | IMG020 ★ REAL PHOTO (Japan Govt 1974)
- **Image:** `assets/real_images/processed/S024_IMG020_Cku-74-20_c45_6_hashima_16x9.jpg`
- **License:** Japanese Government 1974 aerial — attribution-only
- **Attribution required verbatim in YouTube description:**
  > Aerial photograph of Hashima Island (1974) / Source: National Land Image Information (Color Aerial Photographs) / Ministry of Land, Infrastructure, Transport and Tourism of Japan
- **Motion:** slow_pan_right
- **Post-process:** Grade to dark_documentary — 1974 aerial may be warm/faded, align to cooler documentary tone.
- **Audio:**
  - L033 `hashima_L033_outro_02.mp3` → 11:32–11:39.39 (7.39s)
  - Gap: 11:39.39–11:47 (7.61s)
  - L034 `hashima_L034_outro_03.mp3` → 11:47–11:51.39 (4.39s)
  - Visual silence: 11:51.39–11:58 (6.61s)
  - L035 pause: 11:58–12:00 (2s) + fade to black
- **Fade to black:** begins ~11:54, completes at 12:00
- **Music:** Final resolve and fade to silence with image.
- **Ambience:** Ocean waves fade with image.
- **Transition in:** cut | **Transition out:** fade_to_black (complete at 12:00)
- ⚠ **RF-014 LOW:** L034 TOO_SHORT (4.39s vs 9s). Final narration. Confirm content is complete before deciding re-export.

---

## Risk Register

| ID | Scene | Severity | Type | Action Required |
|----|-------|----------|------|-----------------|
| RF-001 | S003 | MEDIUM | TOO_SHORT (L003, 2.66s) | Human listen — confirm content not truncated |
| RF-002 | S005 | LOW | Extended silence (22.56s) | Verify slow_pan covers 40s; add music bed |
| RF-003 | S007 | INFO | Critical audio anchor L008@2:37 | Mark clip at sec=157 in NLE |
| RF-004 | S010 | **HIGH** | Image not assigned | Assign fallback or generate new before assembly |
| RF-005 | S011a | **HIGH** | IMG009 producer review required | Human producer review before NLE import |
| RF-006 | S011a | **HIGH** | L013/L014 sensitive content | Human listen — tone review |
| RF-007 | S011b | MEDIUM | L015 sensitive content | COMP-007 review |
| RF-008 | S012 | **HIGH** | L016 + MG data neutrality | MG must present data as dual-source, not settled |
| RF-009 | S016 | LOW | TOO_SHORT (L020, 4.46s) | Director confirm content complete |
| RF-010 | S019 | **HIGH** | Image not assigned | Assign fallback or generate new before assembly |
| RF-011 | S020 | INFO | Critical audio anchor L028@9:35 | Mark clip at sec=575 in NLE |
| RF-012 | S021 | INFO | Pre-Ma-beat music fade window | Music crossfade complete by sec=620 |
| RF-013 | S022 | **CRITICAL** | Ma beat inviolable | NLE inspector — narration track empty 620–660s |
| RF-014 | S024 | LOW | TOO_SHORT (L034, 4.39s) | Director confirm; fade covers remainder |

---

## Pre-Assembly Checklist

Before importing into NLE:

- [ ] S010 image assigned (from fallback or new generation)
- [ ] S019 image assigned (from fallback or new generation)
- [ ] IMG009 human producer review completed (S011a)
- [ ] Post-processing applied: IMG002, IMG004, IMG008, IMG011, IMG016
- [ ] IMG004 "参考映像" caption overlay ready
- [ ] L008 audio clip marked at sec=157 (2:37)
- [ ] L028 audio clip marked at sec=575 (9:35)
- [ ] Music bed selected and licensed
- [ ] Natural ocean/wind ambience track sourced

Before export:
- [ ] NLE inspector: narration track empty 10:20–11:00 (sec=620–660)
- [ ] Human listen: L001, L003, L008, L013, L014, L028
- [ ] Sensitive content tone review: L013–L016 (COMP-007)
- [ ] Attribution text prepared: IMG006 (CC BY 2.0), IMG020 (Japan Govt 1974)

---

*Timeline Assembly Plan — Stage 38 — hashima-island-mystery-ja — 2026-06-28*
*Machine-readable version: `data/timeline_assembly_plan.json`*
