# Vbee Export Instructions
## hashima-island-mystery-ja
**Date:** 2026-06-27
**Language:** Japanese (ja-JP)
**Recommended mode:** Segmented export (one file per narration line)

---

## Overview

Vbee is a TTS (text-to-speech) platform. This package prepares the full Hashima documentary narration for Vbee export. You will:
1. Choose a Japanese voice
2. Paste narration segments one at a time
3. Export each segment as a separate audio file
4. Save files with the naming convention below
5. Assemble in the editor (pauses and Ma beat are added there, not in Vbee)

**Total segments to export: 28**
**Total speaking time: ~423 seconds (~7 minutes)**
**Pauses: added by editor — not generated in Vbee**

---

## Step 1 — Access Vbee

1. Open Vbee in your browser.
2. Log in to your account.
3. Navigate to the TTS creation screen.

---

## Step 2 — Select Japanese Voice

**Voice requirements:**
- Language: Japanese (日本語)
- Gender preference: Male (推奨) or Female — deep, calm quality
- Style: Standard / Neutral / Documentary
- Do NOT use "expressive," "energetic," "cheerful," or "news anchor" styles

**Recommended Vbee Japanese voices** (choose the one that sounds most like NHK documentary narration):
- Look for voices described as: 落ち着いた, 標準語, ナレーション, ドキュメンタリー
- Test with this sentence: 「かつて、ここに5,259人が暮らしていました。」
- The output should sound: calm, measured, deep, not news-anchor sharp

**Avoid voices that sound:**
- Bright or cheerful (アニメ的, 元気, 明るい)
- Robot-like or monotone
- Fast or TV-commercial-paced
- Over-emotional or dramatic

---

## Step 3 — Speed Settings

Vbee speed controls how fast the TTS reads. Use these settings per delivery mode:

| Delivery mode | Vbee speed setting | Lines |
|--------------|-------------------|-------|
| `very_slow` | 0.75x | L001, L002, L003, L021, L025, L029, L034 |
| `slow` | 0.78x–0.80x | L006, L007, L013, L014, L015, L016, L017, L018, L019, L020, L023, L024, L027, L033 |
| `normal` | 0.85x | L005, L008, L009, L011, L012, L028, L032 |

**If your version of Vbee does not have fractional speed control**, use these approximate settings:
- very_slow → slowest available (or -30%)
- slow → -20%
- normal → -15%

**Why slow?** This is a Japanese documentary. The standard NHK pacing is already slow compared to conversation. Going below 0.75x risks sounding unnatural. Do not go below 0.72x for any line.

---

## Step 4 — Export Mode Choice

### Option A: Segmented Export (RECOMMENDED)

Export one Vbee file per narration line. 28 separate exports.

**Why recommended:**
- Full timeline control in the editor
- Can re-export individual lines without re-doing the whole script
- Allows different speed per section
- Easier to place L008 at 2:37 and L028 at 9:35 independently
- Ma beat placement is precise
- If one line sounds wrong, fix only that line

**Process:**
1. Paste one segment text into Vbee
2. Set speed
3. Preview
4. If pronunciation sounds wrong, check the notes in `vbee_segmented_script.md`
5. Export
6. Name file using the convention below
7. Repeat for next segment

### Option B: Full Script Export (NOT RECOMMENDED)

Paste `vbee_full_script_clean.txt` into Vbee as one block and export as a single file.

**Problems with this approach:**
- Cannot set different speeds per section
- Cannot independently adjust L008 and L028 start times
- Ma beat (40s silence) cannot be inserted correctly inside the audio file
- If any line sounds wrong, must re-export the entire script
- Timeline assembly becomes harder

Use Option B only if Vbee does not support multiple exports or if you need a quick preview draft.

---

## Step 5 — Pronunciation Pre-check

Before exporting, test these specific words and phrases. If Vbee mispronounces them, adjust:

| Word / Phrase | Correct reading | Common Vbee error |
|--------------|-----------------|-------------------|
| 端島 | はしま | Vbee may read as たんとう or はしじま |
| 軍艦島 | ぐんかんじま | Usually correct |
| 閉山 | へいざん | Vbee may read as へいさん or ふうざん |
| 炭坑 | たんこう | Vbee may read as すみあな |
| 三菱合資会社 | みつびしごうしかいしゃ | Watch for incorrect 合 reading |
| 5,259人 | ごせんにひゃくごじゅうくにん | Numbers with commas sometimes break |
| 意に反して | いにはんして | Vbee should handle this — verify |
| 玩具 | おもちゃ | Vbee often reads this as がんぐ — must fix |
| 大正5年 | たいしょうごねん | Test this |

**If Vbee mispronounces a word:** Use furigana or phonetic replacement in the text. For example:
- Replace `端島` with `はしま` (hiragana) in the Vbee input if needed
- Replace `玩具` with `おもちゃ` in the Vbee input

This is a phonetic substitution for Vbee input only — do NOT change the authoritative script files.

---

## Step 6 — Export Format

| Setting | Value |
|---------|-------|
| Format | MP3 (Vbee default) |
| Bitrate | Highest available (192kbps or 320kbps) |
| Sample rate | 44.1kHz or 48kHz (prefer 48kHz if available) |

**After export:** If your editor requires WAV, convert MP3 files to WAV 48kHz 24-bit using Audacity or FFmpeg before import.

Do NOT use AAC or OGG — these may introduce artifacts after conversion.

---

## Step 7 — Naming Convention

Name each exported file exactly as shown in `vbee_segmented_script.md`:

```
hashima_[LineID]_[section]_[sequence].mp3
```

Examples:
```
hashima_L001_hook_01.mp3
hashima_L008_act1_04.mp3
hashima_L014_act2_04.mp3
hashima_L031_act4_03.mp3
```

**Rules:**
- Lowercase only
- No spaces — use underscores
- Line ID must match voice.json (L001, L002... not 001, 1, or line1)
- Do not add dates, version numbers, or personal initials to the filename

---

## Step 8 — Save Location

Save all exported Vbee audio files to:

```
projects/hashima-island-mystery-ja/audio/vbee_raw/
```

This folder does not yet exist — create it before saving.

**Folder structure:**
```
audio/
  vbee_raw/
    hashima_L001_hook_01.mp3
    hashima_L002_hook_02.mp3
    hashima_L003_hook_03.mp3
    ... (all 28 segments)
```

Do NOT save to the `voice/` folder — that folder contains script and direction files, not audio.

---

## Step 9 — After Export

After all 28 files are exported and saved:

1. Run the quality checklist: `vbee_quality_checklist.md`
2. Import all files into the editing timeline
3. Place each file at its intended timecode from `data/timing_plan.json`
4. Insert editor silences: 2s at L004/L010/L022/L026/L030; 40s Ma beat at L031; 2s at L035
5. Place L008 audio at 2:37 (not 2:45) — see `vbee_pause_plan.md`
6. Place L028 audio at 9:35 (not 9:40) — see `vbee_pause_plan.md`
7. Mix narration with music and ambient sound

---

## Export Session Checklist

- [ ] Japanese voice selected and tested
- [ ] Speed verified before first export
- [ ] Pronunciation test done (端島, 閉山, 炭坑, 玩具)
- [ ] `audio/vbee_raw/` folder created
- [ ] All 28 segments exported
- [ ] Files named with correct convention
- [ ] No pause lines exported (L004, L010, L022, L026, L030, L031, L035 — these are editor silences)
- [ ] Quality checklist completed (`vbee_quality_checklist.md`)

---

*Do not rewrite the script. Do not generate the Ma beat in Vbee. Do not modify images.*
