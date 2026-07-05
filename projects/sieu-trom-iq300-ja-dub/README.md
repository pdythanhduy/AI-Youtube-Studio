# sieu-trom-iq300-ja-dub

Bản lồng tiếng Nhật (time-aligned) cho video review phim:
"[Review Phim] Siêu Trộm IQ 300 Cắp Sạch 44 Tỷ USD Trong 1 Đêm"
(https://www.youtube.com/watch?v=mQ_FK6_o678 — 27:22, kênh Nguyễn Review 2).

Giữ nguyên hình của video gốc; thay lời bình tiếng Việt bằng giọng đọc
tiếng Nhật khớp từng phân đoạn phụ đề (136 đoạn, ~12s/đoạn).

## Pipeline

1. **Phụ đề nguồn** — `yt-dlp --write-auto-subs --sub-langs vi --sub-format json3`,
   parse word-timing thành `data/segments_vi.json` (gộp theo khoảng nghỉ >1.2s, tối đa 12s).
2. **Dịch** — `data/ja_translations.json`: dịch cô đọng theo văn phong kể-lại-phim
   tiếng Nhật (常体), canh độ dài để đọc vừa khung thời gian.
3. **TTS** — edge-tts, giọng `ja-JP-KeitaNeural`, rate +10%.
4. **Time-fit** — đo từng đoạn bằng ffprobe; nếu dài hơn slot thì nén `atempo`
   (trần 1.6×), loudnorm -16 LUFS. Báo cáo: `data/fit_report.json`.
5. **Assemble** — đặt từng đoạn đúng `start_ms` trên track dài 1642s.
6. **Nền** — tách giọng Việt khỏi nhạc/hiệu ứng bằng demucs (`--two-stems=vocals`),
   dùng stem `no_vocals` làm nền, sidechain-duck dưới giọng Nhật.
7. **Mux** — copy video track gốc + audio mix mới → `export/sieu_trom_iq300_ja_dub.mp4`.

## Chạy lại

```bash
python tools/build_dub.py --synth --assemble
demucs --two-stems=vocals -n htdemucs -o <tmp>/separated <tmp>/source_audio.wav
python tools/build_dub.py --mix --video <source_video.mp4> --background <no_vocals.wav>
```

File media (audio/, export/) không commit — xem .gitignore gốc repo.

## Rebrand watermark

Kênh tiếng Nhật: **ネタバレ映画館** (gợi ý handle `@netabare-eigakan`).

```bash
python tools/brand_watermark.py --input export/sieu_trom_iq300_ja_dub.mp4 --text "ネタバレ映画館"
```

Xóa logo kênh gốc (tĩnh, góc trên-trái, bbox mặc định `6,6,300,88` cho 1080p)
bằng `delogo`, overlay watermark chữ (Pillow + font Yu Gothic Bold, opacity ~59%)
tại (24,18), encode h264_nvenc cq19, audio copy →
`export/sieu_trom_iq300_ja_dub_branded.mp4`.

## Lưu ý bản quyền

Chỉ dùng khi bạn sở hữu video gốc (kênh của bạn). Video chứa footage phim của
bên thứ ba — trách nhiệm fair-use/bản quyền như bản tiếng Việt gốc.
