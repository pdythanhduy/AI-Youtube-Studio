# input/ — Production Inputs

This folder contains the configuration and inputs for this production run. It is written at Stage 0 (Project Setup) by the Director AI.

---

## Files

### `input.json` — Core production inputs (auto-generated)

Written by the Director AI at Stage 0. Do not edit after the pipeline has started.

```json
{
  "project_id": "YYYYMMDD_topic-slug",
  "topic": "Video topic",
  "language": "en",
  "video_length_minutes": 12,
  "style": "dark_documentary",
  "niche": "internet_mystery",
  "target_word_count": 1560,
  "created_at": "2026-06-27T10:00:00Z",
  "schema_version": "1.0"
}
```

### `project.yaml` — Project configuration overrides (you fill this in)

Copy from `configs/project.yaml.example`. Fill in the four required fields. All other fields are optional overrides. The Director AI reads this file during boot.

**Required fields:**
```yaml
project:
  topic: "Your topic"
  language: "en"
  video_length_minutes: 12
  style: "dark_documentary"
```

---

## Stage 0 Checklist

Before running the Director AI, confirm:

- [ ] `project.yaml` has all four required fields filled in
- [ ] Language code is valid: `en`, `ja`, or `vi`
- [ ] Style ID is valid: `dark_documentary`, `reddit_narration`, `mystery_investigation`, or `japanese_mystery`
- [ ] Duration is an integer between 5 and 60

---

## What Does NOT Belong Here

- Research notes (go in `research/`)
- Draft scripts (go in `script/`)
- Images or visual references (go in `visuals/`)
- Any output files from the pipeline stages
