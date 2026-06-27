# Purpose

Generate one detailed, ready-to-use image generation prompt per beat that requires an AI-generated image. Prompts must be self-contained — a designer or AI image tool (Midjourney, DALL-E, Stable Diffusion, Leonardo) must be able to produce the correct image using only the prompt, with no additional context.

Every prompt must serve the visual style of the video, match the emotional tone of the scene, and follow the image policy rules (no real people depicted unless clearly stylized/non-photorealistic).

# Inputs

| File / Field | Required | Description |
|---|---|---|
| `projects/{project_slug}/storyboard.md` | yes | Identifies which beats need AI images |
| `projects/{project_slug}/image_plan.md` | yes | AI Escalation List with concept notes |
| `projects/{project_slug}/story_bible.md` | yes | Canonical locations, settings, terminology |
| `input.json` → `style` | yes | Visual treatment rules per style |
| `input.json` → `niche` | yes | Affects aesthetic (e.g., Japanese vs. Western mystery) |
| `input.json` → `language` | yes | Output language for descriptive fields |
| `STYLE_GUIDE.md` | yes | Color palette, visual tone, aesthetic references per style |
| `MASTER_RULE.md` | yes | Rule 5 — AI image labeling, no fake evidence |

# Outputs

| File | Location |
|---|---|
| `ai_image_prompts.md` | `projects/{project_slug}/ai_image_prompts.md` |

# Rules

1. **One prompt per beat.** Do not combine multiple beats into one image. Each beat needs its own distinct visual.
2. **Prompts must be self-contained.** The prompt must specify: subject, setting, mood, lighting, color palette, camera angle, style, and aspect ratio. Do not assume the tool has any context about the video.
3. **Do not depict real people realistically.** For dramatizations involving real individuals: use silhouettes, backs of heads, obscured faces, or clearly artistic/non-photorealistic styles. Never generate a realistic likeness of a real person.
4. **Label every AI-generated beat as `[AI-GENERATED]`.** For dramatizations: also label `[DRAMATIZATION — NOT REAL]`.
5. **Match the visual style rules from STYLE_GUIDE.md for `{style}`:**
   - `dark_documentary`: cinematic, realistic, desaturated, cool blue/gray tones
   - `reddit_narration`: slightly stylized, impressionistic, not photorealistic
   - `mystery_investigation`: clean, technical, documentary-style, neutral color
   - `japanese_mystery`: painterly, East Asian aesthetic, atmospheric, red accent available
6. **Aspect ratio must be specified.** Standard: 16:9 (YouTube). Thumbnail: 16:9 crop-ready. Portrait insert: 9:16.
7. **Negative prompts must be included for tools that support them** (Midjourney, Stable Diffusion). Specify what to exclude: text, watermarks, cartoon style, overly bright colors, etc.
8. **No fake evidence.** Do not prompt for images that look like real documents, police reports, news photos, or screenshots of real platforms. AI images must be clearly atmospheric/cinematic, not fabricated evidence.

# Prompt

```
You are a visual art director for an AI YouTube mystery channel.

Your task is to write one complete image generation prompt for every beat that requires an AI-generated image.

---

TOPIC: {topic}
STYLE: {style}
NICHE: {niche}
LANGUAGE: {language}
PROJECT SLUG: {project_slug}

---

Read before proceeding:
- STYLE_GUIDE.md → {style} visual treatment section — apply color palette and aesthetic rules
- MASTER_RULE.md → Rule 5 — Never depict real people realistically. Label all AI images.

INPUT FILES:
- projects/{project_slug}/storyboard.md → identify all beats with image type = ai-generated
- projects/{project_slug}/image_plan.md → AI Escalation List with concept notes
- projects/{project_slug}/story_bible.md → canonical location names and setting details

---

STEP 1 — Read the storyboard. Collect all beats where image type = ai-generated.
Add any beats from the image_plan.md AI Escalation List (beats escalated from real to AI).

STEP 2 — For each beat, write a complete image generation prompt.

STEP 3 — Write the output in this format:

---

# AI Image Prompts: {topic}

**Style:** {style}
**Total AI image prompts:** [count]

---

## Beat [N] — [Scene Name] ([Timecode])

**Scene context:** [One sentence — what is happening in the narration at this moment]
**Emotional tone:** [What should the viewer feel looking at this image]
**Label:** [AI-GENERATED] / [AI-GENERATED | DRAMATIZATION — NOT REAL]

### Midjourney / DALL-E Prompt
```
[Full prompt — include all of the following:]
[Subject]: [What is in the image — be specific]
[Setting]: [Where — interior/exterior, time of day, weather, era]
[Mood]: [Emotional quality — ominous, eerie, peaceful, desolate, etc.]
[Lighting]: [Type and direction of light — moonlight, fluorescent, candlelight, backlit, etc.]
[Color palette]: [Dominant colors — muted blues, warm amber, desaturated gray, deep red accent, etc.]
[Camera angle]: [Wide establishing shot / close-up / overhead / eye-level / low angle]
[Style]: [Cinematic photography / oil painting / concept art / dark illustration / photorealistic]
[Aspect ratio]: 16:9
[Quality tags]: highly detailed, professional lighting, atmospheric, --ar 16:9
```

### Negative Prompt (for Stable Diffusion / Midjourney --no)
```
text, watermark, logo, cartoon, anime, bright colors, oversaturated, cheerful, daytime, happy, modern stock photo aesthetic, low quality, blurry
```

### Alternative Prompt (simpler version for DALL-E if complex prompt fails)
```
[Simplified 1-2 sentence version of the same concept]
```

### Notes
- **Real people:** [None / Silhouette only / Back of head / Not depicted]
- **Specific elements to include:** [Any detail from the story bible that must appear]
- **Specific elements to exclude:** [Anything that would misrepresent the story or look like fake evidence]

---

[Repeat for every AI image beat]

---

## Style Reference Summary

Apply these visual rules to every prompt in this project:

**{style} color palette:**
{
  dark_documentary: "desaturated, cool blue-gray shadows, muted tones, occasional warm amber accent for archival feel",
  reddit_narration: "slightly warm, dark backgrounds, digital-feeling, not cinematic — impressionistic rather than photorealistic",
  mystery_investigation: "neutral, clean, documentary-style — like a high-quality journalism photo",
  japanese_mystery: "atmospheric — mist, rain, deep shadows, traditional architecture accents, occasional deep crimson"
}

**Subjects that must never be depicted realistically:**
- Real named individuals (living or deceased) in documentary contexts
- Crime scenes that resemble actual crime scene photography
- Documents that look like official police or court records
- Screenshots that look like real social media posts (this is fake evidence)

---

Write structural labels in English (for agent compatibility).
Write scene context and notes fields in {language}.
Save to: projects/{project_slug}/ai_image_prompts.md
```

# Validation Checklist

- [ ] Every beat marked `ai-generated` in the storyboard has a prompt entry
- [ ] Every beat in the image_plan.md AI Escalation List has a prompt entry
- [ ] Every prompt includes: subject, setting, mood, lighting, color palette, camera angle, style, and aspect ratio
- [ ] Every prompt includes a negative prompt
- [ ] Every prompt includes an alternative simplified version
- [ ] No prompt attempts to generate a realistic likeness of a real named person
- [ ] No prompt could produce an image that looks like a fake document, screenshot, or police record
- [ ] All dramatization beats are labeled `[DRAMATIZATION — NOT REAL]`
- [ ] Color palette and visual style match the `{style}` rules from STYLE_GUIDE.md
- [ ] Aspect ratio is specified as 16:9 for all standard video beats
- [ ] Style Reference Summary is present at the end of the file
- [ ] File saved to `projects/{project_slug}/ai_image_prompts.md`
