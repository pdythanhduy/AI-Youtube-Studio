# Full-Scale Autopilot Validation Report (Blocker #3)

**Date:** 2026-06-29
**Scope:** One complete full-scale autopilot video through the entire pipeline with real
QA (LLM on) and the human-review loop, to validate production readiness before VPS
go-live. No VPS deploy, no YouTube upload, no auto-publish, no `--skip-qa`, no weakened
gates, no Hashima change.

## Project
- **project_id:** `20260629_t-661ebbe9`
- **topic:** 友ヶ島：日本の無人島に残る砲台跡の謎
- **language / niche:** ja / japanese_mystery
- **command:** `python tools/run_all.py --topic "友ヶ島：…" --niche japanese_mystery --language ja --deliver`

## Pipeline completion (all stages, no limits)
TEXT (10/10) → IMAGES (7) → TTS (106 segments) → RENDER → QA GATE (LLM) → DELIVER ✅

Files generated: research.md, research_verified.md, story.md, story_bible.md, script.md,
storyboard.md, image_plan.md, image_prompts.md, voice_script.txt, seo.md;
`assets/images/beat_*.jpg` ×7; `assets/audio/seg_*.mp3` ×106;
`export/rough/20260629_t-661ebbe9_rough.mp4`; `runtime/20260629_t-661ebbe9/human_review_manifest.json`.

## Output
| | |
|---|---|
| video | `projects/20260629_t-661ebbe9/export/rough/20260629_t-661ebbe9_rough.mp4` |
| duration | **608.5 s (10:08)** |
| file size | **40.6 MB** |
| video / audio | H.264 1920×1080 / AAC — **full decode clean (no errors)** |
| image count | 7 |
| TTS segment count | 106 |
| delivered | Telegram (Drive link) — for human review |

## QA result (real, LLM enabled)
| Check | Status | Note |
|---|---|---|
| source | **PASS** | facts corroborated; disputed items (Laputa/Ghibli, army-treasure, 大坂約定) flagged; minor: 2 sources show implausible "2026" access-dates |
| script | **PASS** | claims grounded; ~600-soldier figure & treasure hedged as weak/unverified; dark-doc framing about a fortress, not victims; no fabrication / fake-shock / horror |
| image | **PASS** | vision: no identifiable faces, no gore/victims |
| render | **PASS** | audio valid; video decodes cleanly |

`safety_status = pass` · `automatic_checks_passed = true` · `gate_status = READY_FOR_HUMAN_REVIEW`
· `required_human_decision = approve` · **`upload_allowed = false`**.

## Output-quality verification
video exists ✅ · decodes cleanly ✅ · audio exists (106) ✅ · no black placeholder cards
(image L-stddev 43–83, threshold ~6) ✅ · no missing images/audio ✅ · no gore/horror/victim
(QA vision + script PASS) ✅ · no fake source (source PASS) ✅ · no unsupported "shock" title
(hooks grounded) ✅ · language = ja ✅ · **upload_allowed = false** ✅.

## Human review loop (token-free simulation)
| Path | Result |
|---|---|
| approve (owner, real manifest) | `HUMAN_APPROVED`, upload_allowed=False ✅ |
| revise (owner, copy) | `NEEDS_REVISION`, upload_allowed=False ✅ |
| reject by unknown user | **REFUSED** (`unauthorized`), rc=1 ✅ |

Approval did **not** set upload_allowed true (invariant held).

## Cost & runtime (approx)
- **Runtime:** ~35 min (21:05 → 21:40), single 2-core dev machine.
- **Claude:** 10 text stages (Opus 4.8, web search on research) + QA (source + script + 7 image-vision) ≈ **$2–3**.
- **FLUX (fal):** 7 images × ~$0.04 ≈ **$0.28**.
- **Vbee TTS:** 106 segments (account credit; per-segment small).
- **Estimated total:** ~**$2.5–3.5** + Vbee credit.

## Blockers found
- **None safety-blocking.** Minor quality nits (non-blocking): (1) a couple of source access-dates
  rendered as "2026" (date hygiene, not fabrication); (2) render is still a rough even-split
  slideshow (~87 s/image over 7 images) — acceptable rough cut, below the hand-crafted Hashima bar
  (motion cards / Ken-Burns / pacing are the polish backlog).

## VPS go-live verdict
**Validated — go-live is now allowed for the autopilot mechanics.** The full pipeline completes,
QA is real and enforced, the gate produces the manifest, delivery is gated on PASS, the human
review loop works, and `upload_allowed` stays false end-to-end. The only remaining item is **M4
deployment** (create `STUDIO_BOT_TOKEN` via @BotFather, deploy `studio_bot.py` on the VPS) — an
operational step, not a pipeline blocker. YouTube upload remains a separate, explicit, human gate
(no automation added).
