# Example Execution — Hashima Island Mystery

This document shows the complete execution of Director AI v1 for a real project. It demonstrates every stage: what input is provided, what Claude Code executes, what output files are created, and what the final project looks like.

**Project:**
```
TOPIC: The Mystery of Hashima Island
LANGUAGE: ja
DURATION_MINUTES: 12
STYLE: dark_documentary
```

---

## Activation

Paste `agents/director_ai_v1.md` into Claude Code. Then provide the four inputs.

---

## System Boot

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DIRECTOR AI v1 — BOOTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Loading system files...
[BOOT] Core rules:      4/4 ✓
[BOOT] Architecture:    2/2 ✓
[BOOT] Engines:         6/6 ✓
[BOOT] Configuration:   4/4 ✓
[BOOT] Template:        1/1 ✓ (templates/japan_template.md)
[BOOT] Prompt files:   10/10 ✓
[BOOT] Runtime:         3/3 ✓
[INFO ERR_INFO_002] Niche 'japanese_mystery' derived from style 'dark_documentary' + topic context.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PRODUCTION JOB CONFIRMED
Topic:          The Mystery of Hashima Island
Language:       ja
Duration:       12 min
Style:          dark_documentary
Niche:          japanese_mystery
Target words:   1,201 (12 × 130 × 0.77 Japanese multiplier)
Project slug:   20260627_mystery-of-hashima-island
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Starting pipeline. Stand by.
```

---

## Stage 0 — Project Setup

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STAGE 0 — PROJECT SETUP
Project: 20260627_mystery-of-hashima-island
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Stage 0] Creating: projects/20260627_mystery-of-hashima-island/
[Stage 0] Creating 8 subdirectories...
[Stage 0] Writing input/input.json...
[Stage 0] Writing input/project.yaml...
[Stage 0] Writing export/export_manifest.json (17 assets)...
[Stage 0] Initializing logs/director_run_log.md...
[Stage 0] Running checklist (7 items)...

[STAGE 0 COMPLETE]
Output:     input/input.json, input/project.yaml, export/export_manifest.json, logs/director_run_log.md
Checklist:  7/7 passed
Status:     PASS
──────────────────────────────────────────────
```

**`input/input.json` created:**
```json
{
  "project_id": "20260627_mystery-of-hashima-island",
  "topic": "The Mystery of Hashima Island",
  "language": "ja",
  "video_length_minutes": 12,
  "style": "dark_documentary",
  "niche": "japanese_mystery",
  "target_word_count": 1201,
  "channel_name": "Mystery Archive JP",
  "notes": "...",
  "created_at": "2026-06-27T10:00:00Z",
  "schema_version": "1.0"
}
```

---

## Stage 1 — Research

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STAGE 1 — RESEARCH
Project: 20260627_mystery-of-hashima-island
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Stage 1] Reading prompt: prompts/01_research.md
[Stage 1] Loading context: configs/language_profiles.md, configs/style_profiles.md,
          templates/japan_template.md, input/input.json
[Stage 1] Template addendum loaded: japan_template.md → Stage Addendum: stage_01
[Stage 1] Resolving 11 placeholders...
[Stage 1] Model: claude-opus-4-8 (primary)
[Stage 1] Generating research brief...
[Stage 1] Writing research/research.md...
[Stage 1] Running checklist (10 items)...

[STAGE 1 COMPLETE]
Output:     research/research.md
Checklist:  10/10 passed
Warnings:   0
Status:     PASS
──────────────────────────────────────────────
```

**`research/research.md` (summary section):**

```markdown
# Research: The Mystery of Hashima Island (端島 / 軍艦島)

## Summary
端島（軍艦島）は、長崎県沖に浮かぶ無人の炭坑島である。
1890年から三菱が運営し、1959年には5,259人が居住していた（当時世界最高の人口密度）。
1974年4月20日に全住民が島を去り、以来50年間、廃墟として存在し続けている。

## Key Facts
1. Location: 長崎港から南西約18.5km、面積0.063km²
2. Mitsubishi operated the island coal mine from 1890 to 1974 (Meiji era through Showa 49)
3. Peak population: 5,259 people in 1959 — approximately 83,500 people per km²
4. Evacuation date: April 20, 1974 (昭和49年4月20日) — coal demand had collapsed
5. During WWII: Korean and Chinese laborers were conscripted to work the mines
6. UNESCO World Heritage Site: July 5, 2015 — part of "Sites of Japan's Meiji Industrial Revolution"
7. The UNESCO inscription was contested by South Korea over the forced labor history
8. Famous appearance: Used as the villain Raoul Silva's lair in James Bond film Skyfall (2012)
9. Reopened to limited tourism: 2009 — guided tours to a small section of the island
10. Concrete apartment blocks built from 1916 onward — among Japan's oldest reinforced concrete buildings

## Sources
1. UNESCO World Heritage Committee, "Sites of Japan's Meiji Industrial Revolution" (2015)
2. Nagasaki City official tourism records and historical documents
3. Mitsubishi Materials Corporation historical archives
4. Pallister-Wilkins, P. "Gunkanjima" — academic analysis of the island's history (2009)
5. Asahi Shimbun reporting on the UNESCO controversy, South Korea protests (2015)
6. Japan Times, "Abandoned island Hashima opens to tourists" (2009)
```

---

## Stage 2 — Source Verification

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STAGE 2 — SOURCE VERIFICATION
Project: 20260627_mystery-of-hashima-island
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Stage 2] Reading prompt: prompts/02_source_verifier.md
[Stage 2] Loading context: research/research.md
[Stage 2] Auditing 10 facts, 6 sources...
[Stage 2] Writing research/source_report.md...
[Stage 2] Writing research/research_verified.md...
[Stage 2] Running checklist (8 items)...
[Stage 2] Source verdict: PASS

[STAGE 2 COMPLETE]
Output:     research/source_report.md, research/research_verified.md
Checklist:  8/8 passed
Warnings:   0
Status:     PASS
──────────────────────────────────────────────
```

**`research/source_report.md` (excerpt):**

```markdown
## Overall Status: PASS

| Fact | Rating | Reason |
|---|---|---|
| Population 5,259 in 1959 | PASS | UNESCO documentation + Nagasaki City records |
| Evacuation April 20, 1974 | PASS | Multiple Japanese historical sources |
| UNESCO inscription 2015 | PASS | Official UNESCO record |
| Forced Korean/Chinese labor WWII | PASS | Multiple verified sources; acknowledged in UNESCO controversy |
| Skyfall appearance 2012 | PASS | Verifiable from film production records |
| "World's most densely populated" claim | FLAG | Frequently cited but the exact measurement methodology varies |
```

---

## Stage 3 — Story Outline

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STAGE 3 — STORY OUTLINE
Project: 20260627_mystery-of-hashima-island
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Stage 3] Reading prompt: prompts/03_story_outline.md
[Stage 3] Loading context: configs/style_profiles.md, templates/japan_template.md,
          research/research_verified.md
[Stage 3] Template addendum: japan_template.md Stage Addendum stage_03 — required beats:
          Cultural Context → Legend vs Reality → Japanese Silence → Ma Beat
[Stage 3] Writing script/story_outline.md...
[Stage 3] Running checklist (10 items)...

[STAGE 3 COMPLETE]
Output:     script/story_outline.md
Checklist:  10/10 passed
Warnings:   0
Status:     PASS
──────────────────────────────────────────────
```

**`script/story_outline.md` (structure):**

```markdown
# Story Outline — The Mystery of Hashima Island

## Hook
Opening image: Aerial drone shot of Hashima — a concrete island rising from the sea like
a battleship. The question: what happened to the city inside?

## Scene Breakdown

| # | Scene | Purpose | Emotion | Target words |
|---|---|---|---|---|
| 1 | The Island Appears | Setup + Cultural Context | Curiosity | 140 |
| 2 | When the City Breathed | Rising Tension | Intrigue | 220 |
| 3 | The Darkness Below | Historical revelation (forced labor) | Unease | 200 |
| 4 | The Day Everyone Left | Climax moment | Dread |  180 |
| 5 | Ma Beat — The Silence | Japanese Silence beat | Stillness | 60 |
| 6 | What the Ruins Remember | Legend vs Reality | Sadness | 180 |
| 7 | The Open Question | Conclusion | Unresolved | 120 |

Hook: 60 words
**Total: 1,160 words (target: 1,201 — within 3.4%)**

## Speculation Flags
- The exact number of forced laborers is disputed in historical records
  → Label as [UNVERIFIED] in script
```

---

## Stage 4 — Script Writing

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STAGE 4 — SCRIPT WRITING
Project: 20260627_mystery-of-hashima-island
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Stage 4] Reading prompt: prompts/04_script_writer.md
[Stage 4] Model: claude-opus-4-8 (primary)
[Stage 4] Target: 1,201 words | Min: 1,081 | Max: 1,321
[Stage 4] Writing script/script.md...
[Stage 4] Running checklist (12 items)...

[STAGE 4 COMPLETE]
Output:     script/script.md (1,187 words)
Checklist:  12/12 passed
Warnings:   0
Status:     PASS
──────────────────────────────────────────────
```

**`script/script.md` (hook and first scene — excerpt):**

```markdown
**Word count: 1,187 / 1,201 target (−1.2%)**

---

## HOOK (0:00 - 0:28)
*[55 words]*

長崎の沖合、18キロ。
霧の中に浮かぶのは、島ではありません。
廃墟となった都市です。

かつてここに、五千人の人間が暮らしていました。
子どもたちが走り、工場が唸り、夜には窓に灯りが灯っていた。
そして1974年4月20日、最後の人間が島を離れ——
それ以来、誰も戻っていません。

これは端島の話です。

---

## Scene 1 — The Island Appears (0:28 - 3:20)
*[140 words]*

[SLOW]
端島。正式名称は端島。しかし世界はこの島を別の名で知っています——軍艦島。

長さ480メートル、幅160メートル。コンクリートの壁に囲まれたこの小島が、
なぜ「軍艦」と呼ばれるのかは、一度見れば理解できます。
[PAUSE:1s]

海の上に浮かぶその姿は、まるで戦艦のようです。
...
[NORMAL]
```

---

## Stage 5 — Story Bible

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STAGE 5 — STORY BIBLE
Project: 20260627_mystery-of-hashima-island
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Stage 5] Reading prompt: prompts/05_story_bible.md
[Stage 5] Model: claude-sonnet-4-6 (secondary)
[Stage 5] Writing script/story_bible.md...
[Stage 5] Running checklist (9 items)...

[STAGE 5 COMPLETE]
Output:     script/story_bible.md
Checklist:  9/9 passed
Warnings:   0
Status:     PASS
──────────────────────────────────────────────
```

**`script/story_bible.md` (pronunciation guide excerpt):**

```markdown
## Pronunciation Guide

| Name | Pronunciation | Notes |
|---|---|---|
| 端島 (Hashima) | HA-shi-ma | Stress first syllable |
| 軍艦島 (Gunkanjima) | GUN-kan-ji-ma | "Battleship Island" |
| 三菱 (Mitsubishi) | mi-TSU-bi-shi | Company that operated the mine |
| 昭和 (Showa) | SHO-wa | Imperial era 1926–1989 |
| 長崎 (Nagasaki) | na-GA-sa-ki | Prefecture in Kyushu |

## Canonical Name Index
端島 → always use 端島 or "Hashima Island" (never "Hashima" alone without context)
軍艦島 → use in second reference only, after 端島 is established
三菱 → "Mitsubishi" (English), "三菱" (Japanese script in subtitles)
```

---

## Stage 6 — Scene Splitting

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STAGE 6 — SCENE SPLITTING
Project: 20260627_mystery-of-hashima-island
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Stage 6] Model: claude-sonnet-4-6 (secondary)
[Stage 6] Writing visuals/storyboard.md...
[Stage 6] Running checklist (10 items)...

[STAGE 6 COMPLETE]
Output:     visuals/storyboard.md
Checklist:  10/10 passed
Status:     PASS
──────────────────────────────────────────────
```

**`visuals/storyboard.md` (excerpt — visual summary):**

```markdown
## Visual Summary

| Image type | Count |
|---|---|
| real | 14 |
| b-roll | 4 |
| map | 3 |
| text-overlay | 2 |
| ai-generated | 5 |
| screen-recording | 0 |
| screenshot | 0 |
| stock | 1 |
| **Total beats** | **29** |

## Beat 04 — The City at Peak Population (1:45 - 2:30)
**Image type:** real
**Description:** Aerial photograph of Hashima Island at peak population — all buildings visible,
  laundry lines between windows, children playing on the small outdoor spaces
**Music mood:** Melancholic, curious, slightly wistful
**On-screen text:** 1959年 — 人口密度、世界一
**Transition:** Slow fade
**Source priority:** Nagasaki City archives, Japanese news archives (Asahi Shimbun, Mainichi)
```

---

## Stage 7 — Image Planning

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STAGE 7 — IMAGE PLANNING
Project: 20260627_mystery-of-hashima-island
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Stage 7] Model: claude-sonnet-4-6 (secondary)
[Stage 7] Processing 24 real/stock/map beats...
[Stage 7] Writing visuals/image_plan.md...
[Stage 7] Running checklist (9 items)...

[STAGE 7 COMPLETE]
Output:     visuals/image_plan.md
Checklist:  9/9 passed
Warnings:   0
Status:     PASS
──────────────────────────────────────────────
```

**`visuals/image_plan.md` (Beat 04 example):**

```markdown
### Beat 04 — The City at Peak Population

**Beat from storyboard:** 04
**Image type needed:** real

**Strategy A (Primary)**
Search: Wikimedia Commons → "Hashima Island" → filter: photographs, 1950s–1960s
Terms: "端島 写真" OR "軍艦島 全盛期" OR "Hashima 1959"
License target: Public domain (pre-1975 Japanese photographs)
Note: Nagasaki City has released historical photographs under open license

**Strategy B (Backup)**
Search: Nagasaki Prefectural Library digital archive
URL pattern: nagasaki-archive.jp (do not fabricate — search for the archive)
Terms: "端島炭鉱" historical collection
License: Educational/editorial — confirm before use

**Strategy C (Emergency)**
Contact: Mitsubishi Materials Corporation press archives
Note: They have released some historical photos for media use; requires attribution

---

## AI Escalation List

The following beats cannot be legally sourced with real images:

| Beat | Reason | Concept for Stage 8 |
|---|---|---|
| 07 | No photographs of mining interior during forced labor period | Dark mining shaft, figure in shadows, period-appropriate tools, no faces |
| 12 | Specific emotional moment (last family leaving) — never photographed | A family silhouette at a concrete doorway, their backs to us, looking at the sea |
| 19 | Ma beat — abstract emptiness | Empty concrete corridor, single window, grey sky, moss on walls |
| 22 | Reconstruction of 1890 island before concrete | Older visual style, wooden structures on small rock outcropping |
| 27 | Contemporary night shot with specific mood not in available archives | The island at night from the sea, all windows dark, city light in background |
```

---

## Stage 8 — AI Image Prompts

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STAGE 8 — AI IMAGE PROMPTS
Project: 20260627_mystery-of-hashima-island
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Stage 8] Model: claude-sonnet-4-6 (secondary)
[Stage 8] Generating prompts for 5 AI beats...
[Stage 8] Writing visuals/ai_image_prompts.md...
[Stage 8] Running checklist (10 items)...

[STAGE 8 COMPLETE]
Output:     visuals/ai_image_prompts.md
Checklist:  10/10 passed
Status:     PASS
──────────────────────────────────────────────
```

**`visuals/ai_image_prompts.md` (Beat 12 example):**

```markdown
### Beat 12 — Last Family Leaving [DRAMATIZATION — NOT REAL]

**Prompt:**
A family silhouette standing in a concrete doorway, backs to the camera,
facing the grey ocean. The doorframe is weathered concrete with rust stains.
A woman holds a small child's hand. A man carries a single suitcase.
The ocean beyond is calm and overcast. No faces visible.
Mood: quiet devastation, finality. Lighting: overcast, flat grey.
Color palette: #3a3a3a concrete grey, #8b9ba8 slate blue, #c4b5a0 aged white.
Camera angle: low angle from behind, framing the family in the doorway arch.
Style: cinematic still, East Asian documentary aesthetic, desaturated.
Aspect ratio: 16:9. No text. No watermarks.

**Negative prompt:**
faces, color grading, bright colors, modern clothing, Japanese text overlay,
HDR, oversaturated, stock photo look, happy expression, modern architecture

**Alternative prompt (simplified):**
Silhouette of family in abandoned concrete doorway, facing grey sea, backs to camera,
suitcase, overcast light, documentary style, 16:9
```

---

## Stage 9 — Voice Direction

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STAGE 9 — VOICE DIRECTION
Project: 20260627_mystery-of-hashima-island
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Stage 9] Model: claude-opus-4-8 (primary)
[Stage 9] Language: ja — applying Japanese voice profile
[Stage 9] Japan template: opening_pace=very_slow, silence_budget=5×[PAUSE:2s]
[Stage 9] Writing voice/voice_script.txt...
[Stage 9] Writing voice/voice_direction.md...
[Stage 9] Writing voice/subtitles.srt (estimated timecodes at 300 mora/min)...
[Stage 9] Running checklist (18 items)...

[STAGE 9 COMPLETE]
Output:     voice/voice_script.txt, voice/voice_direction.md, voice/subtitles.srt
Checklist:  18/18 passed
Warnings:   0
Status:     PASS
──────────────────────────────────────────────
```

**`voice/voice_script.txt` (opening — pure plain text):**

```
[SLOW]
長崎の沖合、十八キロ。
[PAUSE:1.5s]
霧の中に浮かぶのは、島ではありません。
[PAUSE:1s]
廃墟となった都市です。
[PAUSE:2s]
[NORMAL]

かつてここに、五千人の人間が暮らしていました。
子どもたちが走り、工場が唸り、夜には窓に灯りが灯っていた。
[PAUSE:1s]
そして昭和四十九年四月二十日、最後の人間が島を離れ——
それ以来、誰も戻っていません。
[PAUSE:2s]

これは端島の話です。
[PAUSE:3s]
```

**`voice/subtitles.srt` (first segments):**

```
1
00:00:00,000 --> 00:00:03,500
長崎の沖合、十八キロ。

2
00:00:05,000 --> 00:00:08,800
霧の中に浮かぶのは、島ではありません。

3
00:00:09,800 --> 00:00:12,200
廃墟となった都市です。

4
00:00:14,200 --> 00:00:19,000
かつてここに、五千人の人間が暮らしていました。
```

---

## Stage 10 — YouTube SEO

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STAGE 10 — YOUTUBE SEO
Project: 20260627_mystery-of-hashima-island
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Stage 10] Model: claude-sonnet-4-6 (secondary)
[Stage 10] Language: ja — English Tags Addendum required
[Stage 10] Writing seo/seo.md...
[Stage 10] Writing seo/thumbnail_prompt.md...
[Stage 10] Running checklist (13 items)...

[STAGE 10 COMPLETE]
Output:     seo/seo.md, seo/thumbnail_prompt.md
Checklist:  13/13 passed
Warnings:   0
Status:     PASS
──────────────────────────────────────────────
```

**`seo/seo.md` (titles — excerpt):**

```markdown
## Title Options

**Option 1** (62 chars)
軍艦島の真実｜廃墟に眠る五千人の歴史と謎

**Option 2** (58 chars)
端島｜最も危険な炭坑島に何が起きたのか

**Option 3** (55 chars)
軍艦島の謎｜50年間誰も戻らない島の秘密

## English Tags Addendum
Hashima Island, Gunkanjima, abandoned island Japan, Nagasaki mystery,
battleship island, Japan UNESCO, ghost island documentary,
軍艦島 documentary, Hashima Island history, Japan war history,
forced labor Japan WWII, Skyfall filming location
```

**`seo/thumbnail_prompt.md`:**

```markdown
## Thumbnail Concept
The island seen from the sea at dusk — dark, monolithic concrete structure
against an orange-grey sky. Bold Japanese text overlay. Conveys: "This is a
place of weight and history, not typical tourism."

## Image Prompt
Aerial photograph style: Hashima Island viewed from sea level at dusk,
dramatic side angle showing the full concrete seawall profile,
orange and grey sky, dark water, no tourists visible,
cinematic wide lens, low angle, desaturated with warm amber horizon accent.
Style: documentary photography. 16:9.

## Text Overlay
Primary (large): 軍艦島
Secondary (small): 誰も知らない真実

## Color palette
#1a1a2e (deep navy), #c84b31 (deep crimson), #f0e6d3 (aged parchment)
```

---

## Stage 11 — Final QA

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STAGE 11 — FINAL QA
Project: 20260627_mystery-of-hashima-island
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Stage 11] Reading all 14 output files...
[Stage 11] Running 18 QA checks...

[Stage 11] CHECK 11.1: All 15 output files exist — PASS
[Stage 11] CHECK 11.2: source_report Overall Status ≠ FAIL — PASS
[Stage 11] CHECK 11.3: Script word count 1,187 / target 1,201 (−1.2%) — PASS
[Stage 11] CHECK 11.4: No markdown in voice_script.txt — PASS
[Stage 11] CHECK 11.5: SRT sequential, non-overlapping — PASS
[Stage 11] CHECK 11.6: No TBD in image_plan.md — PASS
[Stage 11] CHECK 11.7: All 5 AI beats have prompts — PASS
[Stage 11] CHECK 11.8: All 3 SEO titles ≤70 chars (62/58/55) — PASS
[Stage 11] CHECK 11.9: Hook ≤65 words (55 words) — PASS
[Stage 11] CHECK 11.10: All beats have visual assignments — PASS
[Stage 11] CHECK 11.11: Pronunciation guide complete — PASS
[Stage 11] CHECK 11.12: Tag count 27 (within 15-30) — PASS
[Stage 11] CHECK 11.13: Thumbnail prompt self-contained — PASS
[Stage 11] CHECK 11.14: Name consistency (5 spot-checks) — PASS
[Stage 11] CHECK 11.15: Date consistency (3 spot-checks) — PASS
[Stage 11] CHECK 11.16: SEO chapters match outline — PASS
[Stage 11] CHECK 11.17: Image count matches storyboard — PASS
[Stage 11] CHECK 11.18: Voice word count within ±5% of script — PASS

[STAGE 11 COMPLETE]
Output:     logs/qa_report.md
QA Score:   18/18 (100%)
Verdict:    READY_FOR_EXPORT ✓
Status:     PASS
──────────────────────────────────────────────
```

---

## Stage 12 — Export

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STAGE 12 — EXPORT
Project: 20260627_mystery-of-hashima-island
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Stage 12] QA verdict: READY_FOR_EXPORT ✓
[Stage 12] Finalizing export/export_manifest.json (all assets → validated)...
[Stage 12] Writing export/project_report.md...
[Stage 12] Completing logs/director_run_log.md...

[STAGE 12 COMPLETE]
Output:     export/export_manifest.json (final), export/project_report.md
Status:     PASS
──────────────────────────────────────────────
```

---

## Pipeline Complete

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DIRECTOR AI v1 — PIPELINE COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Project: 20260627_mystery-of-hashima-island
Status:  READY FOR PRODUCTION ✓

Output folder: projects/20260627_mystery-of-hashima-island/

Files ready for editor:
  → voice/voice_script.txt       (TTS / voice actor)
  → visuals/storyboard.md        (29 visual beats)
  → visuals/image_plan.md        (24 real image sourcing briefs)
  → visuals/ai_image_prompts.md  (5 AI image generation prompts)
  → voice/subtitles.srt          (subtitle import)
  → seo/thumbnail_prompt.md      (thumbnail design)
  → seo/seo.md                   (YouTube upload — 3 title options)

QA Score:          18/18 (100%)
Total warnings:    0
Stages completed:  13 / 13
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Next: Open projects/20260627_mystery-of-hashima-island/export/project_report.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Final Project Tree

```
projects/20260627_mystery-of-hashima-island/
├── input/
│   ├── input.json                   ← Stage 0
│   └── project.yaml                 ← Stage 0
├── research/
│   ├── research.md                  ← Stage 1
│   ├── source_report.md             ← Stage 2
│   └── research_verified.md         ← Stage 2
├── script/
│   ├── story_outline.md             ← Stage 3
│   ├── script.md                    ← Stage 4 (1,187 words)
│   └── story_bible.md               ← Stage 5
├── visuals/
│   ├── storyboard.md                ← Stage 6 (29 beats)
│   ├── image_plan.md                ← Stage 7 (24 real + 5 AI)
│   └── ai_image_prompts.md          ← Stage 8 (5 prompts)
├── voice/
│   ├── voice_script.txt             ← Stage 9 (plain text + markers)
│   ├── voice_direction.md           ← Stage 9 (ElevenLabs settings)
│   └── subtitles.srt                ← Stage 9 (estimated timecodes)
├── seo/
│   ├── seo.md                       ← Stage 10 (3 titles, description, 27 tags)
│   └── thumbnail_prompt.md          ← Stage 10
├── export/
│   ├── export_manifest.json         ← All stages (final: ready_for_production)
│   └── project_report.md            ← Stage 12
└── logs/
    ├── director_run_log.md          ← All stages
    ├── stage_00_setup.log
    ├── stage_01_research.log
    ├── stage_02_source_verifier.log
    ├── stage_03_story_outline.log
    ├── stage_04_script_writer.log
    ├── stage_05_story_bible.log
    ├── stage_06_scene_splitter.log
    ├── stage_07_image_finder.log
    ├── stage_08_image_prompt_generator.log
    ├── stage_09_voice_director.log
    ├── stage_10_youtube_seo.log
    ├── stage_11_final_qa.log
    ├── stage_12_export.log
    └── qa_report.md                 ← Stage 11
```

**Total files created by Director AI v1: 22**

---

## Example: Resume After Interruption

If the pipeline stopped after Stage 6 (a session timeout), resume with:

```
RESUME PROJECT: 20260627_mystery-of-hashima-island
```

Director AI reads `export/export_manifest.json`:
- Stages 0–6: all assets `validated` ✓
- Stage 7: `image_plan.status = absent`
- Determines: resume from Stage 7

Output:
```
[RESUME] Resuming project '20260627_mystery-of-hashima-island' from Stage 7.
Stages 0–6 already complete.
```

Pipeline continues from Stage 7 — Image Planning.

---

## What to Do Next

After the pipeline completes, your editor checklist:

- [ ] Review `export/project_report.md` — check for warnings or notes
- [ ] Read `script/script.md` aloud — listen for any awkward phrasing
- [ ] Source real images using `visuals/image_plan.md` — start with Strategy A
- [ ] Generate AI images from `visuals/ai_image_prompts.md` — 5 prompts ready
- [ ] Paste `voice/voice_script.txt` into ElevenLabs — apply `voice/voice_direction.md` settings
- [ ] Design thumbnail using `seo/thumbnail_prompt.md`
- [ ] Edit video using `visuals/storyboard.md` as shot list
- [ ] Upload to YouTube using `seo/seo.md` — choose one of the 3 titles
- [ ] Update `voice/subtitles.srt` timecodes to match actual audio
- [ ] Post the pinned comment immediately after publishing
