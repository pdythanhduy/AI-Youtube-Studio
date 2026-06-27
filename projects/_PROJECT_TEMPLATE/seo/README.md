# seo/ — YouTube SEO Package

This folder contains all YouTube publishing assets. It is written by Stage 10.

---

## Files

### `seo.md` — Complete SEO package (Stage 10)

**Written by:** Director AI running `prompts/10_youtube_seo.md`

Contains:

**Titles (3 options)**
- Each option ≤70 characters (character count stated in file)
- Options ranked from most clickable to safest
- Follows niche-specific title patterns

**Description**
- First 150 characters: hook (appears in search previews — no greeting)
- Body (200-400 words): storytelling, key facts, context
- Chapters: timecoded list matching story_outline.md scenes
- Links section: placeholder for relevant links
- Hashtags: ≤5 embedded in the description body

**Tags (15-30)**
- Mix of broad and specific
- At least 2 long-tail tags (5+ words)
- Non-English projects include English Tags Addendum

**Pinned Comment (2 options)**
- Option A: engagement question for discussion
- Option B: additional context or chapter highlight

**Status after stage:** `seo.status = complete` in manifest

---

### `thumbnail_prompt.md` — Thumbnail design brief (Stage 10)

**Written by:** Director AI running `prompts/10_youtube_seo.md`

Contains:
- **Thumbnail Concept** — what the thumbnail should show and why it works for the niche
- **Image Generation Prompt** — ready to use in Midjourney/DALL-E for the background image
- **Text Overlay** — primary text (max 4 words), secondary text (optional)
- **Color Palette** — 2-3 hex codes matching the style profile
- **Layout Guidance** — where to place text and subject on the frame
- **Style Notes** — what makes a thumbnail in this niche perform well

**Status after stage:** `thumbnail_prompt.status = complete` in manifest

---

## How to Use These Files

1. **Choose a title:** Select one of the three options in `seo.md`. The first option is typically the most click-optimized; the second or third are safer if your channel is more conservative.

2. **Prepare the description:** The description in `seo.md` has placeholder markers where you should add your own links. Fill those in before uploading.

3. **Adjust chapters:** The chapter timecodes are estimated. Update them to match your final video after editing.

4. **Copy tags:** Copy the tags list exactly into YouTube Studio. Do not add extra commas — YouTube's tag limit is per tag, not per character.

5. **Design the thumbnail:** Use `thumbnail_prompt.md` to generate your background image. Then add the text overlay in Canva or Photoshop.

6. **Post the pinned comment:** Immediately after publishing, post one of the two pinned comment options as your first comment.

---

## What Does NOT Belong Here

- Script or narration (go in `script/`)
- Thumbnail image files — create these externally and upload directly to YouTube
- Voice files (go in `voice/`)
