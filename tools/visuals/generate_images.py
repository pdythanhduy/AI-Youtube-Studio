#!/usr/bin/env python3
"""Asset stage: generate scene images from a project's image_prompts.md via FLUX 1.1 [pro] (fal.ai).

Bridges the orchestrator's stage-8 output (prompts/08 -> image_prompts.md, markdown)
to FLUX. Parses each `## Beat N` block, takes the `### Midjourney / DALL-E Prompt`
text, strips Midjourney flags (FLUX has no negative prompt / --ar; safety is baked
into the prompt wording + DRAMATIZATION labels), generates 1920x1080, and saves to
projects/<slug>/assets/images/beat_NN.jpg. Writes images_manifest.json.

Credentials: FAL_KEY from .env (upward search). No secret printed.

Usage:
  python tools/visuals/generate_images.py --project <slug> --list
  python tools/visuals/generate_images.py --project <slug> --limit 2
  python tools/visuals/generate_images.py --project <slug>            # all
"""
from __future__ import annotations
import argparse, json, os, re, sys, time, urllib.request, urllib.error
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PROJECTS = REPO / "projects"
FAL_MODEL = os.environ.get("FLUX_FAL_MODEL", "fal-ai/flux-pro/v1.1")
QUEUE = "https://queue.fal.run"
OUT_W, OUT_H = 1920, 1080


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


def fal_key() -> str | None:
    return os.environ.get("FAL_KEY") or os.environ.get("FAL_API_KEY")


def parse_prompts(md: Path) -> list[dict]:
    text = md.read_text(encoding="utf-8")
    out = []
    for block in re.split(r"\n##\s+", text):
        if not block.lstrip().startswith("Beat"):
            continue
        head = block.splitlines()[0].strip()
        m = re.match(r"Beat\s+(\d+)", head)
        beat = m.group(1).zfill(2) if m else str(len(out) + 1).zfill(2)
        pm = re.search(r"###[^\n]*Prompt\s*\n+(.+?)(?:\n---|\Z)", block, re.S)
        if not pm:
            continue
        prompt = pm.group(1).strip()
        prompt = re.split(r"\s--(?:ar|style|v|q|no|s|chaos|stylize)\b", prompt)[0].strip().rstrip(",").strip()
        out.append({"beat": beat, "title": head, "prompt": prompt})
    return out


def _req(url: str, key: str, method="GET", body=None) -> dict:
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(url, data=data, method=method)
    r.add_header("Authorization", f"Key {key}")
    r.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(r, timeout=60) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        detail = ""
        try:
            detail = json.loads(e.read().decode()).get("detail", "")
        except Exception:
            pass
        raise RuntimeError(f"HTTP {e.code} {detail}".strip()) from None


def generate_one(prompt: str, key: str) -> str:
    payload = {"prompt": prompt, "image_size": {"width": OUT_W, "height": OUT_H},
               "num_images": 1, "output_format": "jpeg", "enable_safety_checker": True}
    sub = _req(f"{QUEUE}/{FAL_MODEL}", key, "POST", payload)
    rid = sub.get("request_id")
    status_url = sub.get("status_url") or f"{QUEUE}/{FAL_MODEL}/requests/{rid}/status"
    resp_url = sub.get("response_url") or f"{QUEUE}/{FAL_MODEL}/requests/{rid}"
    for _ in range(120):
        st = _req(status_url, key)
        if st.get("status") == "COMPLETED":
            break
        if st.get("status") in ("FAILED", "ERROR"):
            raise RuntimeError(f"fal {rid} {st.get('status')}")
        time.sleep(3)
    res = _req(resp_url, key)
    imgs = res.get("images") or []
    if not imgs:
        raise RuntimeError("no image returned")
    return imgs[0]["url"]


def download(url: str, out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=120) as r:
        raw = r.read()
    try:
        from PIL import Image
        import io
        im = Image.open(io.BytesIO(raw)).convert("RGB")
        if im.size != (OUT_W, OUT_H):
            im = im.resize((OUT_W, OUT_H), Image.LANCZOS)
        im.save(out, "JPEG", quality=92)
    except ImportError:
        out.write_bytes(raw)


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # JP titles on cp932 consoles
    except Exception:
        pass
    load_env()
    ap = argparse.ArgumentParser(description="Generate scene images from image_prompts.md via FLUX")
    ap.add_argument("--project", required=True)
    ap.add_argument("--limit", type=int, default=0, help="generate only the first N (0 = all)")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--force", action="store_true", help="overwrite existing images")
    a = ap.parse_args()
    proj = PROJECTS / a.project
    md = proj / "image_prompts.md"
    if not md.is_file():
        sys.exit(f"[ERROR] {md} not found (run stage 8 first)")
    items = parse_prompts(md)
    if a.list:
        for it in items:
            print(f"  beat {it['beat']}: {it['title'][:60]}")
        print(f"total: {len(items)}")
        return 0
    if a.limit:
        items = items[:a.limit]
    key = fal_key()
    if not key:
        sys.exit("[ERROR] FAL_KEY missing in .env")
    outdir = proj / "assets" / "images"
    rows = []
    for it in items:
        out = outdir / f"beat_{it['beat']}.jpg"
        if out.exists() and not a.force:
            print(f"SKIP beat {it['beat']} (exists)")
            continue
        try:
            print(f"GEN  beat {it['beat']} ...", flush=True)
            url = generate_one(it["prompt"], key)
            download(url, out)
            rows.append({"beat": it["beat"], "file": str(out.relative_to(proj)),
                         "title": it["title"], "qa_status": "PENDING_QA"})
            print(f"     saved {out.relative_to(proj)}")
        except Exception as e:
            print(f"[ERROR] beat {it['beat']}: {e}", file=sys.stderr)
    if rows:
        mf = proj / "images_manifest.json"
        prev = {r["beat"]: r for r in json.loads(mf.read_text())["images"]} if mf.exists() else {}
        for r in rows:
            prev[r["beat"]] = r
        mf.write_text(json.dumps({"model": FAL_MODEL, "size": f"{OUT_W}x{OUT_H}",
                                  "images": list(prev.values())}, ensure_ascii=False, indent=2),
                      encoding="utf-8")
        print(f"\nManifest: {mf.relative_to(proj)} (+{len(rows)})")
        print("Next: QA gate before these ship (generating != approving).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
