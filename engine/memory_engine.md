# Memory Engine — AI YouTube Studio OS

The Memory Engine provides persistent, cross-project intelligence. It records what has been produced, what sources have been used, what decisions were made, and what quality outcomes resulted — so that future production runs benefit from accumulated knowledge. It is the system's institutional memory.

---

## Responsibility

The Memory Engine is responsible for **writing, reading, and querying the knowledge layer** (`knowledge/`). It extracts structured data from completed projects, stores it in defined databases, and retrieves relevant context when new projects begin.

**Single sentence:** The Memory Engine ensures the system gets smarter with every video produced.

---

## Inputs

| Input | Source | When |
|---|---|---|
| Completed `export_manifest.json` | `projects/{slug}/` | After project reaches `ready_for_production` |
| Completed `source_report.md` | `projects/{slug}/` | After source verification |
| Completed `research_verified.md` | `projects/{slug}/` | After source verification |
| Completed `seo.md` | `projects/{slug}/` | After SEO generation |
| `decisions.log` | `projects/{slug}/` | After each production run |
| `run.log` | `projects/{slug}/` | After each production run |
| QA reports | `projects/{slug}/` | After each QA pass |
| Query request | Director Engine or Routing Engine | When context for a new project is needed |

---

## Outputs

| Output | Destination | Description |
|---|---|---|
| Source records | `knowledge/source_database.md` | Verified sources appended after each run |
| Project memory entry | `knowledge/memory_database.md` | Per-project metadata and key facts |
| Asset references | `knowledge/asset_library.md` | New assets catalogued |
| Context response | Requesting engine | Relevant past knowledge for current project |

---

## Dependencies

| Dependency | Type | Purpose |
|---|---|---|
| Director Engine | upstream | Triggers memory write after run completion |
| Routing Engine | upstream | Requests memory context for new runs |
| `knowledge/` | read/write | All three databases |
| `core/file_lifecycle.md` | reference | Archive rules |

---

## Core Operations

### Operation 1: Write Project Memory

Triggered after every successful project completion. Extracts and stores:

```
FROM: export_manifest.json
EXTRACT:
  - project_id, topic, style, niche, language
  - video_length_minutes, actual_word_count
  - image_count (real vs. AI)
  - revision_count per stage
  - total_production_time_minutes

FROM: seo.md
EXTRACT:
  - selected_title (whichever option was used)
  - primary_keyword
  - tag_count

FROM: research_verified.md
EXTRACT:
  - verified_fact_count
  - source_count
  - flag_count, fail_count

FROM: decisions.log
EXTRACT:
  - decision_count, auto_resolved_count, human_escalated_count

WRITE TO: knowledge/memory_database.md
  → append new project entry
```

### Operation 2: Write Source Records

For each verified source in `research_verified.md`, check if it already exists in `knowledge/source_database.md`. If not, append:

```
SOURCE RECORD:
  - source_name
  - outlet / platform
  - year
  - url (if confirmed)
  - type (news / documentary / reddit / academic / etc.)
  - topics_covered: [list of topics it was used for]
  - reliability_rating: derived from source_report.md verdict
  - times_used: 1 (incremented on future reuse)
```

If the source already exists: increment `times_used` and add the current topic to `topics_covered`.

### Operation 3: Context Retrieval for New Projects

When a new project begins, the Routing Engine may query the Memory Engine for relevant context:

**Query types:**

| Query Type | Returns | Used By |
|---|---|---|
| `sources_by_topic(topic)` | Past sources related to this topic or person | Researcher prompt — helps find sources faster |
| `similar_projects(niche, style)` | Past projects with same niche/style — word counts, QA outcomes | Director — calibrates expectations |
| `known_assets(topic)` | Assets from past projects covering related topics | Image finder — avoid re-sourcing |
| `decision_history(decision_type)` | Past decisions of this type + outcomes | Decision Engine — improves consistency |
| `qa_failure_patterns(stage)` | Most common QA failures for this stage across all projects | QA Engine — knows what to watch for |

**Response format:**
```json
{
  "query": "sources_by_topic",
  "topic": "Elisa Lam",
  "results": [
    {
      "source_name": "Los Angeles Times",
      "outlet": "Los Angeles Times",
      "year": 2013,
      "url_confirmed": false,
      "type": "news",
      "times_used": 1,
      "reliability_rating": "high"
    }
  ],
  "result_count": 3,
  "query_timestamp": "2026-06-27T10:00:00Z"
}
```

---

## Memory Database Schema

See `knowledge/memory_database.md` for full schema. Summary:

```
memory_database.md structure:

## Projects Index
[Table of all completed projects with key metadata]

## Project Entries
### {project_id}
- Metadata block (topic, style, niche, language, dates)
- Production statistics (word count, stage durations, revision count)
- QA summary (pass rate per stage)
- Decision summary (count by type and outcome)
- Key facts retained (condensed research summary for future reference)
- SEO data (title used, primary keyword)
```

---

## Data Retention Policy

| Data Type | Retention |
|---|---|
| Project metadata | Permanent |
| Source records | Permanent |
| QA reports (per project) | 90 days after archive, then summary only |
| Decision logs (per project) | 90 days after archive, then summary only |
| Run logs (timing, tokens) | 30 days after archive |
| Asset references | Permanent |

Memory databases are append-only. Records are never deleted — only marked as `deprecated` if superseded.

---

## Anti-Patterns the Memory Engine Prevents

| Problem | Memory Engine Solution |
|---|---|
| Re-researching the same topic | `sources_by_topic()` returns past sources immediately |
| Re-sourcing the same images | `known_assets()` returns previously catalogued assets |
| Making the same bad decision repeatedly | `decision_history()` surfaces past failure patterns |
| Not knowing why QA keeps failing on stage X | `qa_failure_patterns(stage)` shows recurring issues |
| Starting each project from zero | Memory context prefills relevant background automatically |

---

## Future Automation Points

| Point | Description |
|---|---|
| Vector search | Embed project memories for semantic retrieval (not just exact-match topic queries) |
| Source reliability scoring | Track which sources correlate with `[FAIL]` vs `[PASS]` QA outcomes |
| YouTube performance feedback | After publish, ingest view count / CTR / retention data back into memory |
| Cross-channel memory | Share source database across multiple channel projects |
| Automatic source discovery | Memory Engine proactively surfaces new relevant sources as they are published |
