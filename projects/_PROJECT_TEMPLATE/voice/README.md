# voice/ — Voice Direction and Audio Assets

This folder contains all voice and audio production files. It is written by Stage 9.

---

## Files

### `voice_script.txt` — TTS-ready narration (Stage 9)

**Written by:** Director AI running `prompts/09_voice_director.md`

This is the file you paste into ElevenLabs (or give to your voice actor). It is plain text only.

**Rules enforced:**
- No markdown characters (`#`, `*`, `_`, `>`, `|`)
- Numbers are spelled out in English: "twenty-three" not "23"
- Abbreviations are expanded: "Doctor" not "Dr."
- Approved pacing markers only:
  - `[PAUSE:0.5s]` `[PAUSE:1s]` `[PAUSE:1.5s]` `[PAUSE:2s]` `[PAUSE:3s]`
  - `[SLOW]` ... `[NORMAL]` `[FAST]` `[WHISPER]`
- Exactly one `[PAUSE:3s]` in the entire file (the climactic beat)
- Maximum three `[PAUSE:2s]` in the entire file

**Status after stage:** `voice_script.status = complete` in manifest

---

### `voice_direction.md` — Delivery notes (Stage 9)

**Written by:** Director AI running `prompts/09_voice_director.md`

Contains:
- **Voice Character** — register, pace, emotional tone, accent guidance
- **ElevenLabs Settings** — stability, similarity_boost, style, speed recommended values
- **Scene-by-Scene Delivery Notes** — specific guidance for each scene
- **Critical Moments** — how to deliver the hook, climax, and closing line
- **Pronunciation Guide** — phonetic spellings for all proper nouns
- **Words to Avoid** — any terms that sound awkward when spoken

This file is for the human directing the voice session or for tuning TTS settings.

**Status after stage:** `voice_direction.status = complete` in manifest

---

### `subtitles.srt` — Subtitle file (Stage 9)

**Written by:** Director AI running `prompts/09_voice_director.md`

SRT format subtitles generated from `voice_script.txt` with estimated timecodes.

**Spec enforced:**
- UTF-8 encoding
- Sequential numbering starting at 1
- No overlapping timecodes
- Timecode format: `HH:MM:SS,mmm --> HH:MM:SS,mmm` (comma, not period)
- Max 42 characters per line
- Max 2 lines per segment
- Segments: 1–7 seconds duration

**Note:** Timecodes are estimated based on language WPM from `configs/language_profiles.md`. Final timecodes should be adjusted after audio is generated.

**Status after stage:** `subtitles.status = complete` in manifest

---

## What You Do After Stage 9

1. Review `voice_script.txt` for any awkward phrasing before TTS generation
2. Configure ElevenLabs with settings from `voice_direction.md`
3. Generate the audio file → save as `voice/voice_output.mp3` (not created by the Director)
4. After audio is generated, update `subtitles.srt` timecodes to match actual audio timing
5. Import `subtitles.srt` into your video editor

---

## What Does NOT Belong Here

- Final audio files go in `voice/` (you create them manually after Stage 9)
- Script text belongs in `script/script.md`
- Music selections belong in the editor's workspace, not here
