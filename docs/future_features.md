# Future Features — AI YouTube Studio OS

Long-term vision and feature ideas for versions beyond v2.0. These are not committed plans — they are design-level thinking about where this system could go. Features here are written as capability descriptions, not implementation specs.

---

## v3.0 Vision: Multi-Channel and Multi-Agent

v3.0 transforms the system from a single-channel production tool into a multi-channel AI content company infrastructure. Multiple independent AI agents work in parallel, each producing a different video for a different channel, coordinated by a master Director.

---

## Feature Areas

### 1. YouTube Integration (v2.0+)

**What:** Direct integration with the YouTube Data API v3 to automate the upload process.

**Capability:**
- Export Engine calls YouTube API to create a video draft
- Pre-populates: title, description, tags, chapters, thumbnail (uploaded separately)
- Sets: category, language, default subtitle language
- Status on creation: `private` — never auto-publish

**Why private on creation:** Human must review the video before it goes live. The system can prepare everything, but a human presses "publish."

**Implementation notes:**
- OAuth2 authentication stored per channel (not in this repo)
- Rate limits: YouTube API has daily quota limits — analytics requests and upload are separate quota buckets
- Thumbnail upload is a separate API call from video metadata
- Playlists: system adds video to appropriate playlist based on niche

---

### 2. TTS Auto-Generation (v2.0+)

**What:** Export Engine calls ElevenLabs (or similar) API with `voice_script.txt` to generate audio automatically.

**Capability:**
- Voice selected from config: `configs/language_profiles.md → tts.recommended_voice_id`
- Settings applied from `voice_direction.md` ElevenLabs section
- Output: `voice_output.mp3` in project folder
- Audio normalized to YouTube spec: -14 LUFS, -1 dBTP peak

**Design notes:**
- Voice_id must be configured per channel (not stored in the system)
- For Japanese/Vietnamese: requires native-language voice selection
- Cost tracking: TTS tokens are separately metered and tracked in analytics

---

### 3. Automated Image Collection (v3.0)

**What:** Image Finder Engine makes real API calls to source images automatically.

**Capability:**
- For each `real` image beat in `image_plan.md`: execute the search strategy
- Call Wikimedia Commons API for public domain images
- Call Pexels/Pixabay API for stock images
- Call Google Custom Search API for news images (with license filter)
- Download approved images to `projects/{slug}/images/` folder
- Update `image_plan.md` with actual file paths after download

**Legal safeguards:**
- Only images with confirmed usable license are downloaded automatically
- Fair use images are flagged for human review before download
- AI-generated beats are added to a generation queue (not auto-generated — costs are too variable)

---

### 4. Multi-Channel Management (v3.0)

**What:** The system manages multiple YouTube channels simultaneously, each with its own config, style, and niche preferences.

**Capability:**
- `channels/` directory with one config per channel
- Director Engine routes projects to the correct channel config
- Analytics tracked per channel (not just per project)
- Memory Engine maintains separate source databases per channel (or shared, configurable)
- Learning Engine runs per-channel learning cycles

**Channel config structure:**
```
channels/
├── channel_mystery_archive/
│   ├── channel_config.json     ← channel-level overrides
│   ├── channel_style.md        ← channel-specific style rules
│   └── channel_assets/         ← intros, outros, thumbnails
└── channel_japan_mystery/
    ├── channel_config.json
    └── ...
```

---

### 5. Agent Orchestration via Managed Agents API (v3.0)

**What:** Replace the manually-triggered pipeline with a persistent Managed Agent that runs autonomously.

**Capability:**
- Each project is a Managed Agent session with its own workspace
- The Director Agent creates a session for each project
- Worker agents (one per stage) execute stages in their own sub-sessions
- All communication is via SSE event stream — real-time progress visible in a dashboard
- Agent sessions are versioned — revert to any previous state

**Why Managed Agents over self-hosted:**
- Per-session container isolation — each project's files are in a separate workspace
- Anthropic manages the loop — no need to build retry/timeout logic
- Long-running sessions can survive hours without timeout
- Skills and MCP tools available in-session

---

### 6. Performance Feedback Loop (v3.0+)

**What:** After a video is published and has 30 days of performance data, the system ingests YouTube analytics and correlates production decisions with audience outcomes.

**Capability:**
- Ingest via YouTube Analytics API: views, watch time, CTR, average view duration, subscriber conversion
- Store in `knowledge/memory_database.md#performance_data`
- Correlation analysis: which niches have highest CTR? Which styles have longest watch time? Which hook types convert best?
- Learning Engine uses performance data alongside QA data for recommendations

**Virtuous cycle:**
```
Produce video → Publish → 30-day performance data → 
Learning Engine analysis → Prompt improvements → 
Better future videos → Better performance
```

---

### 7. Short-Form Adaptation (v3.0)

**What:** From any completed long-form project, automatically generate a Shorts version.

**Capability:**
- New stage: `11_shorts_adapter.md`
- Input: `script.md` + `storyboard.md`
- Output: `shorts_script.md`, `shorts_storyboard.md`, `shorts_seo.md`
- Shorts format: 45-60 seconds, single hook + payoff, vertical 9:16
- Derived from the most compelling 45-60 second section of the original video

---

### 8. Multilingual Dubbing (v4.0)

**What:** Take a completed English project and generate parallel versions in Japanese and Vietnamese.

**Capability:**
- New stage: `12_translation_adapter.md`
- Input: `script.md` (source language) + `voice_script.txt` + `story_bible.md`
- Output: `script_[lang].md`, `voice_script_[lang].txt`, `subtitles_[lang].srt`, `seo_[lang].md`
- The translation is culturally adapted, not literal — niche-appropriate register and tone

**Challenges:**
- Cultural concepts that do not translate directly
- Name romanization differences between languages
- SEO keyword strategy differs significantly by language market

---

### 9. MCP Server for External Tool Integration (v2.0+)

**What:** The system exposes an MCP server that external tools and Claude Code agents can call.

**Tools exposed:**

| Tool | Description |
|---|---|
| `studio.run` | Start a new production run |
| `studio.status` | Get pipeline status for a project |
| `studio.resume` | Resume an interrupted run |
| `studio.approve` | Approve a human-escalation decision |
| `studio.export` | Trigger export for a ready project |
| `studio.search_sources` | Query the source database |
| `studio.search_assets` | Query the asset library |

**Resources exposed (MCP resources):**

| Resource | Content |
|---|---|
| `studio://projects` | List of all active projects |
| `studio://knowledge/sources` | Source database |
| `studio://knowledge/memory` | Project memory entries |
| `studio://config/styles` | Available styles |
| `studio://config/languages` | Supported languages |

---

### 10. Visual Studio Interface (v4.0)

**What:** A web-based UI for managing production runs, reviewing outputs, and approving decisions.

**Capability:**
- Dashboard: all active and completed projects with pipeline status
- Stage viewer: read each stage output inline in the browser
- QA reviewer: step through checklist items, mark pass/fail
- Decision queue: pending human-escalation decisions with one-click approve/reject
- Asset gallery: browse sourced and generated images
- Analytics charts: production metrics over time

**Technology:** Standard web stack — this is a separate project from the core AI system. The UI calls the MCP server for all AI operations.

---

## Features Intentionally Deferred

Some capabilities that might seem obvious are intentionally out of scope indefinitely:

| Feature | Why Deferred |
|---|---|
| Auto-publish to YouTube | Too much risk — human must always approve before publish |
| Automatic social media posting | Out of scope for core production system |
| Comment management | Different product category — not part of production |
| Revenue tracking | Monetization is channel-level, not project-level |
| Multi-platform (TikTok, Instagram) | Different format requirements — separate system |
| Real-time collaboration | Complex state management — not worth it for solo creator use case |
