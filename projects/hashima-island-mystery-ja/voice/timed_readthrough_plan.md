# Timed Read-through Plan
## hashima-island-mystery-ja — FIX-M3
**Date:** 2026-06-27
**Status:** COMPLETE — Simulated timing audit finished. Ready for live talent read-through.

---

## 1. Purpose

This document defines the timing targets, per-section narration budgets, pause placement, and delivery modes required for the FIX-M3 timed read-through. The read-through must be completed by a voice talent (or director reading aloud at target pace) before any recording session begins.

**FIX-M3 requirement source:** `data/voice.json` → `fixes_applied.FIX-M3` — "timed_readthrough_required=true. Must be completed before talent session."

---

## 2. Script Overview

| Metric | Value |
|--------|-------|
| Total video duration | 720 seconds (12:00) |
| Total narration lines | 27 (L001-L034, excluding pauses/silence) |
| Total pause/silence events | 8 (L004, L010, L022, L026, L030, L031, L035 + 1 implicit) |
| Word count (morae estimate) | ~1,201 |
| Pure narration speaking time | ~423 seconds (7 min 3s) |
| Pauses + gaps between lines | ~101 seconds (1 min 41s) |
| Total narrated content | ~524 seconds (8 min 44s) |
| Visual silence (no narration) | ~196 seconds (3 min 16s) — distributed across all scenes |
| Ma beat silence (L031) | 40 seconds — S022, 10:20-11:00 |
| Language | Japanese (ja-JP) |
| Pacing style | deliberate_slow, contemplative |

**Effective pacing:** ~170 morae/min overall (including all pauses and visual silences). This is intentionally slower than standard documentary (250-300 morae/min) to match the 間(ma)-aware aesthetic.

---

## 3. Target: 12 Minutes ± 30 Seconds

The video is structured at exactly 720 seconds (12:00). This is a **fixed editorial target** — scene durations sum to 720s and cannot be changed. The narration must fit within this structure.

**The voice talent does not need to "fill" 720 seconds.** Each narration line plays within its assigned scene. Visual breathing room (scenes holding silently before or after narration) is built into the structure. The talent's job is to deliver each line at the correct pace within its scene window.

---

## 4. Section-by-Section Timing Targets

### HOOK — 0:00 to 1:00 (60 seconds)

| Scene | Timecode | Duration | Line | Text (abbreviated) | Delivery | Est. | Window |
|-------|----------|----------|------|-------------------|----------|------|--------|
| S001 | 0:00-0:10 | 10s | L001 | かつて、ここに5,259人が暮らしていました。 | very_slow | 5s | 10s |
| S002 | 0:10-0:25 | 15s | L002 | 子どもが走り回る声。石炭を掘る男たち... | very_slow | 10s | 15s |
| S003 | 0:25-0:40 | 15s | L003 | そして、ある日——すべてが消えました。 | very_slow | 6s | 15s |
| S004 | 0:40-1:00 | 20s | L004 | [PAUSE 2s] + title card hold | — | 2s | 20s |

**HOOK narration total:** 21s speaking + 7s pauses = 28s
**Visual silence in HOOK:** 32s (image holds before/after narration)
**HOOK target:** Begin speaking at exactly 0:00 on L001. L003 should feel like a sentence that lands, then the image holds in silence. Do not rush.

**Pacing note:** The HOOK opens on absolute stillness. L001 is said slowly, as if discovering. L002 builds — a human world. L003 drops it all away. Let the silence after L003 breathe for 7 seconds before the title card appears.

---

### ACT_I — 1:00 to 3:00 (120 seconds)

| Scene | Timecode | Duration | Line | Text (abbreviated) | Delivery | Est. | Window |
|-------|----------|----------|------|-------------------|----------|------|--------|
| S005 | 1:00-1:40 | 40s | L005 | 明治時代、日本は急速な近代化の道を... | normal | 20s | 40s |
| S006 | 1:40-2:10 | 30s | L006 | 1887年頃、長崎港から南西に約15〜18km... | slow | 15s | 30s |
| S007 | 2:10-2:45 | 35s | L007 | 1890年、三菱合資会社がこの島の採掘権を... | slow | 14s | 35s |
| → | 2:37-2:59 | (spans cut) | L008 | 度重なる埋め立て工事により、島の面積は... | normal | 22s | ⚠️ see note |
| S008 | 2:45-3:00 | 15s | (L008 continues from S007) | | | | |

**ACT_I narration total:** 71s speaking + 5s pauses = 76s
**Visual silence in ACT_I:** 44s

**⚠️ CRITICAL TIMING NOTE — S008/L008:**
S008 is only 15 seconds (2:45-3:00), but L008 is 22 seconds. **L008 must begin during S007 at approximately 2:37** — 8 seconds before the visual cut to S008. The audio L008 plays continuously across the scene cut. The narrator should not pause or change tone at 2:45; the cut is a visual event, not an audio event.

**Director cue:** After L007 ends (approx. 2:25), hold 12 seconds in silence over S007 aerial image. At 2:37, begin L008 narration. The visual cut to S008 (Building 30) happens during L008.

---

### ACT_II — 3:00 to 6:00 (180 seconds)

| Scene | Timecode | Duration | Line | Text (abbreviated) | Delivery | Est. | Window |
|-------|----------|----------|------|-------------------|----------|------|--------|
| S009 | 3:00-3:40 | 40s | L009 | 狭い島の上に、高層のコンクリート建築が... | normal | 28s | 40s |
| S009 | (within) | | L010 | [PAUSE 2s] | — | 2s | |
| S009→S010 | 3:34-3:52 | (spans) | L011 | 「軍艦島」という名前を、あなたはどこかで... | normal | 18s | bleeds |
| S010→S011a | 3:53-4:15 | (spans) | L012 | 2009年、35年間封鎖されていた島の一部が... | normal | 22s | bleeds |
| S011a | 4:17-4:27 | 10s | L013 | しかし、同じこの島の、もう少し深いところに... | slow | 10s | 30s |
| S011a→S011b | 4:29-4:45 | (spans) | L014 | 1939年から1945年にかけて、太平洋戦争の時代。... | slow | 16s | bleeds |
| S011b→S012 | 4:46-5:04 | (spans) | L015 | この事実は、日本政府もユネスコの審議の場で... | normal | 18s | bleeds |
| S012 | 5:05-5:23 | 18s | L016 | 強制労働に関与した具体的な人数、そして... | normal | 18s | 30s |
| S013 | 5:31-5:53 | 22s | L017 | 端島が世界遺産に登録されたのは、明治の... | slow | 22s | 30s |

**ACT_II narration total:** 124s speaking + 9s pauses = 133s
**Visual silence in ACT_II:** 47s (distributed across scene ends)

**ACT_II structure note:** This is the densest narration section. Multiple narration lines span across scene cuts (L011 bleeds from S009 into S010; L012 bleeds from S010 into S011a; L014 bleeds into S011b; L015 bleeds into S012). This is by design — the ACT_II content acceleration mirrors the historical acceleration of events. The audio track is continuous; the visuals cut independently.

**⚠️ SENSITIVE CONTENT FLAG — L013/L014 over S011a (IMG009):**
Lines L013 and L014 narrate forced labor history over the IMG009 mine tunnel image. FIX-M1 applies. Deliver L013 ("しかし、同じこの島の、もう少し深いところに目を向けると——別の物語が見えてきます。") with gravity but no sensationalism. L014 should be read as factual statement, not emotionally loaded. The empty tunnel carries the weight.

---

### ACT_III — 6:00 to 9:00 (180 seconds)

| Scene | Timecode | Duration | Line | Text (abbreviated) | Delivery | Est. | Window |
|-------|----------|----------|------|-------------------|----------|------|--------|
| S014 | 6:02-6:09 | 7s | L018 | 1974年1月15日、閉山が発表されました。 | slow | 7s | 30s |
| S015 | 6:31-6:46 | 15s | L019 | 理由はシンプルでした。石炭の時代が終わったのです。 | slow | 15s | 30s |
| S016 | 7:02-7:10 | 8s | L020 | 同年4月20日。最後の島民が、船に乗りました。 | slow | 8s | 30s |
| S017 | 7:32-7:48 | 16s | L021 | 5,259人が暮らした場所から、一人、また一人と... | very_slow | 16s | 30s |
| S017 | 7:50-7:52 | 2s | L022 | [PAUSE 2s] | — | 2s | |
| S018 | 8:01-8:19 | 18s | L023 | 家具は残されたまま。教科書は机の上に。... | slow | 18s | 30s |
| S019 | 8:31-8:47 | 16s | L024 | それから35年間、島は封鎖されました。... | slow | 16s | 30s |
| S019 | 8:48-9:00 | 12s | L025 | コンクリートだけが残り、かつての生活の痕跡だけが... | very_slow | 12s | 30s |
| S019 | — | [pause] | L026 | [PAUSE 2s — bleeds into S020] | — | 2s | |

**ACT_III narration total:** 92s speaking + 10s pauses = 102s
**Visual silence in ACT_III:** 78s

**ACT_III is the most spacious section in terms of narration:visual ratio.** Many scenes hold silently for 20+ seconds after short narration lines (L018: 7s narration in 30s scene; L020: 8s narration in 30s scene). These visual silences are part of the pacing design. Do not rush to fill them. The narrator should complete their line, then stop. The image continues.

**Delivery note — L018:** "1974年1月15日、閉山が発表されました。" Seven words, seven seconds. Absolute silence for 21 seconds after. This is intentional. The date is the weight.

**Delivery note — L020:** "同年4月20日。最後の島民が、船に乗りました。" Said as facts, not drama. The departure was quiet. Speak it quietly. 20 seconds of visual silence follows.

---

### ACT_IV — 9:00 to 11:00 (120 seconds, including Ma beat)

| Scene | Timecode | Duration | Line | Text (abbreviated) | Delivery | Est. | Window |
|-------|----------|----------|------|-------------------|----------|------|--------|
| S020 | 9:05-9:19 | 14s | L027 | 2015年7月5日、端島は「明治日本の産業革命遺産」... | slow | 14s | 40s |
| S021 | 9:40-10:02 | 22s | L028 | 登録は、日本の産業化の歴史に対する国際的な... | normal | 22s | 40s |
| S021 | 10:03-10:21 | 18s | L029 | 産業の誇りと、強制の記憶——どちらも、この島では... | slow | 18s | 40s |
| S021 | 10:23-10:25 | 2s | L030 | [PAUSE 2s] | — | 2s | |
| S022 | 10:25-11:05 | 40s | L031 | [MA BEAT — 40 seconds of silence] | SILENCE | 40s | 40s |

**ACT_IV narration total:** 54s speaking + 8s pauses = 62s
**Ma beat:** 40 seconds of pure silence (no narration, no dialogue, music and ocean waves only)

**⚠️ MA BEAT CRITICAL TIMING NOTE:**
To achieve the full 40-second Ma beat beginning within scene S022 (10:20-11:00), narration in ACT_IV must be placed as follows:
- **L027 starts at 9:05** (within S020, after L026 pause at 9:04)
- **L028 starts at 9:35** (5 seconds before S021 begins at 9:40 — begins during the visual silence of S020)
- This ensures L028+L029+L030 complete by 10:20, and the 40-second silence (L031) begins exactly at 10:20 and ends at 11:00

If L028 begins at 9:40 (S021 start), L029 and L030 bleed into S022 and the effective Ma silence is only ~35 seconds. **Preferred: begin L028 at 9:35.**

**The Ma beat (間) note:** After L030 ends, the narrator goes completely silent. No cue. No breath audible. 40 seconds of absolute silence in the recording. Music and ocean waves carry it. Do not break.

---

### OUTRO — 11:00 to 12:00 (60 seconds)

| Scene | Timecode | Duration | Line | Text (abbreviated) | Delivery | Est. | Window |
|-------|----------|----------|------|-------------------|----------|------|--------|
| S023 | 11:01-11:13 | 12s | L032 | 今日も、観光客が端島を訪れます。... | normal | 12s | 30s |
| S024 | 11:32-11:44 | 12s | L033 | 端島は、今もそこにあります。... | slow | 12s | 30s |
| S024 | 11:47-11:56 | 9s | L034 | この島が、あなたに問いかけているものは——何でしょうか。 | slow | 9s | 30s |
| S024 | 11:58-12:00 | 2s | L035 | [PAUSE 2s — fade out] | — | 2s | |

**OUTRO narration total:** 33s speaking + 6s pauses = 39s
**Visual silence in OUTRO:** 21s

**OUTRO delivery note — L034:** The final line. "この島が、あなたに問いかけているものは——何でしょうか。" Delivered extremely slowly, with a 3-second pause before it. The question is not rhetorical — it is genuine. Pause after the question. The video fades to black.

---

## 5. Pause Placement Map

| Line | Type | When | Duration | Note |
|------|------|------|----------|------|
| L004 | pause | After L003 (0:32) | 2s | Before title card |
| L010 | pause | After L009 (3:29) | 2s | ACT_I/ACT_II transition, within S009 |
| L022 | pause | After L021 (7:48) | 2s | Within S017 — light beam scene |
| L026 | pause | After L025 (9:00) | 2s | ACT_III/ACT_IV transition — bleeds into S020 |
| L030 | pause | After L029 (10:21) | 2s | Final breath before Ma beat |
| **L031** | **MA SILENCE** | **10:20-11:00** | **40s** | **No narration. No sound except music + ocean waves. Absolute.** |
| L035 | pause | After L034 (11:56) | 2s | Final pause — video fade |

---

## 6. Delivery Modes Reference

| Tag | Target pace | Use case |
|-----|-------------|---------|
| `very_slow` | ~150-180 morae/min | Opening and closing lines; emotional anchor moments |
| `slow` | ~200-230 morae/min | Historical facts, transition lines, date announcements |
| `normal` | ~250-270 morae/min | Contextual information, UNESCO fact, population context |

**All delivery modes are slower than conversational Japanese (~350 morae/min).** The target is contemplative documentary pace throughout. Even "normal" lines should feel measured. No line should feel rushed.

---

## 7. Read-through Procedure (Talent Instructions)

1. Read the full script once at natural pace before timing.
2. For the timed read-through, use a stopwatch or DAW timeline.
3. Mark the START time of each narration line on the script.
4. Mark the END time of each narration line.
5. Note the per-line duration and compare to estimated_duration_seconds in voice.json.
6. Total read-through (speaking only, no scene holds) should fall between 390-450 seconds (6:30-7:30).
7. After reading OUTRO, note total clock time. If under 390s, slow all lines proportionally. If over 450s, review long lines for natural trimming of delivery pace.
8. Flag any line where natural Japanese phrasing creates significant duration difference from estimate (±5s). These are candidates for script review (FIX-M3 follow-up).

---

## 8. Timing Flags for Director Review

| Flag | Scene | Issue | Recommended Action |
|------|-------|-------|-------------------|
| ⚠️ S008 NARROW | 2:45-3:00 | Scene is 15s but L008 narration is 22s | Start L008 at ~2:37 within S007 visual; narration spans scene cut |
| ⚠️ MA BEAT START | 10:20 | L028 start time is critical | Begin L028 at 9:35 (5s into S020 silent hold) to ensure 40s Ma silence begins at 10:20 |
| ℹ️ ACT_II FLOW | 3:00-6:00 | L011, L012, L014, L015 each span scene cuts | Normal in documentary production — do not re-cut; audio is continuous |
| ℹ️ L026 BLEED | 9:00-9:04 | L026 pause bleeds 4s into S020 | Acceptable — L027 starts at 9:05, S020 has 21s of silence remaining |

---

## 9. Voice Session Prerequisites (FIX-M3 Gate)

Before calling the voice talent:
- [ ] Director has completed one live read-through at target pace and confirmed overall timing ≤720s
- [ ] L008 start-point marked at 2:37 on timeline
- [ ] L028 start-point marked at 9:35 on timeline
- [ ] Ma beat (L031) silence confirmed at 40 seconds in DAW
- [ ] All FIX-M1 safety notes reviewed for L013/L014 delivery (factual tone, no dramatization)
- [ ] IMG009 rename confirmed: `IMG009_S011a_mine_tunnel_approved.png` ✓

---

*Created: 2026-06-27 | FIX-M3 gate document | Do not rewrite the script.*
