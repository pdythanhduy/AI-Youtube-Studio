# Vbee Quality Checklist
## hashima-island-mystery-ja — Post-Export Audio Review
**Date:** 2026-06-27
**Complete this checklist after all 28 segments are exported from Vbee.**

---

## How to Use

Play each audio file. Check each item. If any check fails, note the line ID and re-export that segment.

Mark each item: ✅ PASS / ❌ FAIL / ⚠️ NEEDS REVIEW

---

## Section 1 — File Completeness

- [ ] **28 files exported** — count the files in `audio/vbee_raw/`. Must be exactly 28.
- [ ] **All filenames correct** — verify naming convention: `hashima_L[XXX]_[section]_[NN].mp3`
- [ ] **No pause files** — confirm L004, L010, L022, L026, L030, L031, L035 do NOT have audio files (they are editor silences)
- [ ] **No duplicate filenames** — no files accidentally exported twice

---

## Section 2 — Japanese Pronunciation

Listen to each file and verify these specific readings:

| File | Word to check | Should read | ✅/❌ |
|------|--------------|------------|-------|
| L001 | 5,259人 | ごせんにひゃくごじゅうくにん | |
| L006 | 端島 | はしま（not たんとう, not はしじま） | |
| L006 | 軍艦島 | ぐんかんじま | |
| L007 | 三菱合資会社 | みつびしごうしかいしゃ | |
| L008 | 大正5年 | たいしょうごねん | |
| L008 | 30号棟 | さんじゅうごうとう | |
| L008 | 鉄筋コンクリート造 | てっきんコンクリートぞう | |
| L009 | 5,259人 (second occurrence) | ごせんにひゃくごじゅうくにん | |
| L014 | 炭坑 | たんこう（long vowel） | |
| L015 | 意に反して | いにはんして | |
| L018 | 閉山 | へいざん（not へいさん, not ふうざん） | |
| L023 | 玩具 | おもちゃ（not がんぐ） | |
| L027 | 構成資産 | こうせいしさん | |

**If any pronunciation is wrong:** Substitute the correct hiragana reading in the Vbee input field for that segment only. Re-export the affected file.

---

## Section 3 — No Accidental Label Reading

Play each file and confirm none of the following are spoken aloud by the TTS:

- [ ] No "L001", "L002" or any line ID spoken
- [ ] No "HOOK", "ACT_I", "SECTION" or structural labels
- [ ] No "[slow]", "[normal]", "[very_slow]" delivery tags spoken
- [ ] No "hashima_L001" or filename content spoken
- [ ] No "export_filename", "delivery_mode", or JSON keys spoken
- [ ] No timestamp numbers read as narration (e.g., "0:00" or "2:37")

If any label was accidentally included in a paste, re-export that segment with only the narration text.

---

## Section 4 — Pacing Verification

Verify approximate duration for each segment. A ±3s variance from target is acceptable. A ±6s variance requires re-export at adjusted speed.

| File | Target duration | Actual duration | Status |
|------|----------------|----------------|--------|
| L001 | 5s | | |
| L002 | 10s | | |
| L003 | 6s | | |
| L005 | 20s | | |
| L006 | 15s | | |
| L007 | 14s | | |
| L008 | 22s | | |
| L009 | 28s | | |
| L011 | 18s | | |
| L012 | 22s | | |
| L013 | 10s | | |
| L014 | 16s | | |
| L015 | 18s | | |
| L016 | 18s | | |
| L017 | 22s | | |
| L018 | 7s | | |
| L019 | 15s | | |
| L020 | 8s | | |
| L021 | 16s | | |
| L023 | 18s | | |
| L024 | 16s | | |
| L025 | 12s | | |
| L027 | 14s | | |
| L028 | 22s | | |
| L029 | 18s | | |
| L032 | 12s | | |
| L033 | 12s | | |
| L034 | 9s | | |

**If a file is more than 6 seconds over target:** Increase Vbee speed slightly (+0.05x) and re-export.
**If a file is more than 6 seconds under target:** Decrease Vbee speed slightly (-0.05x) and re-export.

---

## Section 5 — Sensitive History Tone (L013-L016)

These four lines cover forced labor history. Play them and check:

- [ ] **L013** — "しかし、同じこの島の、もう少し深いところに目を向けると——別の物語が見えてきます。"
  - Sounds: grave, weighted, pivoting
  - Does NOT sound: dramatic, horror-like, alarmed
  - Does NOT sound: too casual or too light

- [ ] **L014** — "1939年から1945年にかけて、太平洋戦争の時代。朝鮮半島および中国大陸から連行された人々が、この炭坑の地下深くで働かされました。"
  - Sounds: factual, measured, record-like
  - Does NOT sound: sensational, emotionally heightened, mournful
  - Does NOT sound: rushed or careless
  - **FIX-M1 requirement: if this sounds sensational or horror-movie-like, reduce speed or re-export with different voice settings**

- [ ] **L015** — "意に反して" is pronounced correctly and delivered neutrally
  - Does NOT sound like the TTS is emphasizing or editorially loading this phrase

- [ ] **L016** — "歴史の検証は続いています。" ends the section with an open, non-conclusive tone
  - Does NOT sound: declarative, as if reaching a verdict
  - Does sound: open, ongoing, unresolved

**If any of these fails:** Re-export at slightly lower speed and/or with a more neutral voice setting.

---

## Section 6 — No Horror or Overly Dramatic Tone

This is a reflective documentary about a complex historical site. Play the full sequence (all 28 files in order with appropriate gaps) and check:

- [ ] The overall tone is: contemplative, factual, respectful, intellectually engaging
- [ ] The tone is NOT: horror, thriller, ghost story, melodramatic, manipulative
- [ ] No single line sounds like a horror movie
- [ ] The HOOK (L001-L003) feels mysterious but not sinister
- [ ] ACT III (L018-L025) feels mournful but not theatrical
- [ ] The final question (L034) sounds genuinely curious — not ominous

If any section sounds like a horror/thriller narration: try a different Vbee voice or reduce "expressive" settings.

---

## Section 7 — Special Placement Notes (Timeline Gate)

These two checks must be confirmed before assembling in the editor:

- [ ] **L008 placement confirmed:** Audio file duration is approximately 22 seconds. Editor will place this at 2:37 in the timeline (not 2:45). The narration will span the S007/S008 visual cut. This is correct.

- [ ] **L028 placement confirmed:** Audio file duration is approximately 22 seconds. Editor will place this at 9:35 in the timeline (not 9:40). This ensures the Ma beat begins at exactly 10:20.

---

## Section 8 — Ma Beat Integrity

- [ ] **L031 audio file does NOT exist** in `audio/vbee_raw/` — the Ma beat is editor silence, not Vbee audio
- [ ] Editor has confirmed: 40 seconds of silence will be placed at 10:20-11:00 in the timeline
- [ ] Only music and ocean waves play during the Ma beat — confirmed in the mix plan

---

## Section 9 — Full Sequential Playback Test

After placing all files in the editor with correct gaps:

- [ ] Play from 0:00 — HOOK feels powerful and quiet
- [ ] Hook narration completes before 0:30 ✓
- [ ] The ACT I/ACT II transition (around 3:00) is smooth
- [ ] The forced labor section (4:17-5:23) is factual and respectful
- [ ] ACT III (6:00-9:00) feels elegiac — not rushed
- [ ] The UNESCO inscription narration (9:05-9:19) is clear
- [ ] Ma beat (10:20-11:00) is exactly 40 seconds of silence
- [ ] OUTRO final question (11:47-11:56) lands as an open question
- [ ] Video ends cleanly at 12:00

---

## Sign-off

| Item | Status | Notes |
|------|--------|-------|
| All 28 files exported | | |
| Pronunciation verified | | |
| No labels in audio | | |
| Pacing within ±6s | | |
| Sensitive tone correct | | |
| No horror tone | | |
| L008/L028 placement understood | | |
| Ma beat is editor-created (not Vbee) | | |
| Full playback test passed | | |

**Export package ready for timeline assembly:** ⬜ YES / ⬜ NO

---

*Completed by:* ___________________
*Date:* ___________________________
