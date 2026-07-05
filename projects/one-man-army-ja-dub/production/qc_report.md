# QC report — one-man-army-ja-dub v1

Ngày: 2026-07-05

## Nguồn
- Video: https://www.youtube.com/watch?v=3x0PyLWsOzE (1274s, 1080p, "Nguyễn Review 2")
- Phụ đề: auto-captions VI json3, 5742 từ → 105 phân đoạn ~12s, phủ 1276s

## Dub
- edge-tts KeitaNeural +10%, atempo fit: 0 overflow, tempo max 1.21× (S094 đã rút gọn),
  mean 1.14×
- Nền demucs no_vocals + sidechain duck; mix ghi atomic (guard mới)
- Mux video copy → export/one_man_army_ja_dub.mp4 (1274.1s)

## QC âm thanh (6 mốc rải khắp — quy tắc sau sự cố video 1)
| 0:30 | 5:00 | 10:00 | 15:00 | 18:20 | 20:50 |
|------|------|-------|-------|-------|-------|
| -17.1 | -17.0 | -16.8 | -17.1 | -17.7 | -17.6 | (dB RMS, đều có tiếng)

## Watermark
- Logo gốc "nguyen review" cùng vị trí video 1 → delogo bbox 6,6,300,88
- Branded: chữ ネタバレ映画館 overlay (24,18), libx264 veryfast crf19, audio copy
- Verify frame 60s + 1000s: logo cũ xóa sạch, ネタバレ映画館 hiển thị đúng (24,18)
- Audio branded verify lại 6 mốc: khớp y hệt bản mix (−16.8…−17.7 dB), duration 1274.1s
- KẾT LUẬN: PASS — sẵn sàng đăng
