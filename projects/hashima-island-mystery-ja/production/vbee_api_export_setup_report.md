# Vbee API Export Setup Report
## hashima-island-mystery-ja
**Date:** 2026-06-28
**Stage:** 31 — Vbee API Export Automation Setup

---

## Files Created

| File | Purpose |
|------|---------|
| `.env.example` | Placeholder credential template — copy to `.env` and fill in |
| `tools/vbee_export_segments.py` | Main export script — calls Vbee API, saves MP3s, writes manifest |
| `tools/vbee_check_audio_manifest.py` | QA checker — verifies files, detects durations, writes report |
| `audio/vbee_raw/vbee_export_manifest.json` | Manifest stub — overwritten by export script after each run |
| `production/vbee_api_export_setup_report.md` | This report |

---

## Prerequisites

### 1. Python packages

```
pip install requests python-dotenv mutagen
```

| Package | Role | Required? |
|---------|------|-----------|
| `requests` | HTTP calls to Vbee API | Required |
| `python-dotenv` | Load `.env` file | Strongly recommended |
| `mutagen` | Detect audio duration in QA checker | Optional (checker works without it) |

### 2. .env file

Your `.env` already exists at `C:\youtubeAI\.env` with Vbee credentials.
The export script searches upward from the project directory and will find it automatically.

If you need to add Vbee-specific variables, copy `.env.example` to `.env` and add:

```
VBEE_APP_ID=<your app ID>
VBEE_API_KEY=<your JWT token>
VBEE_VOICE_ID=ja-JP-Standard-C
VBEE_SPEED=0.85
VBEE_OUTPUT_FORMAT=mp3
```

**Note:** The script also reads `EXPO_PUBLIC_VBEE_APP_ID` and `EXPO_PUBLIC_VBEE_API_KEY` as fallbacks.
If those are already set in your `.env`, no additional configuration is required.

---

## How to Run the Export

### Option A — Export all segments

```cmd
cd C:\youtubeAI\AI-Youtube-Studio\projects\hashima-island-mystery-ja
python tools\vbee_export_segments.py
```

### Option B — Dry run (no API calls, preview only)

```cmd
python tools\vbee_export_segments.py --dry-run
```

### Option C — Re-export everything (overwrite existing files)

```cmd
python tools\vbee_export_segments.py --overwrite
```

### Option D — Export a single segment

```cmd
python tools\vbee_export_segments.py --segment L001
python tools\vbee_export_segments.py --segment L014 --overwrite
```

### Option E — Disable retry on failure

```cmd
python tools\vbee_export_segments.py --no-retry
```

---

## How to Run the Audio Manifest Check

After export, verify all files:

```cmd
python tools\vbee_check_audio_manifest.py
```

With a custom tolerance window:

```cmd
python tools\vbee_check_audio_manifest.py --tolerance 8
```

The checker writes a full QA report to:
`production/vbee_audio_manifest_check_report.md`

---

## Where Audio Will Be Saved

```
projects/hashima-island-mystery-ja/
└── audio/
    └── vbee_raw/
        ├── hashima_L001_hook_01.mp3
        ├── hashima_L002_hook_02.mp3
        ├── hashima_L003_hook_03.mp3
        ├── hashima_L005_act1_01.mp3
        ├── ... (28 files total)
        ├── hashima_L034_outro_03.mp3
        └── vbee_export_manifest.json
```

---

## Speed Settings Per Segment

The export script applies per-segment speed from `delivery_mode` in `vbee_segmented_script.json`:

| delivery_mode | Vbee speed | Lines |
|--------------|-----------|-------|
| `very_slow` | 0.75x | L001, L002, L003, L021, L025, L029, L034 |
| `slow` | 0.80x | L006, L007, L013, L014, L015, L016, L017, L018, L019, L020, L023, L024, L027, L033 |
| `normal` | 0.85x | L005, L008, L009, L011, L012, L028, L032 |

---

## Critical Notes for Timeline Assembly

After all 28 files pass the QA checker:

| Note | Detail |
|------|--------|
| L008 start | Place at **2:37** in timeline (not at S008 start 2:45) — spans scene cut. TF-001. |
| L028 start | Place at **9:35** in timeline (not at S021 start 9:40) — protects 40s Ma beat. TF-002. |
| Ma beat | 40-second silence at 10:20-11:00 (S022). **Created by editor, not Vbee.** Music + ocean waves only. |
| L013/L014 | Sensitive content. Listen for factual (not dramatic) tone. FIX-M1 compliance. |
| L031 | No audio file should exist for L031. Ma beat = editor silence. |

---

## API Safety Notes

**The export script never logs or saves your API key. Specifically:**

- Credentials are read via `os.environ.get()` and passed directly to the HTTP Authorization header
- No `print()` call outputs the key value
- The manifest JSON contains `voice_id`, `speed_base`, `output_format` — not credentials
- The report file (this document) contains no credentials

**Protect your .env:**
- `C:\youtubeAI\.env` should remain gitignored
- Never commit it to any repository
- Never share the contents of `.env`
- Rotate your Vbee API key if it is accidentally exposed

---

## Troubleshooting

| Error | Likely cause | Fix |
|-------|-------------|-----|
| `VBEE_APP_ID is not set` | .env not found or missing variable | Verify `.env` exists and has `VBEE_APP_ID` or `EXPO_PUBLIC_VBEE_APP_ID` |
| `401 Unauthorized` | Invalid or expired API key | Regenerate Vbee JWT token |
| `403 Forbidden` | Wrong app ID | Check `VBEE_APP_ID` in .env |
| `requests.exceptions.ConnectionError` | No internet or Vbee API down | Check connectivity; retry later |
| `mutagen` not installed | Duration detection disabled | `pip install mutagen` — checker still runs |
| Duration too long/short | Speed setting mismatch | Re-export segment with `--overwrite` at adjusted speed |

---

## Next Action

1. Run dry run to confirm all 28 segments are listed:
   ```cmd
   python tools\vbee_export_segments.py --dry-run
   ```

2. When director has completed live read-through (FIX-M3 gate), run the full export:
   ```cmd
   python tools\vbee_export_segments.py
   ```

3. After export, verify all files:
   ```cmd
   python tools\vbee_check_audio_manifest.py
   ```

4. Review `production/vbee_audio_manifest_check_report.md`

5. Confirm L014 tone is factual (not dramatic). Confirm Ma beat file (L031) does NOT exist.

6. Proceed to timeline assembly in NLE.

---

*Stage 31 — Vbee API Export Automation Setup — COMPLETE*
