# Knowledge Architecture — AI YouTube Studio OS

The knowledge layer is the system's persistent data store. It accumulates structured information across all production runs and makes it available to every engine. It is the only part of the system that grows over time — every other component is static until manually updated.

---

## The Knowledge Layer's Role

Every other directory in this project defines **how** the system works. The knowledge layer records **what** the system has learned and done. This distinction is important:

```
engine/    → HOW stages execute
configs/   → WHAT parameters to use
prompts/   → WHAT to ask the AI
templates/ → WHAT niche additions to apply
knowledge/ → WHAT we have produced and learned (accumulates over time)
```

The knowledge layer is the system's institutional memory. A new system with no knowledge layer is equally capable on paper — but it starts every project from zero. A system with a populated knowledge layer avoids re-researching sources, re-sourcing images, and repeating past mistakes.

---

## Three Databases

| Database | File | What it stores | Who writes | Who reads |
|---|---|---|---|---|
| Source Database | `source_database.md` | Verified source registry | Memory Engine (after each run) | Research prompt (to seed searches), QA Engine |
| Memory Database | `memory_database.md` | Cross-project metadata, analytics, learning log | Memory Engine, Analytics Engine, Learning Engine | Memory Engine (for queries), Director Engine, Learning Engine |
| Asset Library | `asset_library.md` | Image, audio, and text asset catalog | Memory Engine (after each run) | Image Finder prompt, Export Engine |

These three databases serve different purposes and are never merged — each has a distinct schema and access pattern.

---

## Data Flow Into the Knowledge Layer

```
Production Run Completes
        │
        ▼
Memory Engine triggers:
    │
    ├──► Write to source_database.md
    │       → New verified sources from research_verified.md
    │       → Increment times_used for existing sources
    │
    ├──► Write to memory_database.md
    │       → Project metadata entry
    │       → Stage timing and token data
    │       → QA pass/fail summary
    │       → Decision outcomes
    │       → Key facts retained (condensed)
    │
    └──► Write to asset_library.md
            → New images located (real images with source)
            → New AI prompts used (successful ones catalogued)
```

---

## Data Flow Out of the Knowledge Layer

```
New Production Run Begins
        │
        ▼
Routing Engine queries Memory Engine:
    │
    ├──► sources_by_topic(topic)
    │       → Returns past sources that match this topic
    │       → Injected as context: "We have previously used these sources..."
    │
    ├──► similar_projects(niche, style)
    │       → Returns past project stats for calibration
    │       → Used to set expectations: "This style/niche took avg 45 minutes"
    │
    └──► qa_failure_patterns(stage)
            → Returns most common failures for this stage
            → Used to add extra attention to prone failure points
```

---

## Append-Only Policy

The knowledge databases are **append-only**. Records are never deleted. When a record is superseded or incorrect:
- The old record is marked `deprecated: true` with a note
- A new record is appended

This policy ensures:
- Full audit trail of what the system has learned
- Ability to trace when incorrect information entered the system
- No data loss from update operations

---

## File Format and Size Management

All three databases are Markdown files with structured tables and sections. They grow with every project. Management policies:

| Database | Estimated growth per project | Management strategy |
|---|---|---|
| `source_database.md` | 5-20 new rows | Deduplicated on write — existing sources get updated, not duplicated |
| `memory_database.md` | 1 full project entry + aggregate update | Entries compressed after 6 months (full detail → summary) |
| `asset_library.md` | 10-30 new entries | Deduplicated by source URL — same image referenced, not duplicated |

When any database exceeds 500KB, the Memory Engine splits it:
- `source_database_2026.md` / `source_database_2027.md` (by year)
- An index file `source_database_index.md` is maintained pointing to all split files

---

## Schema Versioning

Each database file includes a schema version in its header:

```markdown
# Source Database
**Schema version:** 1.0
**Last updated:** YYYY-MM-DD
**Record count:** [N]
```

Schema version bumps when the structure of records changes. All records in the file use the schema version at time of creation — the Memory Engine handles backward compatibility when reading mixed-schema files.

---

## Security and Privacy Considerations

The knowledge databases may contain:
- Names of real individuals (from mystery cases)
- URLs pointing to sensitive content
- Reddit usernames and post content

Policy:
- Do not store personally identifiable information beyond what appears in public sources
- Do not store the content of posts involving minors
- Do not store URLs that point to illegal content
- All knowledge files are committed to version control — treat them as public documents
