# Export Engine — AI YouTube Studio OS

The Export Engine runs once, at the end of a successful pipeline, when the Director Engine signals that all stages have passed QA. It performs the final packaging: validates the complete project bundle, generates the final `export_manifest.json`, organizes files for handoff to editors or upload tools, and triggers the archival process. It is the last component that touches a project before it leaves the system.

---

## Responsibility

The Export Engine is responsible for **packaging the complete project for production use and archiving the run**. It confirms that everything exists, everything is consistent, and everything is labeled correctly before handing the project to the editor.

**Single sentence:** The Export Engine is the shipping department — it inspects, packages, and dispatches the final product.

---

## Inputs

| Input | Source | Description |
|---|---|---|
| Director signal: `export_ready` | Director Engine | Trigger to begin export |
| All project output files | `projects/{slug}/` | The complete project bundle |
| `export_manifest.json` (current) | `projects/{slug}/` | Current pipeline state |
| `MASTER_RULE.md` Rule 12 | System | Export readiness checklist |
| `configs/output_profiles.md` | `configs/` | Output format specifications |

---

## Outputs

| Output | Destination | Description |
|---|---|---|
| `export_manifest.json` (final) | `projects/{slug}/` | Status set to `ready_for_production` or `needs_revision` |
| `export_bundle/` | `projects/{slug}/export_bundle/` | Organized copy of all files for editor handoff |
| Archive trigger | Memory Engine | Signal to extract project data to knowledge layer |
| `editor_handoff.md` | `projects/{slug}/export_bundle/` | Editor-facing summary of all assets |

---

## Dependencies

| Dependency | Type | Purpose |
|---|---|---|
| Director Engine | upstream | Receives signal; returns export result |
| QA Engine | reference | Final export checklist mirrors QA rules |
| Memory Engine | downstream | Archive trigger after export complete |
| Analytics Engine | downstream | Final run metrics |
| `configs/output_profiles.md` | reference | File format requirements |

---

## Export Process

### Step 1: Pre-Export Validation

Run the complete export readiness checklist from MASTER_RULE.md Rule 12. Every item must pass:

```
EXPORT READINESS CHECKLIST:

Core files (must exist and be non-empty):
[ ] research.md
[ ] source_report.md
[ ] research_verified.md
[ ] story_outline.md
[ ] script.md
[ ] story_bible.md
[ ] storyboard.md
[ ] image_plan.md
[ ] ai_image_prompts.md
[ ] voice_script.txt
[ ] voice_direction.md
[ ] subtitles.srt
[ ] thumbnail_prompt.md
[ ] seo.md

Content checks:
[ ] No TBD entries in image_plan.md
[ ] No [FAIL] entries in source_report.md
[ ] Script word count within target range
[ ] At least one AI image prompt per escalated beat
[ ] SRT file is valid (timecodes sequential, no overlap)
[ ] All SEO title options ≤70 characters
[ ] Description first 150 characters is a hook

Consistency checks:
[ ] All names match story_bible.md canonical forms
[ ] All dates consistent across files
[ ] Image count in image_plan.md matches storyboard visual count
[ ] Voice script word count matches script.md ±5%
[ ] Chapter timestamps in seo.md match scene structure in story_outline.md
```

If any item fails: set `export_manifest.json → status` to `needs_revision`. Return to Director with specific failures listed. Do not create the export bundle.

### Step 2: Build Export Bundle

Create `projects/{slug}/export_bundle/` with a clean, editor-facing file organization:

```
export_bundle/
├── editor_handoff.md           ← Start here — explains every file
│
├── 01_production_assets/
│   ├── voice_script.txt        ← TTS or voice actor input
│   ├── voice_direction.md      ← Delivery notes for voice work
│   └── subtitles.srt           ← Import into editor timeline
│
├── 02_visual_assets/
│   ├── storyboard.md           ← Visual plan — read first
│   ├── image_plan.md           ← Sourcing instructions per beat
│   └── ai_image_prompts.md     ← Generate these before editing
│
├── 03_publishing/
│   ├── thumbnail_prompt.md     ← Design thumbnail from this
│   └── seo.md                  ← Copy/paste into YouTube Studio
│
└── 04_reference/
    ├── script.md               ← Full narration (reference only)
    ├── story_bible.md          ← Canonical names/dates
    └── research_verified.md    ← Source documentation
```

Source files (`research.md`, `source_report.md`, `story_outline.md`, `run.log`, QA reports, `decisions.log`) are not included in the export bundle. They remain in the main project folder for archival.

### Step 3: Write Editor Handoff

Generate `export_bundle/editor_handoff.md`:

```markdown
# Editor Handoff: [Topic]
**Project:** {project_slug}
**Ready for production:** {datetime}

## Quick Start
1. Read `02_visual_assets/storyboard.md` for the complete shot list
2. Source or generate all images using `02_visual_assets/image_plan.md` and `02_visual_assets/ai_image_prompts.md`
3. Generate voice audio using `01_production_assets/voice_script.txt`
4. Import subtitles using `01_production_assets/subtitles.srt`
5. Design the thumbnail using `03_publishing/thumbnail_prompt.md`
6. Upload using the YouTube metadata in `03_publishing/seo.md`

## Asset Summary
| Asset | File | Status |
|---|---|---|
| Voice script | voice_script.txt | Ready |
| Voice direction | voice_direction.md | Ready |
| Subtitle file | subtitles.srt | Ready |
| Storyboard | storyboard.md | Ready |
| Image plan | image_plan.md | [N] real images, [N] AI to generate |
| AI image prompts | ai_image_prompts.md | [N] prompts |
| Thumbnail prompt | thumbnail_prompt.md | Ready |
| SEO package | seo.md | [N] title options, [N] tags |

## Important Notes
[Any flags from QA — warnings, minor issues, things editor should know]
```

### Step 4: Finalize Manifest

Update `export_manifest.json`:
- Set top-level `status` to `ready_for_production`
- Set `exported_at` timestamp
- Set `export_bundle_path`
- Set `editor_handoff_path`

### Step 5: Trigger Downstream Signals

1. Signal Memory Engine → extract project data to knowledge layer
2. Signal Analytics Engine → write final project analytics
3. Signal Learning Engine (if threshold met) → trigger learning cycle

---

## Output Profile Application

Before writing the export bundle, the Export Engine applies output format specifications from `configs/output_profiles.md`:

| Profile Setting | Applied To | Effect |
|---|---|---|
| `encoding` | All `.md` and `.txt` files | Ensure UTF-8 encoding |
| `line_endings` | All text files | Normalize to LF (Unix) or CRLF (Windows) per profile |
| `srt_encoding` | `subtitles.srt` | UTF-8 with BOM for maximum compatibility |
| `json_pretty_print` | `export_manifest.json` | Indent 2 spaces |
| `max_line_length` | `voice_script.txt` | Wrap at 100 chars (optional, for readability) |

---

## Future Automation Points

| Point | Description |
|---|---|
| YouTube auto-upload | Export Engine calls YouTube Data API to draft the video with pre-filled metadata |
| Cloud storage sync | Upload export bundle to Google Drive, Dropbox, or S3 for team access |
| Editor notification | Send Slack/email to editor with handoff summary when export is ready |
| Asset pre-download | Automatically download all real images from image_plan.md sourcing strategies |
| TTS auto-generation | Trigger ElevenLabs API call with voice_script.txt to generate audio file |
| Packaging formats | Export bundle as ZIP or tar for easy transfer |
