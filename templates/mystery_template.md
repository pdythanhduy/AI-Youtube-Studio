# Mystery Template — AI YouTube Studio OS

Niche template for Internet Mystery, Unexplained Events, Lost Places, and Google Maps Mystery content.

**Template version:** 1.0
**Compatible with prompt versions:** All v1.x prompts
**Niche IDs covered:** `internet_mystery`, `unexplained_events`, `lost_places`, `google_maps_mystery`
**Last updated:** 2026-06-27

---

## Template Overview

Internet mystery content covers real-world events, places, and phenomena that remain genuinely unexplained. The defining quality of this niche is ambiguity — the story does not have a clean ending. The audience comes for the unsolved puzzle, not the solution. Content must be factually grounded, atmospherically crafted, and intellectually honest about what is and is not known.

Google Maps mystery is a sub-variant with a distinct visual investigation angle — these videos are driven by satellite imagery, coordinates, and the question of what is visible (and why).

## Niche Parameters

| Parameter | Value |
|---|---|
| `niche_ids` | `internet_mystery`, `unexplained_events`, `lost_places`, `google_maps_mystery` |
| `primary_audience` | EN-speaking mystery, true crime, and paranormal communities |
| `ending_type` | `open_question` — most content ends without resolution |
| `credibility_standard` | HIGH — audience knows the niche and will fact-check |
| `source_priority` | News archives, documentaries, official records > social media |
| `ai_image_ratio_expected` | 30-50% (real events have real photos, but atmospheric fills are needed) |

---

## Stage Addendum: stage_01 (Research)

### Additional Research Requirements

For **`internet_mystery`** and **`unexplained_events`**:
- Research must include the "official explanation" (if one exists) AND why many find it unsatisfying
- Include all major alternative theories — labeled as theories, not facts
- Note whether the case is: `cold_case` / `officially_closed` / `ongoing_investigation` / `never_investigated`
- If the event has a Wikipedia page: use it as a starting point only — find primary sources
- Check the Internet Archive (archive.org) for deleted or changed online content related to the case

For **`lost_places`**:
- Research must include the history of the location before abandonment
- Include the reason for abandonment (verified, not speculated)
- Note current status: accessible / restricted / demolished / partially restored
- Include any documented paranormal claims separately from historical facts
- Identify any legal or safety concerns about visiting the location

For **`google_maps_mystery`**:
- Research must include exact GPS coordinates
- Document what is visible and what is unusual or anomalous
- Research whether Google has updated or blurred the imagery (check current vs. archived)
- Include any official explanations for the anomaly
- Note whether the imagery has changed since the mystery was originally reported

### Priority Sources for This Niche
1. Local and national news archives (first reporting of the event)
2. Official government records (where applicable and public)
3. Academic papers (for historical or scientific mysteries)
4. Documentary sources (BBC, Netflix documentaries with named directors)
5. Established mystery/true crime journalism outlets
6. Original social media posts and threads (for internet-origin mysteries)

---

## Stage Addendum: stage_02 (Source Verifier)

### Niche-Specific Source Considerations

- **Wikipedia entries for mystery topics** are frequently edited by enthusiasts and may contain errors. Always downgrade Wikipedia as a sole source to `[FLAG]`.
- **"Mystery" aggregator websites** (listicles, "Top 10 Unsolved Mysteries" articles) are low-credibility sources. Accept only as secondary pointers to primary sources.
- **Paranormal claims** may only appear in paranormal-focused outlets. This is expected for the niche. Mark as `[FLAG: paranormal source]` but do not automatically reject — the claim's paranormal nature is the point.
- **Deleted content**: If a source points to a page that no longer exists, check the Internet Archive. If the archived version confirms the claim, mark as `[PASS: verified via archive]`.

---

## Stage Addendum: stage_03 (Story Outline)

### Required Narrative Structure for This Niche

The story must follow the **Three-Act Mystery Structure** from STYLE_GUIDE.md, with these additions:

**Required beats (must appear in all internet mystery / unexplained events content):**
1. **The Ordinary** — Show what life/the place/the situation was like before the mystery
2. **The Anomaly** — The first moment something was wrong
3. **The Investigation** — What was done to find answers (by authorities, researchers, or internet communities)
4. **The Dead Ends** — What could not be explained, what was tried and failed
5. **The Open Question** — What remains unknown — stated clearly, not hedged into meaninglessness

**For `lost_places`:** Add a "Then and Now" structural beat showing the contrast between the location's past and its current state.

**For `google_maps_mystery`:** The outline must build the investigation progressively — never reveal the most anomalous image in the first scene. The discovery sequence is: ordinary → unusual → anomalous → unexplained.

### Forbidden Outline Structures
- Ending with a fabricated resolution ("and that's why we now know it was...")
- Presenting speculation as resolution in the conclusion
- Skipping the Dead Ends beat — mystery content must acknowledge what has been tried

---

## Stage Addendum: stage_04 (Script Writer)

### Tone Requirements

- **Authority without certainty.** The narrator knows the facts but does not pretend to know the answers.
- **Respect for the unknown.** Phrases like "no one knows why" and "this has never been explained" are valid and powerful — do not fill them with speculation.
- **No dramatization of tragedy.** If a death or disappearance is involved, it is reported factually. The horror comes from reality, not from embellishment.

### Required Language Patterns for This Niche

| Situation | Required phrasing |
|---|---|
| Presenting an official explanation | "Authorities stated that..." / "The official conclusion was..." |
| Presenting an alternative theory | "Some researchers believe..." / "One theory, proposed by [name], suggests..." |
| Describing something unexplained | "This has never been satisfactorily explained." / "No official explanation has been given." |
| Noting a disputed fact | "While [Source A] reported X, [Source B] found Y." |
| Describing paranormal claims | "Those who believe in the paranormal have pointed to..." / "Among the more unusual explanations offered..." |

### Forbidden Phrases for This Niche
- "This will SHOCK you" (clickbait — forbidden in script, allowed sparingly in title only)
- "The truth is even MORE disturbing than we thought" (unverified superlative)
- "We may never know" as a **conclusion** — this is a dead end, not an ending. The ending must pose a specific open question, not surrender to generic mystery.
- Presenting a theory as a fact anywhere in the script

### Google Maps Mystery Script Specific
- Read coordinates aloud: `37°N 116°W` → "thirty-seven degrees north, one hundred sixteen degrees west"
- Describe what is visible precisely — visual details are the content, not just decoration
- When describing satellite imagery, note the date of the imagery if known

---

## Stage Addendum: stage_05 (Story Bible)

### Additional Entity Types to Track

| Entity Type | Example | Why Track |
|---|---|---|
| GPS Coordinates | `37.2350° N, 115.8111° W` | Ensure consistent format across all files |
| Dates of satellite imagery | `Google Earth imagery dated: 2019-04-15` | Must be consistent and accurate |
| Abandoned location names | `Hashima Island (also known as Gunkanjima)` | Track all known aliases |
| Case status | `officially_closed` / `cold_case` / `ongoing` | Must be stated accurately in script |

---

## Stage Addendum: stage_06 (Scene Splitter)

### Visual Vocabulary for This Niche

**Preferred visual types in priority order:**
1. Real photographs of the actual location or subject
2. Historical photographs showing "before" state
3. News coverage screenshots or clips
4. Satellite/map imagery (for google_maps_mystery)
5. Atmospheric AI images (for mood and transition)
6. Text-overlay cards (for key facts, dates, coordinates)

**Required visual beats:**
- Every date mentioned must be accompanied by a text overlay showing the date
- Every location name (on first mention) must have a text overlay or map pin
- Coordinates must be shown on screen when referenced

**For `lost_places`:** Include at least one side-by-side or sequence of then-vs-now imagery.

**For `google_maps_mystery`:** The anomalous satellite image must be shown at the moment it is described, zoomed in progressively.

---

## Stage Addendum: stage_07 (Image Finder)

### Priority Image Sources for This Niche

**News archives:**
- Newspapers.com — historical news photography
- Getty Images / AP Images — news wire photography (editorial use)
- ProQuest Historical Newspapers — deep archive

**Government and official records (public domain):**
- National Archives (US, UK, JP) — government photography
- NASA imagery — satellite and aerial photography (public domain)

**For `lost_places`:**
- Atlas Obscura — frequently has photography of abandoned locations
- Flickr Creative Commons — urban exploration photography
- Google Street View — may have historical captures of locations

**For `google_maps_mystery`:**
- Direct screenshot from Google Maps / Google Earth (commentary use)
- Web.archive.org captures of past Google Maps states
- Other mapping services (Bing Maps, Apple Maps) for comparison

---

## Stage Addendum: stage_08 (Image Prompt Generator)

### Aesthetic Style for AI Images in This Niche

**Core aesthetic:** Cinematic realism. AI images for this niche should look like photographs, not illustrations. The audience accepts them as mood-setters only if they are believably photographic.

**Visual vocabulary for AI prompts:**
- Lighting: low key, practical sources (flashlights, single bulbs, moonlight through windows)
- Time of day: dusk, night, or overcast day — never bright sunshine
- Color: muted, desaturated — pull toward gray-green or blue-gray
- Atmosphere: fog, mist, dust, overgrowth
- Human presence: absent, implied (footprints, open doors), or silhouetted only

**For `lost_places` AI images:**
- Include architectural decay: peeling paint, broken windows, overgrown floors
- Show scale — empty vastness is more disturbing than close-up detail
- Avoid: modern objects that don't belong in the time period of abandonment

**For `google_maps_mystery` AI images:**
- Use only for atmospheric mood — never generate fake satellite imagery
- If the mystery is a structure: generate a ground-level atmospheric rendering, not a top-down fake

**Forbidden in all AI images for this niche:**
- Images that could be mistaken for real documentary evidence
- Any image resembling a crime scene photograph
- Photorealistic faces of real named individuals

---

## Stage Addendum: stage_09 (Voice Director)

### Voice Character for This Niche

**Delivery profile:** Measured authority. The narrator knows the story deeply but is not performing — they are sharing information with weight and care.

**Key moments requiring special delivery:**
- **First mention of the anomaly:** Slow down. The anomaly is the pivot point of the story.
- **Dead ends:** Slightly deflated tone — these moments should feel genuinely frustrating, not theatrical
- **The open question closing:** Do not rush this. It is the last impression. Deliver it with finality, then silence.

**For `google_maps_mystery`:** The narrator is more analytical — slightly faster, more curious than somber.

---

## Stage Addendum: stage_10 (YouTube SEO)

### SEO Strategy for This Niche

**Primary keyword patterns that perform in this niche:**
- `[Subject] mystery explained`
- `[Subject] unsolved`
- `the truth about [subject]`
- `[location] abandoned mystery`
- `[coordinates] Google Maps mystery`
- `what really happened to [person/place]`

**Thumbnail text patterns:**
- `STILL UNSOLVED`
- `NO ONE KNOWS`
- `WHAT IS THIS?`
- `FOUND ON MAPS`
- `ABANDONED` (for lost places)

**Description hook patterns:**
- Open with the most specific, verifiable fact: "In [year], [specific thing] was discovered at [specific location]..."
- Or open with the unanswered question: "Why does [satellite image / document / photograph] show [anomaly]? [Year] later, no one has explained it."

**Tag strategy:**
- Include: subject name, location, mystery type, unexplained, unsolved, [year of event], true mystery, dark history
- For google_maps_mystery: include "google maps" "satellite image" "google earth mystery" as explicit tags
