# Template Architecture — AI YouTube Studio OS

Defines how niche templates work, how they compose with base prompts, and how the Routing Engine selects and applies them. Templates are not replacements for prompts — they are specializations that add niche-specific context, constraints, and structural requirements on top of the base prompt.

---

## The Prompt vs. Template Distinction

| Component | What it defines | Who owns it | Changes how often |
|---|---|---|---|
| **Prompt** (`prompts/`) | The universal structure and rules for a stage | Prompt engineer | Rarely |
| **Template** (`templates/`) | Niche-specific additions and overrides for that stage | Content strategist | Per-niche iteration |
| **Config** (`configs/`) | Tunable parameters | Architect | On configuration change |

**Rule:** A template must never duplicate content from a prompt. It extends the prompt. If a template finds itself repeating prompt content, the shared content belongs in the prompt.

---

## Template Composition Model

The Workflow Engine constructs an AI request using three layers, injected in order:

```
Layer 1: System Prompt
  = Core identity + condensed MASTER_RULE.md + stage role

Layer 2: Prompt File
  = Universal stage structure, rules, and output format
  → From: prompts/NN_[stage].md

Layer 3: Template Addendum
  = Niche-specific context, constraints, examples, and overrides
  → From: templates/[niche]_template.md#[stage_section]
```

The template addendum is injected after the base prompt, immediately before the stage output begins. This ensures:
- Universal rules from the prompt are always established first
- Niche specializations refine without overriding
- An AI model that reads both layers has complete context

---

## Template File Structure

Each template file is organized as sections corresponding to pipeline stages. The Routing Engine reads only the section relevant to the current stage — it does not inject the entire template file.

```markdown
# [Niche] Template — AI YouTube Studio OS

## Template Overview
[One paragraph: what makes this niche different, what special requirements exist]

## Niche Parameters
| Parameter | Value |
|---|---|
| niche_id | [canonical niche ID] |
| primary_language_markets | [e.g., en, ja] |
| special_rules | [any rules that override or extend MASTER_RULE.md] |

---

## Stage Addendum: stage_01 (Research)
[What additional research this niche requires beyond the base prompt]
[Specific sources to prioritize]
[Cultural context requirements]

## Stage Addendum: stage_02 (Source Verifier)
[Niche-specific source quality considerations]

## Stage Addendum: stage_03 (Story Outline)
[Niche-specific narrative structure requirements]
[Required beats that must appear]

## Stage Addendum: stage_04 (Script Writer)
[Tone, register, and stylistic requirements for this niche]
[Forbidden phrases or tropes]
[Required cultural handling]

## Stage Addendum: stage_05 (Story Bible)
[Any niche-specific entity types to track]

## Stage Addendum: stage_06 (Scene Splitter)
[Visual vocabulary for this niche]
[Required scene types]

## Stage Addendum: stage_07 (Image Finder)
[Preferred image sources for this niche]
[Legal considerations specific to this niche]

## Stage Addendum: stage_08 (Image Prompt Generator)
[Aesthetic style for AI images in this niche]
[Visual references]
[Forbidden visual elements]

## Stage Addendum: stage_09 (Voice Director)
[Delivery character for this niche]
[Pacing philosophy]

## Stage Addendum: stage_10 (YouTube SEO)
[SEO strategy for this niche]
[Primary keywords and search patterns]
[Thumbnail style guidance]
```

---

## Template Injection Point

When the Workflow Engine constructs a prompt for stage N, it appends the template addendum after the base prompt body, using this separator:

```
---

## Niche Specialization: {niche}

The following additional requirements apply to this {niche} production.
They extend the rules above — they do not replace them.

[TEMPLATE ADDENDUM CONTENT]

---
```

This separator makes the boundary between base prompt and template addendum visible in the AI request, preventing context confusion.

---

## Template Overrides

A template may override specific base prompt parameters using an explicit override block:

```markdown
## Parameter Overrides

These values override the base prompt defaults for this niche:

| Parameter | Base Value | This Template's Value | Reason |
|---|---|---|---|
| `hook_type` | `shocking_fact` | `in_media_res` | Reddit posts work better starting mid-story |
| `speculation_labeling` | `required` | `required + folklore_label` | Japanese mysteries need 伝説 vs 事実 distinction |
```

An override must always state the reason. Undocumented overrides are not permitted.

---

## Template Versioning

Templates are versioned independently from prompts. A template version is recorded in the template file's header:

```markdown
# Mystery Template
**Template version:** 1.2
**Compatible with prompt versions:** 01_research v1.x, 04_script_writer v1.x
**Last updated:** 2026-06-27
```

If a prompt is updated in a breaking way, the template's compatibility note is updated. A version mismatch between template and prompt causes the Routing Engine to emit a compatibility warning (not a hard error — the system continues but logs the warning).

---

## Available Templates

| Template File | Niche IDs | Primary Language |
|---|---|---|
| `mystery_template.md` | `internet_mystery`, `unexplained_events`, `lost_places`, `google_maps_mystery` | `en` |
| `japan_template.md` | `japanese_mystery` | `ja`, `en` |
| `reddit_template.md` | `reddit_mystery` | `en`, `vi` |

---

## Creating a New Template

1. Create `templates/[niche_id]_template.md`
2. Follow the standard template structure (all 10 stage addendum sections)
3. Declare `niche_parameters` including `niche_id` (must match `core/naming_conventions.md`)
4. Define stage addenda for all 10 stages (even if some say "No additional requirements for this stage")
5. Add a row to the Available Templates table in this document
6. Add routing support in `engine/routing_engine.md`
7. Write an acceptance test in `tests/acceptance_tests.md`
8. No prompt files need to be modified — templates are additive

---

## Template Quality Standards

A template is complete if:
- All 10 stage sections are present
- No stage section is empty (if no additions needed, state explicitly: "No additional requirements for this stage beyond the base prompt")
- All overrides are documented with reasons
- Version and compatibility info is in the header
- The template has been tested against at least one full pipeline run
