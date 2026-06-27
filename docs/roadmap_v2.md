# Roadmap v2.0 — AI YouTube Studio OS

Version 2.0 transforms the system from a manually-operated prompt collection into a partially-automated AI Operating System. A human provides `input.json` and triggers the pipeline — the system runs autonomously from that point, stopping only for human-escalation decisions.

**Version:** 2.0  
**Status:** Planning  
**Target start:** After v1.0 release  
**Target completion:** Q1 2027  

---

## v2.0 Vision

In v1.0, a human runs each stage manually via Claude Code and validates each output against a checklist.

In v2.0, a human types one command and waits. The Director Engine orchestrates all 10 stages, the QA Engine validates automatically, the Decision Engine handles routine decisions, and the Memory Engine records what was learned. The human only intervenes when a decision requires judgment they cannot delegate.

**The operator becomes a reviewer, not an executor.**

---

## v2.0 Scope

### New Capabilities in v2.0

- [ ] **Director Engine implementation** — automated orchestration of full pipeline
- [ ] **Workflow Engine implementation** — automated stage execution with Claude API calls
- [ ] **QA Engine implementation** — automated validation of all Layer 1 and Layer 2 checks
- [ ] **Memory Engine implementation** — automated knowledge layer updates after each project
- [ ] **Analytics Engine implementation** — automated metrics collection and reporting
- [ ] **Decision Engine implementation** — automated resolution of routine decisions
- [ ] **Export Engine implementation** — automated export bundle creation
- [ ] **Routing Engine implementation** — automated prompt/template selection
- [ ] **Parallel stage execution** — stages 06+07+09 run concurrently where dependencies allow
- [ ] **Human-in-the-loop API** — web interface for human review of escalated decisions
- [ ] **CLI command** — `studio run --input input.json` triggers full pipeline
- [ ] **Run resumption** — `studio resume --project 20260627_topic` resumes interrupted run
- [ ] **`google_maps_mystery` niche** — full template and pipeline support added
- [ ] **`lost_places` niche** — full template and pipeline support added

---

## v2.0 Architecture Changes

### Engine Code Implementation

v1.0 defined engine behavior in documentation. v2.0 implements that behavior as executable code.

**Implementation language:** Python 3.11+  
**AI SDK:** `anthropic` Python SDK  
**Structure:**
```
src/
├── engines/
│   ├── director_engine.py
│   ├── workflow_engine.py
│   ├── routing_engine.py
│   ├── decision_engine.py
│   ├── memory_engine.py
│   ├── qa_engine.py
│   ├── analytics_engine.py
│   ├── learning_engine.py
│   └── export_engine.py
├── models/
│   ├── project.py           (Project state model)
│   ├── manifest.py          (Manifest read/write)
│   └── config.py            (Config loader)
├── validators/
│   ├── schema_validator.py  (Format checks)
│   ├── content_validator.py (Content checks)
│   └── consistency_validator.py (Cross-file checks)
└── cli.py                   (Command-line interface)
```

**No existing documentation files are moved or renamed.** Engine docs in `engine/` remain the behavioral specification. `src/` contains the implementation that follows those specs.

### MCP Integration (v2.0 Feature)

The Director Engine exposes an MCP server interface, allowing Claude Code agents to invoke it via tool calls:

```
Tool: studio_run
  Input: { "input_json": {...} }
  Output: { "project_slug": "...", "status": "started" }

Tool: studio_status
  Input: { "project_slug": "..." }
  Output: { "status": "in_progress", "current_stage": "stage_04", ... }

Tool: studio_resume
  Input: { "project_slug": "..." }
  Output: { "status": "resuming from stage_04" }
```

This enables future agents to orchestrate multiple video productions simultaneously.

### Automated QA

v2.0 implements all QA Engine Layer 1 and Layer 2 checks programmatically:

- Layer 1 (format): regex and file parsing — fully automated
- Layer 2 (content): Claude call to evaluate semantic properties — semi-automated
- Layer 3 (consistency): string matching against story_bible — fully automated

Layer 2 uses a secondary Claude Haiku 4.5 call (fast, cheap, sufficient for checklist evaluation). Layer 3 is pure string matching with no AI call required.

---

## v2.0 Milestones

### Milestone 1: CLI and Project Model
**Deliverable:** `studio init`, `studio run`, `studio status`, `studio resume` commands working

Tasks:
- [ ] Implement Project model (`project_id`, `status`, manifest read/write)
- [ ] Implement config loader (reads `configs/configuration_system.md`)
- [ ] Implement `studio init` — creates project folder, validates `input.json`
- [ ] Implement `studio status` — reads and displays manifest state

### Milestone 2: Automated Stage Execution
**Deliverable:** Workflow Engine runs a single stage automatically via Claude API

Tasks:
- [ ] Implement Routing Engine (prompt + template + config selection)
- [ ] Implement Workflow Engine (placeholder resolution + API call + file write)
- [ ] Implement atomic write protocol (tmp → rename)
- [ ] Run `studio run --stage 1` successfully on test fixture

### Milestone 3: Automated QA
**Deliverable:** QA Engine validates any stage output automatically

Tasks:
- [ ] Implement schema validators for all output file types
- [ ] Implement content validators for all QA checklist items
- [ ] Implement consistency validators (cross-file checks)
- [ ] QA Engine produces structured QA report files
- [ ] Director Engine reads QA result and decides next action

### Milestone 4: Full Pipeline Automation
**Deliverable:** `studio run` executes all 10 stages without human intervention

Tasks:
- [ ] Implement Director Engine (stage sequencing, retry logic, halt conditions)
- [ ] Implement Decision Engine (auto-resolution of routine failures)
- [ ] `studio run` produces `ready_for_production` manifest on a clean test fixture
- [ ] All regression tests pass

### Milestone 5: Memory and Learning
**Deliverable:** Knowledge layer is updated automatically after every project

Tasks:
- [ ] Implement Memory Engine (project entry write, source database update, asset library update)
- [ ] Implement Analytics Engine (metrics collection, analytics_report.md generation)
- [ ] Implement Learning Engine (pattern analysis on schedule)
- [ ] After 3 test projects: learning report generated with at least 1 recommendation

### Milestone 6: v2.0 Release
**Deliverable:** Tagged v2.0 release

Tasks:
- [ ] Full regression suite passes
- [ ] All acceptance tests pass
- [ ] CLI documented in README.md
- [ ] MCP integration tested with Claude Code
- [ ] Release notes written

---

## v2.0 Quality Criteria

v2.0 is complete when:

1. `studio run --input input.json` produces a `ready_for_production` project with zero human intervention on ≥80% of runs (the other 20% require human decision input on escalated items)
2. The system self-improves: at least one learning recommendation is generated and approved after every 10 projects
3. The knowledge layer accurately reflects all projects in the source database
4. All v1.0 regression tests still pass (no regression from v1.0 behavior)

---

## v2.0 Breaking Changes from v1.0

| Component | v1.0 | v2.0 |
|---|---|---|
| Stage execution | Manual via Claude Code | Automated via CLI |
| QA validation | Manual checklist review | Automated + escalation |
| Export manifest | Manually updated | Auto-updated by engines |
| Knowledge layer | Empty (seed files only) | Auto-populated by Memory Engine |
| Analytics | None | Auto-collected per project |
