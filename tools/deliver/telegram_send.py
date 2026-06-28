#!/usr/bin/env python3
"""Full-quality video delivery to Telegram via Telethon (user account).

The Telegram **Bot API** caps file sends at 50 MB; a Telethon **user client**
sends up to 2 GB (4 GB with Premium) — so the 420 MB documentary master goes
into the chat as a real file, no compression. This is the delivery layer for the
AI-Youtube-Studio autopilot.

Credentials (in C:/youtubeAI/.env, upward search — NEVER printed/logged):
  TELEGRAM_API_ID      from https://my.telegram.org → API development tools
  TELEGRAM_API_HASH    from the same page
  TELEGRAM_SESSION      (optional) StringSession; if absent a file session is used
  TELEGRAM_TARGET       (optional) chat to send to; default "me" (Saved Messages)

One-time login (interactive — run in a REAL terminal, e.g. `! python ...`):
  python tools/deliver/telegram_send.py --login
    → prompts for phone + the code Telegram sends you, then prints a SESSION
      STRING. Put it in .env as TELEGRAM_SESSION so future sends are headless.

Usage:
  python tools/deliver/telegram_send.py --check
  python tools/deliver/telegram_send.py --send export/master/hashima_master_v1.mp4 \
      --caption "端島（軍艦島）の謎" --dry-run
  python tools/deliver/telegram_send.py --send <file> --caption "..."
"""
from __future__ import annotations
import argparse, os, sys
from pathlib import Path

HERE = Path(__file__).resolve()


def load_env() -> None:
    for d in [HERE.parent, *HERE.parents]:
        f = d / ".env"
        if f.is_file():
            for line in f.read_text(encoding="utf-8", errors="ignore").splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, _, v = line.partition("=")
                    os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
            return


def _creds() -> tuple[int | None, str | None, str | None, str]:
    api_id = os.environ.get("TELEGRAM_API_ID")
    api_hash = os.environ.get("TELEGRAM_API_HASH")
    session = os.environ.get("TELEGRAM_SESSION")
    target = os.environ.get("TELEGRAM_TARGET", "me")
    return (int(api_id) if api_id and api_id.isdigit() else None, api_hash, session, target)


def _client(api_id, api_hash, session):
    try:
        from telethon.sync import TelegramClient
        from telethon.sessions import StringSession
    except ImportError:
        sys.exit("[ERROR] telethon not installed. Run:  pip install telethon")
    if session:
        return TelegramClient(StringSession(session), api_id, api_hash)
    # file-based session stored next to this script (gitignore it)
    return TelegramClient(str(HERE.parent / "telegram_user.session"), api_id, api_hash)


def cmd_login() -> int:
    api_id, api_hash, _, _ = _creds()
    if not (api_id and api_hash):
        sys.exit("[ERROR] Set TELEGRAM_API_ID and TELEGRAM_API_HASH in .env first "
                 "(get them at https://my.telegram.org).")
    from telethon.sync import TelegramClient
    from telethon.sessions import StringSession
    print("Interactive login — enter your phone (+countrycode) and the code Telegram sends.")
    with TelegramClient(StringSession(), api_id, api_hash) as client:
        me = client.get_me()
        s = client.session.save()
        print(f"\nLogged in as: {getattr(me, 'username', None) or me.first_name} (id={me.id})")
        print("\n=== SESSION STRING (add to .env as TELEGRAM_SESSION, keep secret) ===")
        print(s)
        print("=== end ===")
    return 0


def cmd_check() -> int:
    api_id, api_hash, session, target = _creds()
    print(f"  TELEGRAM_API_ID:   {'SET' if api_id else 'MISSING'}")
    print(f"  TELEGRAM_API_HASH: {'SET' if api_hash else 'MISSING'}")
    print(f"  TELEGRAM_SESSION:  {'SET' if session else 'absent (will use file session)'}")
    print(f"  TELEGRAM_TARGET:   {target}")
    if not (api_id and api_hash):
        print("  → Get api_id/api_hash at https://my.telegram.org, then run --login.")
        return 1
    try:
        with _client(api_id, api_hash, session) as client:
            if not client.is_user_authorized():
                print("  → Not authorized yet. Run:  python tools/deliver/telegram_send.py --login")
                return 1
            me = client.get_me()
            print(f"  Authorized as: {getattr(me, 'username', None) or me.first_name} (id={me.id})  ✅")
    except Exception as e:
        print(f"  [ERROR] {e}")
        return 1
    return 0


def cmd_send(file: str, caption: str | None, dry_run: bool) -> int:
    p = Path(file)
    if not p.is_absolute():
        # resolve relative to project root (two levels up from tools/deliver)
        p = HERE.parents[2] / file
    if not p.is_file():
        sys.exit(f"[ERROR] file not found: {p}")
    size_mb = p.stat().st_size / 1048576
    api_id, api_hash, session, target = _creds()
    if dry_run:
        print(f"DRY  would send {p.name} ({size_mb:.1f} MB) → Telegram target '{target}'"
              + (f"  caption={caption!r}" if caption else ""))
        return 0
    if not (api_id and api_hash):
        sys.exit("[ERROR] Missing TELEGRAM_API_ID/TELEGRAM_API_HASH in .env (see --check).")
    if size_mb > 2048:
        print(f"[WARN] {size_mb:.0f} MB exceeds the 2 GB user-account limit; send may fail.")

    last = {"pct": -1}
    def progress(sent, total):
        pct = int(sent * 100 / total)
        if pct != last["pct"] and pct % 5 == 0:
            print(f"  upload {pct}%", flush=True)
            last["pct"] = pct

    with _client(api_id, api_hash, session) as client:
        if not client.is_user_authorized():
            sys.exit("[ERROR] not authorized — run --login first.")
        print(f"Uploading {p.name} ({size_mb:.1f} MB) → '{target}' ...", flush=True)
        client.send_file(target, str(p), caption=caption or p.name,
                         supports_streaming=True, progress_callback=progress)
    print("Sent ✅")
    return 0


def main() -> int:
    load_env()
    ap = argparse.ArgumentParser(description="Send full-quality video to Telegram via Telethon")
    ap.add_argument("--login", action="store_true", help="interactive one-time login → prints session string")
    ap.add_argument("--check", action="store_true", help="verify creds + authorization")
    ap.add_argument("--send", metavar="FILE", help="file to send")
    ap.add_argument("--caption", help="caption for the sent file")
    ap.add_argument("--dry-run", action="store_true", help="print what would be sent, no API call")
    args = ap.parse_args()
    if args.login:
        return cmd_login()
    if args.check:
        return cmd_check()
    if args.send:
        return cmd_send(args.send, args.caption, args.dry_run)
    ap.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
