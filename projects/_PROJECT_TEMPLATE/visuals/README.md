# visuals/ — Visual Planning and Image Assets

This folder contains all visual production assets. It is written by Stages 6, 7, and 8.

---

## Files

### `storyboard.md` — Shot-by-shot visual plan (Stage 6)

**Written by:** Director AI running `prompts/06_scene_splitter.md`

Contains:
- **Visual beats** — every 30-90 second segment with a distinct visual
- **Image type** per beat: `real` / `ai-generated` / `stock` / `screenshot` / `text-overlay` / `b-roll` / `map` / `screen-recording`
- **Visual description** — what should be on screen
- **Music mood** per scene
- **On-screen text** — any text overlays needed
- **Transition type** — cut / fade / wipe / zoom
- **[DRAMATIZATION]** flag on any AI beats depicting real events
- **Visual Summary table** — total count of beats by image type

This is the editor's shot list.

**Status after stage:** `storyboard.status = complete` in manifest

---

### `image_plan.md` — Image sourcing brief (Stage 7)

**Written by:** Director AI running `prompts/07_image_finder.md`

Contains, for each `real`, `stock`, `screenshot`, `map`, or `screen-recording` beat:
- **Beat reference** — which storyboard beat this covers
- **Search Strategy A** — primary search approach with search terms and source
- **Search Strategy B** — backup search approach
- **License type** to look for
- **Notes** — any special sourcing considerations

Also contains:
- **AI Escalation List** — beats where real image sourcing is unlikely and AI generation is recommended

**No TBD entries allowed.** Every beat must have a complete sourcing strategy.

**Status after stage:** `image_plan.status = complete` in manifest

---

### `ai_image_prompts.md` — Image generation prompts (Stage 8)

**Written by:** Director AI running `prompts/08_image_prompt_generator.md`

Contains one entry per AI-generated beat (from storyboard + escalation list):
- **Beat reference**
- **Full image generation prompt** — subject, setting, mood, lighting, color palette, camera angle, style, aspect ratio (16:9)
- **Negative prompt** — what to avoid
- **Simplified alternative prompt** — backup if the main prompt fails
- **[DRAMATIZATION — NOT REAL]** label for any beat depicting a real event

These prompts are ready to paste into Midjourney, DALL-E, or any image generation tool.

**Status after stage:** `ai_image_prompts.status = complete` in manifest

---

## Human Review Points

After Stage 6: Review the storyboard for pacing. If any scene has too many or too few visual changes, you may adjust and re-run Stage 7.

After Stage 7: Source the real images using the search strategies. Mark which beats you've found images for. Anything still unresolved moves to the AI escalation list.

After Stage 8: Review AI image prompts before generating. Confirm that no prompt depicts real people realistically. Confirm [DRAMATIZATION] labels are present where needed.

---

## What Does NOT Belong Here

- Script or narration (go in `script/`)
- Generated image files — store in a subfolder you create: `visuals/generated/`
- Downloaded/sourced images — store in: `visuals/sourced/`
- Voice files (go in `voice/`)
