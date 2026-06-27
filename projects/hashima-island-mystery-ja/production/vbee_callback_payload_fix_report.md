# Vbee callbackUrl Payload Fix Report
## hashima-island-mystery-ja
**Date:** 2026-06-28
**Trigger:** `--auth-test` returned HTTP 400 Validation Failed: `{"callback_url":"\"callbackUrl\" is required"}`.

---

## Problem Identified

| Finding | Detail |
|---------|--------|
| Auth result (prior) | 401 Unauthorized — wrong endpoint |
| Auth result (after adapter fix) | 400 Validation Failed |
| Error message | `{"callback_url": "\"callbackUrl\" is required"}` |
| Meaning | Authentication now works. Request payload is missing a required field. |
| Affected field | `callbackUrl` (camelCase) — must be included in every TTS request |
| API pattern implied | Asynchronous — Vbee processes audio and POSTs the result to `callbackUrl` |

The 400 is not an auth error. It confirms that the Bearer token is accepted. Vbee's API uses an **async callback model**: callers must provide a webhook URL to receive the finished audio. No `callbackUrl` → request rejected before processing.

---

## Changes Made

### 1. `tools/vbee_export_segments.py`

**New config variables (module-level):**
```python
CALLBACK_URL   = _env('VBEE_CALLBACK_URL')
CALLBACK_FIELD = _env('VBEE_CALLBACK_FIELD', default='callbackUrl')
```

**`_build_request()` — payload now includes callback:**
```python
if CALLBACK_URL:
    payload[CALLBACK_FIELD] = CALLBACK_URL
```
`CALLBACK_FIELD` defaults to `callbackUrl` (camelCase as required by Vbee). Set `VBEE_CALLBACK_FIELD=callback_url` only if Vbee docs indicate otherwise.

**`_require_callback_url(context)` — new guard function:**
Called by `run_auth_test()` and `_call_vbee()` before any API call. Aborts with a clear actionable message if `VBEE_CALLBACK_URL` is not set.

**`print_config()` — new callback section:**
```
Callback URL set  : yes / NO ← add VBEE_CALLBACK_URL to .env
Callback URL      : https://example.com/vbee-callback
Callback field    : callbackUrl  (payload key sent to Vbee)
```

**`run_auth_test()` — callback URL shown in output:**
- Aborts before API call if `VBEE_CALLBACK_URL` is not set
- Displays the callback URL in the test header (non-secret)
- Calls `_interpret_test_response()` to explain what the response means

**`_call_vbee()` — async response handling (new return contract):**

| Response type | Detection | Return value |
|--------------|-----------|--------------|
| Direct binary audio | `Content-Type: audio/*` or `octet-stream` | `('audio', bytes)` |
| JSON with `audio_url` | `audio_url` / `url` / `audio_link` / `link` key present | `('audio', bytes)` after download |
| Async job | `request_id` / `task_id` / `job_id` present, or `status` is `pending`/`processing`/`queued` | `('pending', dict)` |
| Error | `success: false` or non-200 | `RuntimeError` raised |

**`_export_segment()` — handles async return:**
```python
kind, result = _call_vbee(...)
if kind == 'audio':
    out_path.write_bytes(result)
    entry['status'] = 'exported'
elif kind == 'pending':
    entry['status'] = 'pending_async_callback'
    _save_pending_job(line_id, filename, rel_path, result)
```
Segment is **not** marked as exported until an actual audio file exists on disk.

**`_save_pending_job()` — new function:**
Appends pending job to `audio/vbee_raw/vbee_pending_jobs.json`. Detects job ID from common field names (`request_id`, `requestId`, `task_id`, `taskId`, `job_id`, `jobId`). Replaces existing entry for same `line_id` to avoid duplicates on retry.

**`_export_with_retry()` — retry scope narrowed:**
Only retries `failed` status. `pending_async_callback` is not retried (it is correct behaviour, not a failure).

**Manifest — new fields:**
```json
{
  "callback_field":           "callbackUrl",
  "callback_url_set":         true,
  "pending_async_segments":   3,
  "status":                   "pending_async"
}
```
Status values: `complete` (all exported), `pending_async` (async jobs, no failures), `partial` (some failed).

### 2. `.env.example`

New variables added:
```
VBEE_CALLBACK_URL=https://example.com/vbee-callback
VBEE_CALLBACK_FIELD=callbackUrl
```

With documentation explaining:
- For auth testing: any valid URL format works (Vbee validates format, not reachability at request time)
- For production: must be a real HTTPS endpoint that can receive POST requests
- Options: ngrok tunnel, cloud function, webhook receiver

### 3. `audio/vbee_raw/vbee_pending_jobs.json`

Stub file created. Populated at runtime when Vbee returns an async job ID.

Schema per job entry:
```json
{
  "line_id":       "L001",
  "filename":      "hashima_L001_hook_01.mp3",
  "output_path":   "audio/vbee_raw/hashima_L001_hook_01.mp3",
  "job_id":        "abc123",
  "job_id_field":  "request_id",
  "callback_url":  "https://your-endpoint.com/vbee-callback",
  "queued_at":     "2026-06-28T12:00:00+00:00",
  "status":        "pending",
  "raw_response":  {}
}
```

---

## Async Export Workflow

```
1. Script POSTs TTS request with callbackUrl in payload
            │
            ▼
2. Vbee validates request → 200 + async job ID
   (no audio in the response body)
            │
            ▼
3. Vbee processes audio on their servers
            │
            ▼
4. When done: Vbee POSTs to callbackUrl
   with JSON containing audio_url or binary audio
            │
            ▼
5. Your callback endpoint downloads audio_url → saves MP3
   OR:  manually check Vbee dashboard, download MP3,
        save to audio/vbee_raw/<filename>
            │
            ▼
6. Run vbee_check_audio_manifest.py to verify
```

**If you don't have a callback server:**
- Export runs, segments get `pending_async_callback` status
- Check Vbee dashboard for completed jobs
- Download MP3s manually and save to `audio/vbee_raw/` with the correct filenames
- Run `python tools/vbee_export_segments.py --segment <id>` to re-check (file exists → skipped = correct)

---

## Callback URL Options

| Option | Use case |
|--------|----------|
| `https://example.com/vbee-callback` | Auth testing only — URL never actually receives a call |
| ngrok (`ngrok http 8080`) | Local webhook receiver for development |
| Cloud Function / Lambda | Production callback handler |
| Vbee dashboard polling | Manual fallback — no callback needed |

For a simple local receiver during development:
```python
# minimal_callback_server.py
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers['Content-Length'])
        data = json.loads(self.rfile.read(length))
        print("Vbee callback received:", json.dumps(data, indent=2))
        self.send_response(200)
        self.end_headers()

HTTPServer(('', 8080), Handler).serve_forever()
```
Then set `VBEE_CALLBACK_URL=http://your-ngrok-url/vbee-callback`.

---

## Diagnosis Procedure (updated)

### Step 1 — Verify config (includes callback URL)
```cmd
cd C:\youtubeAI\AI-Youtube-Studio\projects\hashima-island-mystery-ja
python tools\vbee_export_segments.py --print-config
```
Expected:
```
Callback URL set  : yes
Callback URL      : https://example.com/vbee-callback
Callback field    : callbackUrl
```

### Step 2 — Run auth test (now includes callbackUrl in payload)
```cmd
python tools\vbee_export_segments.py --auth-test
```

Expected outcomes after this fix:

| HTTP result | Meaning |
|-------------|---------|
| 200 + binary audio | Synchronous — audio returned immediately. Export ready. |
| 200 + `audio_url` | Synchronous — script downloads from signed URL. Export ready. |
| 200 + `request_id` / `task_id` | **Async confirmed.** Job queued. Check callbackUrl. |
| 400 `callbackUrl is required` | `VBEE_CALLBACK_URL` is empty — check `.env` |
| 400 other validation | Other payload field mismatch — check response body |
| 401 | Token rejected — auth regressed |

### Step 3 — Export one segment
```cmd
python tools\vbee_export_segments.py --segment L001 --overwrite
```
If status is `pending_async_callback`: check `audio/vbee_raw/vbee_pending_jobs.json` for the job ID.

### Step 4 — When audio is available: verify with manifest checker
```cmd
python tools\vbee_check_audio_manifest.py
```

---

## Safety Notes (unchanged)

- `VBEE_CALLBACK_URL` is a non-secret public URL — it is displayed in logs (intentional)
- No token or API key values appear in any log output, manifest, or report
- The `callbackUrl` in the request payload is logged as-is (URL, not secret)
- Async response JSON is saved to `vbee_pending_jobs.json` — it should not contain secrets, but verify with `raw_response` field before sharing the file

---

*Stage 31.2 — Vbee callbackUrl Payload Fix — COMPLETE*
