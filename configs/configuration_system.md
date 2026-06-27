# Configuration System — AI YouTube Studio OS

The configuration system provides all tunable parameters for the pipeline — language settings, style settings, model routing, QA thresholds, cost controls, and output formats. Configuration is the single knob panel for the entire system. Logic lives in engines. Instructions live in prompts. Parameters live here.

---

## Design Principles

1. **No logic in configs.** A config file is a value store. It contains no if/then statements, no prompt text, and no generated content.
2. **One config key, one meaning.** Each key means exactly one thing across the entire system. No key is reused with different meanings in different contexts.
3. **Configs have defaults.** Every key has a documented default. Running with no config overrides must produce valid behavior.
4. **Configs are versioned.** Every config file includes a `schema_version` field. A schema version bump means a structural change — engines must handle or reject unknown schema versions.
5. **Configs are environment-independent.** The same config file runs identically on any machine. No hardcoded paths, no environment variables embedded in values.
6. **Configs are human-readable.** The format is Markdown with structured YAML-like blocks or JSON sections, not binary or opaque formats.

---

## Config File Structure

Each config file uses this structure:

```markdown
# [Config File Name]

**Schema version:** 1.0
**Last updated:** YYYY-MM-DD
**Owned by:** [component that reads this config]

---

## Section Name

[Description of this section]

### [Profile or Key Name]

| Key | Type | Default | Description |
|---|---|---|---|
| `key_name` | string/int/bool/float/enum | `default_value` | What it controls |
```

---

## Global System Configuration Schema

The following keys are defined in `configs/configuration_system.md` and govern the entire system:

### Pipeline Control

| Key | Type | Default | Description |
|---|---|---|---|
| `pipeline.auto_retry_enabled` | bool | `true` | Whether failed stages are retried automatically |
| `pipeline.max_auto_retries` | int | `2` | Maximum retries per stage per run |
| `pipeline.halt_on_fail_verdict` | bool | `true` | Whether `[FAIL]` in source_report halts the pipeline |
| `pipeline.require_human_on_escalation` | bool | `true` | Whether human-escalated decisions halt the pipeline |
| `pipeline.parallel_stages_enabled` | bool | `false` | (Future) Whether independent stages run concurrently |

### QA Thresholds

| Key | Type | Default | Description |
|---|---|---|---|
| `qa.word_count_tolerance` | float | `0.10` | ±% word count tolerance for script |
| `qa.voice_script_word_count_tolerance` | float | `0.05` | ±% tolerance for voice_script.txt vs script.md |
| `qa.max_subtitle_line_chars` | int | `42` | Max characters per subtitle line |
| `qa.max_subtitle_duration_seconds` | int | `7` | Max duration per subtitle segment |
| `qa.min_subtitle_duration_seconds` | float | `1.0` | Min duration per subtitle segment |
| `qa.min_tags` | int | `15` | Min YouTube tags |
| `qa.max_tags` | int | `30` | Max YouTube tags |
| `qa.title_max_chars` | int | `70` | Max YouTube title length |
| `qa.description_hook_chars` | int | `150` | Chars that constitute the description hook |
| `qa.min_verified_facts` | int | `5` | Min facts required in research.md |
| `qa.min_sources` | int | `3` | Min sources required in research.md |

### Decision Policies

| Key | Type | Default | Description |
|---|---|---|---|
| `decision.accept_unconfirmed_urls` | bool | `false` | Whether to accept sources with unconfirmed URLs |
| `decision.require_human_on_flag` | bool | `false` | Whether every [FLAG] requires human sign-off |
| `decision.max_flags_before_halt` | int | `5` | Max [FLAG] items before pipeline halts |
| `decision.auto_escalate_to_ai_images` | bool | `true` | Auto-escalate when real image search fails |

### Model Routing

| Key | Type | Default | Description |
|---|---|---|---|
| `model.default` | string | `claude-opus-4-8` | Default model for all stages |
| `model.overrides.stage_05` | string | `claude-sonnet-4-6` | Override for story_bible (extraction task) |
| `model.overrides.stage_06` | string | `claude-sonnet-4-6` | Override for scene_splitter (formatting task) |
| `model.overrides.stage_07` | string | `claude-sonnet-4-6` | Override for image_finder (lookup task) |
| `model.overrides.stage_10` | string | `claude-sonnet-4-6` | Override for youtube_seo (structured output) |
| `model.thinking` | string | `adaptive` | Thinking mode for supported stages |
| `model.streaming` | bool | `true` | Whether to stream responses |

### Cost Controls

| Key | Type | Default | Description |
|---|---|---|---|
| `cost.alert_threshold_usd` | float | `2.00` | Alert if single project exceeds this cost |
| `cost.hard_limit_usd` | float | `10.00` | Hard stop if project exceeds this cost |
| `cost.track_tokens` | bool | `true` | Whether to log token counts per stage |

### Analytics

| Key | Type | Default | Description |
|---|---|---|---|
| `analytics.enabled` | bool | `true` | Whether analytics are collected |
| `analytics.learning_trigger_count` | int | `10` | Projects between learning cycles |
| `analytics.retain_run_logs_days` | int | `30` | Days to retain run.log files |
| `analytics.retain_qa_reports_days` | int | `90` | Days to retain per-project QA reports |

### Export

| Key | Type | Default | Description |
|---|---|---|---|
| `export.create_bundle` | bool | `true` | Whether to create export_bundle/ directory |
| `export.bundle_encoding` | string | `utf-8` | Text encoding for all exported files |
| `export.line_endings` | string | `lf` | Line ending style: `lf` or `crlf` |
| `export.json_indent` | int | `2` | JSON pretty-print indent spaces |
| `export.archive_after_publish` | bool | `true` | Auto-archive when publish confirmed |

---

## Config Override Mechanism

Configs are loaded in this priority order (highest priority first):

```
1. Run-time override (passed directly in dispatch signal)
2. Project-level override (in input.json → config_overrides)
3. Environment-level config (configs/local_overrides.md — not committed to git)
4. System config (configs/configuration_system.md)
5. Built-in defaults (hardcoded in each engine)
```

**Example: project-level override in input.json**
```json
{
  "topic": "...",
  "language": "en",
  "video_length_minutes": 12,
  "style": "dark_documentary",
  "config_overrides": {
    "qa.word_count_tolerance": 0.15,
    "model.overrides.stage_04": "claude-sonnet-4-6"
  }
}
```

---

## What Cannot Be Overridden

The following rules are enforced by engines directly and cannot be overridden by any config:

- No-fabrication rule (MASTER_RULE.md Rule 2)
- No-fake-URL rule (part of Rule 2)
- No realistic depiction of real people in AI images (Rule 5)
- No sensitive content generation (Rule 11)

These are compiled into engine behavior, not config values.

---

## Adding a New Config Key

1. Add the key to the appropriate section in this file with type, default, and description.
2. Bump `schema_version` (minor version for new keys, major version for structural changes).
3. Add handling for the new key in the engine that reads it.
4. Add a test in `tests/acceptance_tests.md` for the new key's effect.
5. Document the key in `docs/roadmap_v1.md` changelog section.
