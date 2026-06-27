# Batch 2A Generation Plan Report
## hashima-island-mystery-ja
**Date:** 2026-06-27
**Gate:** Batch 2A AI Image Generation Plan
**Source:** assets/ai_images/generation_queue.json + safety audit

---

## 1. Scope

Batch 2A covers 5 READY_WITH_REWRITE images selected for low historical sensitivity:

| image_id | scene_id | section | timecode |
|----------|----------|---------|----------|
| IMG003 | S003 | HOOK | 0:25–0:40 |
| IMG010 | S011b | ACT_II | 4:40–5:00 |
| IMG011 | S013 | ACT_II | 5:30–6:00 |
| IMG012 | S015 | ACT_III | 6:30–7:00 |
| IMG013 | S016 | ACT_III | 7:00–7:30 |

**Excluded from Batch 2A (deferred to Batch 2B or later):**
- IMG014 (S017), IMG015 (S018), IMG017 (S021), IMG019 (S023) → Batch 2B
- IMG008 (S009) → Batch 2B (school interior, recently unblocked)
- IMG009 (S011a) → mine gate, separate gate (FIX-M1)
- IMG001, IMG007, IMG016 → HUMAN_REVIEW_REQUIRED (legal hold)

---

## 2. Prompt Audit — Flag Words

Scanned all 5 prompts for: haunting / oppressive / terrifying / horror / ghostly / nightmare / cursed

| image_id | Flag word found | Action |
|----------|-----------------|--------|
| IMG003 | None | No change |
| IMG010 | None | No change |
| IMG011 | **melancholic** | Replaced with **reflective** |
| IMG012 | None | No change |
| IMG013 | None | No change |

**1 flag word corrected. 4 negative prompts expanded.**

---

## 3. Image-by-Image Audit

---

### IMG003 — S003 — Weathered Wooden Door (Hook)

**Scene:** HOOK, 0:25–0:40, 15 seconds, close_up, static
**Narration:** L003 (general island description)
**Historical sensitivity:** NONE

**Audit:**
All 10 safety dimensions pass. Pure architecture/texture. No historical claim. Lowest-risk image in this batch.

**Rewrite:** None required.

**Note on scene mismatch (already resolved):** Original generation_queue.json PROMPT_003 was ocean waves — completely wrong for S003 (wooden door close-up). The rewritten prompt in the queue already corrects this. Final prompt is correct for scene.

---

### IMG010 — S011b — Mine Rock Face Texture (ACT II)

**Scene:** ACT_II, 4:40–5:00, 20 seconds, extreme_close_up, slow_zoom_in
**Narration:** L015 (follows forced labor narration in S011a)
**Historical sensitivity:** LOW — image is pure geology; editorial context is post-forced-labor emotional beat

**Audit:**
All 10 safety dimensions pass. The phrase "dark coal mine rock" identifies geology accurately — it does not depict people, confinement, or suffering. "Dark and austere" is factual tone for underground rock.

**Key distinction:** S011b serves as an emotional exhale after the forced labor narration (S011a). The image itself makes zero historical claim. Rock strata is not forced labor imagery.

**Also note:** This image is the fallback for IMG009 (mine tunnel). Generate it regardless of IMG009 outcome.

**Rewrite:** None to positive prompt. Negative prompt expanded:
- Added: silhouettes, shadows of persons, chains, shackles
- Reason: In dark mine environments, AI models can generate human-coded shapes in shadows. The expanded terms close that risk for a close-up rock texture.

---

### IMG011 — S013 — Heritage Tension Light Ruins (ACT II)

**Scene:** ACT_II, 5:30–6:00, 30 seconds, wide_shot, slow_pan_left
**Narration:** L017 (UNESCO World Heritage tension)
**Historical sensitivity:** LOW — architectural metaphor, no human reference

**Audit:**
1 flag word found: **melancholic**

`melancholic` biases AI models toward heavier grief imagery in an already-dark ruin setting. For the UNESCO tension scene (S013), the correct tone is contemplative — not sorrowful. The narration addresses the tension between cultural heritage and unresolved history, which is a factual observation, not a grieving one.

**Rewrite applied:** "beautiful and melancholic" → "beautiful and reflective"

**Visual duplication note:** IMG014 (S017, Batch 2B) also uses dramatic light shafts. After both images are generated, the director should compare them and ensure variety in angle, beam count, or composition.

---

### IMG012 — S015 — Abandoned Dock (ACT III)

**Scene:** ACT_III, 6:30–7:00, 30 seconds, medium_shot, slow_zoom_out
**Narration:** Context: mine closure period, stillness
**Historical sensitivity:** NONE

**Audit:**
All 10 safety dimensions pass. "Stillness after industrial activity ceased" is accurate: the Hashima mine closed in 1974. No human reference. "Desolate tranquil" is acceptable documentary language.

**Motion note:** "slow zoom out" removed from positive prompt (it is a post-production motion instruction, not a generation parameter). Post-processing note added.

**Rewrite:** None to positive prompt. Negative prompt expanded: added watermark, logos.

---

### IMG013 — S016 — Personal Items Still Life (ACT III)

**Scene:** ACT_III, 7:00–7:30, 30 seconds, close_up, slow_zoom_in
**Narration:** L020 (personal belongings / community that lived here)
**Historical sensitivity:** MEDIUM — emotionally charged objects, requires careful QA

**Audit:**
No flag words. All 10 safety dimensions pass.

**Historical context:** S016 documents the civilian community of Hashima — the 5,000+ residents who lived there as families, including children, for decades before the 1974 evacuation. The child's shoe and personal items reference the evacuation, NOT forced labor. Forced labor occurred 1939–1945 (wartime). S016 is in ACT_III (7:00–7:30), after the forced labor section has ended. These objects represent community memory, not victim exploitation.

**Critical risk — faded photograph prop:**
The `old photograph` element in the prompt is the highest risk in this batch. AI models may generate a face in the photograph prop even with explicit --no instructions. The protection phrase "too damaged and faded to show any identifiable features" is already in the positive prompt. The negative prompt has been expanded to cover all variants:
- `identifiable faces in photographs`
- `human faces visible in photograph prop`
- `recognizable features`
- `legible photograph content`

**Critical QA gate (MANDATORY):** Inspect the photograph prop in every output. Any visible face → reject immediately and regenerate. Max 3 attempts. If 3 attempts all produce a visible face: use the fallback prompt (shoe + can only, no photograph) provided in the batch plan JSON.

**Rewrite:** None to positive prompt. Negative prompt expanded significantly.

---

## 4. Final Verified Prompts

### IMG003
```
Close-up of a weathered wooden door in a ruined concrete building, paint peeling in thick layers, moss and vines creeping across the aged wood surface, texture-focused documentary close-up, muted grey-green tones, concrete wall visible on sides, haikyo aesthetic, cinematic --ar 16:9 --no people, text, logos, bright colors, modern objects, glass, watermark
```

### IMG010
```
Extreme macro close-up of rough hewn rock tunnel wall surface, jagged crevices in dark coal mine rock, geological strata visible, sparse dim light raking across the surface from one side, deep shadows in crevices, mineral deposits and sediment layers, textural abstract beauty, near-abstract composition, dark and austere, no text, no people --ar 16:9 --no people, text, modern equipment, tools, human presence, silhouettes, shadows of persons, chains, shackles, watermark, logos
```

### IMG011
```
Wide view of abandoned concrete ruins, dramatic shafts of natural light breaking through collapsed ceiling, dust particles visible in light beams, suggestion of former grand scale now in decay, haikyo aesthetic, chiaroscuro lighting, beautiful and reflective, cinematic, high contrast, dark surroundings with brilliant light shafts, film grain --ar 16:9 --no people, furniture, text, UNESCO plaque, modern signage, watermark, logos
```

### IMG012
```
Empty abandoned dock or pier extending over calm grey water, rusted metal railing along the side, crumbling concrete edge and bollards, overcast sky, grey-green water, no boats, desolate tranquil atmosphere, stillness after industrial activity ceased, muted color palette, cinematic medium shot, film grain --ar 16:9 --no people, text, bright sunlight, modern elements, boats, vehicles, watermark, logos
```

### IMG013
```
Abandoned personal belongings left behind in ruins, close-up still life: a weathered child's shoe with worn leather, a crumbling old photograph lying face-up but too damaged and faded to show any identifiable features, a rusted empty metal can on dusty concrete surface, dim atmospheric single light source from one side, warm amber tones against dark concrete background, mood of memory and hasty departure, still life photography aesthetic, symbolic --ar 16:9 --no people, faces, identifiable faces in photographs, human faces visible in photograph prop, recognizable features, legible photograph content, legible text, modern objects, logos, watermark, bright colors
```

---

## 5. Output Filenames

| image_id | output_filename |
|----------|----------------|
| IMG003 | `IMG003_S003_wooden_door_closeup.png` |
| IMG010 | `IMG010_S011b_mine_rock_texture.png` |
| IMG011 | `IMG011_S013_heritage_light_ruins.png` |
| IMG012 | `IMG012_S015_abandoned_dock.png` |
| IMG013 | `IMG013_S016_personal_items.png` |

**Save to:** `assets/ai_images/generated/batch_2a/`

---

## 6. QA Gate Summary (After Generation)

| image_id | Primary QA check | Critical gate |
|----------|-----------------|--------------|
| IMG003 | No people, no modern objects, muted palette | No |
| IMG010 | No human-coded shadows, no tools/chains | No |
| IMG011 | No people, no UNESCO plaque, light shafts present | No |
| IMG012 | No boats, calm water, muted palette | No |
| IMG013 | **No face in photograph prop** | **YES — reject on any visible face** |

---

## 7. Final Output

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BATCH 2A GENERATION PLAN — RESULT

Batch 2A image count:     5
Image IDs:                IMG003, IMG010, IMG011, IMG012, IMG013

Safety status:
  IMG003  READY_WITH_REWRITE → APPROVED (no changes)
  IMG010  READY_WITH_REWRITE → APPROVED (negative prompt expanded)
  IMG011  READY_WITH_REWRITE → APPROVED (rewrite: melancholic→reflective)
  IMG012  READY_WITH_REWRITE → APPROVED (negative prompt expanded)
  IMG013  READY_WITH_REWRITE → APPROVED + CRITICAL QA GATE

Batch 2A generation may begin: YES
Output directory: assets/ai_images/generated/batch_2a/
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
