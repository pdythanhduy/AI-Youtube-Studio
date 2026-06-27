# V3 Timeline Image Filename Patch Report
## hashima-island-mystery-ja

**Date:** 2026-06-28  
**Stage:** 43 (patch)  
**Trigger:** V3 render aborted — stale image filenames in timeline JSON

---

## Patches Applied

| Scene | Field | Old filename | New filename | Status |
|-------|-------|-------------|-------------|--------|
| S021 | image_file | `IMG017_S021_heritage_plaque.png` | `IMG017_S021_heritage_plaque_ruin.png` | PATCHED |
| S022 | image_file | `IMG018_S022_ma_beat_ruins_wide.png` | `IMG018_S022_hashima_panorama.png` | PATCHED |
| S023 | image_file | `IMG019_S023_tourist_ferry.png` | `IMG019_S023_tourist_ferry_approach.png` | PATCHED |

**Files patched:** 1 (data/timeline_assembly_plan_v3_tight.json)  
**Markdown** (timeline/timeline_assembly_plan_v3_tight.md): no change needed — uses image IDs only, not file paths.

---

## Full Image Path Verification

All 21 image_file entries in `data/timeline_assembly_plan_v3_tight.json` verified on disk.  
(4 MG scenes have null image_file — correct by design.)

| Scene | Image ID | Path | Status |
|-------|----------|------|--------|
| S001 | IMG001 | assets/ai_images/generated/batch_3/IMG001_S001_island_establishing_predawn.png | OK |
| S002 | IMG002 | assets/ai_images/generated/batch_1/IMG002_S002_interior_ruin.png | OK |
| S003 | IMG003 | assets/ai_images/generated/batch_1/IMG003_S003_wooden_door_closeup.png | OK |
| S004 | — | null (MG001 title card) | OK |
| S005 | IMG004 | assets/ai_images/generated/batch_1/IMG004_S005_meiji_industrial.png | OK |
| S006 | — | null (MG002 animated map) | OK |
| S007 | IMG006 | assets/real_images/downloaded/S007_IMG006_Battle-Ship_Island_Nagasaki_Japan.jpg | OK |
| S008 | IMG007 | assets/ai_images/generated/batch_3/IMG007_S008_building30_exterior.png | OK |
| S009 | IMG008 | assets/ai_images/generated/batch_2b/IMG008_S009_school_interior.png | OK |
| S010 | IMG003 | assets/ai_images/generated/batch_1/IMG003_S003_wooden_door_closeup.png | OK (alt crop) |
| S011a | IMG009 | assets/ai_images/generated/mine_gate/IMG009_S011a_mine_tunnel_approved.png | OK |
| S011b | IMG010 | assets/ai_images/generated/batch_1/IMG010_S011b_mine_rock_texture.png | OK |
| S012 | — | null (MG003 data viz) | OK |
| S013 | IMG011 | assets/ai_images/generated/batch_1/IMG011_S013_heritage_light_ruins.png | OK |
| S014 | — | null (MG004 date overlay) | OK |
| S015 | IMG012 | assets/ai_images/generated/batch_1/IMG012_S015_abandoned_dock.png | OK |
| S016 | IMG013 | assets/ai_images/generated/batch_2a/IMG013_S016_personal_items_v2.png | OK |
| S017 | IMG014 | assets/ai_images/generated/batch_2b/IMG014_S017_light_beams_interior_v2.png | OK |
| S018 | IMG015 | assets/ai_images/generated/batch_2b/IMG015_S018_storm_ruins.png | OK |
| S019 | IMG010 | assets/ai_images/generated/batch_1/IMG010_S011b_mine_rock_texture.png | OK (alt crop) |
| S020 | IMG016 | assets/ai_images/generated/batch_3/IMG016_S020_island_dusk_wide.png | OK |
| S021 | IMG017 | assets/ai_images/generated/batch_2b/IMG017_S021_heritage_plaque_ruin.png | OK (PATCHED) |
| S022 | IMG018 | assets/ai_images/generated/batch_1/IMG018_S022_hashima_panorama.png | OK (PATCHED) |
| S023 | IMG019 | assets/ai_images/generated/batch_2b/IMG019_S023_tourist_ferry_approach.png | OK (PATCHED) |
| S024 | IMG020 | assets/real_images/processed/S024_IMG020_Cku-74-20_c45_6_hashima_16x9.jpg | OK |

**Result: 21/21 image paths valid.**

---

## Render Command

```powershell
python tools\render\render_rough_video.py `
    --timeline data/timeline_assembly_plan_v3_tight.json `
    --output export/rough/hashima_rough_v3_tight.mp4
```

Then verify:

```powershell
python tools\render\verify_rough_timeline.py `
    --timeline data/timeline_assembly_plan_v3_tight.json `
    --video export/rough/hashima_rough_v3_tight.mp4
```

Expected: 556s (9:16), Ma beat 502–519s narration-free, 25 scenes.
