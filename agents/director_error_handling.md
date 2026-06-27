# Director Error Handling — AI YouTube Studio OS

Defines every class of error the Director AI may encounter, how to classify it, what to do about it, and how to report it. The Director AI reads this file during boot and applies these rules throughout the pipeline.

---

## Error Classification System

Every error falls into one of four severity levels. Severity determines what the Director AI does next.

| Severity | Code | What it means | Director action |
|---|---|---|---|
| CRITICAL | `ERR_CRITICAL` | Pipeline cannot continue safely | Halt immediately. Report. Wait for human. |
| HARD FAIL | `ERR_FAIL` | Stage output is invalid, content is wrong | Halt stage. Report. Wait for human. |
| WARNING | `ERR_WARN` | Output is acceptable but imperfect | Log warning. Continue. Flag in final report. |
| INFO | `ERR_INFO` | Informational anomaly, no action needed | Log only. Continue. |

---

## Error Code Reference

### ERR_CRITICAL — Pipeline-halting errors

| Code | Trigger | Message | Human Action |
|---|---|---|---|
| `ERR_CRITICAL_001` | Required input field missing | `Missing required input: {field}. Cannot start pipeline.` | Provide the missing field and re-run |
| `ERR_CRITICAL_002` | Language code not in supported profiles | `Language '{code}' has no profile in configs/language_profiles.md.` | Add a language profile or use a supported language |
| `ERR_CRITICAL_003` | Style ID not in supported profiles | `Style '{id}' has no profile in configs/style_profiles.md.` | Use a valid style ID |
| `ERR_CRITICAL_004` | System file missing at boot | `Required system file not found: {filepath}.` | Restore the missing file |
| `ERR_CRITICAL_005` | Dependency file missing before stage | `Stage {N} requires {filepath} which does not exist.` | Re-run the stage that should have created it |
| `ERR_CRITICAL_006` | Source report verdict is FAIL | `Stage 2 returned FAIL verdict. Research contains unresolvable fabrication.` | Fix source issues in research.md, re-run Stage 2 |
| `ERR_CRITICAL_007` | QA Stage 11 verdict is BLOCKED | `Final QA failed. Critical checks did not pass.` | Fix the specific files listed in qa_report.md |
| `ERR_CRITICAL_008` | Stage 12 attempted without READY_FOR_EXPORT | `Cannot export: QA verdict is not READY_FOR_EXPORT.` | Complete Stage 11 first |

### ERR_FAIL — Stage-halting content errors

| Code | Trigger | Message | Human Action |
|---|---|---|---|
| `ERR_FAIL_001` | Output file not written (stage completed but file missing) | `Stage {N} completed but {filename} was not created.` | Re-run the stage |
| `ERR_FAIL_002` | Output file is empty | `Stage {N} output {filename} is empty.` | Re-run the stage |
| `ERR_FAIL_003` | Script word count outside 15% of target | `Script word count {actual} is outside acceptable range {min}-{max}.` | Re-run Stage 4 with explicit word count instruction |
| `ERR_FAIL_004` | Hook exceeds 65 words | `Hook section contains {N} words. Maximum is 65.` | Revise the hook in script.md |
| `ERR_FAIL_005` | Hook opens with a channel greeting | `Hook begins with a channel greeting. Rewrite required.` | Revise the hook |
| `ERR_FAIL_006` | SRT timecodes overlap | `subtitles.srt contains overlapping timecodes at segment {N}.` | Re-run Stage 9 |
| `ERR_FAIL_007` | SRT line exceeds 42 characters | `subtitles.srt line {N} has {chars} characters. Maximum is 42.` | Re-run Stage 9 |
| `ERR_FAIL_008` | TBD entries in image_plan.md | `image_plan.md contains TBD entries in source strategy.` | Re-run Stage 7 |
| `ERR_FAIL_009` | SEO title exceeds 70 characters | `SEO title option {N} has {chars} characters. Maximum is 70.` | Re-run Stage 10 |
| `ERR_FAIL_010` | Markdown found in voice_script.txt | `voice_script.txt contains markdown characters: {chars found}.` | Re-run Stage 9 |

### ERR_WARN — Non-blocking warnings

| Code | Trigger | Logged message | Impact |
|---|---|---|---|
| `ERR_WARN_001` | Source report verdict is NEEDS_REVISION | `Source report has {N} flagged items. Review recommended.` | Research quality may be reduced |
| `ERR_WARN_002` | Script word count outside 10% but within 15% | `Word count {actual} is outside 10% target but within 15% tolerance.` | Slightly longer or shorter video |
| `ERR_WARN_003` | Fewer than 5 verified facts in research | `Only {N} verified facts found. Minimum recommended is 5.` | Thinner research — monitor script quality |
| `ERR_WARN_004` | Fewer than 3 sources found | `Only {N} sources found. Minimum recommended is 3.` | Reduced source credibility |
| `ERR_WARN_005` | Story outline speculation flags present | `Story outline contains {N} speculation beats. Will be labeled in script.` | Requires careful script handling |
| `ERR_WARN_006` | More than 2 [PAUSE:2s] in voice_script | `Voice script contains {N} dramatic pauses. Recommended maximum is 3.` | Pacing may feel excessive |
| `ERR_WARN_007` | Image plan escalation rate high | `{N}% of visual beats escalated to AI. Recommend increasing real image search.` | Lower visual authenticity |
| `ERR_WARN_008` | SEO tag count at boundary | `Tag count is {N}. Acceptable but at the lower/upper limit.` | Minor SEO impact |
| `ERR_WARN_009` | Consistency flag in story_bible | `Story bible found {N} consistency conflicts, now resolved.` | Previously inconsistent — now canonical |

### ERR_INFO — Informational only

| Code | Trigger | Logged message |
|---|---|---|
| `ERR_INFO_001` | Template version mismatch (warning, not error) | `Template version {V} may not be compatible with prompt version {V}.` |
| `ERR_INFO_002` | Niche derived from context (not explicit input) | `Niche '{niche}' derived from style input. Explicit niche not provided.` |
| `ERR_INFO_003` | Notes field empty | `No notes provided. Proceeding with standard configuration.` |
| `ERR_INFO_004` | channel_name not provided | `channel_name not set. SEO package will use placeholder.` |

---

## Error Response Templates

### CRITICAL Error Output

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⛔ CRITICAL ERROR — Pipeline Halted
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Error Code:   {ERR_CODE}
Stage:        {N} — {Stage Name}
File:         {affected file or "N/A"}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
What happened:
  {Specific description of what went wrong}

Why this is critical:
  {Why the pipeline cannot continue safely}

Required action:
  {Exact steps the human must take — numbered list}

To resume:
  After resolving, re-activate Director AI with:
  RESUME PROJECT: {project_slug}
  The pipeline will restart from Stage {N}.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### HARD FAIL Error Output

```
──────────────────────────────────────────────
❌ STAGE FAIL — Stage {N} Cannot Complete
──────────────────────────────────────────────
Error Code:   {ERR_CODE}
Stage:        {N} — {Stage Name}
Check failed: {exact checklist item}
File:         {affected file}

Issue:   {specific description}
Action:  {what to do to fix it}

Pipeline halted at Stage {N}.
Resolve and resume.
──────────────────────────────────────────────
```

### WARNING Output

```
[⚠ WARN {ERR_CODE}] {Short description}
  Detail: {More specific information}
  Action: Logged. Continuing pipeline.
```

### INFO Output

```
[ℹ INFO {ERR_CODE}] {Short description}
```

---

## Retry Logic

The Director AI may auto-retry a stage once before escalating to ERR_FAIL.

### Auto-Retry Conditions

The Director may silently retry a stage (maximum 1 retry) if:

| Condition | Retry strategy |
|---|---|
| Script word count out of range by ≤15% | Re-run with explicit count instruction appended to prompt |
| Missing pacing markers in voice_script | Re-run with explicit marker instruction |
| SRT segment duration exceeds 7 seconds | Re-run with explicit duration constraint |
| SRT line exceeds 42 characters | Re-run with explicit line length constraint |
| SEO tag count < 15 | Re-run with explicit tag count instruction |

### Auto-Retry Announcement

```
[RETRY] Stage {N}: {reason for retry}
Adjusting constraint: {what is being changed}
Re-running Stage {N}...
```

### Retry Failure

If the retry also fails, escalate immediately to ERR_FAIL — do not retry again.

```
[RETRY FAILED] Stage {N}: Second attempt also failed.
Escalating to ERR_FAIL.
```

---

## The No-Fabrication Error Protocol

This is the most important error class. MASTER_RULE.md Rule 2 forbids fabrication.

When the Director AI detects that it is about to write or has written fabricated content:

**Detection triggers:**
- A URL in research output that the Director cannot verify exists
- A named person whose existence cannot be confirmed from research
- A statistic or date with no source
- Content in the script not traceable to research_verified.md

**Action:**

1. Do not write the fabricated content (or if already written: mark for removal)
2. Log `ERR_FAIL_003` equivalent with the specific fabricated element
3. Replace the fabricated element with:
   - A `[UNVERIFIED — requires human confirmation]` label, OR
   - Removal of the claim entirely, OR
   - A clearly labeled speculation: "It has been suggested that..."
4. Continue the pipeline — fabrication detection does not halt the pipeline unless Stage 2 returns FAIL verdict

**The Director AI does not hallucinate and then hide it. Every uncertain claim is labeled.**

---

## Manifest Status on Error

| Error Type | Manifest `status` | Asset `status` |
|---|---|---|
| CRITICAL | `needs_revision` | `needs_revision` |
| HARD FAIL | `needs_revision` | `needs_revision` |
| WARNING | `in_progress` (continues) | `complete` (continues) |
| INFO | `in_progress` (continues) | unchanged |

After resolution and resume, asset statuses are reset to `pending` for the failed stage and all stages that depend on it.

---

## Error Log Format

Every error is recorded in `logs/director_run_log.md` under the stage entry:

```markdown
### Error: {ERR_CODE}
**Time:** {ISO datetime}
**Severity:** {CRITICAL / FAIL / WARN / INFO}
**Stage:** {N}
**File:** {filepath or "N/A"}
**Description:** {full error message}
**Action taken:** {what the Director did in response}
**Resolved:** {Yes / No — awaiting human}
```
