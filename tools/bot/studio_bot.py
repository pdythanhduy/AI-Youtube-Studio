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

sys.path.insert(0, str(REPO / "tools" / "review"))
from update_human_decision import apply_decision, build_review_card  # noqa: E402

LOCK = threading.Lock()
STATE = {"running": False, "topic": None, "since": None}


def send(text: str, reply_markup: dict | None = None) -> None:
    try:
        body = {"chat_id": OWNER, "text": text}
        if reply_markup:
            body["reply_markup"] = json.dumps(reply_markup)
        urllib.request.urlopen(f"{API}/sendMessage", data=urllib.parse.urlencode(body).encode(), timeout=20).read()
    except Exception as e:
        print(f"[send fail] {e}", file=sys.stderr)


def answer_cb(cb_id: str, text: str = "") -> None:
    try:
        data = urllib.parse.urlencode({"callback_query_id": cb_id, "text": text}).encode()
        urllib.request.urlopen(f"{API}/answerCallbackQuery", data=data, timeout=15).read()
    except Exception:
        pass


def edit_msg(chat_id, message_id, text: str) -> None:
    try:
        data = urllib.parse.urlencode({"chat_id": chat_id, "message_id": message_id, "text": text}).encode()
        urllib.request.urlopen(f"{API}/editMessageText", data=data, timeout=15).read()
    except Exception:
        pass


def _manifest(pid: str):
    mf = REPO / "runtime" / Path(pid).name / "human_review_manifest.json"
    return (mf, json.loads(mf.read_text(encoding="utf-8"))) if mf.exists() else (mf, None)


def _review_keyboard(pid: str, ready: bool) -> dict:
    row = ([{"text": "✅ Approve", "callback_data": f"approve:{pid}"}] if ready else []) + \
          [{"text": "❌ Reject", "callback_data": f"reject:{pid}"},
           {"text": "🔁 Revise", "callback_data": f"revise:{pid}"}]
    return {"inline_keyboard": [row]}


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
    elif cmd == "/review":
        pid = arg.strip()
        if not pid:
            send("Cú pháp: /review <project_id>"); return
        _, m = _manifest(pid)
        if not m:
            send(f"Chưa có manifest cho {pid} (đã chạy QA gate chưa?)"); return
        ready = m.get("gate_status") == "READY_FOR_HUMAN_REVIEW"
        card = build_review_card(pid, m)
        if not ready:
            card += f"\n\n⚠️ {m.get('gate_status')} — KHÔNG cho Approve (QA chưa pass). Chỉ Reject/Revise."
        send(card, reply_markup=_review_keyboard(pid, ready))
    elif cmd == "/status":
        pid = arg.strip()
        if pid:
            _, m = _manifest(pid)
            if not m:
                send(f"Chưa có manifest cho {pid}."); return
            send(f"{pid}\n gate={m.get('gate_status')}  safety={m.get('safety_status')}\n"
                 f" human_decision={m.get('human_decision')}  project_status={m.get('project_status','-')}\n"
                 f" upload_allowed={m.get('upload_allowed')}")
        else:
            send(f"Running: {STATE['running']}" + (f" — {STATE['topic']} (từ {STATE['since']})"
                                                   if STATE["running"] else ""))
    else:
        send("🤖 AI-Youtube-Studio bot\n/make <chủ đề> — sinh video + giao\n"
             "/review <project_id> — duyệt (Approve/Reject/Revise)\n"
             "/status [project_id] — trạng thái job hoặc project\n/help")


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
                cb = upd.get("callback_query")
                if cb:
                    frm = str((cb.get("from") or {}).get("id", ""))
                    if frm != str(OWNER):
                        answer_cb(cb.get("id"), "Not authorized")  # non-owner clicks ignored
                        continue
                    decision, _, pid = (cb.get("data") or "").partition(":")
                    res = apply_decision(decision, by=frm, owner=OWNER, project_id=pid)
                    cmsg = cb.get("message") or {}
                    if res.get("ok"):
                        answer_cb(cb.get("id"), f"{decision} ✓")
                        edit_msg((cmsg.get("chat") or {}).get("id"), cmsg.get("message_id"),
                                 f"[DECISION] {pid} → {res['project_status']} (by owner). "
                                 f"upload_allowed=False — YouTube upload vẫn là gate riêng.")
                    else:
                        answer_cb(cb.get("id"), "Refused")
                        send(f"❌ {pid}: {res.get('error')}")
                    continue
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
