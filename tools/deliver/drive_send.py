#!/usr/bin/env python3
"""Upload a large file to Google Drive (resumable) and send a shareable link to Telegram.

The MCP Drive tool only takes inline content (a 420 MB base64 blob is impossible),
so this uses the Drive API with a one-time OAuth login, then notifies via the
existing japan-news-bot Telegram bot — a *link* message, so the 50 MB bot-file
cap doesn't apply and the file stays full quality on Drive.

Reuses the user's installed-app OAuth client (client_secrets.json). Least-privilege
scope drive.file (the app only ever sees files it created).

One-time auth (interactive browser — run via `! python ...`):
  python tools/deliver/drive_send.py --auth

Upload + notify Telegram:
  python tools/deliver/drive_send.py --upload projects/hashima-island-mystery-ja/export/master/hashima_master_v1.mp4 \
      --caption "端島（軍艦島）の謎" --notify
"""
from __future__ import annotations
import argparse, pickle, sys
from pathlib import Path

HERE = Path(__file__).resolve()
DEFAULT_CLIENT = Path(r"C:/Users/thanh/japan-news-bot/client_secrets.json")
DEFAULT_TG_ENV = Path(r"C:/Users/thanh/japan-news-bot/.env")
TOKEN = HERE.parent / "drive_token.pickle"
SCOPES = ["https://www.googleapis.com/auth/drive.file"]


def _load_env(path: Path) -> dict:
    env = {}
    if path.is_file():
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def _creds(client_secret: Path):
    from google.auth.transport.requests import Request
    from google_auth_oauthlib.flow import InstalledAppFlow
    creds = pickle.loads(TOKEN.read_bytes()) if TOKEN.exists() else None
    if creds and creds.valid:
        return creds
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        TOKEN.write_bytes(pickle.dumps(creds))
        return creds
    if not client_secret.is_file():
        sys.exit(f"[ERROR] OAuth client not found: {client_secret}")
    flow = InstalledAppFlow.from_client_secrets_file(str(client_secret), SCOPES)
    creds = flow.run_local_server(port=0)
    TOKEN.write_bytes(pickle.dumps(creds))
    return creds


def cmd_auth(client_secret: Path) -> int:
    _creds(client_secret)
    print(f"Authorized OK - token saved -> {TOKEN}")
    print("Future --upload runs are headless (refresh token stored).")
    return 0


def cmd_upload(file: str, caption: str | None, notify: bool,
               client_secret: Path, tg_env: Path) -> int:
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    from googleapiclient.errors import HttpError
    p = Path(file)
    if not p.is_absolute():
        p = HERE.parents[2] / file
    if not p.is_file():
        sys.exit(f"[ERROR] file not found: {p}")
    size_mb = p.stat().st_size / 1048576
    creds = _creds(client_secret)
    svc = build("drive", "v3", credentials=creds)
    media = MediaFileUpload(str(p), resumable=True, chunksize=8 * 1024 * 1024)
    req = svc.files().create(body={"name": p.name}, media_body=media,
                             fields="id,name,webViewLink")
    print(f"Uploading {p.name} ({size_mb:.1f} MB) to Google Drive ...", flush=True)
    resp, last = None, -1
    try:
        while resp is None:
            status, resp = req.next_chunk()
            if status:
                pct = int(status.progress() * 100)
                if pct != last and pct % 5 == 0:
                    print(f"  {pct}%", flush=True)
                    last = pct
        fid = resp["id"]
        svc.permissions().create(fileId=fid,
                                 body={"role": "reader", "type": "anyone"}).execute()
    except HttpError as e:
        if "accessNotConfigured" in str(e) or "has not been used" in str(e):
            sys.exit("[ERROR] Drive API is disabled for this OAuth client's Google "
                     "Cloud project. Enable it once at "
                     "https://console.cloud.google.com/apis/library/drive.googleapis.com "
                     "(same project as client_secrets.json), wait ~1 min, retry.")
        raise
    link = resp.get("webViewLink") or f"https://drive.google.com/file/d/{fid}/view"
    print(f"Uploaded OK - link: {link}")

    if notify:
        import requests
        env = _load_env(tg_env)
        tok, chat = env.get("TELEGRAM_BOT_TOKEN"), env.get("TELEGRAM_CHAT_ID")
        if not (tok and chat):
            print("[WARN] TELEGRAM_BOT_TOKEN/CHAT_ID not in .env - skipped notify.")
        else:
            text = (f"{caption or p.name}\n\n"
                    f"\U0001F3AC Full-quality master ({size_mb:.0f} MB)\n\U0001F4E5 {link}")
            r = requests.post(f"https://api.telegram.org/bot{tok}/sendMessage",
                              data={"chat_id": chat, "text": text}, timeout=20)
            print("Telegram notify:", "OK" if r.ok else f"FAILED {r.status_code} {r.text[:200]}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Drive upload + Telegram link notify")
    ap.add_argument("--auth", action="store_true", help="one-time interactive OAuth login")
    ap.add_argument("--upload", metavar="FILE", help="file to upload")
    ap.add_argument("--caption", help="message caption")
    ap.add_argument("--notify", action="store_true", help="send the link via the existing Telegram bot")
    ap.add_argument("--client-secret", default=str(DEFAULT_CLIENT))
    ap.add_argument("--tg-env", default=str(DEFAULT_TG_ENV))
    a = ap.parse_args()
    if a.auth:
        return cmd_auth(Path(a.client_secret))
    if a.upload:
        return cmd_upload(a.upload, a.caption, a.notify, Path(a.client_secret), Path(a.tg_env))
    ap.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
