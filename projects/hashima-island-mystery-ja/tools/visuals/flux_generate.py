#!/usr/bin/env python3
"""FLUX 1.1 [pro] image generator (fal.ai) for hashima-island-mystery-ja.

Reads the already-approved prompt plans (assets/ai_images/*_generation_plan.json),
sends each image to FLUX 1.1 [pro] via the fal.ai queue REST API, downloads the
result, and conforms it to 1920x1080. Mirrors the Vbee tooling conventions:
credentials from C:/youtubeAI/.env (upward search), --dry-run / --auth-test, a
written manifest, and no secret ever printed or logged.

SAFETY (matches project gates):
  - FLUX 1.1 [pro] (fal) has NO negative-prompt field. We use the `dalle3_prompt`
    text (negatives baked in as positive phrasing: "No people, no animals ...").
  - Entries flagged human_review_required / sensitive_content (e.g. IMG009 mine
    tunnel) are SKIPPED unless you name them explicitly AND pass --allow-sensitive.
  - This script only GENERATES candidates. The existing QA gates (batch_*_qa,
    FIX-M1) still decide what ships. Generating != approving.

Usage:
  python tools/visuals/flux_generate.py --list
  python tools/visuals/flux_generate.py --auth-test
  python tools/visuals/flux_generate.py --image IMG002 --dry-run
  python tools/visuals/flux_generate.py --image IMG002
  python tools/visuals/flux_generate.py --all                 # skips existing + sensitive
  python tools/visuals/flux_generate.py --image IMG009 --allow-sensitive
"""
from __future__ import annotations
import argparse, json, os, re, sys, time, urllib.request, urllib.error
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[2]
PLAN_GLOB = "assets/ai_images/*_generation_plan.json"
MANIFEST = PROJECT / "assets/ai_images/generated/flux_generation_manifest.json"

# ── Config (env-overridable) ──────────────────────────────────────────────────
FAL_MODEL   = os.environ.get("FLUX_FAL_MODEL", "fal-ai/flux-pro/v1.1")
QUEUE_BASE  = "https://queue.fal.run"
OUT_W       = int(os.environ.get("FLUX_WIDTH", "1920"))
OUT_H       = int(os.environ.get("FLUX_HEIGHT", "1080"))
OUT_FORMAT  = os.environ.get("FLUX_OUTPUT_FORMAT", "jpeg")
POLL_SECS   = float(os.environ.get("FLUX_POLL_SECS", "3"))
POLL_MAX    = int(os.environ.get("FLUX_POLL_MAX", "120"))   # ~6 min ceiling


# ── .env loader (upward search, no dependency, no value printed) ──────────────
def load_env() -> None:
    here = Path(__file__).resolve()
    for d in [here.parent, *here.parents]:
        f = d / ".env"
        if f.is_file():
            for line in f.read_text(encoding="utf-8", errors="ignore").splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, _, v = line.partition("=")
                k, v = k.strip(), v.strip().strip('"').strip("'")
                os.environ.setdefault(k, v)
    # done silently


def fal_key() -> str | None:
    return os.environ.get("FAL_KEY") or os.environ.get("FAL_API_KEY")


# ── Prompt plan loading ───────────────────────────────────────────────────────
def _strip_mj(prompt: str) -> str:
    """Remove Midjourney flags (--ar/--no/--v/--q ...) from a prompt string."""
    p = re.split(r"\s--(?:ar|no|v|q|stylize|s|chaos|c)\b", prompt)[0]
    return p.strip().rstrip(",").strip()


def load_entries() -> dict[str, dict]:
    """Collect image entries from every *_generation_plan.json. Later files win."""
    entries: dict[str, dict] = {}
    for plan in sorted(PROJECT.glob(PLAN_GLOB)):
        try:
            data = json.loads(plan.read_text(encoding="utf-8"))
        except Exception:
            continue
        gset = data.get("global_generation_settings", {})
        for val in data.values():
            if not isinstance(val, list):
                continue
            for item in val:
                if not isinstance(item, dict) or "image_id" not in item:
                    continue
                if not (item.get("dalle3_prompt") or item.get("final_prompt")):
                    continue
                iid = item["image_id"]
                prompt = item.get("dalle3_prompt") or _strip_mj(item["final_prompt"])
                out_rel = item.get("output_path") or (
                    gset.get("output_directory", "assets/ai_images/generated/")
                    + (item.get("output_filename") or f"{iid}.jpg"))
                entries[iid] = {
                    "image_id": iid,
                    "scene_id": item.get("scene_id"),
                    "prompt": prompt,
                    "output_path": out_rel,
                    "sensitive": bool(item.get("sensitive_content")
                                      or item.get("human_review_required")),
                    "source_plan": plan.name,
                }
    return entries


# ── HTTP helpers ──────────────────────────────────────────────────────────────
def _req(url: str, key: str, method="GET", body: dict | None = None) -> dict:
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


def _payload(prompt: str) -> dict:
    return {
        "prompt": prompt,
        "image_size": {"width": OUT_W, "height": OUT_H},
        "num_images": 1,
        "output_format": OUT_FORMAT,
        "enable_safety_checker": True,
    }


def generate_one(entry: dict, key: str) -> dict:
    submit = _req(f"{QUEUE_BASE}/{FAL_MODEL}", key, "POST", _payload(entry["prompt"]))
    req_id = submit.get("request_id")
    status_url = submit.get("status_url") or f"{QUEUE_BASE}/{FAL_MODEL}/requests/{req_id}/status"
    resp_url   = submit.get("response_url") or f"{QUEUE_BASE}/{FAL_MODEL}/requests/{req_id}"
    for _ in range(POLL_MAX):
        st = _req(status_url, key)
        status = st.get("status")
        if status == "COMPLETED":
            break
        if status in ("FAILED", "ERROR"):
            raise RuntimeError(f"fal job {req_id} {status}: {st}")
        time.sleep(POLL_SECS)
    else:
        raise TimeoutError(f"fal job {req_id} did not complete in time")
    result = _req(resp_url, key)
    images = result.get("images") or []
    if not images:
        raise RuntimeError(f"fal job {req_id} returned no images: {result}")
    return {"request_id": req_id, "url": images[0]["url"],
            "nsfw": (result.get("has_nsfw_concepts") or [False])[0], "seed": result.get("seed")}


def download_and_conform(url: str, out_path: Path) -> str:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    raw = out_path.with_suffix(out_path.suffix + ".raw")
    with urllib.request.urlopen(url, timeout=120) as resp:
        raw.write_bytes(resp.read())
    try:
        from PIL import Image
        im = Image.open(raw).convert("RGB")
        if im.size != (OUT_W, OUT_H):
            im = im.resize((OUT_W, OUT_H), Image.LANCZOS)
        im.save(out_path, quality=95)
        raw.unlink(missing_ok=True)
        return f"{out_path} ({OUT_W}x{OUT_H})"
    except ImportError:
        raw.rename(out_path)
        return f"{out_path} (PIL missing — saved as-is, not resized)"


# ── Manifest ──────────────────────────────────────────────────────────────────
def write_manifest(rows: list[dict]) -> None:
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    prev = {}
    if MANIFEST.exists():
        try:
            prev = {r["image_id"]: r for r in json.loads(MANIFEST.read_text())["images"]}
        except Exception:
            prev = {}
    for r in rows:
        prev[r["image_id"]] = r
    MANIFEST.write_text(json.dumps(
        {"model": FAL_MODEL, "provider": "fal.ai", "size": f"{OUT_W}x{OUT_H}",
         "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
         "images": list(prev.values())}, ensure_ascii=False, indent=2), encoding="utf-8")


# ── CLI ───────────────────────────────────────────────────────────────────────
def main() -> int:
    load_env()
    ap = argparse.ArgumentParser(description="FLUX 1.1 [pro] generator (fal.ai)")
    ap.add_argument("--image", action="append", metavar="IMG_ID", help="generate specific image_id(s)")
    ap.add_argument("--all", action="store_true", help="generate all (skips existing + sensitive)")
    ap.add_argument("--list", action="store_true", help="list discovered prompt entries")
    ap.add_argument("--dry-run", action="store_true", help="print request, do not call the API")
    ap.add_argument("--auth-test", action="store_true", help="check FAL_KEY presence + config")
    ap.add_argument("--force", action="store_true", help="overwrite existing output files")
    ap.add_argument("--out-dir", metavar="DIR", help="override output directory (keeps filename); good for test runs")
    ap.add_argument("--allow-sensitive", action="store_true",
                    help="permit human_review/sensitive entries (named only, never via --all)")
    args = ap.parse_args()

    entries = load_entries()

    if args.list:
        print(f"Discovered {len(entries)} prompt entries:")
        for iid, e in sorted(entries.items()):
            flag = " [SENSITIVE/REVIEW]" if e["sensitive"] else ""
            exists = " (exists)" if (PROJECT / e["output_path"]).exists() else ""
            print(f"  {iid}  {e['scene_id']:6}  -> {e['output_path']}{flag}{exists}")
        return 0

    if args.auth_test:
        key = fal_key()
        print(f"  Model:    {FAL_MODEL}")
        print(f"  Endpoint: {QUEUE_BASE}/{FAL_MODEL}")
        print(f"  Size:     {OUT_W}x{OUT_H}  format={OUT_FORMAT}")
        print(f"  FAL_KEY:  {'SET (len %d)' % len(key) if key else 'MISSING — set FAL_KEY in .env'}")
        print(f"  Entries:  {len(entries)} prompts discovered")
        print("  Note: real auth is validated on the first --image run (fal has no free whoami).")
        return 0 if key else 1

    # select targets
    if args.image:
        want = []
        for iid in args.image:
            if iid not in entries:
                print(f"[ERROR] unknown image_id: {iid}", file=sys.stderr); return 2
            want.append(entries[iid])
    elif args.all:
        want = [e for e in entries.values()]
    else:
        ap.print_help(); return 0

    key = fal_key()
    if not key and not args.dry_run:
        print("[ERROR] FAL_KEY missing in .env", file=sys.stderr); return 1

    rows = []
    for e in sorted(want, key=lambda x: x["image_id"]):
        if args.out_dir:
            out = (Path(args.out_dir) if Path(args.out_dir).is_absolute()
                   else PROJECT / args.out_dir) / Path(e["output_path"]).name
        else:
            out = PROJECT / e["output_path"]
        if e["sensitive"] and not (args.image and args.allow_sensitive):
            print(f"SKIP {e['image_id']} — sensitive/review-gated (name it + --allow-sensitive to generate)")
            continue
        if out.exists() and not args.force:
            print(f"SKIP {e['image_id']} — exists ({e['output_path']}); --force to overwrite")
            continue
        if args.dry_run:
            print(f"DRY  {e['image_id']} -> POST {QUEUE_BASE}/{FAL_MODEL}")
            print(f"       payload={json.dumps(_payload(e['prompt']), ensure_ascii=False)[:200]}...")
            continue
        try:
            print(f"GEN  {e['image_id']} ({e['scene_id']}) ...", flush=True)
            res = generate_one(e, key)
            saved = download_and_conform(res["url"], out)
            row = {"image_id": e["image_id"], "scene_id": e["scene_id"],
                   "output_path": e["output_path"], "request_id": res["request_id"],
                   "seed": res["seed"], "nsfw_flag": res["nsfw"],
                   "source_plan": e["source_plan"],
                   "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                   "qa_status": "PENDING_QA"}
            rows.append(row)
            warn = "  ⚠ nsfw_flag=TRUE — review" if res["nsfw"] else ""
            print(f"     saved {saved}{warn}")
        except Exception as ex:
            print(f"[ERROR] {e['image_id']}: {ex}", file=sys.stderr)

    if rows:
        write_manifest(rows)
        print(f"\nManifest: {MANIFEST.relative_to(PROJECT)}  (+{len(rows)} entries)")
        print("Next: run the existing QA gate on these candidates before they ship.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
