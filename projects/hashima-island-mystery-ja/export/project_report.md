# Project Report — 端島 / 軍艦島：消えた都市の謎
**Project ID:** hashima-island-mystery-ja
**Stage:** 12 — Export / Final Report
**Date:** 2026-06-27
**Pipeline Result: COMPLETE — PASS**

---

## Project Summary

| 項目 | 値 |
|---|---|
| トピック | The Mystery of Hashima Island（端島 / 軍艦島） |
| 言語 | 日本語 (ja) |
| 動画尺 | 12分 |
| スタイル | dark_documentary |
| ニッチ | japanese_mystery |
| テンプレート | japan_template.md |
| 目標語数 | 1,201語（12分 × 130 × 0.77） |
| 実際語数 | 1,201語 |
| ステージ数 | 13（Stage 0〜12） |
| 合格ステージ | 13 / 13 |
| 失敗ステージ | 0 |
| 警告 | 1（解決済み） |
| QA結果 | PASS（20/20チェック） |

---

## Pipeline Execution Log

| Stage | 名称 | 結果 | 主な出力 |
|---|---|---|---|
| 0 | Project Setup | PASS | input.json, project.yaml, export_manifest.json, director_run_log.md |
| 1 | Research | PASS | research.md（12事実、7ソース、4未解明） |
| 2 | Source Verification | NEEDS_REVISION ⚠ | source_report.md（3 FLAG、0 FAIL）→ research_verified.md |
| 3 | Story Outline | PASS | story_outline.md（6セクション、japan_template全ビート） |
| 4 | Script | PASS | script.md（1,201語、[PAUSE:2s]×5） |
| 5 | Story Bible | PASS | story_bible.md（正式名称・日付・数値・禁止表現） |
| 6 | Scene List | PASS | scene_list.csv（24シーン、0:00〜12:00） |
| 7 | Image Plan | PASS | image_plan.csv（20画像、法的ステータス全件記載） |
| 8 | AI Image Prompts | PASS | ai_image_prompts.md（18プロンプト） |
| 9 | Voice | PASS | voice_script.txt + voice_direction.md |
| 10 | SEO | PASS | youtube_seo.md（タイトル3案、タグ29件） |
| 11 | QA | PASS | qa_report.md（20/20チェック合格） |
| 12 | Export | PASS | export_manifest.json（全18アセット complete）+ 本ファイル |

---

## Warnings

| コード | Stage | 内容 | 解決 |
|---|---|---|---|
| ERR_WARN_001 | 2 | 3 FLAG items in source_report（30号棟「最古」、人口密度「世界最高」、スカイフォール一次ソース未確認） | 表現調整済み。research_verified.md・script.mdに反映。 |

---

## Key Facts Used (検証済み事実)

1. 端島（はしま）は長崎県長崎市に属する無人島。別名「軍艦島」。[VERIFIED]
2. 長崎港から南西約15〜18km、面積約6.3ヘクタール。[VERIFIED]
3. 石炭採掘1887年頃開始。1890年三菱合資会社が採掘権取得。[VERIFIED]
4. 1916年「30号棟」建設 — 日本最古級の鉄筋コンクリート集合住宅のひとつ。[VERIFIED / FLAG調整済み]
5. 1959年人口5,259人 — 世界最高水準のひとつとされる人口密度。[VERIFIED / FLAG調整済み]
6. 最盛期施設: アパート（最大9階）、小中学校、病院、映画館等。[VERIFIED]
7. 1939〜1945年、朝鮮・中国人の強制労働。日本政府がUNESCO審議で認定。詳細数字は現在も調査中。[VERIFIED as fact / DISPUTED 数字]
8. 1974年1月15日閉山発表。4月20日全島民離島。[VERIFIED]
9. 2009年4月22日観光再開。[VERIFIED]
10. 2015年7月5日ユネスコ世界遺産登録（ID 1484）。[VERIFIED]
11. 登録審議で日本政府が「against their will」発言。その後日韓で解釈をめぐる論争。[VERIFIED as event]

---

## Sources Used

| ID | ソース | 信頼性 |
|---|---|---|
| S1 | UNESCO World Heritage List (ID 1484) | VERY HIGH |
| S2 | 長崎市公式ウェブサイト | HIGH |
| S3 | 三菱マテリアル株式会社 社史 | HIGH |
| S4 | UNESCO WHC 39th Session (2015) | VERY HIGH |
| S5 | 端島炭坑遺産フォーラム | MEDIUM-HIGH |
| S6 | 韓国文化財庁資料 | HIGH |
| S7 | 読売新聞・朝日新聞 (2015年) | HIGH |

---

## Assets Produced

| # | ファイル | 内容 |
|---|---|---|
| 1 | input/input.json | プロジェクト設定JSON |
| 2 | input/project.yaml | プロジェクト設定YAML |
| 3 | research/research.md | リサーチ（12事実・7ソース・年表・文化背景） |
| 4 | research/source_report.md | ソース検証レポート |
| 5 | research/research_verified.md | 検証済み事実（FLAG調整適用済み） |
| 6 | script/story_outline.md | ストーリーアウトライン（6セクション） |
| 7 | script/script.md | 日本語スクリプト（1,201語） |
| 8 | script/story_bible.md | ストーリーバイブル（正式名称・発音・禁止表現） |
| 9 | visuals/scene_list.csv | シーンリスト（24シーン） |
| 10 | visuals/image_plan.csv | 画像プラン（20画像・法的ステータス） |
| 11 | visuals/ai_image_prompts.md | AI画像プロンプト（18件） |
| 12 | voice/voice_script.txt | ナレーション読み上げ用スクリプト |
| 13 | voice/voice_direction.md | ナレーション演技指示 |
| 14 | seo/youtube_seo.md | YouTube SEO（タイトル・説明文・タグ・サムネイル） |
| 15 | logs/qa_report.md | QAレポート（20/20チェック合格） |
| 16 | logs/director_run_log.md | ディレクターランログ |
| 17 | export/export_manifest.json | エクスポートマニフェスト |
| 18 | export/project_report.md | 本ファイル |

**Total assets: 18 / 18**

---

## Next Human Review Actions

### 優先度：HIGH（制作開始前に必須）

1. **スクリプト最終確認** (`script/script.md`)
   - 日本語ネイティブによる読み上げテスト（流暢さ・自然さ確認）
   - 「against their will」発言の記述表現の外部確認（法務・コンプライアンス）

2. **AI画像生成・承認** (`visuals/ai_image_prompts.md`)
   - 18プロンプトを生成ツール（Midjourney等）で実行
   - 特に PROMPT_008（炭坑内部・強制労働時代）の生成物が「人物描写なし・雰囲気のみ」になっているか確認
   - 生成画像の著作権ポリシーを使用ツールで確認

3. **ソースURL確認** (`research/source_report.md`)
   - S1 UNESCO (whc.unesco.org/en/list/1484) — アクセス確認
   - S2 長崎市公式サイト — 現在のURLを確認（リダイレクト等）
   - S4 UNESCO WHC 39th Session議事録 — 「against their will」発言の原文を取得して保管

### 優先度：MEDIUM（制作中に対応）

4. **ナレーション収録**
   - `voice/voice_direction.md` に基づきキャスティング
   - 「閉山」「徴用」等の発音チェックポイントを必ず事前確認

5. **サムネイル制作** (`seo/youtube_seo.md` — Concept A推奨)
   - 軍艦島シルエット + 「5,259人が消えた」テキスト
   - A/Bテスト推奨（Concept A vs Concept C）

6. **タイトル最終選定** (`seo/youtube_seo.md`)
   - Option A（CTR重視）または Option C（検索重視）を選択
   - チャンネル戦略に応じて決定

### 優先度：LOW（公開前）

7. **概要欄リンク確認**
   - 説明文にチャンネル固有のリンクを追加
   - 関連動画カードの設定

8. **字幕**
   - 本パイプラインには字幕ファイルは含まれていない
   - 必要であれば voice_script.txt からタイムコードつき字幕を作成

---

## Director Notes

端島プロジェクトは、japan_template.mdの4必須ビートすべてを満たし、目標語数1,201語を達成した。強制労働の歴史については、UNESCO公式議事録（S4）という最高信頼度のソースにより事実として確認されているが、数字については日韓双方の資料が異なるため断定を避けた。この表現バランスは今後の日本語ドキュメンタリープロジェクトにおけるモデルケースとして参照可能。

Ma beat（間）の映像指示（S022: 10秒無音）は、japan_templateの核心的要件であり、編集段階で必ず保持すること。

**Pipeline: COMPLETE**
**Director AI v1.0 — 2026-06-27**
