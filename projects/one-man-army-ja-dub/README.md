# one-man-army-ja-dub

Bản lồng tiếng Nhật (time-aligned) cho video review phim:
"[Review Phim] Cuộc Chiến Một Mình Tiêu Diệt Cả Sở Cảnh Sát!"
(https://www.youtube.com/watch?v=3x0PyLWsOzE — 21:14, kênh Nguyễn Review 2).

Phim: hành động Nga kiểu "First Blood" — thiếu tá đặc nhiệm マルーンベレー
tên サマン một mình chống cả sở cảnh sát tha hóa.

Pipeline giống `projects/sieu-trom-iq300-ja-dub` (xem README ở đó):
105 phân đoạn ~12s phủ 1276s, dịch cô đọng theo slot, edge-tts KeitaNeural +10%,
atempo fit (0 overflow, max 1.21× sau khi rút gọn S094), demucs no_vocals + duck,
mux video copy, sau đó brand watermark ネタバレ映画館 (bbox logo cũ giống video 1).

Chạy lại: xem `tools/build_dub.py`, `tools/brand_watermark.py`, `tools/parse_captions.py`.
Media (audio/, export/) không commit.
