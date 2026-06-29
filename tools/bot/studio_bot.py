#!/usr/bin/env python3
"""M4 — Telegram command bot for the AI-Youtube-Studio autopilot.

Listens (long-poll) for the owner's commands and runs the full pipeline via
tools/run_all.py, which delivers the finished rough video back to Telegram
(Drive link). Mirrors japan-news-bot/telegram_command_bot.py.

IMPORTANT: use a SEPARATE bot token (create one with @BotFather) so getUpdates
does not 409-conflict with the live japan-news-bot. Put it in .env:
    STUDIO_BOT_TOKEN=...
Owner chat id is reused from TELEGRAM_CHAT_ID (a user's chat id is the same for
any bot). Only the owner may command the bot.

Commands:
  /make <topic>   run the full pipeline for <topic> (ja, japanese_mystery) and deliver
  /status         show whether a job is running
  /help

Run (VPS):  python tools/bot/studio_bot.py     (under tmux/systemd; one instance only)
"""
from __future__ import annotations
import os, sys, time, threading, subprocess, urllib.request, urllib.parse, urllib.error, json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PY = sys.executable


def load_env() -> None:
    for d in [Path(__file__).resolve().parent, *Path(__file__).resolve().parents]:
        f = d / ".env"
        if f.is_file():
            for line in f.read_text(encoding="utf-8", errors="ignore").splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, _, v = line.partition("=")
                    os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
            return


load_env()
TOKEN = os.environ.get("STUDIO_BOT_TOKEN")
OWNER = os.environ.get("STUDIO_OWNER_CHAT_ID") or os.environ.get("TELEGRAM_CHAT_ID")
API = f"https://api.telegram.org/bot{TOKEN}"
LOCK = threading.Lock()
STATE = {"running": False, "topic": None, "since": None}


def send(text: str) -> None:
    try:
        data = urllib.parse.urlencode({"chat_id": OWNER, "text": text}).encode()
        urllib.request.urlopen(f"{API}/sendMessage", data=data, timeout=20).read()
    except Exception as e:
        print(f"[send fail] {e}", file=sys.stderr)


def run_job(topic: str) -> None:
    STATE.update(running=True, topic=topic, since=time.strftime("%H:%M:%S"))
    send(f"🎬 Bắt đầu pipeline: {topic}\n(text → ảnh → TTS → render → giao). Mất ~25–40 phút.")
    try:
        r = subprocess.run([PY, "tools/run_all.py", "--topic", topic,
                            "--niche", "japanese_mystery", "--language", "ja", "--deliver"],
                           cwd=str(REPO), capture_output=True, text=True)
        if r.returncode == 0:
            send("✅ Xong — video đã giao qua link Telegram phía trên.")
        else:
            send(f"❌ Lỗi pipeline:\n{(r.stderr or r.stdout)[-800:]}")
    except Exception as e:
        send(f"❌ Exception: {e}")
    finally:
        STATE.update(running=False, topic=None, since=None)
        LOCK.release()


def handle(text: str) -> None:
    cmd, _, arg = text.strip().partition(" ")
    cmd = cmd.lower()
    if cmd in ("/make", "/làm", "/lam"):
        topic = arg.strip()
        if not topic:
            send("Cú pháp: /make <chủ đề>"); return
        if not LOCK.acquire(blocking=False):
            send(f"⏳ Đang chạy job khác ({STATE['topic']}). Đợi xong đã."); return
        threading.Thread(target=run_job, args=(topic,), daemon=True).start()
    elif cmd == "/status":
        send(f"Running: {STATE['running']}" + (f" — {STATE['topic']} (từ {STATE['since']})"
                                               if STATE["running"] else ""))
    else:
        send("🤖 AI-Youtube-Studio bot\n/make <chủ đề> — sinh video tự động + giao\n/status\n/help")


def main() -> int:
    if not TOKEN:
        sys.exit("[ERROR] STUDIO_BOT_TOKEN not in .env (create a new bot via @BotFather)")
    if not OWNER:
        sys.exit("[ERROR] no owner chat id (set STUDIO_OWNER_CHAT_ID or TELEGRAM_CHAT_ID)")
    print(f"studio_bot up. owner={OWNER}. polling…")
    offset = 0
    while True:
        try:
            url = f"{API}/getUpdates?timeout=50&offset={offset}"
            data = json.loads(urllib.request.urlopen(url, timeout=60).read().decode())
            for upd in data.get("result", []):
                offset = upd["update_id"] + 1
                msg = upd.get("message") or {}
                chat_id = str((msg.get("chat") or {}).get("id", ""))
                text = msg.get("text") or ""
                if chat_id != str(OWNER):
                    continue  # owner-only
                if text:
                    handle(text)
        except urllib.error.URLError:
            time.sleep(5)
        except Exception as e:
            print(f"[poll err] {e}", file=sys.stderr); time.sleep(5)


if __name__ == "__main__":
    raise SystemExit(main())
