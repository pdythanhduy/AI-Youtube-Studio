# AI Image Prompts — 端島 / 軍艦島：消えた都市の謎
**Project:** hashima-island-mystery-ja
**Stage:** 8 — AI Image Prompts
**Date:** 2026-06-27

---

## Usage Notes

- These prompts are for AI image generation (Midjourney, DALL-E, Stable Diffusion, Firefly, etc.)
- All prompts produce fictional/AI-generated imagery — not photographs of Hashima Island
- Do NOT label AI-generated images as photographs in video
- Cross-reference with `image_plan.csv` for priority and scene assignment
- Negative prompts (`--no`) are formatted for Midjourney syntax; adapt for other tools

---

## Global Style Reference

**Consistent style across all images:**
- Cinematic, dark documentary
- Desaturated color palette (grey, blue-grey, muted brown)
- Film grain texture
- 16:9 aspect ratio
- No people visible in most shots (exceptions noted)

---

## Prompts

---

### PROMPT_001 — IMG001 (S001: Hook opening)

```
Abandoned concrete island rising from the sea, overcast grey sky, mist on the water, crumbling multi-story buildings visible above a weathered seawall, dramatic low angle view from sea level, cinematic wide shot, desaturated color palette, film grain, moody and atmospheric, dark documentary style --ar 16:9 --no people, text, logos, bright colors, clear weather
```

**Scene:** S001 HOOK opening
**Priority:** HIGH
**Notes:** The establishing image of the entire video. Should evoke isolation and mystery. Island should feel large and looming.

---

### PROMPT_002 — IMG002 (S002: Interior ruin)

```
Interior of abandoned multi-story concrete building, broken staircase leading into darkness, partially collapsed ceiling with shafts of natural light breaking through, peeling walls, exposed rebar, debris on floor, haikyo aesthetic, high contrast dramatic lighting, cinematic, desaturated with warm dust tones, film grain --ar 16:9 --no people, animals, furniture, modern objects, bright colors
```

**Scene:** S002 HOOK interior
**Priority:** HIGH
**Notes:** Haikyo (廃墟) aesthetic — Japanese ruin photography style. Light shafts are important visual element.

---

### PROMPT_003 — IMG003 (S003: Wave detail)

```
Close-up of powerful ocean waves crashing against aged weathered concrete seawall, white foam, spray, grey ocean, overcast sky, textural shot, slow shutter motion blur feel, documentary nature photography, muted grey-blue palette, cinematic --ar 16:9 --no people, text, logos, tropical colors
```

**Scene:** S003 HOOK wave
**Priority:** MEDIUM

---

### PROMPT_004 — IMG004 (S005: Meiji era atmosphere)

```
Simulated early 20th century Japanese industrial landscape, black and white, factory chimneys with smoke rising, steel structures, raw atmosphere of industrialization, grainy vintage photograph aesthetic, sepia toned, no identifiable individuals, atmosphere suggests labor and industry, Meiji era Japan --ar 16:9 --no modern elements, color, faces, logos, text
```

**Scene:** S005 ACT I Meiji context
**Priority:** HIGH
**Notes:** Simulated archive look. Should feel like a historical photograph, not a modern digital render. No identifiable real people.

---

### PROMPT_005 — IMG005 (S007: Aerial CG view)

```
Aerial bird's eye view of a small isolated concrete island in the middle of open ocean, densely packed multi-story concrete apartment buildings covering nearly the entire island, weathered and crumbling, dramatic overcast sky, cinematic CG render style, architectural detail visible, dark dramatic atmosphere --ar 16:9 --no people, boats, clear sky, bright colors
```

**Scene:** S007 ACT I aerial
**Priority:** HIGH
**Notes:** Should convey the extraordinary density of buildings on such a tiny island. The scale contrast is the story.

---

### PROMPT_006 — IMG006 (S008: Building 30 exterior)

```
Exterior of a very large deteriorating concrete apartment block, multiple stories, 1910s Japanese architectural style, vegetation growing through cracks in concrete, broken windows, grey overcast sky, wide angle establishing shot, somber documentary photography style, desaturated, film grain, sense of abandoned grandeur --ar 16:9 --no people, modern signage, cars, bright sunlight
```

**Scene:** S008 ACT I Building 30
**Priority:** HIGH

---

### PROMPT_007 — IMG007 (S010: Interior detail)

```
Interior ruin detail, close-up of metal chair frame partially collapsed, concrete debris surrounding it, broken window frame in background with overcast sky visible, selective focus, decay detail, haikyo photography aesthetic, warm dust light against cool concrete, melancholic --ar 16:9 --no people, faces, recognizable objects, bright colors
```

**Scene:** S010 ACT II interior detail
**Priority:** MEDIUM

---

### PROMPT_008 — IMG008 (S011: Mine atmosphere)

```
Abstract mine tunnel interior, narrow passage disappearing into darkness, single dim light source casting harsh shadows on rough rock walls, deep shadow, noir lighting, oppressive atmosphere, no people, abstract and atmospheric, cinematic close-up perspective --ar 16:9 --no people, modern equipment, text
```

**Scene:** S011 ACT II mine atmosphere
**Priority:** HIGH
**Notes:** CRITICAL — this scene represents the period of forced labor history. Must be abstract and atmospheric ONLY. No people. No documentary-style depictions.

---

### PROMPT_009 — IMG009 (S015: Empty dock)

```
Empty abandoned dock or pier extending over calm water, rusted metal railing along side, overcast sky, grey-green water, no boats, no people, desolate tranquil atmosphere, muted color palette, cinematic medium shot, film grain --ar 16:9 --no people, text, bright sunlight, modern elements
```

**Scene:** S015 ACT III empty dock
**Priority:** MEDIUM

---

### PROMPT_010 — IMG010 (S016: Symbolic still life)

```
Abandoned weathered book lying on a crumbling concrete desk or surface, dust, dim atmospheric single light source, dark background, mood of memory and abandonment, still life photography aesthetic, warm amber tones against dark background, symbolic --ar 16:9 --no people, faces, identifiable text, modern objects
```

**Scene:** S016 ACT III symbolic
**Priority:** HIGH
**Notes:** Symbolic representation of lives left behind. Not documentary reconstruction. Keep abstract.

---

### PROMPT_011 — IMG011 (S017: Light study)

```
Dramatic shafts of natural light breaking through collapsed concrete ceiling of abandoned building, dust particles visible in light beams, chiaroscuro lighting, beautiful and melancholic, cinematic, high contrast, dark surroundings with brilliant light shafts, film grain --ar 16:9 --no people, furniture, text
```

**Scene:** S017 ACT III light
**Priority:** HIGH

---

### PROMPT_012 — IMG012 (S018: Storm sea)

```
Stormy grey ocean waves near a dark concrete structure, heavy dark clouds, turbulent water, dramatic weather photography, grey-green palette, wide cinematic shot, powerful and threatening atmosphere --ar 16:9 --no people, boats, sunlight, tropical colors
```

**Scene:** S018 ACT III storm
**Priority:** MEDIUM

---

### PROMPT_013 — IMG013 (S019: Concrete texture)

```
Extreme macro close-up of crumbling concrete wall surface, deep cracks spreading across the surface, rusted corroded rebar exposed, salt and mineral deposits, textural abstract beauty, muted grey-brown tones, high detail --ar 16:9
```

**Scene:** S019 ACT III texture
**Priority:** MEDIUM

---

### PROMPT_014 — IMG014 (S020: Ma beat wide)

```
Minimalist wide landscape, ocean horizon, overcast sky, barely visible silhouette of ruined island in far distance, very slow contemplative mood, extreme wide angle, muted grey-blue palette, timeless, empty, film grain, no focal point, abstract landscape --ar 16:9 --no people, boats, bright colors, clear sky, sunlight
```

**Scene:** S020 ACT IV Ma beat
**Priority:** HIGH
**Notes:** The Ma beat image. Emptiness IS the subject. Should feel like visual silence.

---

### PROMPT_015 — IMG015 (S021: Faded sign)

```
Close-up of concrete ruin wall with partially visible faded Japanese signage, characters worn and barely legible, concrete surface crumbling, weathered and aged, documentary close-up, desaturated with muted warmth --ar 16:9 --no modern text, logos, bright colors, legible modern Japanese
```

**Scene:** S021 ACT IV faded sign
**Priority:** MEDIUM

---

### PROMPT_016 — IMG016 (S022: Ma beat ocean — silence)

```
Abstract ocean waves in extreme wide shot, island edge barely visible at far left or right of frame, sky and sea taking up most of frame, minimalist composition, slow gentle waves, contemplative, near monochrome, extreme emptiness --ar 16:9 --no people, text, boats, focal objects, bright colors
```

**Scene:** S022 ACT IV silence (Ma beat core — no narration over this)
**Priority:** HIGH
**Notes:** This is the 10-second pure silence section of the Ma beat. Most abstract image in the project.

---

### PROMPT_017 — IMG017 (S023: Tourist boat)

```
Small tourist vessel on calm ocean, approaching a large weathered concrete island in distance, slightly warmer palette than rest of video, contemporary feel, medium shot from water level, subtle optimism in lighting compared to earlier scenes --ar 16:9 --no people visible, text, logos, dramatic weather
```

**Scene:** S023 OUTRO tourist boat
**Priority:** LOW

---

### PROMPT_018 — IMG018 (S024: Final frame)

```
Hashima Island full panoramic view, concrete ruins rising from ocean, wide sky above, clouds, ocean in foreground, final cinematic establishing shot, balanced composition, haunting and beautiful, desaturated cinematic, prepares for fade to black --ar 16:9 --no people, text, bright colors
```

**Scene:** S024 OUTRO final frame
**Priority:** HIGH

---

## Generation Checklist

| ID | Scene | Priority | Generated | Approved |
|---|---|---|---|---|
| PROMPT_001 | S001 | HIGH | ☐ | ☐ |
| PROMPT_002 | S002 | HIGH | ☐ | ☐ |
| PROMPT_003 | S003 | MEDIUM | ☐ | ☐ |
| PROMPT_004 | S005 | HIGH | ☐ | ☐ |
| PROMPT_005 | S007 | HIGH | ☐ | ☐ |
| PROMPT_006 | S008 | HIGH | ☐ | ☐ |
| PROMPT_007 | S010 | MEDIUM | ☐ | ☐ |
| PROMPT_008 | S011 | HIGH | ☐ | ☐ |
| PROMPT_009 | S015 | MEDIUM | ☐ | ☐ |
| PROMPT_010 | S016 | HIGH | ☐ | ☐ |
| PROMPT_011 | S017 | HIGH | ☐ | ☐ |
| PROMPT_012 | S018 | MEDIUM | ☐ | ☐ |
| PROMPT_013 | S019 | MEDIUM | ☐ | ☐ |
| PROMPT_014 | S020 | HIGH | ☐ | ☐ |
| PROMPT_015 | S021 | MEDIUM | ☐ | ☐ |
| PROMPT_016 | S022 | HIGH | ☐ | ☐ |
| PROMPT_017 | S023 | LOW | ☐ | ☐ |
| PROMPT_018 | S024 | HIGH | ☐ | ☐ |
