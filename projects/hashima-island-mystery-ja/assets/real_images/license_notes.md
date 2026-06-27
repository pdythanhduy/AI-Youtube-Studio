# License Notes — Hashima Island Real Image Candidates
## FIX-H1 | AI-Youtube-Studio Production v1.0

Last updated: 2026-06-27

---

## 1. License Tier Summary

| Tier | License | ShareAlike? | Attribution? | Commercial YouTube | Status |
|------|---------|-------------|--------------|-------------------|--------|
| **A** | Public Domain | No | No (recommended) | SAFE | READY |
| **B** | Japan Govt Attribution | No | Yes (specific text) | SAFE | READY |
| **C** | CC BY 2.0 | No | Yes | SAFE | READY |
| **D** | CC BY-SA 3.0 / 4.0 | **YES** | Yes | **CAUTION** | CONSULT LEGAL |
| **E** | Paid Stock (PIXTA / Getty / Alamy) | No | No | SAFE | PAID LICENSE REQUIRED |

---

## 2. The ShareAlike Problem for Commercial YouTube

**This is the most important legal issue in this candidate set.**

The majority of Wikimedia Commons images in this project are licensed under **CC BY-SA** (ShareAlike). The SA clause requires:

> "If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original."

### How this applies to video production:

| Action | SA Triggered? |
|--------|--------------|
| Using image as-is, unmodified, in a video | Disputed (gray area) |
| Applying color grade / desaturation / film grain to image | **YES — derivative work** |
| Cropping or resizing | Probably YES |
| Adding Ken Burns / zoom motion effect to image | **YES — derivative work** |

Since this project applies a **dark_documentary color grade, film grain, and Ken Burns motion effects to all images**, the SA clause is almost certainly triggered for every CC BY-SA image in production.

### Consequence for this project:

If CC BY-SA images are used with color grading:
- The video incorporating those images must be released under CC BY-SA
- CC BY-SA is **incompatible with most commercial YouTube monetization models**
- YouTube's Content ID system also complicates SA video licensing

### Recommended legal strategy:

**Option 1 (Cleanest):** Use only CC BY 2.0 / Attribution-only / Public Domain images. For this project that means: C007-A, C007-B, C007-C (CC BY 2.0), C007-B/C024-B (Japan Govt), C024-C (Public Domain). This covers S007 and S024 cleanly. S001, S008, S020 would require either:
  - Paid stock licenses (Getty / PIXTA) — RECOMMENDED
  - Legal review confirming SA does not apply to the video as a compilation work

**Option 2 (Legal gray area — consult counsel):** Some legal opinions hold that incorporating CC BY-SA images into a larger editorial work (documentary video) does not make the whole video a "derivative work" requiring SA — particularly if the images are used as short visual illustrations rather than the primary creative content. This view is contested. **Do not rely on this interpretation without written legal advice.**

**Option 3 (Pragmatic):** Use CC BY-SA images and release the video description stating: "Some B-roll images used in this video are licensed under CC BY-SA 4.0. The narration, script, and all other original elements are © [Channel Name]." This is common practice but NOT technically compliant with SA. Risk: low enforcement probability for non-commercial Wikimedia images; risk increases for commercial channels.

---

## 3. Attribution Text Requirements

For every CC-licensed image used, add the following to the video description under a "Image Credits" section:

### Required attributions per candidate:

**C001-A / C024-A** (Hashima_Island_2023.jpg):
```
Hashima Island (2023) by ノーマルエディタ / Wikimedia Commons
License: CC BY-SA 4.0 — https://creativecommons.org/licenses/by-sa/4.0/
```

**C007-A / C020-C** (Battle-Ship_Island_Nagasaki_Japan.jpg):
```
Battle-Ship Island Nagasaki Japan (2008) by kntrty / Wikimedia Commons
License: CC BY 2.0 — https://creativecommons.org/licenses/by/2.0/
```

**C007-B / C024-B** (Cku-74-20_c45_6_hashima.jpg — Japan Govt 1974):
```
Aerial photograph of Hashima Island (1974)
Source: National Land Image Information (Color Aerial Photographs)
Ministry of Land, Infrastructure, Transport and Tourism of Japan
```

**C007-C** (The_island_of_a_warship):
```
The island of a warship (2008) by kntrty / Wikimedia Commons
License: CC BY 2.0 — https://creativecommons.org/licenses/by/2.0/
```

**C008-A** (第四竪坑捲座跡-01.jpg):
```
Fourth mine pit hoistroom, Hashima Island (1992) by Gohachiyasu1214 / Wikimedia Commons
License: CC BY-SA 4.0 — https://creativecommons.org/licenses/by-sa/4.0/
```

**C008-B** (Hashima_Dorr_thickener-01.jpg):
```
Hashima Dorr thickener (1992) by Gohachiyasu1214 / Wikimedia Commons
License: CC BY-SA 4.0 — https://creativecommons.org/licenses/by-sa/4.0/
```

**C008-C** (Hashima_BeltConveyor):
```
Hashima Belt Conveyor and Building 70 (2017) by Ka23 13 / Wikimedia Commons
License: CC BY-SA 4.0 — https://creativecommons.org/licenses/by-sa/4.0/
```

**C020-A** (Hashima_Island_ruins_1.jpg):
```
Hashima Island ruins (2017) by Nsxbln / Wikimedia Commons
License: CC BY-SA 4.0 — https://creativecommons.org/licenses/by-sa/4.0/
```

**C024-C** (Hashima circa 1930):
```
Hashima Island (circa 1930) — Public Domain
Source: Series of Japanese geography and folk culture: Vol.13, Shinkosha
Digitized by Abasaa / Wikimedia Commons
```

---

## 4. Images NOT Cleared for Commercial Use

No candidates in this set are explicitly non-commercial. However the following are **not yet confirmed safe** without additional steps:

- **All CC BY-SA images** — commercial use is technically allowed, but the SA clause creates a derivative works obligation if any modification is made. MUST be resolved before publish.
- **Getty Images / PIXTA / Alamy** — safe after purchase, but payment required first.
- **Hashima circa 1930** — public domain status is based on uploader's documentation of the source book's publication date. Best practice: confirm source book publication date independently before relying on PD status.

---

## 5. Sensitive Content Note

**C008-A, C008-B, C008-C** (mine/industrial equipment images for S008):

These images depict the industrial mining infrastructure of Hashima Island. They do NOT show:
- Forced labor workers
- Identifiable individuals
- Scenes of violence, suffering, or coercion
- War-era imagery

They are purely industrial archaeology photographs taken decades after closure (1992, 2017). These are appropriate for the scene S008 context (which describes the island's industrial past) and do NOT trigger the sensitive_content flag that applies to S011a/IMG009 (the tunnel interior).

---

## 6. Recommended Attribution Format for YouTube Description

Add this block to the bottom of the YouTube video description:

```
━━━━ IMAGE CREDITS ━━━━
Some images in this video are used under Creative Commons license.
[List individual attributions here per selected candidates]
Full license details: https://creativecommons.org/
```
