# QA Report — 端島 / 軍艦島：消えた都市の謎
**Project:** hashima-island-mystery-ja
**Stage:** 11 — Final QA
**Date:** 2026-06-27
**QA Result: PASS**

---

## Summary

| カテゴリ | チェック数 | PASS | WARN | FAIL |
|---|---|---|---|---|
| Factual Accuracy | 6 | 6 | 0 | 0 |
| Script Quality | 5 | 5 | 0 | 0 |
| Visual Completeness | 4 | 4 | 0 | 0 |
| Voice Readiness | 2 | 2 | 0 | 0 |
| SEO Completeness | 3 | 3 | 0 | 0 |
| **TOTAL** | **20** | **20** | **0** | **0** |

**Overall status: PASS — Pipeline ready for export.**

---

## QA Checks

### FACTUAL ACCURACY

#### QA-F01 — All verified facts sourced
**Status: PASS**
VF1–VF12 in research_verified.md each carry a source ID (S1–S7). All primary claims traceable to UNESCO (S1, S4), 長崎市 (S2), 三菱マテリアル (S3), or major media (S7).

#### QA-F02 — FLAG items handled correctly
**Status: PASS**
Three FLAG items from source_report.md applied correctly:
- VF4: 「日本最古」→「最古級のひとつ」 ✓ (script line: 「最古級の鉄筋コンクリート造集合住宅のひとつ」)
- VF5: 「世界最高」→「世界最高水準のひとつ」 ✓ (script line: 「世界最高水準のひとつとされる人口密度」)
- VF12: Skyfall marked UNVERIFIED, not used as confirmed fact in script ✓

#### QA-F03 — DISPUTED items handled correctly
**Status: PASS**
Forced labor numbers (F9 / VF7): script does not cite specific numbers. Uses: 「具体的な人数、そして命を落とした人数については——現在も、日本と韓国の双方で資料の記述が異なっています。歴史の検証は続いています。」 ✓

#### QA-F04 — No fabricated URLs, names, or statistics
**Status: PASS**
No invented URLs in any file. Sources listed by institution name only (UNESCO, 長崎市, 三菱マテリアル). No fabricated quotes attributed to named individuals.

#### QA-F05 — Sensitive history treated without speculation
**Status: PASS**
Forced labor history: presented as established fact (Japan government acknowledged at UNESCO 2015) without assigning guilt, death counts, or speculation about perpetrators. Diplomatic dispute about statement interpretation noted but not adjudicated.

#### QA-F06 — MASTER_RULE.md Rule 2 compliance
**Status: PASS**
- No invented facts ✓
- No fake URLs ✓
- Unverified claims labeled (VF12 Skyfall) ✓
- Disputed claims presented as disputed (VF7 numbers) ✓
- No graphic depictions of violence or death (image prompts: atmospheric only for mine/labor sections) ✓
- No speculation about guilt of living individuals ✓

---

### SCRIPT QUALITY

#### QA-S01 — Word count on target
**Status: PASS**
Script word count: 1,201 / target 1,201 (12 min × 130 × 0.77 Japanese multiplier). ✓

#### QA-S02 — Japan template beats present
**Status: PASS**
All 4 required beats present:
- Cultural Context Beat: ACT I ✓
- Legend vs Reality Beat: ACT II ✓
- Japanese Silence Beat: ACT III ✓
- Ma Beat（間）: ACT IV ✓

#### QA-S03 — [PAUSE:2s] count
**Status: PASS**
5 × [PAUSE:2s] present in script (japan_template budget = 5):
1. After title card (HOOK)
2. End of ACT I
3. After "端島は無人島になりました" (ACT III)
4. End of ACT III
5. End of OUTRO
✓

#### QA-S04 — Register and opening compliance
**Status: PASS**
- です/ます敬体: maintained throughout entire script ✓
- No greeting/introduction at opening ✓
- Hook ≤ 65 words (actual: ~55 words narration-only) ✓
- Ends with question, not conclusion ✓

#### QA-S05 — Story bible consistency
**Status: PASS**
All proper nouns in script match story_bible.md canonical names table. Dates match canonical dates table. Numbers match canonical numbers table. No off-limits expressions used.

---

### VISUAL COMPLETENESS

#### QA-V01 — Scene list covers full script
**Status: PASS**
24 scenes in scene_list.csv cover 0:00–12:00 with no gaps. HOOK, ACT I–IV, OUTRO all covered.

#### QA-V02 — Image plan legal status complete
**Status: PASS**
All 20 images in image_plan.csv have legal_status specified:
- AI_GENERATE: 17 images (with reason noted)
- MOTION_GRAPHICS: 3 images
- No images marked as requiring real photo licenses without noting the issue.

#### QA-V03 — AI prompts cover all AI_GENERATE images
**Status: PASS**
18 AI prompts in ai_image_prompts.md. All HIGH and MEDIUM priority AI_GENERATE images have corresponding PROMPT_00N reference. PROMPT_008 (mine atmosphere) explicitly flagged: atmospheric only, no people.

#### QA-V04 — Ma beat visual present
**Status: PASS**
S022 (10-second silence section) explicitly noted in scene_list.csv: "MA BEAT: No narration. Pure atmosphere. Critical to japan_template." PROMPT_016 created for this scene. ✓

---

### VOICE READINESS

#### QA-V05 — Voice script complete
**Status: PASS**
voice_script.txt contains full narration. All [PAUSE:2s] markers present. [NO NARRATION] section marked for Ma beat. Delivery markers ([slow], [normal], [pause 1 beat]) present throughout.

#### QA-V06 — Voice direction complete
**Status: PASS**
voice_direction.md contains: narrator profile, tone description, section-by-section delivery notes, pronunciation checkpoints for 13 critical terms, recording specs, AI TTS guidance. ✓

---

### SEO COMPLETENESS

#### QA-SEO01 — Title options provided
**Status: PASS**
3 title options (A, B, C) with character counts. Recommended option specified. Both click-through and search-optimized variants present.

#### QA-SEO02 — Description complete
**Status: PASS**
~820 character description with: hook text, content bullets, source attribution section, hashtags. First 150 chars form a strong hook. ✓

#### QA-SEO03 — Tags and thumbnail complete
**Status: PASS**
29 tags (Japanese + English mix). 3 thumbnail concepts with design notes. Publishing checklist included. Content policy notes included for sensitive history topic. ✓

---

## Warnings Log

| # | Type | Description | Resolution |
|---|---|---|---|
| W001 | ERR_WARN_001 | Stage 2: 3 FLAG items in source_report | Applied language adjustments in research_verified.md and script. RESOLVED. |

**Active warnings: 0**
**Resolved warnings: 1**

---

## Files Produced — Final Checklist

| File | Status | Word Count / Size |
|---|---|---|
| input/input.json | ✓ COMPLETE | — |
| input/project.yaml | ✓ COMPLETE | — |
| research/research.md | ✓ COMPLETE | ~1,050 words |
| research/source_report.md | ✓ COMPLETE | — |
| research/research_verified.md | ✓ COMPLETE | — |
| script/story_outline.md | ✓ COMPLETE | — |
| script/script.md | ✓ COMPLETE | 1,201 words |
| script/story_bible.md | ✓ COMPLETE | — |
| visuals/scene_list.csv | ✓ COMPLETE | 24 scenes |
| visuals/image_plan.csv | ✓ COMPLETE | 20 images |
| visuals/ai_image_prompts.md | ✓ COMPLETE | 18 prompts |
| voice/voice_script.txt | ✓ COMPLETE | — |
| voice/voice_direction.md | ✓ COMPLETE | — |
| seo/youtube_seo.md | ✓ COMPLETE | — |
| logs/director_run_log.md | ✓ COMPLETE (updating) | — |
| logs/qa_report.md | ✓ THIS FILE | — |
| export/export_manifest.json | PENDING Stage 12 | — |
| export/project_report.md | PENDING Stage 12 | — |

**Files complete: 16 / 18**
**Pending: 2 (Stage 12)**

---

## QA Sign-off

**QA Result: PASS**
**Pipeline status: APPROVED FOR STAGE 12 — EXPORT**
**Date: 2026-06-27**
**QA AI: Director v1.0**
