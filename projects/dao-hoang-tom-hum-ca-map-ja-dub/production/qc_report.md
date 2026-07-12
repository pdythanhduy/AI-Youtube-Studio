# QC report — dao-hoang-tom-hum-ca-map-ja-dub

Source: https://www.youtube.com/watch?v=DkeK3zCXq2k (Sinh Tồn Trên Đảo Hoang, 32:15, 1080p)

## Segments / translation
- 159 segments parsed from VI auto-captions (7964 words, 1937s covered)
- 159/159 JA translations synthesized; fit_report tempo max ≤1.4 for all segments
  (0 overflow, no resynth needed)

## Audio
RMS level dB sampled at 6 points spread to the end of the 1935s track:

| t (s) | RMS dB |
|-------|--------|
| 30    | -16.58 |
| 350   | -17.82 |
| 700   | -17.88 |
| 1100  | -17.73 |
| 1500  | -16.98 |
| 1900  | -16.95 |

All points within normal speaking-level range, no silent/dropped sections.

## Video / branding
- Final mux duration: 1935.1s (matches source)
- Frame checks at 5s, 300s, 1200s, 1900s: JA title bar "無人島サバイバル挑戦"
  renders correctly over the covered VI title bar; old @SinhTonRV logo fully
  removed (delogo bbox x=55,y=132,w=250,h=56); ネタバレ映画館 watermark placed
  top-left, visible through the end of the video.
- Encode: libx264 veryfast crf19 (NVENC unavailable — driver/ffmpeg API mismatch,
  same as prior projects), video re-encoded (delogo requires full decode/encode,
  can't stream-copy).

## Output
- export/dao_hoang_tom_hum_ca_map_ja_dub_branded.mp4 — final deliverable
- export/dao_hoang_tom_hum_ca_map_ja_dub.mp4 — unbranded (JA audio + original video)
- export/channel_watermark.png, export/ja_title_bar.png — overlay assets

## Note for user
Channel watermark defaulted to ネタバレ映画館 (@netabare-eigakan) per the
established JA-dub channel branding used on prior movie-recap videos. This
video is a survival/reality vlog, not a movie recap — flag if a different
channel/branding should be used for this content type going forward.

## Naming collision note
This project was originally named `sinh-ton-dao-hoang-ja-dub` (matching the VI
title "Sinh Tồn Trên Đảo Hoang"). Renamed to `dao-hoang-tom-hum-ca-map-ja-dub`
because a different, unrelated JA-dub project (K6IWmbcGJDo, "Một Mình Sinh Tồn
Trên Đảo Hoang", Dung Review channel) already occupies that exact folder name
in the main checkout (C:/youtubeAI/AI-Youtube-Studio/projects/). Same video
source (DkeK3zCXq2k, Sinh Tồn Review channel) throughout — only the folder/file
name changed.
