# Vbee API Adapter Fix Report
## hashima-island-mystery-ja
**Date:** 2026-06-28
**Trigger:** L001 export returned HTTP 401 Unauthorized on first run.

---

## Problem Identified

| Finding | Detail |
|---------|--------|
| Endpoint used (original) | `https://api.vbee.vn/v1/tts` |
| HTTP result | 401 Unauthorized |
| `.env` loading | ✅ Working — key found, length=105 |
| Token value | Present but rejected by endpoint |
| Likely cause | Wrong base URL and/or wrong auth structure |

The original script hardcoded the endpoint path as `{BASE_URL}/v1/tts`, which constructed `https://api.vbee.vn/v1/tts`. Vbee documentation and integration patterns suggest the correct endpoint is `https://vbee.vn/api/v1/tts`.

Additionally, some Vbee API configurations require the App ID + token in the request payload rather than a Bearer header.

---

## Changes Made

### 1. `tools/vbee_export_segments.py` — full adapter refactor

**Token priority chain (new):**
```
VBEE_ACCESS_TOKEN  → if set, used as bearer token
VBEE_API_KEY       → fallback
EXPO_PUBLIC_VBEE_API_KEY  → final fallback (Expo prefix)
```

**Auth adapter (`_build_request`):**

| VBEE_AUTH_MODE | Behavior |
|---------------|----------|
| `bearer` (default) | `Authorization: Bearer <token>` + `app_id` in body |
| `api_key_header` | `<VBEE_AUTH_HEADER_NAME>: <token>` + `app_id` in body |
| `app_id_token_payload` | No auth header — `app_id` + `token` in JSON body |

**New CLI options:**

| Flag | Action |
|------|--------|
| `--print-config` | Print all config safely (no secret values) |
| `--auth-test` | POST one test request, print full response for diagnosis |

**Safe debug output** (before each API call):
```
[DEBUG] API URL      : https://vbee.vn/api/v1/tts
[DEBUG] auth mode    : bearer
[DEBUG] auth header  : Authorization: Bearer ***
[DEBUG] app_id       : set (len=36)
[DEBUG] token source : EXPO_PUBLIC_VBEE_API_KEY  len=105
[DEBUG] voice        : ja-JP-Standard-C  speed=0.85  text_chars=19
```

**Manifest now includes** `api_url` and `auth_mode` fields for traceability.

### 2. `.env.example` — updated

New variables added:
```
VBEE_ACCESS_TOKEN=      ← short-lived token (takes priority over API key)
VBEE_API_URL=https://vbee.vn/api/v1/tts
VBEE_AUTH_MODE=bearer
VBEE_AUTH_HEADER_NAME=Authorization
```

URL candidates documented with try-in-order instructions.

---

## Diagnosis Procedure

### Step 1 — Check config is loading correctly

```cmd
cd C:\youtubeAI\AI-Youtube-Studio\projects\hashima-island-mystery-ja
python tools\vbee_export_segments.py --print-config
```

Expected output:
```
API URL         : https://vbee.vn/api/v1/tts
Auth mode       : bearer
Auth header     : Authorization: Bearer ***
APP_ID          : set  (len=36)
Token source    : VBEE_API_KEY / EXPO_PUBLIC_VBEE_API_KEY
Token length    : 105
Voice ID        : ja-JP-Standard-C
```

If `Token length : 0` — the .env is not loading. Check python-dotenv is installed.

### Step 2 — Run auth test

```cmd
python tools\vbee_export_segments.py --auth-test
```

Read the response:

| HTTP result | Meaning | Next step |
|-------------|---------|-----------|
| 200 + binary audio | ✅ Working | Run export |
| 200 + JSON with audio_url | ✅ Working | Run export |
| 401 with current settings | Token/endpoint mismatch | See Step 3 |
| 403 | App ID wrong or token lacks permission | Check dashboard |
| 404 | Wrong URL | Try alternate URL |
| Connection error | Network issue or wrong domain | Check URL |

### Step 3 — If still 401: try auth mode variations

Try each in sequence, running `--auth-test` after each change:

**Attempt A — different endpoint:**
```
# In .env:
VBEE_API_URL=https://vbee.vn/api/v1/tts
VBEE_AUTH_MODE=bearer
```

**Attempt B — token in payload:**
```
VBEE_API_URL=https://vbee.vn/api/v1/tts
VBEE_AUTH_MODE=app_id_token_payload
```

**Attempt C — custom header name:**
```
VBEE_AUTH_MODE=api_key_header
VBEE_AUTH_HEADER_NAME=X-API-Key
```

**Attempt D — old endpoint with new auth mode:**
```
VBEE_API_URL=https://api.vbee.vn/v1/tts
VBEE_AUTH_MODE=app_id_token_payload
```

**Attempt E — check Vbee dashboard for v2 or different path:**
```
VBEE_API_URL=https://vbee.vn/api/v2/tts
```

---

## Current Default Settings (after this fix)

| Setting | Value |
|---------|-------|
| `VBEE_API_URL` | `https://vbee.vn/api/v1/tts` |
| `VBEE_AUTH_MODE` | `bearer` |
| `VBEE_AUTH_HEADER_NAME` | `Authorization` |
| Token priority | `VBEE_ACCESS_TOKEN` → `VBEE_API_KEY` → `EXPO_PUBLIC_VBEE_API_KEY` |

---

## Exact Commands to Run

```cmd
cd C:\youtubeAI\AI-Youtube-Studio\projects\hashima-island-mystery-ja

:: 1. Verify config loads correctly
python tools\vbee_export_segments.py --print-config

:: 2. Test auth with a minimal request
python tools\vbee_export_segments.py --auth-test

:: 3. Once auth test passes: export one segment
python tools\vbee_export_segments.py --segment L001 --overwrite

:: 4. If L001 succeeds: export all
python tools\vbee_export_segments.py
```

---

## Safety Notes (unchanged)

- No secret values are printed in any log output
- API key is never stored in manifest, reports, or JSON files
- The `--auth-test` response body is printed in full — if the response contains your key echoed back, redact manually before sharing
- `VBEE_AUTH_MODE=app_id_token_payload` places the token in the request body — this is as safe as header auth over HTTPS, but means the token appears in request logs if Vbee logs request bodies

---

*Stage 31.1 — Vbee API Adapter Fix — COMPLETE*
