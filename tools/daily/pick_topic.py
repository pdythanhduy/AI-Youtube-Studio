#!/usr/bin/env python3
"""Pick a fresh Japanese lost-place / mystery topic for the daily autopilot.

Generates ONE topic (Japanese) via Claude, avoiding the history file and unsafe themes,
appends it to runtime/topic_history.json, and prints it to stdout (last line = the topic).

Usage: python tools/daily/pick_topic.py
"""
from __future__ import annotations
import json, os, sys, time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
HIST = REPO / "runtime" / "topic_history.json"


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


def api_key() -> str | None:
    return os.environ.get("EXPO_PUBLIC_ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")


def history() -> list[dict]:
    if HIST.exists():
        try:
            return json.loads(HIST.read_text(encoding="utf-8"))
        except Exception:
            return []
    return []


SYSTEM = (
    "You generate ONE fresh Japanese-language documentary topic for a dark-but-respectful "
    "'Japanese mystery / lost place' YouTube channel. Hard rules:\n"
    "- A real, documentable place or phenomenon in Japan (abandoned site, ruins, folklore, "
    "unsolved local mystery, lost village, forgotten infrastructure, etc.).\n"
    "- SAFE & respectful: NO forced-labor or wartime-atrocity framing, NO real named victims, "
    "NO suicide locations, NO gore, NO living private individuals, NO defamation.\n"
    "- Must be DISTINCT from every entry in the AVOID list (different place AND angle).\n"
    "- Output ONLY the topic line in Japanese (a compelling title-like phrase). No quotes, no extra text."
)


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    load_env()
    if not api_key():
        sys.exit("[ERROR] ANTHROPIC/EXPO_PUBLIC_ANTHROPIC_API_KEY not in .env")
    import anthropic
    past = history()
    avoid = "\n".join(f"- {h['topic']}" for h in past) or "(none yet)"
    client = anthropic.Anthropic(api_key=api_key())
    r = client.messages.create(
        model="claude-sonnet-4-6", max_tokens=300, system=SYSTEM,
        messages=[{"role": "user", "content": f"AVOID (already produced):\n{avoid}"}],
    )
    text = "".join(b.text for b in r.content if b.type == "text").strip()
    topic = text.splitlines()[-1].strip().strip("「」\"' ").strip() if text else ""
    if not topic:
        sys.exit("[ERROR] empty topic from model")
    past.append({"topic": topic, "at": time.strftime("%Y-%m-%d")})
    HIST.parent.mkdir(parents=True, exist_ok=True)
    HIST.write_text(json.dumps(past, ensure_ascii=False, indent=2), encoding="utf-8")
    print(topic)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
