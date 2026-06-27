#!/usr/bin/env python3
"""
Vbee TTS API Export — hashima-island-mystery-ja
Exports narration segments to audio/vbee_raw/ using vbee_segmented_script.json.

Usage:
    python tools/vbee_export_segments.py --print-config
    python tools/vbee_export_segments.py --auth-test
    python tools/vbee_export_segments.py --auth-test-fetch
    python tools/vbee_export_segments.py --fetch-pending
    python tools/vbee_export_segments.py --fetch-request <REQUEST_ID>
    python tools/vbee_export_segments.py --dry-run
    python tools/vbee_export_segments.py --segment L001 --overwrite
    python tools/vbee_export_segments.py
    python tools/vbee_export_segments.py --overwrite

Requirements:
    pip install requests python-dotenv mutagen
"""

import os
import sys
import json
import time
import argparse
import pathlib
from datetime import datetime, timezone

# ── .env loading ──────────────────────────────────────────────────────────────
def _load_env_file():
    """Search upward from script then cwd for a .env file. Silent if dotenv missing."""
    try:
        from dotenv import load_dotenv, find_dotenv
        found = find_dotenv(usecwd=True) or find_dotenv(usecwd=False)
        if found:
            load_dotenv(found, override=False)
            return
        for parent in pathlib.Path(__file__).resolve().parents:
            candidate = parent / '.env'
            if candidate.is_file():
                load_dotenv(candidate, override=False)
                return
    except ImportError:
        pass


_load_env_file()


# ── Config helpers ────────────────────────────────────────────────────────────
def _env(key: str, *fallbacks: str, default: str = None, required: bool = False) -> str:
    """Read env var. Tries key then each fallback in order. Never logs the value."""
    val = os.environ.get(key)
    if not val:
        for fb in fallbacks:
            val = os.environ.get(fb)
            if val:
                break
    if not val:
        val = default
    if required and not val:
        print(f"[ERROR] Required variable {key!r} is not set.", file=sys.stderr)
        print(f"        Add it to .env (see .env.example).", file=sys.stderr)
        sys.exit(1)
    return val or ''


# ── Credentials — loaded once at module level, never printed ──────────────────
# Token priority: VBEE_ACCESS_TOKEN > VBEE_API_KEY > EXPO_PUBLIC_VBEE_API_KEY
_ACCESS_TOKEN = _env('VBEE_ACCESS_TOKEN')
_API_KEY      = _env('VBEE_API_KEY', 'EXPO_PUBLIC_VBEE_API_KEY')
TOKEN         = _ACCESS_TOKEN or _API_KEY

APP_ID        = _env('VBEE_APP_ID', 'EXPO_PUBLIC_VBEE_APP_ID')
VOICE_ID      = _env('VBEE_VOICE_ID', 'EXPO_PUBLIC_VBEE_JA_VOICE_CODE', default='ja-JP-Standard-C')
BASE_SPEED    = float(_env('VBEE_SPEED', default='0.85'))
OUT_FMT       = _env('VBEE_OUTPUT_FORMAT', default='mp3')

# Auth adapter settings
API_URL          = _env('VBEE_API_URL', default='https://vbee.vn/api/v1/tts')
AUTH_MODE        = _env('VBEE_AUTH_MODE', default='bearer').lower().strip()
AUTH_HDR_NAME    = _env('VBEE_AUTH_HEADER_NAME', default='Authorization')

# Callback settings (required by Vbee API)
CALLBACK_URL     = _env('VBEE_CALLBACK_URL')
CALLBACK_FIELD   = _env('VBEE_CALLBACK_FIELD', default='callbackUrl')

# Payload field names — configurable so no code edit is needed if Vbee changes names
TEXT_FIELD   = _env('VBEE_TEXT_FIELD',   default='inputText')
VOICE_FIELD  = _env('VBEE_VOICE_FIELD',  default='voiceCode')
SPEED_FIELD  = _env('VBEE_SPEED_FIELD',  default='speed')
FORMAT_FIELD = _env('VBEE_FORMAT_FIELD', default='audioType')

# Vbee rejects the speed field at /api/v1/tts — disabled by default.
# Set VBEE_INCLUDE_SPEED=true only if a future endpoint or voice accepts it.
INCLUDE_SPEED = _env('VBEE_INCLUDE_SPEED', default='false').lower() == 'true'

# Async result fetcher — polls Vbee for completed jobs by request_id
# URL template: use {request_id} for path substitution (confirmed pattern).
# Fallback: if {request_id} absent, request_id is sent as a query parameter.
RESULT_API_URL          = _env('VBEE_RESULT_API_URL',
                               default='https://vbee.vn/api/v1/tts/{request_id}/callback-result')
RESULT_REQUEST_ID_FIELD = _env('VBEE_RESULT_REQUEST_ID_FIELD', default='request_id')
RESULT_METHOD           = _env('VBEE_RESULT_METHOD', default='GET').upper()

# Maps the camelCase field name Vbee expects → the env var that controls it
# Used to give actionable hints when a 400 names a missing field.
_FIELD_ENV_MAP = {
    'inputText':   ('VBEE_TEXT_FIELD',    TEXT_FIELD),
    'voiceCode':   ('VBEE_VOICE_FIELD',   VOICE_FIELD),
    'speed':       ('VBEE_SPEED_FIELD',   SPEED_FIELD),
    'speed_rate':  ('VBEE_SPEED_FIELD',   SPEED_FIELD),   # confirmed field name from response
    'audioType':   ('VBEE_FORMAT_FIELD',  FORMAT_FIELD),
    'callbackUrl': ('VBEE_CALLBACK_FIELD', CALLBACK_FIELD),
    'app_id':      ('VBEE_APP_ID',        '(credentials)'),
    'token':       ('VBEE_API_KEY',       '(credentials)'),
}

SUPPORTED_AUTH_MODES = ('bearer', 'api_key_header', 'app_id_token_payload')

# ── Paths ─────────────────────────────────────────────────────────────────────
PROJECT_ROOT      = pathlib.Path(__file__).resolve().parent.parent
SCRIPT_JSON       = PROJECT_ROOT / 'voice' / 'vbee_export' / 'vbee_segmented_script.json'
OUT_DIR           = PROJECT_ROOT / 'audio' / 'vbee_raw'
MANIFEST_OUT      = OUT_DIR / 'vbee_export_manifest.json'
PENDING_JOBS_FILE = OUT_DIR / 'vbee_pending_jobs.json'

# ── Speed map ─────────────────────────────────────────────────────────────────
SPEED_MAP = {
    'very_slow': 0.75,
    'slow':      0.80,
    'normal':    0.85,
}


# ── Auth adapter ──────────────────────────────────────────────────────────────
def _build_request(text: str, voice_code: str, speed: float, audio_type: str):
    """Return (headers, payload) for the configured auth mode. Never logs secrets."""
    headers = {'Content-Type': 'application/json'}
    payload = {
        TEXT_FIELD:   text,
        VOICE_FIELD:  voice_code,
        FORMAT_FIELD: audio_type,
    }
    if INCLUDE_SPEED:
        payload[SPEED_FIELD] = speed

    # Always include callbackUrl — required by Vbee API
    if CALLBACK_URL:
        payload[CALLBACK_FIELD] = CALLBACK_URL

    if AUTH_MODE == 'bearer':
        if not TOKEN:
            _abort_no_token('bearer')
        headers['Authorization'] = f'Bearer {TOKEN}'
        if APP_ID:
            payload['app_id'] = APP_ID

    elif AUTH_MODE == 'api_key_header':
        if not TOKEN:
            _abort_no_token('api_key_header')
        headers[AUTH_HDR_NAME] = TOKEN
        if APP_ID:
            payload['app_id'] = APP_ID

    elif AUTH_MODE == 'app_id_token_payload':
        if not APP_ID:
            print("[ERROR] VBEE_APP_ID is required for app_id_token_payload mode.", file=sys.stderr)
            sys.exit(1)
        if not TOKEN:
            _abort_no_token('app_id_token_payload')
        payload['app_id'] = APP_ID
        payload['token']  = TOKEN

    else:
        print(f"[ERROR] Unknown VBEE_AUTH_MODE={AUTH_MODE!r}.", file=sys.stderr)
        print(f"        Supported: {', '.join(SUPPORTED_AUTH_MODES)}", file=sys.stderr)
        sys.exit(1)

    return headers, payload


def _abort_no_token(mode: str):
    print(f"[ERROR] No token for auth mode {mode!r}.", file=sys.stderr)
    print("        Set VBEE_ACCESS_TOKEN or VBEE_API_KEY in .env.", file=sys.stderr)
    sys.exit(1)


def _require_callback_url(context: str = ''):
    """Abort with a clear message if VBEE_CALLBACK_URL is not set."""
    if not CALLBACK_URL:
        print(f"\n[ERROR] VBEE_CALLBACK_URL is not set.{' (' + context + ')' if context else ''}", file=sys.stderr)
        print("        Vbee requires a callbackUrl in every request.", file=sys.stderr)
        print("        For auth testing, any valid URL works:", file=sys.stderr)
        print("          VBEE_CALLBACK_URL=https://example.com/vbee-callback", file=sys.stderr)
        print("        For production export, use a real webhook endpoint.", file=sys.stderr)
        sys.exit(1)


# ── Safe debug print ──────────────────────────────────────────────────────────
def _print_request_debug(voice_code: str, speed: float, text_chars: int):
    """Print safe request metadata. Never prints token or key values."""
    tok_src = ('VBEE_ACCESS_TOKEN' if _ACCESS_TOKEN
               else 'VBEE_API_KEY / EXPO_PUBLIC_VBEE_API_KEY' if _API_KEY
               else 'NOT SET')

    print(f"      [DEBUG] API URL        : {API_URL}")
    print(f"      [DEBUG] auth mode      : {AUTH_MODE}")

    if AUTH_MODE == 'bearer':
        print(f"      [DEBUG] auth header    : Authorization: Bearer ***")
    elif AUTH_MODE == 'api_key_header':
        print(f"      [DEBUG] auth header    : {AUTH_HDR_NAME}: ***")
    elif AUTH_MODE == 'app_id_token_payload':
        print(f"      [DEBUG] auth in body   : app_id + token (payload)")

    print(f"      [DEBUG] app_id         : {'set (len=' + str(len(APP_ID)) + ')' if APP_ID else 'NOT SET'}")
    print(f"      [DEBUG] token source   : {tok_src}  len={len(TOKEN) if TOKEN else 0}")
    cb_display = CALLBACK_URL if CALLBACK_URL else 'NOT SET ← required'
    print(f"      [DEBUG] {CALLBACK_FIELD:15}: {cb_display}")
    print(f"      [DEBUG] payload fields : {TEXT_FIELD}  {VOICE_FIELD}  {SPEED_FIELD}  {FORMAT_FIELD}")
    print(f"      [DEBUG] voice          : {voice_code}  speed={speed}  chars={text_chars}")


# ── Safe config print ─────────────────────────────────────────────────────────
def print_config():
    """Print full safe configuration — no token/key values."""
    tok_src = ('VBEE_ACCESS_TOKEN' if _ACCESS_TOKEN
               else 'VBEE_API_KEY / EXPO_PUBLIC_VBEE_API_KEY' if _API_KEY
               else 'NOT SET')

    print(f"\n{'='*64}")
    print(f"Vbee Configuration — hashima-island-mystery-ja")
    print(f"{'='*64}")
    print(f"  API URL           : {API_URL}")
    print(f"  Auth mode         : {AUTH_MODE}")

    if AUTH_MODE == 'bearer':
        print(f"  Auth header       : Authorization: Bearer ***")
    elif AUTH_MODE == 'api_key_header':
        print(f"  Auth header       : {AUTH_HDR_NAME}: ***")
    elif AUTH_MODE == 'app_id_token_payload':
        print(f"  Auth in body      : app_id + token (payload field)")

    print(f"  APP_ID            : {'set  (len=' + str(len(APP_ID)) + ')' if APP_ID else 'NOT SET'}")
    print(f"  Token source      : {tok_src}")
    print(f"  Token length      : {len(TOKEN) if TOKEN else 0}{' ← not set!' if not TOKEN else ''}")
    print(f"  Access token      : {'set  (len=' + str(len(_ACCESS_TOKEN)) + ')' if _ACCESS_TOKEN else 'not set (using API key)'}")

    cb_set = bool(CALLBACK_URL)
    cb_display = CALLBACK_URL if cb_set else 'NOT SET ← required!'
    print(f"  Callback URL set  : {'yes' if cb_set else 'NO ← add VBEE_CALLBACK_URL to .env'}")
    print(f"  Callback URL      : {cb_display}")
    print(f"  Payload fields    :")
    print(f"    text field      : {TEXT_FIELD:20} (VBEE_TEXT_FIELD)")
    print(f"    voice field     : {VOICE_FIELD:20} (VBEE_VOICE_FIELD)")
    speed_status = f"{SPEED_FIELD} [INCLUDED]" if INCLUDE_SPEED else f"{SPEED_FIELD} [EXCLUDED — Vbee rejects it]"
    print(f"    speed field     : {speed_status:20} (VBEE_SPEED_FIELD / VBEE_INCLUDE_SPEED={'true' if INCLUDE_SPEED else 'false'})")
    print(f"    format field    : {FORMAT_FIELD:20} (VBEE_FORMAT_FIELD)")
    print(f"    callback field  : {CALLBACK_FIELD:20} (VBEE_CALLBACK_FIELD)")

    print(f"  Voice ID          : {VOICE_ID}")
    print(f"  Output format     : {OUT_FMT}")
    print(f"  Base speed        : {BASE_SPEED}")
    print(f"  Output dir        : {OUT_DIR}")

    url_mode = 'path template' if '{request_id}' in RESULT_API_URL else 'query param fallback'
    print(f"  Result API URL    : {RESULT_API_URL}  [{url_mode}]")
    print(f"  Result method     : {RESULT_METHOD}")

    seg_exists = SCRIPT_JSON.exists()
    print(f"  Segment JSON      : {SCRIPT_JSON.relative_to(PROJECT_ROOT)}  ({'exists' if seg_exists else 'MISSING'})")

    issues = []
    if not TOKEN:
        issues.append("Set VBEE_ACCESS_TOKEN or VBEE_API_KEY in .env")
    if not CALLBACK_URL:
        issues.append("Set VBEE_CALLBACK_URL in .env  (any valid URL works for testing)")
    if not APP_ID and AUTH_MODE == 'app_id_token_payload':
        issues.append("Set VBEE_APP_ID in .env (required for app_id_token_payload mode)")
    if AUTH_MODE not in SUPPORTED_AUTH_MODES:
        issues.append(f"VBEE_AUTH_MODE={AUTH_MODE!r} not recognised — use: {', '.join(SUPPORTED_AUTH_MODES)}")

    if issues:
        print()
        for issue in issues:
            print(f"  [ACTION NEEDED] {issue}")

    print(f"{'='*64}\n")


# ── Auth test ─────────────────────────────────────────────────────────────────
def run_auth_test():
    """Send a minimal test request and print the full response for diagnosis."""
    try:
        import requests as _req
    except ImportError:
        print("[ERROR] 'requests' not installed. Run: pip install requests", file=sys.stderr)
        sys.exit(1)

    _require_callback_url('auth-test')

    test_text = 'テストです。'
    print(f"\n{'='*64}")
    print(f"Auth Test — {API_URL}")
    print(f"{'='*64}")
    print(f"  Test text       : {test_text!r}  ({len(test_text)} chars)")
    print(f"  {CALLBACK_FIELD:15} : {CALLBACK_URL}")
    print()

    headers, payload = _build_request(test_text, VOICE_ID, BASE_SPEED, OUT_FMT)
    _print_request_debug(VOICE_ID, BASE_SPEED, len(test_text))
    print()

    try:
        resp = _req.post(API_URL, headers=headers, json=payload, timeout=30)
        print(f"  HTTP status     : {resp.status_code}")
        print(f"  Content-Type    : {resp.headers.get('Content-Type', '(none)')}")

        ct = resp.headers.get('Content-Type', '')

        if 'audio/' in ct or 'octet-stream' in ct:
            print(f"  Body            : <binary audio — {len(resp.content):,} bytes>")
            print()
            print("  ← RESULT: Direct audio returned. No callback needed. Export ready.")

        else:
            raw = resp.text[:1200]
            print(f"  Raw body        : {raw}")
            try:
                parsed = resp.json()
                print(f"  Parsed JSON:")
                print(json.dumps(parsed, ensure_ascii=False, indent=6))
                _interpret_test_response(resp.status_code, parsed, ct)
            except Exception:
                pass

    except Exception as exc:
        print(f"  [EXCEPTION] {type(exc).__name__}: {exc}", file=sys.stderr)

    print(f"{'='*64}\n")


def _diagnose_400(data: dict):
    """Parse a 400 response body and give actionable field-level hints."""
    import re

    # Vbee 400 format: {"status":0,"error_code":400,"error_message":"...","details":[{field:msg}]}
    # Validation errors live in 'details', not at the top level.
    details = data.get('details') or data.get('errors') or data.get('validation_errors')

    if isinstance(details, list):
        error_items = {}
        for item in details:
            if isinstance(item, dict):
                error_items.update(item)
    elif isinstance(details, dict):
        error_items = details
    else:
        # Fallback: top-level keys minus known response envelope keys
        _ENVELOPE = {'status', 'error_code', 'error_message', 'details', 'errors',
                     'message', 'success', 'code', 'data', 'result'}
        error_items = {k: v for k, v in data.items() if k not in _ENVELOPE}

    if not error_items:
        print(f"    Raw 400 body    : {data}")
        print(f"    → Run --print-config to confirm payload field names.")
        return

    for field_key, error_msg in error_items.items():
        msg_str = str(error_msg)
        is_not_allowed = 'not allowed' in msg_str.lower()
        is_required    = 'required'    in msg_str.lower()

        # Extract camelCase field name from quoted string in message, e.g. '"inputText" is required'
        match = re.search(r'"([A-Za-z_][A-Za-z0-9_]*)"', msg_str)
        expected_field = match.group(1) if match else field_key

        env_info = _FIELD_ENV_MAP.get(expected_field)

        if is_not_allowed:
            print(f"    Rejected field  : {expected_field!r}  — Vbee does not accept this field")
            if env_info:
                env_var, current_val = env_info
                print(f"    Controlled by   : {env_var}={current_val!r}")
            print(f"    → The field has been removed from the default payload.")
            print(f"      To re-enable: set VBEE_INCLUDE_{expected_field.upper()}=true in .env")
        elif is_required:
            if env_info:
                env_var, current_val = env_info
                print(f"    Missing field   : {expected_field!r}")
                print(f"    Env var         : {env_var}={current_val!r}  (current value)")
                print(f"    → Field is mapped. Verify .env has this variable, then re-run --auth-test.")
            else:
                print(f"    Missing field   : {expected_field!r}  (not in current payload map)")
                print(f"    → Add to _build_request(). Suggested env var:")
                print(f"      VBEE_{expected_field.upper()}_FIELD={expected_field}")
        else:
            print(f"    Field issue     : {expected_field!r} — {msg_str}")

        print()


def _interpret_test_response(status: int, data: dict, ct: str):
    """Print a human-readable interpretation of the auth test response."""
    print()
    if status == 200:
        # Unwrap Vbee's result wrapper: {"status": 1, "result": {...}}
        inner = data.get('result') if isinstance(data.get('result'), dict) else None
        effective = inner if inner else data

        audio_url = _find_audio_url(effective) or _find_audio_url(data)
        job_id    = _extract_job_id(data)  # searches both levels
        inner_status = str(effective.get('status', '')).lower()

        if audio_url:
            print(f"  ← RESULT: 200 with audio_url — synchronous. Export ready.")
            print(f"    audio_url: {audio_url[:80]}")
        elif job_id or inner_status in ('in_progress', 'pending', 'processing', 'queued'):
            jid, jfield = job_id if job_id else ('unknown', 'unknown')
            print(f"  ← RESULT: 200 — ASYNC job accepted.")
            print(f"    Job field : {jfield}")
            print(f"    Job ID    : {jid}")
            print(f"    Status    : {effective.get('status', 'unknown')}")
            print(f"    Vbee is processing audio — result must be fetched by request_id.")
            print(f"    Next step : python tools\\vbee_export_segments.py --auth-test-fetch")
            if 'speed_rate' in effective:
                print()
                print(f"    [NOTE] Response includes 'speed_rate'={effective['speed_rate']!r}")
                print(f"           Vbee uses 'speed_rate' for speed control (not 'speed').")
                print(f"           To enable: VBEE_SPEED_FIELD=speed_rate  VBEE_INCLUDE_SPEED=true")
        else:
            print(f"  ← RESULT: 200 but no audio_url or job_id found.")
            print(f"    Top-level keys : {list(data.keys())}")
            if inner:
                print(f"    Result keys    : {list(inner.keys())}")
            print(f"    Check parsed JSON above for audio delivery mechanism.")
    elif status == 400:
        print(f"  ← RESULT: 400 Validation Failed — wrong or missing payload field(s).")
        _diagnose_400(data)
    elif status == 401:
        print(f"  ← RESULT: 401 Token rejected. Check VBEE_API_KEY / auth mode.")
    elif status == 403:
        print(f"  ← RESULT: 403 Forbidden. Check VBEE_APP_ID / token permissions.")
    else:
        print(f"  ← RESULT: HTTP {status}. See body above.")


# ── Duration detection ────────────────────────────────────────────────────────
def _detect_duration(path: pathlib.Path):
    try:
        ext = path.suffix.lower()
        if ext == '.mp3':
            from mutagen.mp3 import MP3
            return round(MP3(str(path)).info.length, 2)
        if ext == '.wav':
            from mutagen.wave import WAVE
            return round(WAVE(str(path)).info.length, 2)
        if ext in ('.m4a', '.aac'):
            from mutagen.mp4 import MP4
            return round(MP4(str(path)).info.length, 2)
    except Exception:
        pass
    return None


# ── Job ID extraction ─────────────────────────────────────────────────────────
def _extract_job_id(data: dict):
    """Return (job_id_str, field_name) or None. Searches top-level and nested 'result'."""
    candidates = [data]
    if isinstance(data.get('result'), dict):
        candidates.append(data['result'])
    for d in candidates:
        for field in ('request_id', 'requestId', 'task_id', 'taskId', 'job_id', 'jobId'):
            val = d.get(field)
            if val and isinstance(val, (str, int)) and str(val).strip():
                return (str(val), field)
    return None


# ── Pending jobs manifest ─────────────────────────────────────────────────────
def _save_pending_job(line_id: str, filename: str, output_path: str, response_data: dict):
    """Append or update a pending async job in vbee_pending_jobs.json."""
    job_id_result = _extract_job_id(response_data)
    job_id   = job_id_result[0] if job_id_result else None
    job_field = job_id_result[1] if job_id_result else None

    entry = {
        'line_id':       line_id,
        'filename':      filename,
        'output_path':   output_path,
        'job_id':        job_id,
        'job_id_field':  job_field,
        'callback_url':  CALLBACK_URL,
        'queued_at':     datetime.now(timezone.utc).isoformat(),
        'status':        'pending',
        'raw_response':  response_data,
    }

    # Load or initialise
    if PENDING_JOBS_FILE.exists():
        try:
            existing = json.loads(PENDING_JOBS_FILE.read_text(encoding='utf-8'))
        except Exception:
            existing = {'project_id': 'hashima-island-mystery-ja', 'jobs': []}
    else:
        existing = {'project_id': 'hashima-island-mystery-ja', 'jobs': []}

    # Replace existing entry for same line_id
    existing['jobs'] = [j for j in existing.get('jobs', []) if j.get('line_id') != line_id]
    existing['jobs'].append(entry)
    existing['updated_at'] = datetime.now(timezone.utc).isoformat()
    existing['pending_count'] = len(existing['jobs'])

    PENDING_JOBS_FILE.write_text(
        json.dumps(existing, ensure_ascii=False, indent=2),
        encoding='utf-8'
    )

    id_display = job_id if job_id else 'no ID in response'
    print(f"    [PENDING] Async job queued.  ID={id_display}  → vbee_pending_jobs.json")
    print(f"    [PENDING] Vbee will POST audio URL to: {CALLBACK_URL}")


# ── Audio URL finder (checks multiple possible field names) ───────────────────
def _find_audio_url(d: dict):
    """Return the first audio URL found in dict d, checking all known field names."""
    for key in ('audio_url', 'audioUrl', 'file_url', 'fileUrl', 'url', 'audio_link', 'link'):
        val = d.get(key)
        if val and isinstance(val, str) and val.startswith('http'):
            return val
    # One level deeper — result.payload or result.result
    for sub in ('payload', 'result', 'data'):
        nested = d.get(sub)
        if isinstance(nested, dict):
            for key in ('audio_url', 'audioUrl', 'audio_link', 'audioLink',
                        'file_url', 'fileUrl', 'url'):
                val = nested.get(key)
                if val and isinstance(val, str) and val.startswith('http'):
                    return val
    return None


# ── Vbee API call ─────────────────────────────────────────────────────────────
def _call_vbee(text: str, voice_code: str, speed: float, audio_type: str):
    """POST to Vbee. Returns ('audio', bytes) or ('pending', dict). Never logs secrets."""
    try:
        import requests
    except ImportError:
        print("[ERROR] 'requests' not installed. Run: pip install requests", file=sys.stderr)
        sys.exit(1)

    _require_callback_url('export')

    headers, payload = _build_request(text, voice_code, speed, audio_type)
    _print_request_debug(voice_code, speed, len(text))

    resp = requests.post(API_URL, headers=headers, json=payload, timeout=90)

    if resp.status_code == 401:
        _handle_http_error(401, resp)
        raise RuntimeError("401 Unauthorized")
    if resp.status_code == 403:
        _handle_http_error(403, resp)
        raise RuntimeError("403 Forbidden")
    if not resp.ok:
        body_hint = ''
        try:
            body_hint = f"  body: {resp.json()}"
        except Exception:
            body_hint = f"  body: {resp.text[:200]}"
        raise RuntimeError(f"HTTP {resp.status_code}{body_hint}")

    ct = resp.headers.get('Content-Type', '')

    # ── Pattern A: direct binary audio ────────────────────────────────────────
    if 'audio/' in ct or 'octet-stream' in ct:
        print(f"      [DEBUG] direct binary audio received ({len(resp.content):,} bytes)")
        return ('audio', resp.content)

    # ── Pattern B: JSON response ───────────────────────────────────────────────
    try:
        data = resp.json()
    except ValueError:
        raise RuntimeError(
            f"Non-JSON, non-audio response (Content-Type={ct!r}). "
            f"Body: {resp.text[:300]}"
        )

    print(f"      [DEBUG] JSON response keys: {list(data.keys())}")

    # Vbee outer envelope: {"status": 1, "result": {...}}
    # status=0 is error; status=1 is success
    outer_status = data.get('status')
    if outer_status == 0:
        raise RuntimeError(
            f"Vbee error: {data.get('error_message') or data.get('error') or data}"
        )
    if data.get('success') is False:
        raise RuntimeError(
            f"Vbee error: {data.get('message') or data.get('error') or data}"
        )

    # Unwrap 'result' wrapper — job fields live inside result, not at top level
    inner = data.get('result') if isinstance(data.get('result'), dict) else None
    effective = inner if inner else data

    # Immediate audio URL — check both wrapper levels
    audio_url = _find_audio_url(effective) or _find_audio_url(data)
    if audio_url:
        print(f"      [DEBUG] downloading audio from signed URL")
        dl = requests.get(audio_url, timeout=90)
        dl.raise_for_status()
        return ('audio', dl.content)

    # Async job — request_id in result, status=IN_PROGRESS
    job_id_result = _extract_job_id(data)  # searches both top-level and nested result
    inner_status  = str(effective.get('status', '')).lower()
    is_async = (
        job_id_result is not None
        or inner_status in ('in_progress', 'pending', 'processing', 'queued', 'submitted', 'accepted')
        or outer_status == 1
    )

    if is_async:
        jid = job_id_result[0] if job_id_result else 'unknown'
        print(f"      [DEBUG] async job accepted — job_id={jid}  status={inner_status or outer_status}")
        return ('pending', data)

    raise RuntimeError(
        f"Response OK but no audio_url and no recognisable job ID. "
        f"Keys: {list(data.keys())} / result: {list(effective.keys()) if inner else 'n/a'}. "
        f"Body: {json.dumps(data, ensure_ascii=False)[:300]}"
    )


def _handle_http_error(code: int, resp):
    print(f"\n      [ERROR] HTTP {code} from Vbee.", file=sys.stderr)
    if code == 401:
        print(f"        → Token rejected.  auth_mode={AUTH_MODE}  url={API_URL}", file=sys.stderr)
    elif code == 403:
        print(f"        → Forbidden. Check APP_ID / token scope.", file=sys.stderr)
    try:
        body = resp.json()
        print(f"        → Body: {json.dumps(body, ensure_ascii=False)[:400]}", file=sys.stderr)
    except Exception:
        if resp.text:
            print(f"        → Body: {resp.text[:400]}", file=sys.stderr)
    print("        Run: python tools\\vbee_export_segments.py --auth-test", file=sys.stderr)


# ── Async result fetcher ──────────────────────────────────────────────────────
def _resolve_result_url(request_id: str):
    """
    Return (resolved_url, extra_params) for the result API call.
    If RESULT_API_URL contains {request_id}, substitute it in the path.
    Otherwise fall back to sending request_id as a query parameter.
    request_id is URL-safe (UUID hex + dashes) but we encode defensively.
    """
    import urllib.parse
    encoded = urllib.parse.quote(request_id, safe='')
    if '{request_id}' in RESULT_API_URL:
        return RESULT_API_URL.replace('{request_id}', encoded), {}
    return RESULT_API_URL, {RESULT_REQUEST_ID_FIELD: request_id}


def _fetch_result(request_id: str, save_debug: bool = False):
    """
    Call Vbee's callback-result endpoint for one request_id.
    Returns (kind, data):
      'audio_bytes'  → binary audio content (bytes)
      'audio_url'    → audio URL string (caller must download)
      'pending'      → still IN_PROGRESS
      'log_only'     → 200 response but no audio URL (push-only callback model)
      'not_found'    → error_code 1005 (request not found / too soon)
      'error'        → other error
    Never logs secrets.
    """
    try:
        import requests
    except ImportError:
        print("[ERROR] 'requests' not installed. Run: pip install requests", file=sys.stderr)
        sys.exit(1)

    resolved_url, extra_params = _resolve_result_url(request_id)
    auth_hdr = {}
    if TOKEN:
        auth_hdr['Authorization'] = f'Bearer {TOKEN}'

    try:
        if RESULT_METHOD == 'GET':
            resp = requests.get(resolved_url, params=extra_params or None,
                                headers=auth_hdr, timeout=30)
        else:
            body = {RESULT_REQUEST_ID_FIELD: request_id}
            body.update(extra_params)
            resp = requests.post(resolved_url, json=body, headers=auth_hdr, timeout=30)
    except Exception as exc:
        return ('error', {'exception': str(exc)})

    print(f"    [FETCH] {RESULT_METHOD} {resolved_url}  →  HTTP {resp.status_code}")

    if save_debug:
        debug_dir = OUT_DIR / 'debug'
        debug_dir.mkdir(parents=True, exist_ok=True)
        debug_file = debug_dir / f'request_{request_id}.json'
        try:
            resp_body = (resp.json() if 'json' in resp.headers.get('Content-Type', '')
                         else resp.text[:2000])
            debug_payload = {
                'fetched_at':     datetime.now(timezone.utc).isoformat(),
                'request_id':     request_id,
                'resolved_url':   resolved_url,
                'url_template':   RESULT_API_URL,
                'http_status':    resp.status_code,
                'response':       resp_body,
            }
            debug_file.write_text(
                json.dumps(debug_payload, ensure_ascii=False, indent=2),
                encoding='utf-8'
            )
            print(f"    [FETCH] Debug saved → {debug_file.relative_to(PROJECT_ROOT)}")
        except Exception:
            pass

    ct = resp.headers.get('Content-Type', '')

    # Direct binary audio
    if 'audio/' in ct or 'octet-stream' in ct:
        return ('audio_bytes', resp.content)

    try:
        data = resp.json()
    except ValueError:
        return ('error', {'raw': resp.text[:500], 'http_status': resp.status_code})

    outer_status = data.get('status')
    error_code   = data.get('error_code')

    # ── error_code 1005: Request not found ────────────────────────────────────
    if outer_status == 0 and error_code == 1005:
        return ('not_found', data)

    # ── Other Vbee error ──────────────────────────────────────────────────────
    if outer_status == 0:
        return ('error', data)

    # ── Success envelope: {"status": 1, "result": {...}} ──────────────────────
    inner     = data.get('result') if isinstance(data.get('result'), dict) else None
    effective = inner if inner else data

    # Audio URL — check all known field names at both nesting levels
    audio_url = _find_audio_url(effective) or _find_audio_url(data)
    if audio_url:
        return ('audio_url', audio_url)

    # Still processing
    inner_status = str(effective.get('status', '')).lower()
    if inner_status in ('in_progress', 'pending', 'processing', 'queued', 'submitted'):
        return ('pending', data)

    # 200 / status=1 but no audio URL and not a known in-progress status
    # This is a callback-log-only response (Vbee logged the delivery, audio was pushed to callback)
    return ('log_only', data)


def _fetch_and_save(job: dict, overwrite: bool = False):
    """
    Fetch result for one pending job. Download audio if available.
    Returns updated job entry dict.
    """
    try:
        import requests
    except ImportError:
        return {**job, 'status': 'error', 'fetch_error': 'requests not installed'}

    request_id = job.get('job_id') or job.get('request_id')
    if not request_id:
        return {**job, 'status': 'error', 'fetch_error': 'no request_id in job entry'}

    out_path = PROJECT_ROOT / job['output_path']
    line_id  = job.get('line_id', '?')

    if out_path.exists() and not overwrite:
        print(f"    [SKIP] {line_id}: file already exists — {out_path.name}")
        return {**job, 'status': 'exported', 'skipped_reason': 'file_exists'}

    kind, result = _fetch_result(request_id, save_debug=False)

    if kind == 'audio_bytes':
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_bytes(result)
        size_kb = len(result) / 1024
        print(f"    [OK] {line_id}: saved {out_path.name}  {size_kb:.1f} KB")
        return {**job, 'status': 'exported', 'exported_at': datetime.now(timezone.utc).isoformat()}

    if kind == 'audio_url':
        audio_url = result
        print(f"    [FETCH] downloading audio from URL")
        try:
            import requests as _req
            dl = _req.get(audio_url, timeout=90)
            dl.raise_for_status()
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_bytes(dl.content)
            size_kb = len(dl.content) / 1024
            print(f"    [OK] {line_id}: saved {out_path.name}  {size_kb:.1f} KB")
            return {**job, 'status': 'exported', 'exported_at': datetime.now(timezone.utc).isoformat()}
        except Exception as exc:
            print(f"    [FAIL] {line_id}: download error — {exc}")
            return {**job, 'status': 'error', 'fetch_error': str(exc)}

    if kind == 'pending':
        print(f"    [STILL_PENDING] {line_id}: still IN_PROGRESS — try again later")
        return {**job, 'status': 'pending', 'last_checked': datetime.now(timezone.utc).isoformat()}

    if kind == 'not_found':
        ec = result.get('error_code', '?')
        msg = result.get('error_message', '')
        print(f"    [NOT_FOUND] {line_id}: error_code={ec} — {msg}")
        print(f"      → Check URL template is correct or wait longer before fetching.")
        print(f"      → URL template: {RESULT_API_URL}")
        return {**job, 'status': 'not_found', 'last_checked': datetime.now(timezone.utc).isoformat()}

    if kind == 'log_only':
        print(f"    [LOG_ONLY] {line_id}: response has no audio URL")
        print(f"      Keys: {list(result.keys())}")
        print(f"      Vbee may use push-only delivery — audio goes to VBEE_CALLBACK_URL.")
        return {**job, 'status': 'callback_log_only', 'log_response': result}

    # kind == 'error'
    print(f"    [FAIL] {line_id}: fetch error — {result}")
    return {**job, 'status': 'error', 'fetch_error': str(result)}


def run_fetch_pending(overwrite: bool = False):
    """Load vbee_pending_jobs.json, fetch result for each, save audio if available."""
    if not PENDING_JOBS_FILE.exists():
        print(f"[INFO] No pending jobs file at {PENDING_JOBS_FILE}")
        return

    data = json.loads(PENDING_JOBS_FILE.read_text(encoding='utf-8'))
    jobs = data.get('jobs', [])

    if not jobs:
        print("[INFO] No pending jobs to fetch.")
        return

    print(f"\n{'='*64}")
    print(f"Fetch Pending — {len(jobs)} job(s)")
    print(f"  Result API : {RESULT_API_URL}")
    print(f"{'='*64}\n")

    updated_jobs = []
    for job in jobs:
        print(f"  [{job.get('line_id','?')}]  request_id={job.get('job_id','?')}")
        updated = _fetch_and_save(job, overwrite=overwrite)
        updated_jobs.append(updated)

    # Keep only still-pending jobs in the file
    still_pending = [j for j in updated_jobs if j.get('status') not in ('exported',)]
    data['jobs']          = still_pending
    data['pending_count'] = len(still_pending)
    data['updated_at']    = datetime.now(timezone.utc).isoformat()
    PENDING_JOBS_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding='utf-8'
    )

    exported = sum(1 for j in updated_jobs if j.get('status') == 'exported')
    still    = len(still_pending)
    print(f"\n  Exported now : {exported}")
    print(f"  Still pending: {still}")
    print(f"  Pending file : {PENDING_JOBS_FILE}")

    # Update main manifest if segments were exported
    if exported > 0 and MANIFEST_OUT.exists():
        _patch_manifest_after_fetch(updated_jobs)


def run_fetch_request(request_id: str):
    """Fetch one request_id, print safe result, save debug JSON."""
    print(f"\n{'='*64}")
    print(f"Fetch Request — {request_id}")
    print(f"  Result API : {RESULT_API_URL}")
    print(f"{'='*64}\n")

    kind, result = _fetch_result(request_id, save_debug=True)
    print(f"  Kind       : {kind}")

    if kind == 'audio_bytes':
        print(f"  ← AUDIO_AVAILABLE: binary audio {len(result):,} bytes")
        print(f"    Use --fetch-pending to save to the correct output path.")
    elif kind == 'audio_url':
        print(f"  ← AUDIO_AVAILABLE: audio_url = {result}")
    elif kind == 'pending':
        inner = result.get('result') if isinstance(result.get('result'), dict) else result
        print(f"  ← STILL_PENDING: status={inner.get('status', '?')}  retry later")
    elif kind == 'not_found':
        ec  = result.get('error_code', '?')
        msg = result.get('error_message', '')
        print(f"  ← REQUEST_NOT_FOUND: error_code={ec}  {msg}")
        print(f"    Possible causes:")
        print(f"      1. Request ID not yet registered — wait a few seconds and retry")
        print(f"      2. URL template wrong — current: {RESULT_API_URL}")
        print(f"         Set VBEE_RESULT_API_URL in .env if Vbee uses a different path")
    elif kind == 'log_only':
        print(f"  ← LOG_ONLY: callback log received — no audio URL in response")
        print(f"    Keys: {list(result.keys())}")
        print(f"    Vbee may use push-only delivery to VBEE_CALLBACK_URL.")
    else:
        print(f"  ← ERROR: {result}")

    debug_file = OUT_DIR / 'debug' / f'request_{request_id}.json'
    if debug_file.exists():
        print(f"\n  Debug  : {debug_file.relative_to(PROJECT_ROOT)}")
    print(f"{'='*64}\n")


def run_auth_test_fetch():
    """Submit a tiny test job, wait 5s, fetch the result once, print outcome."""
    try:
        import requests as _req
    except ImportError:
        print("[ERROR] 'requests' not installed. Run: pip install requests", file=sys.stderr)
        sys.exit(1)

    _require_callback_url('auth-test-fetch')

    test_text = 'テストです。'
    print(f"\n{'='*64}")
    print(f"Auth Test + Fetch — {API_URL}")
    print(f"{'='*64}")
    print(f"  Step 1: Submit TTS job  ({test_text!r})")

    headers, payload = _build_request(test_text, VOICE_ID, BASE_SPEED, OUT_FMT)
    try:
        resp = _req.post(API_URL, headers=headers, json=payload, timeout=30)
    except Exception as exc:
        print(f"  [ERROR] Submit failed: {exc}", file=sys.stderr)
        return

    print(f"  Submit HTTP : {resp.status_code}")
    if not resp.ok:
        print(f"  Submit body : {resp.text[:300]}")
        return

    try:
        submit_data = resp.json()
    except ValueError:
        print(f"  Submit body : <non-JSON> {resp.text[:200]}")
        return

    job_id_result = _extract_job_id(submit_data)
    if not job_id_result:
        print(f"  [WARN] No request_id in submit response. Keys: {list(submit_data.keys())}")
        inner = submit_data.get('result')
        if isinstance(inner, dict):
            print(f"         Result keys: {list(inner.keys())}")
        return

    request_id, id_field = job_id_result
    print(f"  request_id  : {request_id}  (field: {id_field})")

    print(f"\n  Step 2: Wait 5s for Vbee to process...")
    time.sleep(5)

    print(f"\n  Step 3: Fetch result for {request_id}")
    kind, result = _fetch_result(request_id, save_debug=True)

    print(f"\n  Fetch kind  : {kind}")
    if kind == 'audio_bytes':
        print(f"  ← AUDIO_AVAILABLE: binary audio ({len(result):,} bytes). Export ready.")
    elif kind == 'audio_url':
        print(f"  ← AUDIO_AVAILABLE: URL received: {result[:80]}")
        print(f"    Run: python tools\\vbee_export_segments.py --fetch-pending")
    elif kind == 'pending':
        inner = result.get('result') if isinstance(result.get('result'), dict) else result
        print(f"  ← STILL_PENDING after 5s. Status: {inner.get('status', '?')}")
        print(f"    Run --fetch-pending again in ~30s.")
    elif kind == 'not_found':
        ec  = result.get('error_code', '?')
        msg = result.get('error_message', '')
        print(f"  ← REQUEST_NOT_FOUND (error_code={ec}): {msg}")
        print(f"    The request_id was not found. Possible causes:")
        print(f"      1. URL template is wrong — check VBEE_RESULT_API_URL in .env")
        print(f"         Current template: {RESULT_API_URL}")
        print(f"      2. 5s was not enough — try --fetch-request <request_id> manually in 10s")
    elif kind == 'log_only':
        print(f"  ← LOG_ONLY: callback log returned, no audio URL.")
        print(f"    Keys: {list(result.keys())}")
        print(f"    Audio is delivered to VBEE_CALLBACK_URL, not via polling.")
    else:
        print(f"  ← ERROR: {result}")

    debug_file = OUT_DIR / 'debug' / f'request_{request_id}.json'
    if debug_file.exists():
        print(f"\n  Debug saved : {debug_file.relative_to(PROJECT_ROOT)}")
    print(f"{'='*64}\n")


def _patch_manifest_after_fetch(updated_jobs: list):
    """Update vbee_export_manifest.json to mark fetched segments as exported."""
    try:
        manifest = json.loads(MANIFEST_OUT.read_text(encoding='utf-8'))
    except Exception:
        return

    exported_ids = {j['line_id'] for j in updated_jobs if j.get('status') == 'exported'}
    for entry in manifest.get('files', []):
        if entry.get('line_id') in exported_ids:
            entry['status'] = 'exported'

    counts = {'exported': 0, 'skipped': 0, 'pending_async_callback': 0, 'failed': 0}
    for entry in manifest.get('files', []):
        s = entry.get('status', 'failed')
        if s in counts:
            counts[s] += 1
        elif s == 'pending_async_callback':
            counts['pending_async_callback'] += 1

    manifest['exported_segments']      = counts['exported']
    manifest['pending_async_segments'] = counts['pending_async_callback']
    manifest['failed_segments']        = counts['failed']
    manifest['status'] = ('complete' if counts['failed'] == 0 and counts['pending_async_callback'] == 0
                          else 'pending_async' if counts['failed'] == 0 else 'partial')
    manifest['last_fetch_at'] = datetime.now(timezone.utc).isoformat()

    MANIFEST_OUT.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding='utf-8'
    )
    print(f"  Manifest updated: {MANIFEST_OUT.name}")


# ── Export one segment ────────────────────────────────────────────────────────
def _export_segment(seg: dict, overwrite: bool) -> dict:
    line_id  = seg['line_id']
    filename = seg['export_filename']
    out_path = OUT_DIR / filename
    rel_path = str(out_path.relative_to(PROJECT_ROOT)).replace('\\', '/')

    entry = {
        'line_id':             line_id,
        'scene_id':            seg.get('scene_id', ''),
        'section':             seg.get('section', ''),
        'expected_start_time': seg.get('intended_start_time', ''),
        'expected_end_time':   seg.get('intended_end_time', ''),
        'duration_target_sec': seg.get('duration_target_sec'),
        'delivery_mode':       seg.get('delivery_mode', 'normal'),
        'sensitive_content':   seg.get('sensitive_content_flag', False),
        'output_path':         rel_path,
        'filename':            filename,
        'status':              'unknown',
        'duration_sec':        None,
        'async_job_id':        None,
        'error':               None,
    }

    if out_path.exists() and not overwrite:
        print(f"    [SKIP] {filename} (exists — use --overwrite to re-export)")
        entry['status']       = 'skipped'
        entry['duration_sec'] = _detect_duration(out_path)
        return entry

    speed = SPEED_MAP.get(seg.get('delivery_mode', 'normal'), BASE_SPEED)
    text  = seg['text']

    if seg.get('sensitive_content_flag'):
        print(f"    [SENSITIVE] {line_id} — factual delivery only (FIX-M1)")

    try:
        kind, result = _call_vbee(text, VOICE_ID, speed, OUT_FMT)

        if kind == 'audio':
            out_path.write_bytes(result)
            entry['status']       = 'exported'
            entry['duration_sec'] = _detect_duration(out_path)
            size_kb = len(result) / 1024
            dur_str = f"{entry['duration_sec']}s" if entry['duration_sec'] else "duration unknown"
            print(f"    [OK] {filename}  {size_kb:.1f} KB  {dur_str}")

        elif kind == 'pending':
            job_id_result = _extract_job_id(result)
            entry['status']       = 'pending_async_callback'
            entry['async_job_id'] = job_id_result[0] if job_id_result else None
            _save_pending_job(line_id, filename, rel_path, result)

    except Exception as exc:
        entry['status'] = 'failed'
        entry['error']  = str(exc)
        print(f"    [FAIL] {line_id}: {exc}")

    return entry


# ── Retry wrapper ─────────────────────────────────────────────────────────────
def _export_with_retry(seg: dict, overwrite: bool, retries: int = 2) -> dict:
    entry = _export_segment(seg, overwrite)
    # Only retry hard failures — not pending (async) or skipped
    if entry['status'] not in ('failed',):
        return entry
    for attempt in range(1, retries + 1):
        wait = 3 * attempt
        print(f"    [RETRY {attempt}/{retries}] waiting {wait}s...")
        time.sleep(wait)
        entry = _export_segment(seg, overwrite=True)
        if entry['status'] != 'failed':
            break
    return entry


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description='Vbee TTS export — hashima-island-mystery-ja'
    )
    parser.add_argument('--print-config',    action='store_true',
                        help='Print safe configuration summary and exit')
    parser.add_argument('--auth-test',       action='store_true',
                        help='Send one test request and print full response')
    parser.add_argument('--auth-test-fetch', action='store_true',
                        help='Submit test job, wait 5s, fetch result once')
    parser.add_argument('--fetch-pending',   action='store_true',
                        help='Fetch results for all jobs in vbee_pending_jobs.json')
    parser.add_argument('--fetch-request',   type=str, metavar='REQUEST_ID',
                        help='Fetch and print result for one request_id')
    parser.add_argument('--overwrite',       action='store_true',
                        help='Re-export or re-download files that already exist')
    parser.add_argument('--segment',         type=str, metavar='LINE_ID',
                        help='Export only one segment (e.g. --segment L001)')
    parser.add_argument('--dry-run',         action='store_true',
                        help='List segments without calling the API')
    parser.add_argument('--no-retry',        action='store_true',
                        help='Disable automatic retry on API failure')
    args = parser.parse_args()

    if args.print_config:
        print_config()
        return

    if args.auth_test:
        run_auth_test()
        return

    if args.auth_test_fetch:
        run_auth_test_fetch()
        return

    if args.fetch_pending:
        run_fetch_pending(overwrite=args.overwrite)
        return

    if args.fetch_request:
        run_fetch_request(args.fetch_request)
        return

    # ── Load segments ─────────────────────────────────────────────────────────
    if not SCRIPT_JSON.exists():
        print(f"[ERROR] Segment JSON not found: {SCRIPT_JSON}", file=sys.stderr)
        sys.exit(1)

    with SCRIPT_JSON.open(encoding='utf-8') as f:
        script_data = json.load(f)

    all_segments = script_data.get('segments', [])

    if args.segment:
        segments = [s for s in all_segments if s.get('line_id') == args.segment]
        if not segments:
            avail = [s.get('line_id') for s in all_segments]
            print(f"[ERROR] No segment with line_id={args.segment!r}", file=sys.stderr)
            print(f"        Available: {avail}", file=sys.stderr)
            sys.exit(1)
    else:
        segments = all_segments

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*64}")
    print(f"Vbee TTS Export — hashima-island-mystery-ja")
    print(f"  API URL      : {API_URL}")
    print(f"  Auth mode    : {AUTH_MODE}")
    print(f"  Callback set : {'yes (' + CALLBACK_URL[:50] + ('...' if len(CALLBACK_URL) > 50 else '') + ')' if CALLBACK_URL else 'NO ← add VBEE_CALLBACK_URL to .env'}")
    print(f"  Voice        : {VOICE_ID}  Format: {OUT_FMT}  Base speed: {BASE_SPEED}")
    print(f"  Segments     : {len(segments)}  Output: {OUT_DIR}")
    print(f"{'='*64}\n")

    if args.dry_run:
        print("DRY RUN — no API calls:\n")
        for seg in segments:
            speed = SPEED_MAP.get(seg.get('delivery_mode', 'normal'), BASE_SPEED)
            flag  = ' [SENSITIVE]' if seg.get('sensitive_content_flag') else ''
            print(f"  {seg['line_id']:6}  {seg.get('delivery_mode','normal'):10}  "
                  f"speed={speed}  {seg['export_filename']}{flag}")
        print(f"\n{len(segments)} segments listed. No API calls made.")
        return

    # ── Export loop ───────────────────────────────────────────────────────────
    results   = []
    exported  = skipped = failed = pending = 0
    retries   = 0 if args.no_retry else 2

    for i, seg in enumerate(segments, 1):
        line_id = seg.get('line_id', f'seg{i}')
        print(f"[{i:02d}/{len(segments):02d}] {line_id}  {seg.get('section','')}  "
              f"{seg.get('intended_start_time','?')}-{seg.get('intended_end_time','?')}")

        entry = _export_with_retry(seg, overwrite=args.overwrite, retries=retries)
        results.append(entry)

        if   entry['status'] == 'exported':               exported += 1
        elif entry['status'] == 'skipped':                skipped  += 1
        elif entry['status'] == 'pending_async_callback': pending  += 1
        else:                                             failed   += 1

        if i < len(segments) and entry['status'] == 'exported':
            time.sleep(0.5)

    # ── Write manifest ────────────────────────────────────────────────────────
    all_done   = (failed == 0 and pending == 0)
    has_async  = pending > 0
    manifest_status = ('complete' if all_done
                       else 'pending_async' if has_async and failed == 0
                       else 'partial')

    manifest = {
        'generated_at':             datetime.now(timezone.utc).isoformat(),
        'status':                   manifest_status,
        'project_id':               'hashima-island-mystery-ja',
        'api_url':                  API_URL,
        'auth_mode':                AUTH_MODE,
        'callback_field':           CALLBACK_FIELD,
        'callback_url_set':         bool(CALLBACK_URL),
        'voice_id':                 VOICE_ID,
        'speed_base':               BASE_SPEED,
        'output_format':            OUT_FMT,
        'total_segments':           len(segments),
        'exported_segments':        exported,
        'skipped_segments':         skipped,
        'pending_async_segments':   pending,
        'failed_segments':          failed,
        'files':                    results,
    }

    MANIFEST_OUT.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding='utf-8'
    )

    print(f"\n{'='*64}")
    print(f"  Exported       : {exported}")
    print(f"  Skipped        : {skipped}")
    print(f"  Pending (async): {pending}")
    print(f"  Failed         : {failed}")
    print(f"  Manifest       : {MANIFEST_OUT}")
    if pending > 0:
        print(f"  Pending jobs   : {PENDING_JOBS_FILE}")
    print(f"{'='*64}")

    if pending > 0:
        print(f"\n[INFO] {pending} segment(s) are awaiting async callback from Vbee.")
        print(f"  Vbee will POST the audio URL to: {CALLBACK_URL}")
        print(f"  When audio arrives, download it and save to audio/vbee_raw/<filename>")
        print(f"  Then re-run: python tools\\vbee_export_segments.py --segment <id>  (if file not saved)")

    if failed > 0:
        print(f"\n[WARNING] {failed} segment(s) failed.")
        print("  Diagnose: python tools\\vbee_export_segments.py --auth-test")
        print("  Retry:    python tools\\vbee_export_segments.py --segment <id> --overwrite")

    sys.exit(0 if failed == 0 else 1)


if __name__ == '__main__':
    main()
