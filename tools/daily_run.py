#!/usr/bin/env python3
"""Daily autopilot — pick a fresh topic, then run the full pipeline and deliver to Telegram.

For a daily cron: pick_topic -> run_all (text -> images -> TTS -> render -> QA gate ->
deliver). Delivers to Telegram FOR HUMAN REVIEW only (run_all keeps upload_allowed=false;
no YouTube publish). A once-per-day guard prevents accidental double-spend.

Usage (cron): python tools/daily_run.py
"""
from __future__ import annotations
import subprocess, sys, time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PY = sys.executable
LOG = REPO / "runtime" / "daily_log.txt"
RAN = REPO / "runtime" / "daily_last_run.txt"


def log(msg: str) -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    print(line, flush=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def prune_old(keep: int = 5) -> None:
    """Disk guard: on the older projects, drop the heavy assets (images/audio/rough video)
    but keep the text, manifests and thumbnail. Bounds disk use for unattended daily runs."""
    projs = sorted([p for p in (REPO / "projects").glob("*") if p.is_dir()])
    for p in projs[:-keep] if len(projs) > keep else []:
        freed = 0
        for sub in [p / "assets" / "images", p / "assets" / "audio", p / "export" / "rough"]:
            for f in sub.glob("*") if sub.exists() else []:
                try:
                    freed += f.stat().st_size
                    f.unlink()
                except Exception:
                    pass
        if freed:
            log(f"pruned {p.name}: freed {freed // 1048576} MB")


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    force = "--force" in sys.argv
    today = time.strftime("%Y-%m-%d")
    if not force and RAN.exists() and RAN.read_text(encoding="utf-8").strip() == today:
        log("already ran today — skip (use --force to override)")
        return 0
    log("===== daily autopilot START =====")

    p = subprocess.run([PY, "tools/daily/pick_topic.py"], cwd=str(REPO), capture_output=True, text=True)
    if p.returncode != 0 or not p.stdout.strip():
        log(f"topic pick FAILED rc={p.returncode}: {(p.stderr or '')[-300:]}")
        return 1
    topic = p.stdout.strip().splitlines()[-1].strip()
    log(f"topic: {topic}")

    # run_all performs QA + delivery (thumbnail + title/description/hashtags), upload stays gated
    rc = subprocess.run([PY, "tools/run_all.py", "--topic", topic, "--niche", "japanese_mystery",
                         "--language", "ja", "--deliver"], cwd=str(REPO)).returncode
    RAN.parent.mkdir(parents=True, exist_ok=True)
    RAN.write_text(today, encoding="utf-8")
    try:
        prune_old(keep=5)
    except Exception as e:
        log(f"prune skipped: {e}")
    log(f"===== daily autopilot END rc={rc} =====")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
