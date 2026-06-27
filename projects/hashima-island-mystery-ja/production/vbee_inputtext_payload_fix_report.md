# Vbee inputText Payload Fix Report
## hashima-island-mystery-ja
**Date:** 2026-06-28
**Trigger:** `--auth-test` returned HTTP 400: `{"input_text":"\"inputText\" is required"}`

---

## Problem Identified

| Finding | Detail |
|---------|--------|
| Auth result | ✅ No longer 401 — auth is correct |
| callbackUrl | ✅ No longer missing — callback fix applied |
| New 400 error | `{"input_text": "\"inputText\" is required"}` |
| Meaning | Text field in payload was named `text` — Vbee expects `inputText` |
| Pattern | All payload field names use camelCase, not snake_case |

The previous payload used Python-conventional snake_case names (`text`, `voice_code`, `audio_type`). Vbee's API requires camelCase names for all fields. The 400 error body format is `{snake_case_key: "\"camelCaseExpected\" is required"}`.

**Known required field mapping:**

| Our old name | Vbee expected name | Fix |
|-------------|-------------------|-----|
| `text`       | `inputText`        | ✅ Applied |
| `voice_code` | `voiceCode`        | ✅ Applied |
| `audio_type` | `audioType`        | ✅ Applied |
| `speed`      | `speed`            | No change needed |
| `callbackUrl`| `callbackUrl`      | Already correct |

---

## Changes Made

### 1. `tools/vbee_export_segments.py`

**New config variables (module-level):**
```python
TEXT_FIELD   = _env('VBEE_TEXT_FIELD',   default='inputText')
VOICE_FIELD  = _env('VBEE_VOICE_FIELD',  default='voiceCode')
SPEED_FIELD  = _env('VBEE_SPEED_FIELD',  default='speed')
FORMAT_FIELD = _env('VBEE_FORMAT_FIELD', default='audioType')
```

**`_build_request()` — before vs after:**

Before (wrong field names):
```python
payload = {
    'text':       text,
    'voice_code': voice_code,
    'speed':      speed,
    'bit_rate':   128000,
    'audio_type': audio_type,
}
```

After (configurable, defaults to Vbee's expected camelCase):
```python
payload = {
    TEXT_FIELD:   text,        # inputText
    VOICE_FIELD:  voice_code,  # voiceCode
    SPEED_FIELD:  speed,       # speed
    'bit_rate':   128000,
    FORMAT_FIELD: audio_type,  # audioType
}
```

**`_FIELD_ENV_MAP` — diagnostic lookup table:**
Maps each camelCase field name Vbee might report missing → the env var that controls it and its current value. Used by `_diagnose_400()` to give actionable hints without code edits.

**`_diagnose_400(data)` — new function:**
Called when auth-test returns 400. Parses each error key/value pair, extracts the expected field name using regex (`r'"([A-Za-z_][A-Za-z0-9_]*)"'`), looks it up in `_FIELD_ENV_MAP`, and prints:
- Which field is missing
- Which env var controls it
- The current configured value
- Whether it's already mapped or needs a new entry

Example output for a 400 on `inputText`:
```
    Missing field   : 'inputText'
    Env var         : VBEE_TEXT_FIELD='inputText'  (current value)
    → Field is already mapped. Check that .env has this variable set,
      then re-run --auth-test.
```

Example for a completely unknown field:
```
    Unknown field   : 'bitRate'  (not in current payload map)
    → Add to .env.example and .env, then update _build_request() to include it.
      Example: VBEE_BITRATE_FIELD=bitRate
```

**`_print_request_debug()` — new payload fields line:**
```
[DEBUG] payload fields : inputText  voiceCode  speed  audioType
```

**`print_config()` — new payload fields section:**
```
  Payload fields    :
    text field      : inputText            (VBEE_TEXT_FIELD)
    voice field     : voiceCode            (VBEE_VOICE_FIELD)
    speed field     : speed                (VBEE_SPEED_FIELD)
    format field    : audioType            (VBEE_FORMAT_FIELD)
    callback field  : callbackUrl          (VBEE_CALLBACK_FIELD)
```

### 2. `.env.example`

New payload field variables added in a dedicated section:
```
VBEE_CALLBACK_FIELD=callbackUrl
VBEE_TEXT_FIELD=inputText
VBEE_VOICE_FIELD=voiceCode
VBEE_SPEED_FIELD=speed
VBEE_FORMAT_FIELD=audioType
```

---

## Payload Fields Now Used

Complete payload sent to Vbee (with current defaults):
```json
{
  "inputText":   "<narration text>",
  "voiceCode":   "ja-JP-Standard-C",
  "speed":       0.85,
  "bit_rate":    128000,
  "audioType":   "mp3",
  "callbackUrl": "https://example.com/vbee-callback",
  "app_id":      "<from VBEE_APP_ID>"
}
```

---

## .env Lines to Add

Add to `C:\youtubeAI\.env`:
```
VBEE_TEXT_FIELD=inputText
VBEE_VOICE_FIELD=voiceCode
VBEE_SPEED_FIELD=speed
VBEE_FORMAT_FIELD=audioType
```

These are already the default values — the script works correctly even if you don't add them. Only add them if you need to override (e.g., if Vbee changes a field name in a future API version).

---

## Commands

### Verify config (confirm payload field names shown):
```cmd
cd C:\youtubeAI\AI-Youtube-Studio\projects\hashima-island-mystery-ja
python tools\vbee_export_segments.py --print-config
```

### Run auth test (should now return 200):
```cmd
python tools\vbee_export_segments.py --auth-test
```

Expected 200 outcomes:
- Binary audio → synchronous, export ready
- JSON with `audio_url` → synchronous, export ready
- JSON with `request_id` / `task_id` → async, check `vbee_pending_jobs.json`

If another 400 appears, `_diagnose_400()` will name the missing field and the env var to set.

### Export L001 after successful auth test:
```cmd
python tools\vbee_export_segments.py --segment L001 --overwrite
```

### Full export (after FIX-M3 live read-through):
```cmd
python tools\vbee_export_segments.py
```

---

## If Another 400 Appears

The `_diagnose_400()` function will parse the response and print:
```
Missing field   : '<fieldName>'
Env var         : VBEE_<FIELD>_FIELD='<currentValue>'
```

If the field is not in the current map (truly new unknown field), it will print:
```
Unknown field   : '<fieldName>'  (not in current payload map)
→ Add to .env.example and .env, then update _build_request() to include it.
  Example: VBEE_<FIELDNAME>_FIELD=<fieldName>
```

No code edit is needed for the four main fields — just set the env var and re-run.

---

## Backward Compatibility

- Default values (`inputText`, `voiceCode`, `speed`, `audioType`) are set in code
- Users who don't add the new env vars get the correct Vbee field names automatically
- Users who previously had `VBEE_TEXT_FIELD=text` in .env would need to update it — but since these are new variables, no existing .env file has them

---

*Stage 33 — Vbee inputText Payload Fix — COMPLETE*
