# Project Structure — AI YouTube Studio OS

Definitive reference for the folder layout, ownership of each directory, and the rules that govern what lives where.

---

## Structural Philosophy

The project is organized by **function**, not by file type. Every directory has a single, non-overlapping responsibility. A file belongs in exactly one place. If the right place is ambiguous, the answer is always: put it where the thing that *creates* it lives, not where the thing that *consumes* it lives.

**The four layers of the system:**

```
┌─────────────────────────────────────────────┐
│  LAYER 1 — CONTROL                          │
│  engine/   configs/                         │  ← Logic + Settings
├─────────────────────────────────────────────┤
│  LAYER 2 — CONTENT                          │
│  prompts/  templates/  knowledge/           │  ← Instructions + Structure + Data
├─────────────────────────────────────────────┤
│  LAYER 3 — OUTPUT                           │
│  projects/                                  │  ← Generated per-video assets
├─────────────────────────────────────────────┤
│  LAYER 4 — SYSTEM                           │
│  core/  tests/  docs/  assets/              │  ← Definitions + Verification + History
└─────────────────────────────────────────────┘
```

No layer depends on a layer below it. Layers only call downward.

---

## Full Directory Tree

```
AI-Youtube-Studio/
│
├── README.md                        # Entry point — quick start
├── MASTER_PLAN.md                   # System architecture reference
├── MASTER_RULE.md                   # Operating rules — authoritative
├── WORKFLOW.md                      # Production pipeline steps
├── STYLE_GUIDE.md                   # Visual/narrative style reference
│
├── core/                            # System definitions — read-only at runtime
│   ├── project_structure.md         # This file
│   ├── naming_conventions.md        # All naming rules
│   └── file_lifecycle.md            # How files move through the system
│
├── engine/                          # AI engine subsystem documentation
│   ├── director_engine.md           # Orchestration — top-level pipeline control
│   ├── workflow_engine.md           # Stage execution — runs individual steps
│   ├── routing_engine.md            # Routing — selects correct prompts/templates
│   ├── decision_engine.md           # Branching logic — if/then decisions
│   ├── memory_engine.md             # Cross-project persistent memory
│   ├── qa_engine.md                 # Quality assurance and validation
│   ├── analytics_engine.md          # Metrics, timing, performance tracking
│   ├── learning_engine.md           # Feedback loop — improves prompts over time
│   └── export_engine.md             # Final packaging and export manifest
│
├── configs/                         # Configuration — no logic, only settings
│   ├── configuration_system.md      # Config schema, inheritance, override rules
│   ├── language_profiles.md         # Per-language settings (en/ja/vi)
│   ├── style_profiles.md            # Per-style settings
│   └── output_profiles.md           # Output format and encoding settings
│
├── prompts/                         # Reusable AI prompt files (per pipeline stage)
│   ├── 01_research.md
│   ├── 02_source_verifier.md
│   ├── 03_story_outline.md
│   ├── 04_script_writer.md
│   ├── 05_story_bible.md
│   ├── 06_scene_splitter.md
│   ├── 07_image_finder.md
│   ├── 08_image_prompt_generator.md
│   ├── 09_voice_director.md
│   └── 10_youtube_seo.md
│
├── templates/                       # Niche-specific production templates
│   ├── template_architecture.md     # How templates compose with prompts
│   ├── mystery_template.md          # Internet / unexplained mysteries
│   ├── japan_template.md            # Japanese mystery niche
│   └── reddit_template.md           # Reddit / NoSleep niche
│
├── knowledge/                       # Persistent data layer
│   ├── knowledge_architecture.md    # How the knowledge layer is organized
│   ├── source_database.md           # Verified source registry
│   ├── memory_database.md           # Cross-project narrative memory
│   └── asset_library.md             # Image/audio/text asset catalog
│
├── tests/                           # Testing and validation
│   ├── testing_strategy.md          # Testing philosophy and test types
│   ├── acceptance_tests.md          # Feature-level acceptance criteria
│   └── regression_tests.md          # Regression suite
│
├── docs/                            # Planning and roadmap
│   ├── roadmap_v1.md                # Current version goals
│   ├── roadmap_v2.md                # Next major version
│   └── future_features.md           # Long-term vision
│
├── projects/                        # Generated per-video output (runtime)
│   └── YYYYMMDD_topic-slug/
│       ├── input.json
│       ├── research.md
│       ├── source_report.md
│       ├── research_verified.md
│       ├── story_outline.md
│       ├── script.md
│       ├── story_bible.md
│       ├── storyboard.md
│       ├── image_plan.md
│       ├── ai_image_prompts.md
│       ├── voice_script.txt
│       ├── voice_direction.md
│       ├── subtitles.srt
│       ├── thumbnail_prompt.md
│       ├── seo.md
│       └── export_manifest.json
│
└── assets/                          # Shared static assets (channel-level)
    ├── music/                       # Background music tracks
    ├── fonts/                       # Subtitle and overlay fonts
    ├── intros/                      # Channel intro files
    └── outros/                      # Channel outro files
```

---

## Directory Responsibilities

### `core/` — System Definitions
**Owns:** The rules, conventions, and lifecycle definitions that govern the entire system.
**Written by:** Lead architect. Updated rarely.
**Read by:** All agents at startup. All humans onboarding to the project.
**Must not contain:** Prompt text, configuration values, generated content.

### `engine/` — Subsystem Architecture
**Owns:** The behavioral specification of every engine component.
**Written by:** Lead architect. Updated when engine behavior changes.
**Read by:** Implementation agents building the actual engine code.
**Must not contain:** Prompt text, project data, configuration values.

### `configs/` — Configuration
**Owns:** All tunable parameters — language settings, style parameters, output formats.
**Written by:** Architect or operator. Must be versioned.
**Read by:** All engines at runtime.
**Must not contain:** Logic, prompt text, or generated content.

### `prompts/` — AI Prompt Library
**Owns:** The reusable prompt instructions for each pipeline stage.
**Written by:** Prompt engineer.
**Read by:** The workflow engine (to construct AI requests), templates (to compose niche-specific variants).
**Must not contain:** Configuration values (those come from configs/), project data.

### `templates/` — Niche Templates
**Owns:** Niche-specific compositions of prompts + configs + structure.
**Written by:** Content strategist.
**Read by:** The routing engine (to select the correct template), the workflow engine (to execute it).
**Must not contain:** Raw prompt text (templates reference prompts, not duplicate them).

### `knowledge/` — Data Layer
**Owns:** Persistent cross-project data: source registry, narrative memory, asset catalog.
**Written by:** System during production runs (updated automatically by engines).
**Read by:** Memory engine, QA engine, analytics engine.
**Must not contain:** Logic, prompt text, configuration.

### `tests/` — Quality Assurance
**Owns:** All test definitions, acceptance criteria, and regression suites.
**Written by:** QA engineer.
**Read by:** QA engine at runtime, CI/CD systems.
**Must not contain:** Generated project output.

### `docs/` — Planning and Roadmap
**Owns:** Roadmaps, future feature specs, design decisions.
**Written by:** Lead architect and product owner.
**Read by:** Humans only (not runtime agents).
**Must not contain:** Runtime configuration or prompt text.

### `projects/` — Runtime Output
**Owns:** Every generated asset for every video.
**Written by:** Pipeline engines during production runs.
**Read by:** Editors, voice artists, YouTube upload tools.
**Must not contain:** System definitions, templates, or shared assets.

---

## Dependency Rules

| Directory | May import from | Must not import from |
|---|---|---|
| `engine/` | `configs/`, `prompts/`, `templates/`, `knowledge/` | `projects/`, `tests/`, `docs/` |
| `configs/` | nothing | everything |
| `prompts/` | `configs/` | `engine/`, `projects/` |
| `templates/` | `prompts/`, `configs/` | `engine/`, `projects/` |
| `knowledge/` | nothing (data only) | everything |
| `projects/` | read-only: `engine/`, `templates/`, `knowledge/` | `core/`, `tests/`, `docs/` |
| `tests/` | `projects/` (for output verification) | `engine/` (direct) |

---

## Version Control Policy

| Directory | Commit frequency | Branch strategy |
|---|---|---|
| `core/`, `engine/`, `configs/` | On architectural change | Feature branch → main |
| `prompts/`, `templates/` | On prompt iteration | Versioned files (v1, v2...) |
| `knowledge/` | After each production run | Auto-commit by system |
| `projects/` | Per video — archive after publish | Project-specific branch or tag |
| `tests/` | With corresponding feature change | Same branch as feature |
| `docs/` | On planning milestone | main (no branch needed) |
