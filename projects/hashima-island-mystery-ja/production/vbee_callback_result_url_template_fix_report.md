# Vbee Callback Result URL Template Fix Report
## hashima-island-mystery-ja
**Date:** 2026-06-28
**Trigger:** `--auth-test-fetch` returned error_code 1005 "Request is not found"

---

## Problem Identified

| Finding | Detail |
|---------|--------|
| Old URL called | `GET https://vbee.vn/api/v1/tts/callback-result?request_id=<id>` |
| Vbee response | `{"status":0,"error_code":1005,"error_message":"Request is not found"}` |
| Correct URL (docs) | `GET https://vbee.vn/api/v1/tts/{request_id}/callback-result` |
| Difference | `request_id` must be in the **URL path**, not as a query parameter |

---

## Changes Made

### 1. `tools/vbee_export_segments.py`

**New helper — `_resolve_result_url(request_id)`:**
```python
def _resolve_result_url(request_id: str):
    encoded = urllib.parse.quote(request_id, safe='')
    if '{request_id}' in RESULT_API_URL:
        return RESULT_API_URL.replace('{request_id}', encoded), {}
    return RESULT_API_URL, {RESULT_REQUEST_ID_FIELD: request_id}
```
- If `{request_id}` appears in `VBEE_RESULT_API_URL`: substitute into path (URL-encoded)
- Otherwise: fall back to query parameter (backward compatible with previous default)

**Updated default:**
```python
RESULT_API_URL = _env('VBEE_RESULT_API_URL',
    default='https://vbee.vn/api/v1/tts/{request_id}/callback-result')
```

**`_fetch_result()` — resolved URL is printed, not the template:**
```
[FETCH] GET https://vbee.vn/api/v1/tts/ab850041-fd14-4db8-87e0-dcd3c9cb0011/callback-result  →  HTTP 200
```
The `request_id` is visible in the fetch log — it is not a secret.

**Debug JSON now includes both fields:**
```json
{
  "resolved_url": "https://vbee.vn/api/v1/tts/ab850041-.../callback-result",
  "url_template": "https://vbee.vn/api/v1/tts/{request_id}/callback-result"
}
```

**New response classification — `'not_found'`:**

| `status` | `error_code` | Kind returned | Meaning |
|----------|-------------|---------------|---------|
| 0 | 1005 | `'not_found'` | Request ID not found — wrong URL or too soon |
| 0 | other | `'error'` | Other Vbee error |
| 1 | — | audio / pending / log_only | Success path (unchanged) |

`run_fetch_request()` and `run_auth_test_fetch()` now print `← REQUEST_NOT_FOUND` with diagnosis:
- URL template might be wrong
- Or: submitted too recently, wait a few more seconds

**Renamed kind:** `'audio'` → `'audio_bytes'` (to distinguish from `'audio_url'` clearly).
All callers (`_fetch_and_save`, `run_fetch_request`, `run_auth_test_fetch`) updated.

**`print_config()` — new result API section:**
```
  Result API URL    : https://vbee.vn/api/v1/tts/{request_id}/callback-result  [path template]
  Result method     : GET
```
Shows `[path template]` or `[query param fallback]` so URL mode is always visible.

### 2. `.env.example`

```
VBEE_RESULT_API_URL=https://vbee.vn/api/v1/tts/{request_id}/callback-result
VBEE_RESULT_REQUEST_ID_FIELD=request_id
VBEE_RESULT_METHOD=GET
```

---

## Response Classification Summary

After this fix, `_fetch_result()` returns one of:

| Kind | Meaning | Next action |
|------|---------|-------------|
| `audio_bytes` | Binary audio in response body | Save directly |
| `audio_url` | Audio URL in JSON response | Download URL |
| `pending` | `status=IN_PROGRESS` | Retry in ~30s |
| `not_found` | error_code 1005 | Check URL or wait longer |
| `log_only` | 200 but no audio/URL | Push-only model — need real callbackUrl |
| `error` | Other error | See error body |

---

## Result URL Template Now Used

```
https://vbee.vn/api/v1/tts/{request_id}/callback-result
```

## .env Line Required

Add to `C:\youtubeAI\.env`:
```
VBEE_RESULT_API_URL=https://vbee.vn/api/v1/tts/{request_id}/callback-result
```

(Already the default — only needed if you want to make it explicit or override.)

---

## Exact Commands

### Run auth-test-fetch (full async round-trip):
```cmd
cd C:\youtubeAI\AI-Youtube-Studio\projects\hashima-island-mystery-ja
python tools\vbee_export_segments.py --auth-test-fetch
```

### Submit L001 and fetch result:
```cmd
python tools\vbee_export_segments.py --segment L001 --overwrite
python tools\vbee_export_segments.py --fetch-pending
```

---

*Stage 36 — Vbee Callback Result URL Template Fix — COMPLETE*
