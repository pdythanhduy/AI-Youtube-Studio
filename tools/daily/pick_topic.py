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
    "You generate ONE fresh Japanese-language documentary topic for a respectful "
    "'Japanese mystery / lost place' YouTube channel.\n"
    "CHOOSE from clearly-safe categories: abandoned villages / hotels / amusement parks "
    "(depopulation, NOT labor-death), folklore & legends, unsolved local mysteries, lost or "
    "hidden shrines & rituals, forgotten infrastructure or transport, strange natural phenomena, "
    "ghost towns, old ruins with a peaceful or curious story.\n"
    "HARD EXCLUSIONS — NEVER choose a place/topic with ANY association to: wartime forced labor "
    "or laborers who built/died at a site; military headquarters / bunkers / tunnels / mines built "
    "or worked by laborers (e.g. 松代大本営, 軍艦島の強制労働, forced-labor coal mines); mass death, "
    "massacres, war crimes, Unit 731, biological/chemical weapons; atomic-bomb victims; "
    "kamikaze / mass-suicide (玉砕・特攻・自決); real named victims; suicide locations; forced "
    "relocation or suffering of Korean/Chinese/minority laborers. A plain historic fort with NO "
    "laborer-death or atrocity history (like a coastal gun battery) is fine; anything tied to "
    "forced labor, atrocity, or mass victims is NOT — pick a different, clearly-safe place.\n"
    "- Real & documentable in Japan. DISTINCT from every AVOID entry (different place AND angle).\n"
    "- Output ONLY the topic line in Japanese (a compelling title-like phrase). No quotes, no extra text."
)

# deterministic denylist — if the generated topic contains any of these, reject and regenerate
DENY = ["大本営", "松代", "731", "強制", "徴用", "慰安", "虐殺", "玉砕", "特攻", "自決",
        "被爆", "原爆", "毒ガス", "生体", "軍艦島", "端島", "地下壕", "防空壕", "炭鉱", "捕虜",
        "青木ヶ原", "樹海", "自殺", "東尋坊", "心中", "処刑", "殉職", "遭難", "心霊"]


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
    past_titles = [h["topic"] for h in past]
    client = anthropic.Anthropic(api_key=api_key())
    rejected: list[str] = []
    topic = ""
    for _ in range(5):                       # regenerate until a topic clears the denylist
        avoid = "\n".join(f"- {t}" for t in past_titles + rejected) or "(none yet)"
        r = client.messages.create(
            model="claude-sonnet-4-6", max_tokens=300, system=SYSTEM,
            messages=[{"role": "user", "content": f"AVOID (already produced or rejected):\n{avoid}"}],
        )
        text = "".join(b.text for b in r.content if b.type == "text").strip()
        cand = text.splitlines()[-1].strip().strip("「」\"' ").strip() if text else ""
        if not cand:
            continue
        hit = next((w for w in DENY if w in cand), None)
        if hit:
            print(f"[reject] '{cand}' contains banned '{hit}' — regenerating", file=sys.stderr)
            rejected.append(cand)
            continue
        topic = cand
        break
    if not topic:
        sys.exit("[ERROR] could not produce a safe topic after 5 attempts")
    past.append({"topic": topic, "at": time.strftime("%Y-%m-%d")})
    HIST.parent.mkdir(parents=True, exist_ok=True)
    HIST.write_text(json.dumps(past, ensure_ascii=False, indent=2), encoding="utf-8")
    print(topic)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
