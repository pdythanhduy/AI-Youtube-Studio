# Analytics Engine — AI YouTube Studio OS

The Analytics Engine records, aggregates, and reports on production metrics. It tracks how long stages take, how many tokens are consumed, how often QA fails, how many retries occur, and — eventually — how produced videos perform on YouTube. It is read-only during pipeline execution and write-only after each stage completes.

---

## Responsibility

The Analytics Engine is responsible for **turning production activity into structured, queryable data**. It answers questions like: "Which stage takes the longest?", "Which niche produces the most QA failures?", "What is our average cost per video?", "Which style requires the most retries?"

**Single sentence:** The Analytics Engine makes the system observable — turning raw production logs into actionable intelligence.

---

## Inputs

| Input | Source | When |
|---|---|---|
| Stage completion signals | Workflow Engine | After each stage |
| QA validation results | QA Engine | After each validation |
| Decision log | Decision Engine | After each decision |
| Retry events | Director Engine | When a retry is triggered |
| `run.log` | `projects/{slug}/` | After project completion |
| YouTube performance data | External (future) | After video is published |

---

## Outputs

| Output | Destination | Description |
|---|---|---|
| Per-run analytics entry | `knowledge/memory_database.md#analytics` | Appended after each completed project |
| Analytics summary report | `projects/{slug}/analytics_report.md` | Human-readable summary per project |
| Aggregate metrics | `knowledge/memory_database.md#aggregate_metrics` | Updated rolling averages |

---

## Dependencies

| Dependency | Type | Purpose |
|---|---|---|
| Director Engine | upstream | Triggers analytics write after run |
| Memory Engine | downstream | Writes analytics data to knowledge layer |
| `run.log` | input | Raw timing and token data |

---

## Metrics Collected

### Per-Stage Metrics

For every pipeline stage, record:

| Metric | Unit | Description |
|---|---|---|
| `stage_id` | string | Which stage |
| `duration_seconds` | integer | Wall clock time from start to complete |
| `input_tokens` | integer | Tokens in the AI request |
| `output_tokens` | integer | Tokens in the AI response |
| `estimated_cost_usd` | float | Based on model pricing at time of run |
| `qa_result` | enum | `pass`, `fail`, `retry_pass`, `retry_fail` |
| `retry_count` | integer | How many retries were needed |
| `output_word_count` | integer | Words in the output file |
| `model_used` | string | Which Claude model was called |

### Per-Project Metrics

For the full project run:

| Metric | Unit | Description |
|---|---|---|
| `project_id` | string | Project identifier |
| `niche` | string | Content niche |
| `style` | string | Production style |
| `language` | string | Output language |
| `total_duration_minutes` | float | Total wall clock time |
| `total_input_tokens` | integer | Sum of all stage input tokens |
| `total_output_tokens` | integer | Sum of all stage output tokens |
| `total_cost_usd` | float | Estimated total API cost |
| `stage_count` | integer | Number of stages executed |
| `qa_pass_rate` | float | % of stages that passed QA first try |
| `retry_count_total` | integer | Total retries across all stages |
| `human_escalation_count` | integer | Number of times human review was required |
| `revision_count` | integer | Files that required revision |

### Aggregate Metrics (Rolling)

Updated after every project:

| Metric | Description |
|---|---|
| `avg_duration_by_niche` | Average total production time per niche |
| `avg_cost_by_style` | Average API cost per style |
| `qa_pass_rate_by_stage` | QA first-pass rate, per stage, all projects |
| `most_common_qa_failures` | Top 5 failing checklist items across all projects |
| `avg_retry_count_by_stage` | Average retries needed per stage |
| `total_videos_produced` | Cumulative count |
| `total_spend_usd` | Cumulative API spend |

---

## Analytics Report Format

Written to `projects/{slug}/analytics_report.md` after every completed run:

```markdown
# Analytics Report
**Project:** 20260627_disappearance-of-elisa-lam
**Completed:** 2026-06-27T11:30:00Z

## Production Summary
| Metric | Value |
|---|---|
| Total duration | 48 minutes |
| Total API cost (estimated) | $0.87 |
| Stages completed | 10 / 10 |
| QA first-pass rate | 80% (8/10 stages) |
| Retries required | 2 |
| Human escalations | 0 |

## Stage Breakdown
| Stage | Duration | Tokens In | Tokens Out | QA | Retries |
|---|---|---|---|---|---|
| 01_research | 6m 12s | 412 | 3,847 | PASS | 0 |
| 02_source_verifier | 4m 33s | 4,201 | 2,103 | PASS | 0 |
| 03_story_outline | 3m 45s | 5,892 | 1,456 | PASS | 0 |
| 04_script_writer | 9m 18s | 7,234 | 2,891 | RETRY→PASS | 1 |
| ... | ... | ... | ... | ... | ... |

## Cost Breakdown by Model
| Model | Calls | Input Tokens | Output Tokens | Est. Cost |
|---|---|---|---|---|
| claude-opus-4-8 | 7 | 38,421 | 18,334 | $0.65 |
| claude-sonnet-4-6 | 3 | 12,104 | 5,893 | $0.22 |

## Notes
- stage_04 retry: word count was 1,412 (target 1,560) — re-ran with explicit count constraint
- All QA checks passed on final submission
```

---

## Future Automation Points

| Point | Description |
|---|---|
| YouTube API integration | Ingest actual view count, CTR, retention data after publish |
| Cost alerting | Alert if single project exceeds configurable cost threshold |
| Trend detection | Flag if QA pass rate drops below 70% over last 10 projects |
| A/B analytics | Compare quality metrics between prompt v1 and v2 for same niche |
| Dashboard | Web interface showing rolling metrics across all projects |
| Profit tracking | If channel monetized: track estimated revenue per video vs. production cost |
