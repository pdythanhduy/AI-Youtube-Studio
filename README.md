# AI YouTube Studio OS

A reusable AI content production system for YouTube channels. Input a topic — get a complete, publish-ready video package.

---

## What This Is

This is not a prompt library. It is an operating system for producing YouTube videos at scale using AI. Every file in this project serves a specific function in the production pipeline. Together they define how to go from a raw topic to a fully packaged video — consistently, repeatably, and automatically.

**Primary niche:** Internet Mystery, Japanese Mystery, Reddit Mystery, strange online stories, Google Maps mysteries, lost places, unexplained events.

---

## Quick Start

### User Inputs (required)

| Input | Description | Example |
|---|---|---|
| `topic` | The core subject of the video | "The Disappearance of Elisa Lam" |
| `language` | Target language for script and subtitles | `en`, `ja`, `vi` |
| `video_length` | Target duration in minutes | `8`, `12`, `20` |
| `style` | Narrative style (see STYLE_GUIDE.md) | `dark_documentary`, `reddit_narration`, `mystery_investigation` |

### System Outputs (generated)

| Output | File |
|---|---|
| Research brief + sources | `research.md` |
| Full narration script | `script.md` |
| Scene-by-scene storyboard | `storyboard.md` |
| Image plan (real vs AI) | `image_plan.md` |
| Voice script (TTS-ready) | `voice_script.txt` |
| Subtitle file | `subtitles.srt` |
| Thumbnail prompt | `thumbnail_prompt.md` |
| SEO package | `seo.md` |
| Export manifest | `export_manifest.json` |

---

## Project Files

| File | Purpose |
|---|---|
| `README.md` | This file. Quick-start guide. |
| `MASTER_PLAN.md` | System architecture, folder structure, component specs |
| `MASTER_RULE.md` | Core operating rules, quality standards, image policy |
| `WORKFLOW.md` | Step-by-step production pipeline from topic to export |
| `STYLE_GUIDE.md` | Visual, narrative, voice, and editing consistency rules |

---

## Folder Structure

```
AI-Youtube-Studio/
├── README.md
├── MASTER_PLAN.md
├── MASTER_RULE.md
├── WORKFLOW.md
├── STYLE_GUIDE.md
│
├── projects/                  # One subfolder per video
│   └── YYYYMMDD_topic-slug/
│       ├── input.json         # User inputs
│       ├── research.md
│       ├── script.md
│       ├── storyboard.md
│       ├── image_plan.md
│       ├── voice_script.txt
│       ├── subtitles.srt
│       ├── thumbnail_prompt.md
│       ├── seo.md
│       └── export_manifest.json
│
├── templates/                 # Reusable prompt templates
│   ├── research_prompt.md
│   ├── script_prompt.md
│   ├── storyboard_prompt.md
│   ├── seo_prompt.md
│   └── thumbnail_prompt.md
│
└── assets/                    # Shared static assets
    ├── channel_intro.mp3
    ├── channel_outro.mp3
    ├── music/
    └── fonts/
```

---

## Design Principles

1. **Inputs are minimal.** Four fields. Nothing more required.
2. **Outputs are complete.** Every asset needed for production is generated.
3. **Rules are explicit.** No ambiguity about quality, style, or image sourcing.
4. **Automation-ready.** Every step is designed to be executed by a Claude Code agent.
5. **Consistent.** The same style guide governs every video, regardless of topic.

---

## Version

`v1.0` — First production-ready version. Designed for single-agent automation with Claude Code.
