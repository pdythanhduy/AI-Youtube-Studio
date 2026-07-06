# QC report — janitor-assassin-ja-dub v1

Ngày: 2026-07-06

## Nguồn
- Video: https://www.youtube.com/watch?v=S749n_bNs0k (3504s = 58:24, 1080p, "Nguyễn Review 2")
- Phim: The Day of the Jackal (2024) S1 —「ジャッカルの日」
- Phụ đề: auto-captions VI json3, 17097 từ → 289 phân đoạn ~12s, phủ 3505s

## Dub
- Dịch 4 phần merge; vòng tinh chỉnh: rút gọn 30 đoạn nén ≥1.45× → kết quả
  0 overflow, tempo max 1.447, mean 1.25
- edge-tts KeitaNeural +10%; demucs no_vocals + duck; mix atomic
- Mux video copy → export/janitor_assassin_ja_dub.mp4 (3504.0s)

## QC âm thanh (6 mốc rải khắp 58 phút)
| 0:30 | 10:00 | 25:00 | 40:00 | 50:00 | 58:00 |
|------|-------|-------|-------|-------|-------|
| -16.7 | -17.2 | -16.6 | -16.7 | -16.5 | -17.6 | (dB RMS — PASS)

## Watermark
- delogo bbox 6,6,300,88 (logo nguồn giống 2 video trước) + ネタバレ映画館 (24,18)
- Encode bị kill lần 1 do trần timeout job nền (~60'); chạy lại detached
  (Start-Process) → hoàn tất. Bài học: video >45' phải render detached.
- Verify frame 60s + 3000s: logo cũ xóa sạch, ネタバレ映画館 đúng vị trí
- Audio branded verify 6 mốc: khớp bản mix (−16.5…−17.6 dB), duration 3504.0s
- KẾT LUẬN: PASS — sẵn sàng đăng
