# How to Run Director AI v1 — AI YouTube Studio OS

A step-by-step guide for running the Director AI to produce a complete YouTube video content package.

---

## Prerequisites

Before running Director AI, confirm:

- [ ] You are in the `AI-Youtube-Studio/` project directory
- [ ] The full directory structure exists (run `ls` to confirm the folders below)
- [ ] All system files are present (README.md, MASTER_PLAN.md, MASTER_RULE.md, WORKFLOW.md, STYLE_GUIDE.md, all files in core/, engine/, configs/, templates/, prompts/)
- [ ] You have Claude Code open in this directory

**Required directories:**
```
agents/
configs/
core/
engine/
knowledge/
projects/
prompts/
templates/
```

---

## Step 1 — Prepare Your Inputs

Decide on the four required inputs for your video:

| Input | Options | Example |
|---|---|---|
| `TOPIC` | Any subject | "The Disappearance of Elisa Lam" |
| `LANGUAGE` | `en` / `ja` / `vi` | `en` |
| `DURATION_MINUTES` | Integer 5–60 | `12` |
| `STYLE` | `dark_documentary` / `reddit_narration` / `mystery_investigation` / `japanese_mystery` | `dark_documentary` |

**Style guide:**
- `dark_documentary` — authoritative, researched, cinematic narration
- `reddit_narration` — first-person reading of a post, community reaction, current status
- `mystery_investigation` — progressive reveal, evidence-based, map-heavy
- `japanese_mystery` — slower pacing, cultural context, Ma (間) principle, です/ます

---

## Step 2 — Start Claude Code and Load the Director

Open Claude Code and paste the entire contents of `agents/director_ai_v1.md` as your first message.

Then on the next line, provide your four inputs:

```
TOPIC: The Disappearance of Elisa Lam
LANGUAGE: en
DURATION_MINUTES: 12
STYLE: dark_documentary
```

**What happens next:**
1. Director AI boots and reads all system files (you will see the boot confirmation message)
2. Director AI confirms your inputs are valid
3. Director AI creates a new project folder at `projects/YYYYMMDD_topic-slug/`
4. Director AI begins Stage 0

---

## Step 3 — Monitor the Pipeline

The Director AI announces every stage start and end. You will see progress like:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STAGE 1 — RESEARCH
Project: 20260627_disappearance-of-elisa-lam
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Stage 1] Reading prompt: prompts/01_research.md
[Stage 1] Generating research brief...
[Stage 1] Writing research/research.md...
[Stage 1] Running checklist (10 items)...
[STAGE 1 COMPLETE]
Output:     research/research.md
Checklist:  10/10 passed
Warnings:   0
Status:     PASS
──────────────────────────────────────────────
```

**You do not need to do anything while the pipeline runs.** Director AI handles all stages automatically. Only intervene if:
- The pipeline halts with an error (a `⛔ CRITICAL` or `❌ FAIL` message)
- You want to review and edit content at a specific stage (see Step 5)

---

## Step 4 — Handle Errors (if any)

### If you see a CRITICAL error:

```
⛔ CRITICAL ERROR — Pipeline Halted
Error Code:   ERR_CRITICAL_006
Stage:        2 — Source Verification
...
```

Read the error message carefully. It tells you:
1. What went wrong
2. Why it's critical
3. What you need to do to fix it

Fix the issue (e.g., update `research/research.md` with better sources), then resume:
```
RESUME PROJECT: 20260627_disappearance-of-elisa-lam
```

### If you see a STAGE FAIL error:

Similar to above — read the specific failed check, fix the file, and resume.

### If you see warnings (⚠):

Warnings do not stop the pipeline. The Director logs them and continues. Review the warnings in `logs/director_run_log.md` after the pipeline completes.

---

## Step 5 — Optional: Review Content Mid-Pipeline

You can review and edit content at any point between stages. The best review points are:

| After Stage | What to review | Can you edit? |
|---|---|---|
| Stage 1 | `research/research.md` — is the research complete? | Yes — then re-run Stage 2 |
| Stage 2 | `research/source_report.md` — are you happy with the ratings? | Yes — may need to re-run Stage 2 |
| Stage 3 | `script/story_outline.md` — is the structure right for your vision? | Yes — then re-run Stage 4 |
| Stage 4 | `script/script.md` — is the narration the right tone? | Yes — then re-run Stages 5-12 |
| Stage 9 | `voice/voice_script.txt` — does it read well aloud? | Yes — minor edits only |
| Stage 10 | `seo/seo.md` — do the titles work for your channel? | Yes — final human choice |

To resume after a mid-pipeline edit:
```
RESUME PROJECT: {project_slug}
```

The Director reads the manifest and resumes from the earliest incomplete stage.

---

## Step 6 — Review the Final Output

When the pipeline completes successfully:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DIRECTOR AI v1 — PIPELINE COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Project: 20260627_disappearance-of-elisa-lam
Status:  READY FOR PRODUCTION ✓
...
```

Open `projects/{project_slug}/export/project_report.md` first. This is the human-readable summary of everything that was produced.

Then open each file in sequence for review:

1. `research/research_verified.md` — confirm the facts are solid
2. `script/script.md` — read the full script (listen to it aloud if possible)
3. `visuals/storyboard.md` — visualize the shot list
4. `visuals/image_plan.md` — start sourcing real images
5. `visuals/ai_image_prompts.md` — generate AI images where needed
6. `voice/voice_script.txt` — paste into ElevenLabs
7. `seo/seo.md` — choose a title and prepare the description
8. `seo/thumbnail_prompt.md` — design the thumbnail

---

## Step 7 — Post-Production

After reviewing the output files, complete these manual steps:

**Audio:**
1. Paste `voice/voice_script.txt` into ElevenLabs
2. Apply settings from `voice/voice_direction.md`
3. Generate audio → save as `voice/voice_output.mp3`

**Images:**
1. Source real images using search strategies in `visuals/image_plan.md`
2. Generate AI images using prompts in `visuals/ai_image_prompts.md`
3. Design thumbnail using `seo/thumbnail_prompt.md`

**Video editing:**
1. Import audio into your editor
2. Follow `visuals/storyboard.md` for shot sequence
3. Add `voice/subtitles.srt` (update timecodes to match actual audio)
4. Export video

**YouTube upload:**
1. Upload video
2. Fill title, description, tags from `seo/seo.md`
3. Add thumbnail
4. Set to `private` for final review, then publish
5. Immediately post one of the pinned comment options from `seo/seo.md`

---

## Common Questions

**Q: How long does the pipeline take?**
A: Depends on the model and duration. A 10-minute video on claude-opus-4-8 with adaptive thinking typically takes 15-25 minutes of AI generation time across all stages.

**Q: Can I run multiple projects at the same time?**
A: Yes. Each project is isolated in its own `projects/{slug}/` folder. You would need separate Claude Code sessions.

**Q: What if the script word count is too short or too long?**
A: The Director auto-retries once with an explicit count instruction. If it still fails, resume the project and it will re-run Stage 4 with stronger constraints.

**Q: The pipeline produced research I'm not happy with. Can I completely redo Stage 1?**
A: Yes. Open `export/export_manifest.json`, set `research.status` and `research_verified.status` to `absent`, then resume the project.

**Q: What does "NEEDS_REVISION" mean in the source report?**
A: Some claims were flagged — not confirmed but not definitively false. The pipeline continues, but the flagged claims are labeled in `research_verified.md`. Review them before scripting.

**Q: Can I use this for topics outside the mystery niche?**
A: The system is optimized for mystery content. It will still work for other topics, but the templates and prompts are tuned for the mystery niche. For other niches, you would need to add new templates in `templates/` and update the routing in `engine/routing_engine.md`.

---

## File Reference

| File | Purpose | When to open it |
|---|---|---|
| `agents/director_ai_v1.md` | The Director AI prompt | Every new production run |
| `agents/director_runtime_protocol.md` | Runtime behavior reference | When the pipeline behaves unexpectedly |
| `agents/director_error_handling.md` | Error code reference | When an error occurs |
| `agents/director_project_checklist.md` | Validation checklists | When debugging a failed stage |
| `configs/project.yaml.example` | All available config options | When setting up a project |
| `projects/_PROJECT_TEMPLATE/` | Folder structure reference | When creating a new project manually |
| `docs/roadmap_v1.md` | v1 scope and limitations | When wondering if a feature is supported |

---

## Known Limitations in v1

| Limitation | Workaround |
|---|---|
| No actual image generation | Use `ai_image_prompts.md` with external tools |
| No TTS generation | Use `voice_script.txt` with ElevenLabs manually |
| No video rendering | Use `storyboard.md` with your video editor |
| No YouTube upload | Use `seo.md` to fill YouTube Studio manually |
| No MCP integration | Run Director AI manually in Claude Code |
| Pipeline requires one session | Use Resume protocol if session is interrupted |

All of these are addressed in the v2.0 roadmap. See `docs/roadmap_v2.md` for details.
