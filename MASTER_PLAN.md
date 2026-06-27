# MASTER PLAN — AI YouTube Studio OS

System architecture, component specifications, input/output contracts, and folder structure.

---

## System Overview

The AI YouTube Studio OS is a modular production pipeline. Each component takes a defined input, performs a specific task, and produces a defined output. Components are stateless — they can be run independently or chained together by an orchestration agent.

```
[User Input]
     │
     ▼
[1. Research]  →  research.md
     │
     ▼
[2. Script]    →  script.md
     │
     ▼
[3. Storyboard] → storyboard.md
     │
     ▼
[4. Image Plan] → image_plan.md
     │
     ▼
[5. Voice Script] → voice_script.txt
     │
     ▼
[6. Subtitles]  → subtitles.srt
     │
     ▼
[7. Thumbnail]  → thumbnail_prompt.md
     │
     ▼
[8. SEO]        → seo.md
     │
     ▼
[9. Export]     → export_manifest.json
```

---

## Input Contract

Every project begins with `input.json`. This file is the single source of truth for all downstream components.

```json
{
  "topic": "The Disappearance of Elisa Lam",
  "language": "en",
  "video_length_minutes": 12,
  "style": "dark_documentary",
  "niche": "internet_mystery",
  "channel_name": "Mystery Archive",
  "target_audience": "18-35, mystery and true crime fans",
  "notes": "Focus on the Cecil Hotel. Include the elevator footage analysis."
}
```

### Field Definitions

| Field | Type | Required | Description |
|---|---|---|---|
| `topic` | string | yes | Main subject of the video |
| `language` | string | yes | ISO 639-1 code (en, ja, vi, etc.) |
| `video_length_minutes` | integer | yes | Target duration in minutes |
| `style` | string | yes | Must match a style in STYLE_GUIDE.md |
| `niche` | string | yes | Content category (see Niches section) |
| `channel_name` | string | no | Used in outro and SEO |
| `target_audience` | string | no | Informs tone and complexity |
| `notes` | string | no | Specific instructions or angles to include |

### Supported Niches

| Niche ID | Description |
|---|---|
| `internet_mystery` | Viral mysteries, online unsolved cases, digital lore |
| `japanese_mystery` | Japanese urban legends, disappearances, strange phenomena |
| `reddit_mystery` | Reddit posts: NoSleep, AskReddit, Unresolved Mysteries |
| `google_maps_mystery` | Anomalies found on Google Maps/Earth |
| `lost_places` | Abandoned buildings, ghost towns, forgotten history |
| `unexplained_events` | Paranormal, strange physics, unexplained phenomena |

---

## Component Specifications

### Component 1: Research

**Input:** `input.json`

**Task:** Generate a structured research brief covering the topic. Include verified facts, key timeline, named individuals, locations, and unresolved questions. Flag claims that need source verification.

**Output:** `research.md`

```markdown
# Research: [Topic]

## Summary
[2-3 sentence overview]

## Key Facts
- [Fact 1 — Source]
- [Fact 2 — Source]

## Timeline
| Date | Event |
|---|---|
| YYYY-MM-DD | Event description |

## Key People
| Name | Role |
|---|---|
| Person | Their connection to the story |

## Key Locations
- Location name — significance

## Unresolved Questions
- What is still unknown?

## Sources
- [Title](URL) — type: news/wiki/documentary/reddit
```

**Quality standard:** Minimum 5 verified facts. At least 3 named sources. No fabricated URLs.

---

### Component 2: Script

**Input:** `input.json` + `research.md`

**Task:** Write a full narration script for the video. Structured as scenes. Matches target video length (approximately 130 words per minute for English narration).

**Output:** `script.md`

```markdown
# Script: [Topic]

## Hook (0:00 - 0:30)
[Opening lines — grab attention immediately]

## Introduction (0:30 - 1:30)
[Establish context, stakes, and what the viewer will learn]

## Scene 1: [Name] (1:30 - 4:00)
[Narration text]

## Scene 2: [Name] (4:00 - 7:00)
[Narration text]

## Conclusion (X:XX - X:XX)
[Resolution or open question — call to action]

---
Total estimated word count: [N]
Estimated runtime: [N] minutes
```

**Quality standard:** Hook must be under 30 seconds. Every scene must have a clear narrative purpose. No filler.

**Word count targets by video length:**

| Length | Word Count |
|---|---|
| 8 min | ~1,000 words |
| 12 min | ~1,500 words |
| 20 min | ~2,500 words |

---

### Component 3: Storyboard

**Input:** `script.md`

**Task:** Translate each scene into a visual storyboard. Describe what appears on screen for each 30-60 second segment.

**Output:** `storyboard.md`

```markdown
# Storyboard: [Topic]

## Scene 1 — [Name]
- **Timecode:** 0:00 - 0:30
- **Narration:** [First line of narration for this beat]
- **Visual:** [What the viewer sees — photo, video, map, text overlay, AI image]
- **Image type:** real / ai-generated / stock / text-overlay
- **Source note:** [If real: where to find it. If AI: short prompt idea]
- **Music:** [Ambient / intense / silence]
- **Text overlay:** [Any on-screen text, none if not needed]
```

**Quality standard:** Every narration beat must have a corresponding visual. No unplanned black screens.

---

### Component 4: Image Plan

**Input:** `storyboard.md`

**Task:** For every visual in the storyboard, specify exactly where the image or video comes from and how to obtain it.

**Output:** `image_plan.md`

```markdown
# Image Plan: [Topic]

| # | Scene | Type | Source Strategy | Search Terms / Prompt |
|---|---|---|---|---|
| 1 | Hook | real | Google Images / news archives | "Elisa Lam Cecil Hotel elevator" |
| 2 | Scene 1 | ai-generated | Midjourney / DALL-E | "dark hotel corridor, cinematic, 1950s, fog" |
| 3 | Scene 2 | stock | Pixabay / Pexels | "Los Angeles night skyline" |
| 4 | Scene 3 | screenshot | Reddit / original post | Direct screenshot of r/UnresolvedMysteries thread |
```

**Image type rules:** See MASTER_RULE.md — Image Policy section.

**Quality standard:** Every image slot must be filled before production begins. No "TBD" in final image plan.

---

### Component 5: Voice Script

**Input:** `script.md`

**Task:** Reformat the script for TTS (text-to-speech) use. Remove all markdown, stage directions, and scene headers. Add pacing markers. Output clean plain text ready for ElevenLabs or similar.

**Output:** `voice_script.txt`

```
[PAUSE:1s] In January of 2013, a 21-year-old student checked into the Cecil Hotel in downtown Los Angeles.
[PAUSE:0.5s] No one could have predicted what would happen next.
[PAUSE:1.5s] This is the story of Elisa Lam.
[PAUSE:2s]
```

**Pacing markers:**
- `[PAUSE:0.5s]` — short breath
- `[PAUSE:1s]` — natural sentence pause
- `[PAUSE:1.5s]` — scene transition pause
- `[PAUSE:2s]` — dramatic pause (use sparingly)
- `[SLOW]` / `[NORMAL]` / `[FAST]` — pacing instruction

**Quality standard:** No markdown. No brackets except pacing markers. Clean, readable plain text.

---

### Component 6: Subtitles

**Input:** `voice_script.txt` + estimated TTS output timing

**Task:** Generate a properly formatted SRT subtitle file. Segment into short readable lines (max 42 characters per line, max 2 lines per segment, max 7 seconds per segment).

**Output:** `subtitles.srt`

```
1
00:00:00,000 --> 00:00:04,200
In January of 2013, a 21-year-old student

2
00:00:04,200 --> 00:00:07,800
checked into the Cecil Hotel
in downtown Los Angeles.
```

**Quality standard:** Max 42 chars per line. No segment longer than 7 seconds. Timecodes must be sequential and non-overlapping.

---

### Component 7: Thumbnail Prompt

**Input:** `input.json` + `script.md` (hook section)

**Task:** Generate a detailed image generation prompt for the video thumbnail. Must be designed for high CTR in the mystery niche.

**Output:** `thumbnail_prompt.md`

```markdown
# Thumbnail Prompt: [Topic]

## Concept
[One sentence describing the visual idea]

## Image Generation Prompt
[Full prompt for Midjourney or DALL-E]

## Text Overlay
- Main text: [BOLD HEADLINE — max 4 words]
- Sub text: [optional secondary line]
- Text position: [top / bottom / left / right]

## Color Palette
- Primary: [hex or description]
- Accent: [hex or description]
- Background tone: [dark / light / gradient]

## Style References
[Describe comparable thumbnails for reference]
```

**Quality standard:** Prompt must be self-contained. A designer or AI tool must be able to produce the thumbnail from the prompt alone, without reading the script.

---

### Component 8: SEO Package

**Input:** `input.json` + `script.md` + `research.md`

**Task:** Generate a complete YouTube SEO package for the video.

**Output:** `seo.md`

```markdown
# SEO Package: [Topic]

## Title Options (pick one)
1. [Title option — max 70 chars]
2. [Title option — max 70 chars]
3. [Title option — max 70 chars]

## Description
[Full YouTube description — first 150 chars must hook the viewer]
[Include natural keywords]
[Include timestamps]
[Include links section placeholder]

## Tags
tag1, tag2, tag3, tag4, tag5 (min 15, max 30 tags)

## Hashtags (for description)
#Mystery #TrueCrime #[TopicSpecific]

## Chapters (Timestamps)
0:00 - Introduction
1:30 - [Scene name]
...

## Search Keywords Targeted
- Primary: [main keyword]
- Secondary: [keyword 2], [keyword 3]
- Long-tail: [full question people search for]
```

**Quality standard:** Title max 70 chars. Description must include at least one natural keyword in the first sentence. Minimum 15 tags.

---

### Component 9: Export Manifest

**Input:** All previous outputs

**Task:** Generate a structured JSON file listing all project assets, their status, and their file paths. Used by editors and automation agents.

**Output:** `export_manifest.json`

```json
{
  "project_id": "20240115_elisa-lam",
  "topic": "The Disappearance of Elisa Lam",
  "status": "ready_for_production",
  "created_at": "2024-01-15T14:30:00Z",
  "assets": {
    "research": { "file": "research.md", "status": "complete" },
    "script": { "file": "script.md", "status": "complete" },
    "storyboard": { "file": "storyboard.md", "status": "complete" },
    "image_plan": { "file": "image_plan.md", "status": "complete" },
    "voice_script": { "file": "voice_script.txt", "status": "complete" },
    "subtitles": { "file": "subtitles.srt", "status": "complete" },
    "thumbnail_prompt": { "file": "thumbnail_prompt.md", "status": "complete" },
    "seo": { "file": "seo.md", "status": "complete" }
  },
  "metadata": {
    "language": "en",
    "video_length_minutes": 12,
    "style": "dark_documentary",
    "niche": "internet_mystery",
    "word_count": 1520,
    "image_count": 18,
    "ai_image_count": 7,
    "real_image_count": 11
  }
}
```

---

## Automation Agent Design

Each component is designed to be run by a Claude Code agent with the following pattern:

```
AGENT TASK: [Component Name]

Read: input.json [+ any prerequisite files]
Apply: templates/[component]_prompt.md
Write: [output file]
Validate: [quality checklist from this document]
Update: export_manifest.json — set status to "complete"
```

The orchestration agent runs components in order, passing outputs as inputs to the next step. If any component fails validation, it is flagged in `export_manifest.json` and the pipeline halts.

---

## Version History

| Version | Date | Notes |
|---|---|---|
| 1.0 | 2026-06-26 | Initial system design |
