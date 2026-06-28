#!/usr/bin/env python3
"""AI-Youtube-Studio pipeline orchestrator — turns the prompts/ + schemas/ spec
framework into an automated, runnable text pipeline (Claude API).

The studio's "engine"/"runtime"/"agents" dirs are design *specs* (.md); the real
per-stage instructions live in prompts/NN_*.md (each has a `# Prompt` code block
with {placeholders}). This driver: loads a stage prompt, fills placeholders from
input.json + prior stage outputs, calls Claude (Opus 4.8, adaptive thinking; web
search on research stages to avoid fabrication, handling pause_turn), and writes
the stage's output file. State is tracked in pipeline_manifest.json (resumable).

Model/credentials: reads EXPO_PUBLIC_ANTHROPIC_API_KEY (or ANTHROPIC_API_KEY) from
.env (upward search). Per claude-api guidance: claude-opus-4-8 + adaptive thinking.

Usage:
  python tools/orchestrator/run_pipeline.py --init "Topic here" --niche japanese_mystery --language ja
  python tools/orchestrator/run_pipeline.py --project <slug> --stage 1
  python tools/orchestrator/run_pipeline.py --project <slug> --all
  python tools/orchestrator/run_pipeline.py --project <slug> --stage 1 --dry-run
"""
from __future__ import annotations
import argparse, hashlib, json, os, re, sys, time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PROMPTS = REPO / "prompts"
PROJECTS = REPO / "projects"
MODEL = "claude-opus-4-8"

# stage number -> (prompt file stem, output filename, use_web_search)
STAGES = {
    1:  ("01_research",                "research.md",        True),
    2:  ("02_source_verifier",         "research_verified.md", True),
    3:  ("03_story_outline",           "story.md",           False),
    4:  ("04_script_writer",           "script.md",          False),
    5:  ("05_story_bible",             "story_bible.md",     False),
    6:  ("06_scene_splitter",          "storyboard.md",      False),
    7:  ("07_image_finder",            "image_plan.md",      False),
    8:  ("08_image_prompt_generator",  "image_prompts.md",   False),
    9:  ("09_voice_director",          "voice_script.txt",   False),
    10: ("10_youtube_seo",             "seo.md",             False),
}


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
    return os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("EXPO_PUBLIC_ANTHROPIC_API_KEY")


def slugify(topic: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", topic.lower()).strip("-")[:48]
    # non-ASCII topics (ja/vi) yield an empty slug — use a short topic hash so
    # same-day projects don't collide on "untitled".
    return s or ("t-" + hashlib.md5(topic.encode("utf-8")).hexdigest()[:8])


def extract_prompt_block(stem: str) -> str:
    """Return the fenced code block under the `# Prompt` heading of prompts/<stem>.md."""
    md = (PROMPTS / f"{stem}.md").read_text(encoding="utf-8")
    m = re.search(r"#\s*Prompt\s*\n+```[a-zA-Z]*\n(.*?)\n```", md, re.S)
    if not m:
        raise ValueError(f"no fenced Prompt block in {stem}.md")
    return m.group(1).strip()


def fill(template: str, ctx: dict) -> str:
    def repl(m):
        key = m.group(1)
        return str(ctx.get(key, m.group(0)))  # leave unknown placeholders intact
    return re.sub(r"\{([a-zA-Z_][a-zA-Z0-9_]*)\}", repl, template)


def call_claude(system: str, user: str, use_search: bool) -> str:
    import anthropic
    client = anthropic.Anthropic(api_key=api_key())
    tools = [{"type": "web_search_20260209", "name": "web_search", "max_uses": 6}] if use_search else []
    messages = [{"role": "user", "content": user}]
    for _ in range(8):  # pause_turn loop for server-side web search
        resp = client.messages.create(
            model=MODEL, max_tokens=12000,
            thinking={"type": "adaptive"},
            system=system, messages=messages,
            tools=tools or anthropic.NOT_GIVEN,
        )
        if resp.stop_reason == "pause_turn":
            messages.append({"role": "assistant", "content": resp.content})
            continue
        if resp.stop_reason == "refusal":
            raise RuntimeError(f"Claude refused: {getattr(resp, 'stop_details', None)}")
        break
    return "".join(b.text for b in resp.content if b.type == "text").strip()


def run_stage(proj: Path, stage: int, dry: bool) -> int:
    stem, outfile, use_search = STAGES[stage]
    inp = json.loads((proj / "input.json").read_text(encoding="utf-8"))
    ctx = dict(inp)
    ctx["project_slug"] = proj.name
    ctx.setdefault("notes", inp.get("notes", "(none)"))
    prompt = fill(extract_prompt_block(stem), ctx)
    # The prompt's "Save the output to ..." line is an instruction for the *runner*,
    # not the model — leaving it in makes the model role-play an agentic file-writer
    # (preamble + "I've saved it" + a summary instead of the full document). Strip it.
    prompt = re.sub(r"(?im)^.*save (the )?output to.*$\n?", "", prompt)

    # prior stage outputs as upstream context
    prior = []
    for n in range(1, stage):
        of = proj / STAGES[n][1]
        if of.exists():
            prior.append(f"=== {STAGES[n][1]} (upstream output) ===\n{of.read_text(encoding='utf-8')}")
    rules = (REPO / "MASTER_RULE.md")
    system = ("You are a production assistant for AI-Youtube-Studio. Follow the project's "
              "MASTER_RULE.md strictly: no fabrication of facts, names, dates, quotes, or URLs. "
              "Produce the stage output exactly in the format the task specifies.")
    if rules.exists():
        system += "\n\n--- MASTER_RULE.md ---\n" + rules.read_text(encoding="utf-8")[:8000]
    contract = (
        "\n\n=== OUTPUT CONTRACT (critical — overrides any earlier 'save the file' wording) ===\n"
        f"- Respond with ONLY the finished {outfile} document, in the exact format specified above.\n"
        "- NO preamble, narration, or meta-commentary. Do not write 'I'll research...', 'Let me search...',\n"
        "  'I've saved it...', or 'Here's a summary'. Your FIRST character must be the document's first line.\n"
        "- You are NOT writing or saving any file. Your response text itself IS the document.\n"
        "- Produce EVERY required section IN FULL — not a condensed summary.\n"
        "- In the Sources section, list the real URLs you actually found via web search. If a URL is\n"
        "  unconfirmed, write 'URL not confirmed' — never invent one.\n"
        f"- Write the entire document in: {ctx.get('language', 'en')}.\n"
    )
    user = (("\n\n".join(prior) + "\n\n") if prior else "") + prompt + contract

    print(f"[stage {stage}] {stem} -> {outfile}  (web_search={use_search})")
    if dry:
        print(f"  DRY: system {len(system)} chars, user {len(user)} chars; would call {MODEL}")
        return 0
    if not api_key():
        sys.exit("[ERROR] ANTHROPIC/EXPO_PUBLIC_ANTHROPIC_API_KEY not in .env")
    t0 = time.time()
    out = call_claude(system, user, use_search)
    (proj / outfile).write_text(out, encoding="utf-8")
    upd_manifest(proj, stage, outfile, len(out), time.time() - t0)
    print(f"  wrote {outfile} ({len(out)} chars) in {time.time()-t0:.0f}s")
    return 0


def upd_manifest(proj: Path, stage: int, outfile: str, nchars: int, secs: float) -> None:
    mf = proj / "pipeline_manifest.json"
    data = json.loads(mf.read_text()) if mf.exists() else {"project": proj.name, "stages": {}}
    data["stages"][str(stage)] = {
        "output": outfile, "chars": nchars, "seconds": round(secs, 1),
        "completed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    data["last_completed_stage"] = max(int(k) for k in data["stages"])
    mf.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def cmd_init(topic: str, niche: str, language: str, length: int, style: str) -> int:
    slug = time.strftime("%Y%m%d_") + slugify(topic)
    proj = PROJECTS / slug
    if proj.exists():
        sys.exit(f"[ERROR] project already exists: {proj}")
    proj.mkdir(parents=True)
    inp = {"topic": topic, "language": language, "niche": niche,
           "video_length_minutes": length, "style": style, "notes": ""}
    (proj / "input.json").write_text(json.dumps(inp, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Initialized project: {proj.relative_to(REPO)}")
    print(f"  next: python tools/orchestrator/run_pipeline.py --project {slug} --stage 1")
    return 0


def main() -> int:
    load_env()
    ap = argparse.ArgumentParser(description="AI-Youtube-Studio pipeline orchestrator")
    ap.add_argument("--init", metavar="TOPIC", help="create a new project")
    ap.add_argument("--niche", default="japanese_mystery")
    ap.add_argument("--language", default="ja")
    ap.add_argument("--length", type=int, default=12)
    ap.add_argument("--style", default="dark_documentary")
    ap.add_argument("--project", metavar="SLUG", help="existing project slug")
    ap.add_argument("--stage", type=int, help="run one stage (1-10)")
    ap.add_argument("--all", action="store_true", help="run all remaining stages")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    if a.init:
        return cmd_init(a.init, a.niche, a.language, a.length, a.style)
    if not a.project:
        ap.print_help(); return 0
    proj = PROJECTS / a.project
    if not (proj / "input.json").exists():
        sys.exit(f"[ERROR] no input.json in {proj} (run --init first)")
    if a.stage:
        return run_stage(proj, a.stage, a.dry_run)
    if a.all:
        mf = proj / "pipeline_manifest.json"
        start = (json.loads(mf.read_text())["last_completed_stage"] + 1) if mf.exists() else 1
        for s in range(start, 11):
            rc = run_stage(proj, s, a.dry_run)
            if rc: return rc
        return 0
    ap.print_help(); return 0


if __name__ == "__main__":
    raise SystemExit(main())
