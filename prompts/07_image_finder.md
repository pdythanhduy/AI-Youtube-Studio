# Purpose

For every `real`, `stock`, `screenshot`, `map`, or `screen-recording` beat in the storyboard, produce a specific image-finding brief: where to look, what to search for, what license to check, and what to do if no suitable real image exists. This prompt does not generate AI images — it sources real, legally usable images first, and escalates to AI only when real images genuinely cannot be found.

The output is a sourcing action plan, not the images themselves. A human or automation agent uses this plan to collect the actual assets.

# Inputs

| File / Field | Required | Description |
|---|---|---|
| `projects/{project_slug}/storyboard.md` | yes | Scene-by-scene visual plan |
| `projects/{project_slug}/story_bible.md` | yes | Canonical names and locations for search terms |
| `input.json` → `topic` | yes | Search context |
| `input.json` → `niche` | yes | Affects where to search |
| `input.json` → `language` | yes | Output language |
| `MASTER_RULE.md` | yes | Rule 5 (Image Policy) — legal and type requirements |

# Outputs

| File | Location |
|---|---|
| `image_plan.md` | `projects/{project_slug}/image_plan.md` |

# Rules

1. **Real images first.** For every beat marked `real`, `stock`, `screenshot`, `map`, or `screen-recording` in the storyboard, attempt to find a real, legally usable image before escalating to AI.
2. **AI escalation is a last resort.** Only recommend AI generation when:
   - No real image of the subject exists (historical events, private locations, fictional subjects)
   - The only available real images are under restrictive copyright with no fair use justification
   - The scene is explicitly a dramatization
   - The topic is a purely online/fictional story (NoSleep, creepypasta)
3. **Legal source priority (highest to lowest):**
   - Public domain (Wikimedia Commons, Internet Archive, government archives)
   - Creative Commons licensed (CC0, CC BY, CC BY-SA) — note attribution requirements
   - News images used under fair use (brief educational/commentary use, not for commercial thumbnails)
   - Official screenshots from the platform that is the subject (Reddit, Google Maps — for commentary)
   - Stock photo sites with standard license (Pexels, Pixabay, Unsplash — check license per image)
   - Screen captures from documentaries or news broadcasts (fair use — short clips only)
4. **For each beat, provide 2-3 alternative search strategies.** If the first search fails, the second and third should offer a viable path.
5. **Never recommend sourcing from watermarked images** unless you also identify the originating platform where the clean version can be licensed or downloaded.
6. **For screenshots of Reddit, social media, or internet content:** Specify the exact URL pattern or subreddit to navigate to. Note whether the content requires login to access.
7. **For maps and satellite imagery:** Specify exact coordinates, zoom level, and whether Google Maps, Google Earth, or another mapping service is most appropriate.
8. **Flag any beat where no legal real image is likely available** with `[ESCALATE TO AI]`. These beats feed directly into Stage 8 (image prompt generator).

# Prompt

```
You are an image research specialist for an AI YouTube mystery channel.

Your task is to create a detailed image sourcing plan for every visual beat in the storyboard that requires a real, stock, screenshot, map, or screen-recorded image.

---

TOPIC: {topic}
NICHE: {niche}
LANGUAGE: {language}
PROJECT SLUG: {project_slug}

---

Read before proceeding:
- MASTER_RULE.md Rule 5 (Image Policy) — apply legal sourcing hierarchy strictly
- projects/{project_slug}/story_bible.md — use canonical search terms

INPUT: projects/{project_slug}/storyboard.md

---

STEP 1 — Read the storyboard. Identify every beat with image type: real / stock / screenshot / map / screen-recording.
Skip beats marked ai-generated and text-overlay — those are handled in Stage 8.

STEP 2 — For each identified beat, produce a sourcing brief.

STEP 3 — Write the image plan in this format:

---

# Image Plan: {topic}

**Total beats requiring real images:** [count]
**Total beats escalated to AI:** [count]

---

## Beat [N] — [Scene Name] ([Timecode])

| Field | Content |
|---|---|
| **Storyboard description** | [Visual description from storyboard] |
| **Image type** | real / stock / screenshot / map / screen-recording |
| **Subject to photograph/find** | [What specifically needs to be shown] |

### Search Strategy A (Primary)
- **Platform:** [Where to search first]
- **Search terms:** `[exact search string]`
- **License to look for:** [Public domain / CC0 / CC BY / Fair use / Stock standard]
- **Expected result:** [What type of image should appear]

### Search Strategy B (Fallback)
- **Platform:** [Second option]
- **Search terms:** `[exact search string]`
- **License:** [License type]

### Search Strategy C (Last resort)
- **Platform:** [Third option]
- **Notes:** [Any special instructions — login required, archive URL pattern, etc.]

### Legal Notes
- [Any copyright risk, attribution requirements, or fair use considerations]

### Escalation
- [REAL IMAGE AVAILABLE — do not escalate] OR [ESCALATE TO AI — reason: no real image exists / all images under restrictive copyright / scene is a dramatization]

---

[Repeat for every applicable beat]

---

## Platform Quick Reference

### For news/documentary images:
- Wikimedia Commons: commons.wikimedia.org/wiki/Special:Search?search=[term]
- Internet Archive: archive.org/search?query=[term]
- BBC / Reuters / AP Photo — search site directly, use for fair use commentary

### For maps and satellite:
- Google Maps: maps.google.com → navigate to coordinates → screenshot
- Google Earth: earth.google.com → coordinates → 3D or satellite view
- For Japanese locations: Google Maps Japan interface often has street view

### For Reddit/forum screenshots:
- Direct URL: reddit.com/r/[subreddit]/comments/[post_id]
- Archive version: web.archive.org/web/*/reddit.com/r/[subreddit]/...
- Note: Reddit requires login for some content — specify if so

### For stock photos:
- Pexels: pexels.com/search/[term] — free, no attribution required
- Pixabay: pixabay.com/images/search/[term] — free, check individual license
- Unsplash: unsplash.com/s/photos/[term] — free, attribution appreciated

---

## AI Escalation List
Beats that cannot be sourced with real images and must use AI generation:

| Beat | Scene | Reason for Escalation | Concept for AI Prompt |
|---|---|---|---|
| [N] | [Scene name] | [Why no real image] | [Brief concept — expands in Stage 8] |

---

Write the image plan in {language} for any on-screen text fields.
All structural labels remain in English for agent compatibility.
Save to: projects/{project_slug}/image_plan.md
```

# Validation Checklist

- [ ] Every beat with `real`, `stock`, `screenshot`, `map`, or `screen-recording` type from the storyboard has a sourcing brief
- [ ] AI-generated and text-overlay beats are skipped (handled in Stage 8)
- [ ] Every sourcing brief has at least 2 search strategies
- [ ] Every sourcing brief specifies the license type to check
- [ ] Search terms use canonical names from `story_bible.md` (not inconsistent spellings)
- [ ] All Reddit/social media sourcing notes specify exact URL pattern or subreddit
- [ ] All map beats specify coordinates and mapping platform
- [ ] Legal notes are present for any fair use usage
- [ ] AI Escalation List is present and lists only beats that cannot be sourced with real images
- [ ] AI Escalation List includes a concept note for each escalated beat (feeds Stage 8)
- [ ] No watermarked images recommended without identifying the clean source
- [ ] File saved to `projects/{project_slug}/image_plan.md`
