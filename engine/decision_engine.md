# Decision Engine — AI YouTube Studio OS

The Decision Engine evaluates branching conditions throughout the pipeline and returns a structured decision. It is the system's reasoning layer for non-obvious choices: whether to escalate a flagged fact, whether an image can be sourced legitimately, whether a script needs human review, whether a QA failure is auto-recoverable. It does not generate content and does not take action — it returns a decision signal and explains its reasoning.

---

## Responsibility

The Decision Engine answers: **"Given this condition, what should happen next?"** It evaluates evidence and returns one of a fixed set of decision outcomes. Every decision is logged with reasoning so it can be audited and improved.

**Single sentence:** The Decision Engine is the system's judgment layer — it evaluates ambiguity and returns a clear, reasoned choice.

---

## Inputs

| Input | Source | Description |
|---|---|---|
| Decision request | Any engine (usually Director or QA) | What to evaluate + relevant context |
| `MASTER_RULE.md` | System | Rules governing decisions |
| Relevant project files | `projects/{slug}/` | Evidence for the decision |
| `configs/configuration_system.md` | `configs/` | Thresholds and policy overrides |
| Historical decision log | `knowledge/memory_database.md` | Past decisions on similar conditions |

---

## Outputs

| Output | Destination | Description |
|---|---|---|
| Decision signal | Requesting engine | Outcome + decision ID + reasoning |
| Decision log entry | `projects/{slug}/decisions.log` | Full audit trail |

---

## Dependencies

| Dependency | Type | Purpose |
|---|---|---|
| Director Engine | upstream | Primary requester |
| QA Engine | upstream | Requests decisions on validation failures |
| Memory Engine | downstream | Reads historical decisions |
| `MASTER_RULE.md` | reference | Decision policy authority |

---

## Decision Types

### Type 1: Source Quality Decision

**Trigger:** Source verifier (stage_02) returns a `[FLAG]` rating on a fact.

**Inputs:** The flagged fact, the source name, the source type, the claim's importance to the narrative.

**Decision outcomes:**

| Outcome | When | Action |
|---|---|---|
| `accept_with_label` | Source is credible type but URL unconfirmed | Keep fact, label `[FLAG]` in research_verified.md |
| `request_alternative` | Source is weak (Wikipedia, anonymous) but fact is important | Flag for operator to find a better source |
| `remove_fact` | Source cannot be verified AND fact is non-essential | Remove from research_verified.md |
| `halt_pipeline` | Source cannot be verified AND fact is foundational to the entire narrative | Pipeline halts — human must resolve |

**Reasoning template:**
```
DECISION: source_quality
FACT: [abbreviated fact]
SOURCE: [source name + type]
OUTCOME: [accept_with_label / request_alternative / remove_fact / halt_pipeline]
REASON: [One sentence explaining why]
RULE APPLIED: MASTER_RULE.md Rule 2 (No Fabrication), source type hierarchy
```

---

### Type 2: Image Escalation Decision

**Trigger:** Image finder (stage_07) cannot find a legal real image for a beat.

**Inputs:** Beat description, beat image type (from storyboard), available real image options, legal constraints.

**Decision outcomes:**

| Outcome | When | Action |
|---|---|---|
| `use_real_with_attribution` | Real image exists under CC BY | Use it, note attribution in image_plan.md |
| `use_real_fair_use` | Real image exists, commentary use justified | Use it, note fair use in image_plan.md |
| `escalate_to_ai` | No usable real image | Add to AI Escalation List in image_plan.md |
| `use_text_overlay` | Scene is narration-only, no visual needed | Substitute with text overlay beat |

---

### Type 3: QA Failure Recovery Decision

**Trigger:** QA engine (qa_engine) marks a file `needs_revision`.

**Inputs:** QA report, failure type, failure severity, current retry count.

**Decision outcomes:**

| Outcome | When | Action |
|---|---|---|
| `auto_retry` | Failure is mechanical (word count, formatting) AND retry count ≤ 2 | Re-dispatch stage to Workflow Engine |
| `human_review` | Failure is content-related OR retry count > 2 | Halt, notify operator |
| `partial_accept` | Failure is minor and non-blocking for downstream stages | Accept with flag, continue pipeline, fix before export |
| `pipeline_halt` | Failure is foundational (fabricated fact, source FAIL) | Hard halt — cannot proceed |

---

### Type 4: Script Fact Audit Decision

**Trigger:** QA engine identifies a fact in script.md that does not appear in research_verified.md.

**Inputs:** The disputed fact from script.md, full research_verified.md content, the scene context.

**Decision outcomes:**

| Outcome | When | Action |
|---|---|---|
| `fact_is_verifiable` | Fact exists in research_verified.md under different phrasing | Accept, log the matching entry |
| `fact_is_speculation_labeled` | Fact uses hedged language ("some believe...") | Accept — speculation is allowed if labeled |
| `fact_is_fabricated` | Fact not in research, not labeled as speculation | Remove from script + flag for rewrite |
| `fact_needs_research` | Fact seems plausible but unverified | Add to research gap list, flag scene |

---

### Type 5: Language/Register Decision

**Trigger:** Stage output is in the correct language but register or tone seems inconsistent with style.

**Inputs:** The output text sample, the style profile, the language profile.

**Decision outcomes:**

| Outcome | When | Action |
|---|---|---|
| `accept` | Register matches style profile | Continue |
| `soft_flag` | Register is slightly off but intelligible | Note in QA report, accept |
| `rewrite_scene` | Register is substantially wrong (casual where formal required) | Flag specific scenes for rewrite |

---

## Decision Log Format

Every decision is appended to `projects/{slug}/decisions.log`:

```
[2026-06-27T10:25:00Z] DECISION #001
  Type: source_quality
  Stage: stage_02
  Input: Fact #3 — "Elisa Lam was last seen on January 31, 2013"
  Source: "Los Angeles Times, 2013" (URL not confirmed)
  Outcome: accept_with_label
  Reason: LA Times is a credible major outlet. Date claim is consistent with
           other sources. URL unconfirmed but source type is high credibility.
           Retaining with [FLAG] label per MASTER_RULE.md Rule 2.
  Rule: MASTER_RULE.md Rule 2, source type hierarchy rank 2
  Reviewed_by: decision_engine_v1.0
```

---

## Policy Overrides

Decision policies can be tightened or loosened via `configs/configuration_system.md`:

| Policy Key | Default | Description |
|---|---|---|
| `decision.max_auto_retries` | 2 | Max retries before human escalation |
| `decision.accept_unconfirmed_urls` | false | Whether to accept sources with unconfirmed URLs |
| `decision.require_human_on_flag` | false | If true, every [FLAG] requires human sign-off |
| `decision.fact_speculation_threshold` | 0.5 | Minimum hedging confidence to accept as speculation |

---

## Future Automation Points

| Point | Description |
|---|---|
| ML decision scoring | Train a classifier on past decision logs to improve accuracy |
| Confidence scores | Decision Engine returns a confidence score (0.0-1.0) alongside outcomes |
| Human-in-the-loop API | Operator reviews decisions via a web interface rather than log files |
| Cross-project pattern matching | Memory Engine feeds past decision outcomes to improve future decisions |
| Explainability report | Generate a human-readable "why we made these choices" document per project |
