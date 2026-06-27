# Purpose

Transform the verified research brief into a structured narrative outline. The outline defines the story arc, scene order, emotional beats, and pacing plan for the full video — before any script is written. This is the blueprint the script writer follows.

A good outline answers: What does the viewer feel at each moment? What information do they learn? What question keeps them watching?

# Inputs

| File / Field | Required | Description |
|---|---|---|
| `projects/{project_slug}/research_verified.md` | yes | Verified facts and sources |
| `input.json` → `topic` | yes | Video subject |
| `input.json` → `language` | yes | Output language |
| `input.json` → `video_length_minutes` | yes | Determines number of scenes |
| `input.json` → `style` | yes | Narrative style — see STYLE_GUIDE.md |
| `input.json` → `niche` | yes | Content category — shapes structure |
| `input.json` → `notes` | no | Specific angles to include or exclude |
| `STYLE_GUIDE.md` | yes | Narrative structure templates per style |
| `MASTER_RULE.md` | yes | Hook standard (Rule 4), no fabrication (Rule 2) |

# Outputs

| File | Location |
|---|---|
| `story_outline.md` | `projects/{project_slug}/story_outline.md` |

# Rules

1. **The hook must be chosen first.** Select the single most compelling moment from the research. Build the outline backward and forward from that moment.
2. **Every scene must have a purpose.** Label each scene's narrative function: Setup / Rising Tension / Revelation / Dead End / Climax / Resolution / Open Question.
3. **The outline must not contain fabricated events.** Every scene must trace back to a verified fact in `research_verified.md`. If a scene requires speculation, label it `[Speculation — will be labeled in script]`.
4. **Word count targets must be distributed across scenes.** Use `video_length_minutes` to calculate total words, then allocate per scene based on importance.
5. **Follow the narrative structure for the specified `style`.** See STYLE_GUIDE.md for the Three-Act Mystery, Reddit Narration, and Investigation structures.
6. **For `reddit_mystery` niche:** The outline must include a beat for the original post, a beat for community reaction, and a beat for the update or disappearance of OP.
7. **For `japanese_mystery` niche:** The outline must include a cultural context beat early in the video.
8. **For `google_maps_mystery` niche:** The outline must build the discovery progressively — don't reveal everything in the first scene.
9. **Emotional arc must be explicit.** Label the intended viewer emotion at each scene: Curiosity / Unease / Dread / Shock / Sadness / Confusion / Intrigue.
10. **The ending must be honest.** If the case is unsolved, the outline must end on an open question, not a fabricated resolution.

# Prompt

```
You are a narrative architect for an AI YouTube mystery channel.

Your task is to create a story outline for the following video. The outline is not the script — it is the blueprint the script writer will follow.

---

TOPIC: {topic}
LANGUAGE: {language}
VIDEO LENGTH: {video_length_minutes} minutes
STYLE: {style}
NICHE: {niche}
SPECIAL NOTES: {notes}

---

Read before proceeding:
- STYLE_GUIDE.md — use the narrative structure template for {style}
- MASTER_RULE.md — apply Hook Standard (Rule 4) and No Fabrication (Rule 2)

INPUT: projects/{project_slug}/research_verified.md

---

STEP 1 — Identify the Hook Moment.

From the verified research, select the single most compelling moment: the most shocking fact, the most disturbing image, the most unanswerable question. This is your hook.

Write: "HOOK MOMENT: [what it is and why it works]"

STEP 2 — Calculate scene structure.

Total word target = {video_length_minutes} × 130
Scene count guide:
- 5-8 min → 3-4 scenes + hook + conclusion
- 8-12 min → 4-5 scenes + hook + conclusion
- 12-20 min → 5-7 scenes + hook + conclusion

STEP 3 — Write the story outline in this format:

---

# Story Outline: {topic}

## Hook (Target: 0:00 - 0:30 | ~65 words)
- **Moment:** [What the viewer hears/sees immediately]
- **Viewer emotion:** [What they feel]
- **Question planted:** [What question makes them keep watching?]

## Introduction / Context (Target: 0:30 - ~1:30 | ~130 words)
- **Purpose:** Setup
- **Key information delivered:** [What the viewer learns here]
- **Viewer emotion:** [Curiosity / Initial unease]
- **Transition hook:** [What question or statement pulls them into Scene 1?]

## Scene 1: [Name] (Target: ~1:30 - ~X:XX | ~[N] words)
- **Purpose:** [Setup / Rising Tension / Revelation / Dead End / Climax]
- **Facts used:** [List the specific facts from research_verified.md that appear here]
- **Viewer emotion:** [What the viewer feels in this scene]
- **Key beat:** [The most important moment of this scene — one sentence]
- **Transition:** [How does this scene end and lead to the next?]

[Repeat for all scenes]

## Climax Scene: [Name] (Target: ~X:XX - ~X:XX | ~[N] words)
- **Purpose:** Climax
- **The central unanswerable question or most disturbing fact**
- **Viewer emotion:** Dread / Shock / Profound unease

## Conclusion (Target: last ~1:00 | ~130 words)
- **Purpose:** Resolution or Open Question
- **What is known for certain:** [Summary of confirmed facts]
- **What remains unknown:** [The unresolved question]
- **Final image/statement:** [What is the last thing the viewer thinks about?]
- **Call to action:** [Subscribe prompt — one line only, not melodramatic]

---

## Emotional Arc Summary
List the intended viewer emotion for each scene in order:
Hook → [emotion] → Scene 1 → [emotion] → ... → Conclusion → [emotion]

## Word Count Plan
| Section | Target Words |
|---|---|
| Hook | ~65 |
| Introduction | ~130 |
| Scene 1 | ~[N] |
| ... | ... |
| Conclusion | ~130 |
| **Total** | **~[total]** |

## Speculation Flags
List any outline beats that require speculation (events not in research_verified.md):
- Scene [N]: [what is speculative] — will be labeled in script

---

Write the outline in {language}.
Save to: projects/{project_slug}/story_outline.md
```

# Validation Checklist

- [ ] Hook moment is identified and clearly described
- [ ] Every scene has a named narrative purpose (Setup / Rising Tension / etc.)
- [ ] Every scene lists the specific verified facts it draws from
- [ ] Every scene has an explicit viewer emotion label
- [ ] Word count plan is present and totals within ±10% of `video_length_minutes × 130`
- [ ] Narrative structure matches the `{style}` template in STYLE_GUIDE.md
- [ ] For `reddit_mystery`: original post beat, community reaction beat, and OP update beat all present
- [ ] For `japanese_mystery`: cultural context beat present in early scenes
- [ ] For `google_maps_mystery`: discovery is revealed progressively (not in scene 1)
- [ ] Conclusion ends on honest open question if the case is unsolved — no fabricated resolution
- [ ] Speculation flags section lists any non-verified beats
- [ ] Output is in the correct language (`{language}`)
- [ ] File saved to `projects/{project_slug}/story_outline.md`
