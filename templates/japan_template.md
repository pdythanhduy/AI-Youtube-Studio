# Japan Template — AI YouTube Studio OS

Niche template for Japanese Mystery content — urban legends, real disappearances, J-horror cases, and Japanese paranormal phenomena.

**Template version:** 1.0
**Compatible with prompt versions:** All v1.x prompts
**Niche IDs covered:** `japanese_mystery`
**Primary languages:** `ja`, `en`
**Last updated:** 2026-06-27

---

## Template Overview

Japanese mystery content operates at the intersection of documented reality and deep cultural tradition. Japan has a rich canon of urban legends (都市伝説, toshi densetsu) that blur into real paranormal reportage, alongside genuine unsolved cases and social phenomena (missing persons, suicide forests, hikikomori stories) that carry enormous weight in Japanese culture.

This template demands a level of cultural literacy that other templates do not. Inaccuracy about Japanese cultural context is not just factually wrong — it is disrespectful to the culture and will be recognized and rejected by the audience this content is designed to reach.

## Niche Parameters

| Parameter | Value |
|---|---|
| `niche_id` | `japanese_mystery` |
| `primary_language_markets` | `ja` (primary), `en` (international mystery audience) |
| `cultural_sensitivity` | CRITICAL |
| `ending_type` | `open_question` or `cultural_reflection` |
| `register` | Formal in Japanese; respectful in English |
| `legend_vs_fact_distinction` | REQUIRED — always label |
| `suicide_topic_handling` | Follow Japanese media guidelines |

---

## Stage Addendum: stage_01 (Research)

### Cultural Context Research (Required)

Every Japanese mystery video must include research on cultural context. This is not optional decoration — it is load-bearing content. An international audience cannot understand the mystery without understanding the cultural framework.

**Required research elements:**

| Element | Required For |
|---|---|
| Japanese folklore or legend context | Any content involving urban legends, supernatural claims |
| Social phenomena context | Hikikomori, karoshi, suicide prevention, disappearance rates |
| Historical context | Pre-war, wartime, or postwar events related to the location |
| Japanese legal/investigative context | How missing persons cases are handled in Japan vs. other countries |
| Geographic context | Prefecture, city, neighborhood — with correct administrative naming |

### Language Research Requirements

When researching Japanese mystery content:
- Search Japanese-language sources as primary (NHK, Asahi Shimbun, Mainichi, local newspapers)
- Search Japanese Wikipedia alongside English Wikipedia — content often differs significantly
- If content will be in English: note the Japanese terms for all key concepts and include in story_bible
- Government statistics (ministry-level data) are often the most reliable for social phenomena

### Source Types Specific to This Niche

| Source Type | Credibility | Notes |
|---|---|---|
| NHK reporting | VERY HIGH | Japan's public broadcaster — most trusted |
| Major Japanese dailies (朝日, 読売, 毎日) | HIGH | Cross-reference multiple papers |
| Academic papers (Japanese universities) | HIGH | For historical and social phenomena |
| Toshi densetsu websites | LOW — folklore value | Acceptable for legend content, label as legend |
| 2channel / 5channel / Twitter (X) Japan | LOW — anecdotal | Screenshots of original content acceptable |
| English-language Japan mystery blogs | MEDIUM — verify independently | Often contain inaccuracies |

### Suicide and Self-Harm Content Policy

This niche frequently involves topics related to suicide (Aokigahara, Tojinbo, etc.).

**Required handling:**
- Do not describe methods
- Do not use the location's reputation in a sensationalized way
- Include suicide prevention context where appropriate: in Japan, the number is 0120-783-556
- Follow the safe messaging guidelines established by the Japan Suicide Prevention Council (日本いのちの電話)
- Frame the location's history with empathy and cultural understanding

---

## Stage Addendum: stage_02 (Source Verifier)

### Japan-Specific Source Verification

- **Japanese Wikipedia (ja.wikipedia.org)** is often more detailed and accurate for Japanese subjects than the English version. Still treat as secondary — find primary sources it cites.
- **Urban legend sources**: Sources about toshi densetsu (都市伝説) are inherently folklore. Do not try to verify them as facts — verify that the legend is real and how it is described in cultural sources. The legend itself is the verifiable claim.
- **Official statistics**: Japanese government statistics (白書, hakusho — white papers) are authoritative. NPA (National Police Agency) statistics for missing persons and crime data are the gold standard.
- **Dates in Japanese sources**: Japanese dates may use the Imperial calendar (令和, 平成, etc.). Convert to Gregorian in the research file and note the original.

### Imperial Calendar Conversion Reference

| Era | Western Year Equivalent |
|---|---|
| 令和 (Reiwa) | 2019 onward (Reiwa 1 = 2019) |
| 平成 (Heisei) | 1989-2019 (Heisei 1 = 1989) |
| 昭和 (Showa) | 1926-1989 (Showa 1 = 1926) |
| 大正 (Taisho) | 1912-1926 |

---

## Stage Addendum: stage_03 (Story Outline)

### Narrative Structure for Japanese Mystery

Use the **Three-Act Mystery Structure** from STYLE_GUIDE.md, modified as follows:

**Required beats unique to this template:**

1. **Cultural Context Beat** — Must appear in Act 1, before the main story. Establishes the Japanese cultural or folkloric framework the mystery exists within.
2. **The Legend vs. Reality Beat** — If the content involves an urban legend: establish the legend first, then pivot to any documented real events connected to it.
3. **The Japanese Silence Beat** — One scene that reflects the Japanese cultural tendency toward reticence about such topics. What is NOT talked about publicly, and why.
4. **The Ma Beat** (間) — One scene where the narration pauses and the imagery speaks. This is a culturally authentic structural element.

**Parameter Override:**
| Parameter | Base Value | This Template | Reason |
|---|---|---|---|
| `opening_pace` | `slow` | `very_slow` | Japanese mystery requires longer atmospheric setup |
| `silence_budget` | `3 x [PAUSE:2s]` | `5 x [PAUSE:2s]` | Ma principle — meaningful silence is structural |
| `cultural_context_required` | N/A | `true` (hard requirement) | Non-negotiable for this niche |

---

## Stage Addendum: stage_04 (Script Writer)

### Language Requirements

**For Japanese-language scripts (`language: ja`):**
- Write entirely in Japanese from the start — do not translate from English
- Use です/ます register (polite formal) throughout narration
- Use 漢字 appropriately — target JLPT N2 reading level (accessible but not simplified)
- Do not use excessive katakana for Japanese words that have kanji
- Foreign personal names: use katakana with the most common accepted reading
- Japanese personal names: family name first (山田太郎, not 太郎山田)

**For English-language scripts about Japanese topics (`language: en`):**
- Include Japanese terms (with romanization) for key concepts on first use: 都市伝説 (toshi densetsu — urban legend)
- Do not over-romanticize Japan or use orientalist framing
- Do not assume the audience is unfamiliar with Japan — the mystery audience is often knowledgeable

### Tone Requirements Specific to This Template

- **Reverence without fetishization.** Japanese mystery culture is not exotic — it is a culture with a long relationship with the supernatural that is taken seriously. Write accordingly.
- **The unsaid is as important as the said.** A sentence that trails off, a description that stops short of conclusion — these are stylistically authentic.
- **Real disappearance cases:** Do not speculate about guilt. Japanese missing persons cases (especially involving minors) are often still open investigations. Exercise extreme caution.

### Forbidden Phrases and Framings
- "In Japan, they have a saying..." (generic orientalist construction)
- Describing Japan as "mysterious by nature" or "a land of mystery"
- Using horror movie language for real tragedy (deaths are not "kills")
- "Even in the land of the rising sun, darkness lurks..." (cliché — forbidden)
- Any framing that treats Japanese cultural beliefs as primitive or superstitious

---

## Stage Addendum: stage_05 (Story Bible)

### Additional Entity Types for Japanese Mystery

| Entity Type | Required Format | Example |
|---|---|---|
| Japanese personal name | Family name + given name in kanji, with romanization | 山田太郎 (Yamada Taro) |
| Location name | Prefecture → Municipality → Specific location | 青森県三沢市 → 十和田湖 |
| Japanese legend name | Japanese name + romanization + English gloss | 口裂け女 (Kuchisake-onna — "Slit-Mouthed Woman") |
| Imperial date | Imperial calendar date → Gregorian | 昭和44年 → 1969 |
| Japanese organization | Full Japanese name + abbreviation + English gloss | 警視庁 (NPA — National Police Agency) |

---

## Stage Addendum: stage_06 (Scene Splitter)

### Visual Vocabulary for Japanese Mystery

**Core atmospheric visuals:**
- Empty streets at night — especially shopping arcades (shotengai), narrow alleys, train platforms
- Torii gates leading into darkness
- Traditional architecture (machiya townhouses, older apartment buildings)
- Aokigahara: dense forest, signage, tape, tree textures — not bodies or graphic content
- Urban Japan at night: vending machines, convenience store lights in darkness

**Required visual beats specific to this template:**
- Cultural context beat: show the Japanese setting explicitly — not generic "Asian" imagery
- If a legend is described: show the legend's typical visual representation (historically documented, not invented)
- The Ma beat: a long still image (5-8 seconds) with no cut — let the atmosphere sit

**Forbidden visuals:**
- Stereotypically Western-horror imagery applied to Japanese content
- Generic "Asian" or Chinese imagery used as a substitute for Japanese-specific imagery
- Graphic imagery of Aokigahara or any suicide-related location

---

## Stage Addendum: stage_07 (Image Finder)

### Priority Image Sources for Japanese Mystery

| Source | Content Type | Notes |
|---|---|---|
| NHK Photo Archive | Documentary photography | Publicly available NHK journalism images |
| Wikimedia Commons (Japan category) | Historical and location photography | Filter for CC-licensed |
| Google Maps Street View (Japan) | Location imagery | Use for establishing shots of real locations |
| Japanese news wire photos | Event photography | Mainichi Photo Bank, Kyodo News |
| Pixta (ピクスタ) | Japanese stock photography | Commercial stock — requires license |
| The Japan Times archive | English-language Japan reporting | Free articles available |

**For urban legend content:**
- Illustrations of legends from Japanese books (may require fair use assessment)
- Traditional woodblock prints (ukiyo-e) if the legend has historical roots (public domain)
- Do not use fan art or modern illustration without license

---

## Stage Addendum: stage_08 (Image Prompt Generator)

### Aesthetic Style for Japanese Mystery AI Images

**Core visual style:** East Asian Cinematic + Atmospheric. Between photorealism and painted. Think: the visual language of films like Ringu, Ju-on, and the work of Kiyoshi Kurosawa — but for documentary use, not horror movie.

**Visual vocabulary for AI prompts:**
```
Style keywords to include:
- "Japanese cinematic photography"
- "atmospheric East Asian urban landscape"
- "dark Japanese alleyway, night"
- "traditional machiya architecture, dusk"
- "dense forest, Aokigahara style, misty"
- "Japanese torii gate, fog"
- "Japanese convenience store at 3am, empty street"
```

**Color direction:**
- Base: near-black, charcoal, deep navy
- Accent: deep crimson (#8b0000) — used sparingly for emotional peaks
- Avoid: bright colors, warm tones, anything that reads as "cheerful Japan" tourist imagery

**Forbidden AI image subjects for this template:**
- Depictions of specific real missing persons — silhouettes only
- Graphic representations of self-harm or suicide
- Mockery or trivialization of the supernatural elements — even in an "AI image" these must be treated with gravity

---

## Stage Addendum: stage_09 (Voice Director)

### Voice Character for Japanese Mystery

**Delivery philosophy:** Ma (間). The space between words is as important as the words themselves. The narrator holds silence with intention.

**For Japanese narration:**
- Pace: 270-300 morae per minute (slightly slower than average Japanese speech)
- Register: formal polite — consistent です/ます, no casual contractions
- Emotional range: contained — Japanese professional narration does not externalize emotion
- Sentence-final particles: avoid question-final rising intonation for statements (common TTS error)

**For English narration about Japanese topics:**
- Use full pronunciation of Japanese names — do not anglicize
- Pause after introducing a Japanese term with its pronunciation
- The atmosphere should feel slightly more formal and measured than other styles

**Critical delivery notes:**
- The cultural context beat: measured and educational — not sensational
- The Ma beat: the narrator should go completely silent for the visual. This is intentional and must be marked `[PAUSE:3s]` or longer.
- The open question closing: deliver slowly, with finality — this is 余韻 (yoin — the lingering resonance after the last note)

---

## Stage Addendum: stage_10 (YouTube SEO)

### SEO Strategy for Japanese Mystery

**For Japanese-language content:**
- Primary keyword format: `[名前/場所] 謎` / `[名前/場所] 未解決` / `都市伝説 [場所]`
- Include 3-5 English tags for international reach: "japan mystery", "japanese urban legend", "unsolved japan"
- Thumbnail text in Japanese must be highly readable — large, bold, white on dark
- Thumbnail text examples: `未解決`, `謎の真相`, `なぜ消えた？`

**For English-language Japanese mystery content:**
- Title patterns: "Japan's Most Disturbing Unsolved Mystery", "The Dark Truth About [Location]", "Japan's [Legend] — What Really Happened"
- Include Japanese terms as tags: "toshi densetsu", "kuchisake onna", "aokigahara", etc.
- Description must provide cultural context in the first paragraph — this audience wants to understand

**Thumbnail design:**
- Dark background with deep red accent (consistent with style profile)
- Japanese characters in thumbnail increase CTR in both Japanese and international mystery audiences
- Consider kanji + English bilingual thumbnail text: 未解決 | UNSOLVED
