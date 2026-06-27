# Vbee Speed Field Fix Report
## hashima-island-mystery-ja
**Date:** 2026-06-28
**Trigger:** `--auth-test` returned 400: `{"details":[{"speed":"\"speed\" is not allowed"}]}`

---

## Problems Identified

### Problem 1 — `speed` field rejected by Vbee

| Finding | Detail |
|---------|--------|
| HTTP status | 400 Validation Failed |
| Vbee error location | `details` array |
| Error | `{"speed": "\"speed\" is not allowed"}` |
| Meaning | Vbee's `/api/v1/tts` endpoint does not accept a `speed` parameter |
| Impact | Speed control via delivery_mode is not available at this endpoint |

### Problem 2 — `_diagnose_400()` parsed the response envelope instead of `details`

The function iterated over top-level response keys (`status`, `error_code`, `error_message`) and misidentified them as missing payload fields. Vbee puts validation errors inside a `details` array, not at the top level.

---

## Changes Made

### 1. `tools/vbee_export_segments.py`

**New config variable:**
```python
INCLUDE_SPEED = _env('VBEE_INCLUDE_SPEED', default='false').lower() == 'true'
```
Default is `false` because Vbee rejects the field. Set `VBEE_INCLUDE_SPEED=true` only if a future endpoint or voice accepts it.

**`_build_request()` — speed removed from default payload:**

Before:
```python
payload = {
    TEXT_FIELD:   text,
    VOICE_FIELD:  voice_code,
    SPEED_FIELD:  speed,    # ← rejected by Vbee
    'bit_rate':   128000,
    FORMAT_FIELD: audio_type,
}
```

After:
```python
payload = {
    TEXT_FIELD:   text,
    VOICE_FIELD:  voice_code,
    FORMAT_FIELD: audio_type,
}
if INCLUDE_SPEED:
    payload[SPEED_FIELD] = speed
```

Note: `bit_rate` also removed. It was a guess at a field name and is not confirmed as accepted by Vbee. Removing unknown fields reduces the chance of future 400 errors.

**`_diagnose_400()` — rewritten to parse `details` correctly:**

Vbee 400 response structure:
```json
{
  "status": 0,
  "error_code": 400,
  "error_message": "Validation Failed",
  "details": [
    {"speed": "\"speed\" is not allowed"}
  ]
}
```

New logic:
1. Check `data.get('details')` → list of `{field: msg}` dicts → flatten into `error_items`
2. Also check `data.get('errors')`, `data.get('validation_errors')` as alternatives
3. Fallback: top-level keys minus known envelope fields (`status`, `error_code`, `error_message`, etc.)
4. For each error, detect whether it's `"not allowed"` or `"required"` and print the right hint

New output for a "not allowed" error:
```
    Rejected field  : 'speed'  — Vbee does not accept this field
    Controlled by   : VBEE_SPEED_FIELD='speed'
    → The field has been removed from the default payload.
      To re-enable: set VBEE_INCLUDE_speed=true in .env
```

New output for a "required" error on a mapped field:
```
    Missing field   : 'inputText'
    Env var         : VBEE_TEXT_FIELD='inputText'  (current value)
    → Field is mapped. Verify .env has this variable, then re-run --auth-test.
```

New output for an unmapped missing field:
```
    Missing field   : 'someNewField'  (not in current payload map)
    → Add to _build_request(). Suggested env var:
      VBEE_SOMENEWFIELD_FIELD=someNewField
```

**`print_config()` — speed exclusion shown:**
```
    speed field     : speed [EXCLUDED — Vbee rejects it]  (VBEE_SPEED_FIELD / VBEE_INCLUDE_SPEED=false)
```

### 2. `.env.example`

```
VBEE_SPEED_FIELD=speed
VBEE_INCLUDE_SPEED=false
```
With documentation: Vbee `/api/v1/tts` rejects the speed field. Keep `false` unless a future endpoint confirms it.

---

## Payload Now Sent to Vbee

```json
{
  "inputText":   "<narration text>",
  "voiceCode":   "ja-JP-Standard-C",
  "audioType":   "mp3",
  "callbackUrl": "https://example.com/vbee-callback",
  "app_id":      "<from VBEE_APP_ID>"
}
```

Speed is **not** included. All segments will be read at Vbee's default speed for the selected voice.

---

## Impact on Delivery Modes

The segmented script assigns `delivery_mode` (very_slow / slow / normal) to each segment, which previously mapped to speeds (0.75 / 0.80 / 0.85). Since Vbee rejects the speed parameter:

- Speed variation between segments is **not available** at this endpoint
- All segments will use the voice's default pacing
- If Vbee offers speed control through a different mechanism (voice code variant, API v2, or a different endpoint), the `VBEE_INCLUDE_SPEED=true` flag + `VBEE_SPEED_FIELD` can re-enable it without code changes

---

## Commands

### Verify config:
```cmd
cd C:\youtubeAI\AI-Youtube-Studio\projects\hashima-island-mystery-ja
python tools\vbee_export_segments.py --print-config
```

### Run auth test (should now return 200):
```cmd
python tools\vbee_export_segments.py --auth-test
```

### Export L001 after successful auth test:
```cmd
python tools\vbee_export_segments.py --segment L001 --overwrite
```

---

*Stage 34 — Vbee Speed Field Fix — COMPLETE*
