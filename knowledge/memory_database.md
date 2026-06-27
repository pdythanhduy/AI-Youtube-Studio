# Memory Database — AI YouTube Studio OS

Cross-project metadata store. Records production statistics, QA outcomes, decision patterns, and key facts from every completed project. Used by the Learning Engine for pattern analysis and by the Director Engine for calibration.

**Schema version:** 1.0
**Last updated:** [Updated automatically by Memory Engine]
**Project count:** 0 (seed file — no projects completed yet)

---

## Schema Definition

### Project Entry Schema

| Field | Type | Description |
|---|---|---|
| `project_id` | string | Canonical project slug |
| `topic` | string | Human-readable topic |
| `niche` | string | Niche ID |
| `style` | string | Style ID |
| `language` | string | ISO 639-1 code |
| `video_length_minutes_target` | integer | Planned video length |
| `status` | string | Final project status |
| `created_at` | ISO datetime | Project creation timestamp |
| `completed_at` | ISO datetime | Export completion timestamp |
| `total_duration_minutes` | float | Wall-clock production time |
| `total_cost_usd_estimated` | float | Estimated API cost |
| `word_count_target` | integer | Target word count |
| `word_count_actual` | integer | Actual script word count |
| `image_count_total` | integer | Total visual beats |
| `image_count_real` | integer | Real image beats |
| `image_count_ai` | integer | AI-generated image beats |
| `stage_qa_results` | object | Per-stage QA outcomes |
| `revision_count_total` | integer | Total revisions across all stages |
| `human_escalation_count` | integer | Number of human-review escalations |
| `decision_count` | integer | Total decisions made |
| `seo_title_selected` | string | Which title option was used |
| `primary_keyword` | string | Primary SEO keyword |
| `source_count` | integer | Number of sources used |
| `verified_fact_count` | integer | Verified facts in research |
| `key_facts_summary` | string | 2-3 sentence summary of the project topic |

### Stage QA Results Schema (nested)

```json
{
  "stage_01": { "first_pass": true, "retry_count": 0, "qa_verdict": "pass" },
  "stage_02": { "first_pass": true, "retry_count": 0, "qa_verdict": "pass" },
  "stage_03": { "first_pass": false, "retry_count": 1, "qa_verdict": "pass" },
  ...
}
```

---

## Projects Index

*Populated automatically by Memory Engine.*

| Project ID | Topic | Niche | Style | Lang | Completed | Cost (est.) | QA Pass Rate |
|---|---|---|---|---|---|---|---|
| *No projects yet* | | | | | | | |

---

## Project Entries

*Full project entries are appended here by the Memory Engine after each project completes.*

*No entries yet — this is a seed file.*

---

## Aggregate Metrics

*Updated by Analytics Engine after each project.*

### Production Statistics

| Metric | Value | Last Updated |
|---|---|---|
| Total projects completed | 0 | — |
| Total videos produced | 0 | — |
| Avg production time (minutes) | — | — |
| Avg estimated cost per video (USD) | — | — |
| Total estimated spend (USD) | 0.00 | — |
| Total words generated | 0 | — |

### QA Statistics

| Metric | Value |
|---|---|
| Overall QA first-pass rate | — |
| Stage with lowest first-pass rate | — |
| Most common QA failure | — |
| Avg retries per project | — |
| Human escalation rate | — |

### Niche Statistics

| Niche | Projects | Avg Cost | Avg QA Pass Rate | Avg Duration |
|---|---|---|---|---|
| internet_mystery | 0 | — | — | — |
| japanese_mystery | 0 | — | — | — |
| reddit_mystery | 0 | — | — | — |
| google_maps_mystery | 0 | — | — | — |
| lost_places | 0 | — | — | — |
| unexplained_events | 0 | — | — | — |

### Style Statistics

| Style | Projects | Avg Word Count | Avg QA Pass Rate |
|---|---|---|---|
| dark_documentary | 0 | — | — |
| reddit_narration | 0 | — | — |
| mystery_investigation | 0 | — | — |
| japanese_mystery | 0 | — | — |

### Language Statistics

| Language | Projects | Avg Duration | Avg Cost |
|---|---|---|---|
| en | 0 | — | — |
| ja | 0 | — | — |
| vi | 0 | — | — |

---

## Learning Log

*Records of all Learning Engine cycles and their outcomes.*

| Date | Trigger | Recommendations Made | Approved | Rejected | Deferred |
|---|---|---|---|---|---|
| *No learning cycles yet* | | | | | |

---

## Decision Pattern Index

*Tracks decision types and outcomes across all projects for the Decision Engine.*

| Decision Type | Total Count | Auto-Resolved | Human-Escalated | Most Common Outcome |
|---|---|---|---|---|
| source_quality | 0 | 0 | 0 | — |
| image_escalation | 0 | 0 | 0 | — |
| qa_failure_recovery | 0 | 0 | 0 | — |
| script_fact_audit | 0 | 0 | 0 | — |
| language_register | 0 | 0 | 0 | — |

---

## QA Failure Pattern Index

*Tracks which QA checks fail most often, for each stage.*

| Stage | Check | Failure Count | Last Failed | Notes |
|---|---|---|---|---|
| *No failures recorded yet* | | | | |

---

## Memory Engine Write Protocol

After every completed project, the Memory Engine:

1. Creates a new Project Entry following the schema above
2. Appends the entry under the `## Project Entries` section
3. Updates the `## Projects Index` table with a summary row
4. Updates all `## Aggregate Metrics` rolling averages
5. Updates `## Decision Pattern Index` with decisions from this project's `decisions.log`
6. Updates `## QA Failure Pattern Index` with failures from this project's QA reports
7. Updates `last_updated` and `project_count` in the file header

All updates are atomic — the full file is rewritten, not appended line by line.
