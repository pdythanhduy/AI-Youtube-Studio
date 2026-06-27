# Workflow Engine — AI YouTube Studio OS

The Workflow Engine executes individual pipeline stages. It receives a dispatch signal from the Director Engine, constructs the AI request, calls the model, writes the output file, and returns a completion signal. It knows nothing about what comes before or after its assigned stage — that is the Director's concern.

---

## Responsibility

The Workflow Engine is responsible for **how a single stage runs**. It loads the correct prompt, injects the correct inputs, calls the AI model, receives the response, and writes the output file.

**Single sentence:** The Workflow Engine is the factory floor — it builds exactly what the Director orders, nothing more.

---

## Inputs

| Input | Source | Description |
|---|---|---|
| Dispatch signal | Director Engine | Which stage to run, which project, which template |
| `prompts/NN_[stage].md` | `prompts/` | Prompt template for this stage |
| `templates/[niche]_template.md` | `templates/` | Niche-specific overrides and context |
| `configs/language_profiles.md` | `configs/` | Language-specific settings |
| `configs/style_profiles.md` | `configs/` | Style-specific settings |
| Project input files | `projects/{slug}/` | All upstream files the stage depends on |
| `input.json` | `projects/{slug}/` | User-provided parameters |

---

## Outputs

| Output | Destination | Description |
|---|---|---|
| Stage output file | `projects/{slug}/` | The generated content file |
| Completion signal | Director Engine | Success/failure + metadata |
| Run log entry | `projects/{slug}/run.log` | Timing, token count, model used |

---

## Dependencies

| Dependency | Type | Purpose |
|---|---|---|
| Director Engine | upstream | Receives dispatch; returns completion |
| Routing Engine | internal | Selects correct prompt + template combination |
| AI model (Claude) | external | Generates content |
| `core/naming_conventions.md` | reference | Canonical output file names |
| `core/file_lifecycle.md` | reference | Atomic write rules |

---

## Execution Flow

For every dispatched stage:

```
1. Receive dispatch signal
2. Mark asset status: "in_progress" in manifest
3. Load prompt file → prompts/NN_[stage].md
4. Load template file → templates/[niche]_template.md (via Routing Engine)
5. Load all dependency files from projects/{slug}/
6. Load config: language_profiles.md + style_profiles.md for this run
7. Construct AI request:
   a. System prompt = core identity + MASTER_RULE.md rules (condensed)
   b. User prompt = stage prompt with all {placeholders} resolved
   c. Context = dependency file contents (injected as context blocks)
   d. Constraints = word count, language, style from input.json + config
8. Write output file (atomic write — tmp → rename)
9. Update manifest: set asset status to "complete"
10. Return completion signal to Director Engine
```

### Placeholder Resolution

Every `{placeholder}` in a prompt file is resolved before the AI call:

| Placeholder | Resolved from |
|---|---|
| `{topic}` | `input.json` → `topic` |
| `{language}` | `input.json` → `language` |
| `{style}` | `input.json` → `style` |
| `{niche}` | `input.json` → `niche` |
| `{project_slug}` | Computed from date + topic |
| `{video_length_minutes}` | `input.json` → `video_length_minutes` |
| `{channel_name}` | `input.json` → `channel_name` (or empty string) |

Any unresolved placeholder causes the Workflow Engine to halt before the AI call and return an error to the Director.

---

## AI Request Construction

### System Prompt Structure
```
You are a [role from prompt file] for the AI YouTube Studio OS.

You must follow these rules at all times:
[MASTER_RULE condensed — top 5 most relevant rules for this stage]

Language: {language}
Style: {style}
Niche: {niche}
```

### Context Injection Order
Context files are injected in this order (smallest to largest, most specific last):
1. `input.json` (always first — establishes all parameters)
2. `story_bible.md` (if exists — canonical names)
3. Stage-specific dependency files (e.g., `research_verified.md` for script writer)
4. Stage prompt body

### Model Settings (default)
| Setting | Value | Rationale |
|---|---|---|
| Model | `claude-opus-4-8` | Maximum capability for creative/analytical tasks |
| Thinking | `{type: "adaptive"}` | Enabled for complex stages (research, script, outline) |
| Streaming | Yes | Prevents timeout on long outputs |
| Max tokens | Stage-dependent | See stage token budgets below |

### Stage Token Budgets

| Stage | Typical Output | Max Tokens |
|---|---|---|
| 01_research | 1,500-3,000 words | 4,096 |
| 02_source_verifier | 1,000-2,000 words | 3,072 |
| 03_story_outline | 800-1,500 words | 2,048 |
| 04_script_writer | 1,000-3,000 words | 6,144 |
| 05_story_bible | 600-1,200 words | 2,048 |
| 06_scene_splitter | 1,500-3,000 words | 4,096 |
| 07_image_finder | 1,000-2,500 words | 3,072 |
| 08_image_prompt_generator | 1,500-3,500 words | 4,096 |
| 09_voice_director | 2,000-4,000 words | 6,144 |
| 10_youtube_seo | 800-1,500 words | 2,048 |

---

## Error Handling

| Error Type | Action |
|---|---|
| Unresolved placeholder | Halt before AI call. Return error to Director. |
| Dependency file missing | Halt. Return error: "stage_XX dependency [file] not found." |
| AI call timeout | Retry once. If timeout again: return error to Director. |
| AI call returns empty response | Return error to Director. |
| Output file write failure | Delete `.tmp`. Return error to Director. |
| Token limit exceeded | Reduce context (trim oldest dependency file). Retry once. |

---

## Run Log Format

Every stage execution appends to `projects/{slug}/run.log`:

```
[2026-06-27T10:43:15Z] stage_04 STARTED
  prompt: prompts/04_script_writer.md
  template: templates/mystery_template.md
  model: claude-opus-4-8
  input_tokens: 3847
[2026-06-27T10:44:02Z] stage_04 COMPLETE
  output: script.md
  output_tokens: 2103
  duration_seconds: 47
  word_count: 1547
```

---

## Future Automation Points

| Point | Description |
|---|---|
| Parallel execution | Run independent stages (voice_script + storyboard) concurrently |
| Model routing | Route cheap stages (subtitles, SEO) to Haiku 4.5 to reduce cost |
| Streaming preview | Stream output to a live preview UI as it generates |
| Cache layer | Cache unchanged stage inputs — skip re-execution if inputs unchanged |
| Batch API | Use Claude Batch API for non-time-sensitive stages to reduce cost |
