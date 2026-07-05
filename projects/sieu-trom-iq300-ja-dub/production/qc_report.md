# QC report — sieu-trom-iq300-ja-dub v1

Ngày: 2026-07-05

## Nguồn
- Video: https://www.youtube.com/watch?v=mQ_FK6_o678 (1642s, 1080p, "Nguyễn Review 2")
- Phụ đề: auto-captions tiếng Việt (json3, word-level timing), 8057 từ

## Phân đoạn & khớp thời gian
- 136 phân đoạn, phủ 1641/1642s (đoạn cuối S136 kết thúc 1641.2s)
- Mỗi đoạn: end = start của đoạn kế → không hở, không chồng lấn
- Time-fit sau khi rút gọn 5 câu dịch dài (S109/S125/S127/S128/S130):
  - overflow > 0.3s: **0/136**
  - tempo nén trung bình ~1.13×, tối đa ~1.39× (trên nền edge-tts +10%)

## Giọng & âm thanh
- TTS: edge-tts `ja-JP-KeitaNeural`, rate +10%, loudnorm -16 LUFS/đoạn
- Nền: demucs htdemucs two-stems — dùng `no_vocals` (loại giọng Việt,
  giữ nhạc + hiệu ứng phim), sidechain-duck dưới giọng Nhật
- Mix cuối: loudnorm -14 LUFS, TP -1.0

## Đầu ra
- `export/sieu_trom_iq300_ja_dub.mp4` — video track copy nguyên gốc (không re-encode),
  audio AAC 192k

## Hạn chế đã biết
- Bản dịch cô đọng (~không dịch từng chữ) để lời Nhật đọc vừa đúng khung 12s/đoạn;
  nội dung cốt truyện giữ nguyên theo từng phân đoạn.
- Tên nhân vật lấy theo phụ đề tự động (Berlin/Roy/Cameron/Brooks/Kayla/Ken…),
  phụ đề gốc có nhiễu chính tả nên một số tên là phiên âm gần đúng.
- Giọng nói trong phim (thoại gốc của diễn viên) cũng bị demucs loại cùng giọng
  bình luận tiếng Việt — nền chỉ còn nhạc + hiệu ứng.
