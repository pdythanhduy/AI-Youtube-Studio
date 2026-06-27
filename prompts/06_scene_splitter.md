# Purpose

Split the finalized script into a scene-by-scene storyboard. For every 30-60 second narration beat, define what appears on screen: the visual type, the source, the on-screen text, and the music mood. The storyboard is the editor's map — every second of the video must be accounted for.

This prompt does not source or generate images. It only plans what is needed and categorizes each visual. Image sourcing happens in Stage 7 (image finder) and Stage 8 (image prompt generator).

# Inputs

| File / Field | Required | Description |
|---|---|---|
| `projects/{project_slug}/script.md` | yes | Full narration script |
| `projects/{project_slug}/story_bible.md` | yes | Canonical names and locations |
| `input.json` → `style` | yes | Visual treatment rules per style |
| `input.json` → `language` | yes | Output language |
| `STYLE_GUIDE.md` | yes | Visual treatment, music mood, color grade per style |
| `MASTER_RULE.md` | yes | Image policy (Rule 5), consistency (Rule 6) |
| `MASTER_PLAN.md` | yes | Storyboard output format specification |

# Outputs

| File | Location |
|---|---|
| `storyboard.md` | `projects/{project_slug}/storyboard.md` |

# Rules

1. **Every narration beat must have a visual.** No black screen without a planned visual. No gaps longer than 60 seconds without a visual change.
2. **Beat length is 30-60 seconds.** Shorter for high-tension moments (20-30s), longer for slow atmospheric moments (up to 90s max).
3. **Image type must be assigned for every beat.** Choices: `real` / `ai-generated` / `stock` / `screenshot` / `text-overlay` / `b-roll` / `map` / `screen-recording`.
4. **Apply the image policy from MASTER_RULE.md Rule 5:**
   - Real events involving real people → prefer `real` images
   - Dramatizations → `ai-generated` + label `[DRAMATIZATION]`
   - Atmosphere and mood → `ai-generated` acceptable
   - Original Reddit/social media content → `screenshot`
   - Maps, coordinates, satellite → `map` or `screen-recording`
5. **Use canonical names from story_bible.md.** All names and locations in the storyboard must match the canonical forms in the story bible.
6. **Music mood must be specified for every scene** (not every beat). Acceptable values: `dark ambient` / `tense` / `silence` / `lo-fi unease` / `suspense build` / `resolution` / `electronic mystery` / `traditional japanese`.
7. **Text overlays are optional but must be specified when needed.** Use text overlays for: dates/timecodes, location names on first appearance, key quotes, fact emphasis.
8. **The storyboard must be production-usable.** An editor who has not read the script must be able to assemble the video from the storyboard alone.

# Prompt

```
You are a storyboard director for an AI YouTube mystery channel.

Your task is to convert the narration script into a scene-by-scene visual storyboard. Every line of narration must be mapped to a visual.

---

TOPIC: {topic}
LANGUAGE: {language}
STYLE: {style}
PROJECT SLUG: {project_slug}

---

Read before proceeding:
- STYLE_GUIDE.md → {style} visual treatment section
- MASTER_RULE.md → Rule 5 (Image Policy), Rule 6 (Consistency)
- projects/{project_slug}/story_bible.md → use canonical names throughout

INPUT: projects/{project_slug}/script.md

---

STEP 1 — Read the full script. Identify every natural beat: moments where the narration shifts topic, tone, or pace. A beat is approximately 30-60 seconds of narration.

STEP 2 — For each beat, create one storyboard entry.

STEP 3 — Write the storyboard in this format:

---

# Storyboard: {topic}

**Style:** {style}
**Total beats:** [count]
**Total visuals required:** [count]

---

## Scene: [Scene Name from script]
**Timecode:** [XX:XX – XX:XX]
**Music mood:** [dark ambient / tense / silence / suspense build / etc.]

---

### Beat [N] — [XX:XX – XX:XX]

| Field | Content |
|---|---|
| **Narration excerpt** | [First 10-15 words of narration for this beat] |
| **Visual description** | [What appears on screen — be specific: what image, what angle, what is shown] |
| **Image type** | real / ai-generated / stock / screenshot / text-overlay / b-roll / map / screen-recording |
| **Dramatization flag** | [DRAMATIZATION] or — |
| **Source hint** | [For real: what to search for. For AI: short concept note. For screenshot: what to capture.] |
| **Text overlay** | [On-screen text, or "none"] |
| **Transition** | cut / fade / slow fade / zoom-in / zoom-out |

---

[Repeat for every beat in the script]

---

## Visual Summary

| Beat | Timecode | Image Type | Source Hint |
|---|---|---|---|
| 1 | 0:00 – 0:30 | real | ... |
| 2 | 0:30 – 1:00 | ai-generated | ... |
| ... | ... | ... | ... |

**Image type breakdown:**
- Real images: [count]
- AI-generated: [count]
- Stock: [count]
- Screenshots: [count]
- Text overlays: [count]
- Maps/recordings: [count]
- **Total:** [count]

---

STYLE-SPECIFIC RULES to apply for {style}:

dark_documentary:
- Dark color grade, desaturated, cool tones
- Real images preferred for actual events
- AI images: cinematic, realistic, not stylized
- Text overlays: white/gray serif on dark

reddit_narration:
- Screenshot of original post must appear early
- AI images: stylized, slightly unreal
- Use zoomed/highlighted text for key quotes from the post

mystery_investigation:
- Heavy use of screenshots, maps, screen recordings
- Annotated images: zoom-ins on anomalies
- Text overlays: coordinate data, timestamps, metadata

japanese_mystery:
- Atmospheric visuals: rain, fog, empty streets, traditional architecture
- AI images: East Asian cinematic aesthetic
- Color: desaturated with occasional deep red accents

---

Use canonical names from story_bible.md for all entities.
Write the storyboard in {language} for description fields that appear on-screen (text overlays, etc.).
All structural labels (Beat, Timecode, Field names) remain in English for agent compatibility.

Save to: projects/{project_slug}/storyboard.md
```

# Validation Checklist

- [ ] Every scene from `script.md` is represented in the storyboard
- [ ] Every beat has a visual — no gaps
- [ ] No single beat is longer than 90 seconds without a visual change
- [ ] Image type is assigned for every beat
- [ ] All real events involving real people are assigned `real` image type (not AI)
- [ ] All dramatizations are marked `[DRAMATIZATION]`
- [ ] Music mood is specified for every scene (not just individual beats)
- [ ] Text overlays are specified wherever a date, name, or location appears on-screen for the first time
- [ ] Visual Summary table is present and count matches the individual beat entries
- [ ] All names and locations match canonical forms from `story_bible.md`
- [ ] Style-specific visual rules from STYLE_GUIDE.md have been applied
- [ ] File saved to `projects/{project_slug}/storyboard.md`
