# Vbee Async Result Fetcher Report
## hashima-island-mystery-ja
**Date:** 2026-06-28
**Trigger:** `--auth-test` returned HTTP 200 with async job response:
```json
{"status": 1, "result": {"request_id": "ab850041-...", "status": "IN_PROGRESS", ...}}
```

---

## Confirmed API Behaviour

| Finding | Detail |
|---------|--------|
| HTTP status | 200 — success |
| Response structure | `{"status": 1, "result": {...}}` — result nested under `result` key |
| Job field | `result.request_id` — job ID for polling |
| Job status | `result.status = "IN_PROGRESS"` — audio not ready yet |
| Speed field | `result.speed_rate = 1` — confirmed field name is `speed_rate`, not `speed` |
| Delivery model | Fully asynchronous — audio must be fetched by `request_id` |

**Previous code bug fixed:** `_extract_job_id()` only searched top-level keys. Vbee wraps all job fields inside `result`. Updated to search both levels. `_call_vbee()` now unwraps `result` before checking for audio URL or job ID.

---

## Changes Made

### 1. `tools/vbee_export_segments.py` — new config variables

```python
RESULT_API_URL          = _env('VBEE_RESULT_API_URL',
                               default='https://vbee.vn/api/v1/tts/callback-result')
RESULT_REQUEST_ID_FIELD = _env('VBEE_RESULT_REQUEST_ID_FIELD', default='request_id')
RESULT_METHOD           = _env('VBEE_RESULT_METHOD', default='GET').upper()
```

### 2. New functions

| Function | Purpose |
|----------|---------|
| `_find_audio_url(d)` | Checks 8+ field name variants across nested dicts for audio URL |
| `_fetch_result(request_id, save_debug)` | Calls result API, returns `('audio'\|'audio_url'\|'pending'\|'log_only'\|'error', data)` |
| `_fetch_and_save(job, overwrite)` | Fetches + saves audio for one pending job entry |
| `run_fetch_pending(overwrite)` | Processes all jobs in `vbee_pending_jobs.json` |
| `run_fetch_request(request_id)` | Fetches + prints one request_id, saves debug JSON |
| `run_auth_test_fetch()` | Submits test job, waits 5s, fetches result, prints outcome |
| `_patch_manifest_after_fetch(jobs)` | Updates `vbee_export_manifest.json` after fetch exports |

### 3. New CLI commands

| Command | Action |
|---------|--------|
| `--auth-test-fetch` | Submit test job → wait 5s → fetch → print result |
| `--fetch-pending` | Fetch all jobs in `vbee_pending_jobs.json` |
| `--fetch-request <ID>` | Fetch one request_id, save debug JSON |

### 4. `_fetch_result()` response handling

Checks for audio in this order:
1. `Content-Type: audio/*` → binary audio bytes
2. Audio URL at any of: `audio_url`, `audioUrl`, `file_url`, `fileUrl`, `url`, `audio_link`, `link` (top level or nested under `result`, `payload`, `data`)
3. Status `IN_PROGRESS` / `pending` / `processing` → still pending
4. 200 response with no audio URL → `log_only` (callback delivery only, no polling result)

### 5. `audio/vbee_raw/debug/` directory

Debug JSONs saved here by `--fetch-request` and `--auth-test-fetch`. Each file:
```json
{
  "fetched_at":  "2026-06-28T...",
  "request_id":  "ab850041-...",
  "result_url":  "https://vbee.vn/api/v1/tts/callback-result",
  "http_status": 200,
  "response":    {...}
}
```

### 6. `vbee_pending_jobs.json` management

`run_fetch_pending()`:
- Loads all jobs from file
- Calls `_fetch_and_save()` for each
- Removes successfully exported jobs from the file
- Updates `pending_count` and `updated_at`
- Calls `_patch_manifest_after_fetch()` if any exports succeeded

### 7. Bug fixes in response parsing

| Bug | Fix |
|-----|-----|
| `_extract_job_id()` missed `result.request_id` | Now searches both top-level and `data['result']` |
| `_call_vbee()` missed async detection on `{"status":1,"result":{...}}` | Now unwraps `result`, detects `IN_PROGRESS`, `outer_status==1` |
| `_interpret_test_response()` showed "no job_id found" despite 200 async | Now unwraps `result`, shows job ID, status, and next step |

### 8. `speed_rate` discovery

The 200 response contains `result.speed_rate = 1`. This confirms:
- Vbee's internal speed field is `speed_rate`, not `speed`
- `speed` was correctly rejected as an unknown field
- To try speed control: set `VBEE_SPEED_FIELD=speed_rate` and `VBEE_INCLUDE_SPEED=true`
- This is not enabled by default — needs testing to confirm it's accepted as input

`speed_rate` has been added to `_FIELD_ENV_MAP` for diagnostic hints.

---

## Audio Availability Model

```
Script submits job → Vbee returns request_id (IN_PROGRESS)
        │
        ├── Option A: Callback delivery
        │   Vbee POSTs audio URL to VBEE_CALLBACK_URL when done
        │   Run --fetch-pending to check/download
        │
        └── Option B: Polling
            Call VBEE_RESULT_API_URL?request_id=<id> to check status
            Run --fetch-request <id> or --fetch-pending
            If response has audio_url → download
            If response has log_only → Vbee only logs callbacks, polling unsupported
```

---

## .env Lines to Add

```
VBEE_RESULT_API_URL=https://vbee.vn/api/v1/tts/callback-result
VBEE_RESULT_REQUEST_ID_FIELD=request_id
VBEE_RESULT_METHOD=GET
```

These are already the defaults — only needed if the endpoint differs.

---

## Commands

**Async fetcher created:** ✅

**Pending jobs file:** `audio/vbee_raw/vbee_pending_jobs.json`

**Result API URL:** `https://vbee.vn/api/v1/tts/callback-result` (configurable via `VBEE_RESULT_API_URL`)

### Test the full async round-trip:
```cmd
cd C:\youtubeAI\AI-Youtube-Studio\projects\hashima-island-mystery-ja
python tools\vbee_export_segments.py --auth-test-fetch
```

### Export L001 (will be saved as pending, then fetch):
```cmd
python tools\vbee_export_segments.py --segment L001 --overwrite
python tools\vbee_export_segments.py --fetch-pending
```

### Fetch all pending jobs:
```cmd
python tools\vbee_export_segments.py --fetch-pending
```

### Inspect one specific request:
```cmd
python tools\vbee_export_segments.py --fetch-request ab850041-fd14-4db8-87e0-dcd3c9cb0011
```

---

## If `--fetch-pending` Returns `log_only`

The result endpoint may only return a callback delivery log rather than the audio URL itself. This means:
- Vbee's async model is push-only (callback URL receives the audio, polling doesn't return it)
- A real reachable `VBEE_CALLBACK_URL` is required for automated audio delivery
- Manual workaround: download MP3 from Vbee dashboard and save to `audio/vbee_raw/<filename>`

---

*Stage 35 — Vbee Async Result Fetcher — COMPLETE*
