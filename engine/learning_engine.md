# Learning Engine — AI YouTube Studio OS

The Learning Engine analyzes patterns across production runs and generates improvements to prompts, configs, and templates. It does not modify system files directly — it produces recommended changes and flags them for human review and approval. Over time, it transforms raw operational data into compounding quality improvements.

---

## Responsibility

The Learning Engine is responsible for **identifying what is going wrong, what is going right, and how the system can be improved** based on evidence from past runs. It reads analytics, QA reports, and decision logs, then writes specific, actionable recommendations.

**Single sentence:** The Learning Engine is the system's self-improvement mechanism — it turns production experience into better production.

---

## Inputs

| Input | Source | When |
|---|---|---|
| Aggregate analytics | `knowledge/memory_database.md#aggregate_metrics` | Triggered by Director after N completed projects |
| QA failure history | `knowledge/memory_database.md` | All past QA reports |
| Decision logs | `knowledge/memory_database.md` | All past decision outcomes |
| Current prompt files | `prompts/` | For diff-comparison with recommended changes |
| Current config files | `configs/` | For policy review |
| `MASTER_RULE.md` | System | Rules that cannot be changed by Learning Engine |

---

## Outputs

| Output | Destination | Description |
|---|---|---|
| Improvement recommendations | `docs/learning_report_YYYYMMDD.md` | Structured list of proposed changes |
| Prompt change proposals | Alongside current prompt files | Draft of modified prompt (not replacing original) |
| Config change proposals | Alongside current config files | Draft of modified config section |
| Learning summary | `knowledge/memory_database.md#learning_log` | Log of all recommendations made |

---

## Dependencies

| Dependency | Type | Purpose |
|---|---|---|
| Analytics Engine | upstream | Supplies aggregate metrics |
| Memory Engine | upstream | Supplies QA and decision history |
| Director Engine | downstream | Schedules learning runs |
| QA Engine | reference | Understands what was validated |
| Human operator | approval | No change is made without approval |

---

## Learning Trigger Conditions

The Learning Engine runs automatically when any of these thresholds are met:

| Trigger | Threshold | Description |
|---|---|---|
| Project count | Every 10 completed projects | Routine learning cycle |
| QA pass rate drop | Stage pass rate < 70% over 5 runs | Prompt may need revision |
| Retry rate spike | >40% of runs require retries on same stage | Systematic prompt failure |
| Cost threshold | Avg cost per video exceeds configurable limit | Cost optimization needed |
| Manual trigger | Human operator request | On-demand analysis |

---

## Analysis Modules

### Module 1: QA Pattern Analysis

Reads all QA failure records from `knowledge/memory_database.md`. Groups failures by:
- Stage (which stage fails most often)
- Check type (which checklist item fails most often)
- Niche (which content niche produces most failures)
- Style (which style produces most failures)

Produces: a ranked list of the top failure patterns, with frequency and impact score.

**Example output:**
```
TOP QA FAILURES (last 20 projects):

1. stage_04 / check: "Script word count in range"
   Frequency: 8/20 runs (40%)
   Avg shortfall: -12% below target
   Niche breakdown: japanese_mystery (5/8), reddit_mystery (3/8)
   Hypothesis: Script prompt does not enforce word count strongly enough
               for short-niche topics. Japanese mystery topics tend to
               have less available research, leading to shorter scripts.
   Recommendation: Add explicit word count enforcement to 04_script_writer.md
                   and add a note about research depth for japanese_mystery.
```

### Module 2: Retry Pattern Analysis

Identifies stages and conditions that most frequently require retries. Surfaces the specific retry reasons from `decisions.log`.

### Module 3: Prompt Effectiveness Analysis

For each prompt, calculates:
- First-pass QA success rate
- Average output quality score (derived from retry count + human escalations)
- Token efficiency (output quality per 1,000 tokens)

Flags prompts with degrading effectiveness over time.

### Module 4: Cost Optimization Analysis

Identifies stages where the current model assignment may be over-specified. Flags cases where:
- A stage consistently passes QA on first try with minimal variation
- The stage is being run on `claude-opus-4-8` but may succeed on `claude-sonnet-4-6`

Proposes model routing changes with estimated cost savings.

### Module 5: Cross-Project Pattern Mining

Identifies patterns across all projects:
- Topics that consistently require more research depth
- Niches where image escalation to AI is more frequent than expected
- Styles where the voice director prompt produces the most revisions

---

## Recommendation Format

All recommendations are written in a structured format that can be reviewed and approved by a human:

```markdown
# Learning Report — 2026-06-27
Generated after: 10 completed projects
Trigger: Scheduled (10-project cycle)

## Summary
- 3 HIGH priority recommendations
- 2 MEDIUM priority recommendations
- 1 LOW priority recommendation

---

## Recommendation #001 [HIGH]
**Target:** prompts/04_script_writer.md
**Issue:** Word count shortfall in 40% of runs
**Evidence:** 8/20 QA failures on "word count in range" check. Avg shortfall: -12%.
             Disproportionately affects japanese_mystery niche.
**Root cause hypothesis:** The current word count rule in the prompt is advisory,
                          not enforcement. The model treats it as a target, not a limit.
**Proposed change:**
  Current: "Hit target word count within ±10%"
  Proposed: "Your output MUST contain exactly {target_words} words ±10%.
             After writing, count your words. If under {min_words}, expand Scene 2
             or Scene 3 with additional context. Do not proceed if word count is
             outside this range."
**Estimated impact:** Reduce word count QA failures by ~60%
**Risk:** Low — change is additive, not structural
**Approval required:** Yes — human must review and merge

---

## Recommendation #002 [HIGH]
**Target:** configs/configuration_system.md → model_overrides
**Issue:** claude-opus-4-8 is used for stage_05 (story_bible), but this stage
          has 100% first-pass QA rate and purely mechanical output.
**Evidence:** stage_05 QA pass rate: 20/20 (100%). No retries in any run.
**Proposed change:** Route stage_05 to claude-sonnet-4-6
**Estimated cost savings:** ~$0.08 per project (≈$0.80 per 10 projects)
**Risk:** Low
**Approval required:** Yes
```

---

## What the Learning Engine Cannot Change

The following are protected — Learning Engine recommendations cannot target them:

- `MASTER_RULE.md` — Core operating rules are human-only decisions
- `core/` — System definitions require architectural decision
- The no-fabrication rule (Rule 2) — Cannot be relaxed
- The no-fake-URL rule — Cannot be relaxed
- Stage execution order — Cannot be reordered

---

## Approval and Merge Process

1. Learning Engine writes `docs/learning_report_YYYYMMDD.md`
2. Human operator reviews all recommendations
3. For each recommendation:
   - `APPROVED` → Human (or authorized agent) applies the change manually
   - `REJECTED` → Human notes rejection reason in the report
   - `DEFERRED` → Revisit in next learning cycle
4. After all reviews: update `knowledge/memory_database.md#learning_log` with outcomes
5. Applied changes trigger a version bump in the modified file's version history section

---

## Future Automation Points

| Point | Description |
|---|---|
| Automated prompt patching | With human approval gate, apply approved changes automatically |
| Semantic similarity analysis | Use embeddings to find structurally similar QA failures across different text |
| YouTube performance correlation | Correlate production metrics (word count, image ratio) with CTR and retention |
| Prompt regression testing | Before applying a learning recommendation, run acceptance tests to verify improvement |
| Self-documenting improvements | Learning Engine writes the changelog entry for every applied change |
