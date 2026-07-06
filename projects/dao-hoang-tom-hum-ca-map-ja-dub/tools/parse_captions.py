#!/usr/bin/env python3
"""Parse YouTube json3 auto-captions into clean timed segments.

Usage: python tools/parse_captions.py <source.vi.json3> <out_segments.json>
Groups word-timed tokens into segments (pause > 1.2s or length > 12s);
each segment's end is snapped to the next segment's start (gap-free timeline).
"""
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")

GAP_MS = 1200
MAXLEN_MS = 12000
TAIL_MS = 2000

src, out = sys.argv[1], sys.argv[2]
data = json.load(open(src, encoding="utf-8"))

words = []
for ev in data.get("events", []):
    t0 = ev.get("tStartMs")
    segs = ev.get("segs")
    if t0 is None or not segs:
        continue
    for s in segs:
        txt = s.get("utf8", "")
        if not txt or txt == "\n":
            continue
        words.append((t0 + s.get("tOffsetMs", 0), txt.strip()))
words.sort(key=lambda w: w[0])

segments = []
cur = None
for t, w in words:
    if cur is None:
        cur = {"start": t, "end": t, "text": [w]}
    elif (t - cur["end"] > GAP_MS) or (t - cur["start"] > MAXLEN_MS):
        segments.append(cur)
        cur = {"start": t, "end": t, "text": [w]}
    else:
        cur["text"].append(w)
        cur["end"] = t
if cur:
    segments.append(cur)

for i, seg in enumerate(segments):
    seg["end"] = (segments[i + 1]["start"] if i + 1 < len(segments)
                  else seg["end"] + TAIL_MS)

result = [
    {"id": f"S{i+1:03d}", "start_ms": s["start"], "end_ms": s["end"],
     "dur_ms": s["end"] - s["start"], "vi": " ".join(s["text"])}
    for i, s in enumerate(segments)
]
json.dump(result, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
total = sum(r["dur_ms"] for r in result)
print(f"words: {len(words)}, segments: {len(result)}, covered: {total/1000:.0f}s")
