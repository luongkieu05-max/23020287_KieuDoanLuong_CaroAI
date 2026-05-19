# 23020287_KieuDoanLuong_CaroAI

Game **Caro** (bàn cờ 9×9, thắng khi có **4 quân** liên tiếp theo ngang / dọc / chéo) với AI dùng **Minimax** và **Alpha-Beta Pruning**, giao diện **pygame**. Người chơi là **X**, máy là **O**.

## Thành viên nhóm

| STT | Họ tên | MSSV | Vai trò |
|-----|--------|------|---------|
| 1 | Kiều Doãn Lượng | 23020287 | GitHub, biểu diễn bàn cờ, quy tắc trò chơi, giao diện |
| 2 | Nguyễn Văn Hưng | 23020280 | Thuật toán, hàm đánh giá, tích hợp, kiểm thử |
| 3 | Nguyễn Duy Mạnh | 23020289 | Thuật toán, hàm đánh giá, tích hợp, kiểm thử |

## Tính năng

- Giao diện pygame: menu chọn **Minimax** hoặc **Alpha-Beta** ngay trên cửa sổ game.
- Có thể chọn **độ sâu** tìm kiếm (theo cấu hình trong `board.py`: `depth2` / `depth3` / `depth4`).
- AI chỉ xét các ô trống **lân cận** quân đã đánh (`o_trong` trong `board.py`) để giảm không gian tìm kiếm.
- Hàm đánh giá heuristic dùng chung: `evaluation.py` (hàm `chuoi4o`).
- File `Benchmark.py`: giao diện so sánh / đo thử Minimax và Alpha-Beta trên các bàn mẫu (tùy chọn).

## Yêu cầu môi trường

- **Python 3** (khuyến nghị 3.10 trở lên).
- Thư viện **pygame**.

Cài pygame (trong môi trường ảo nếu có):

```bash
pip install pygame
```

## Cách chạy

**Chạy game (mặc định):** mở pygame, chọn chế độ AI trên menu, đánh bằng chuột.

```bash
python source_code/main.py
```

Có thể chạy trực tiếp giao diện (tương đương):

```bash
python source_code/ui_pygame.py
```

**Chạy benchmark (tùy chọn):** so sánh thuật toán trên các bàn cờ thử nghiệm.

```bash
python source_code/Benchmark.py
```

> Trên Windows, nếu lệnh báo không tìm thấy file, dùng đúng chữ hoa/thường tên `Benchmark.py`.

## Cấu trúc thư mục

```text
23020287_KieuDoanLuong_CaroAI/
├── source_code/
│   ├── main.py           # Điểm vào: gọi giao diện pygame
│   ├── ui_pygame.py      # Giao diện game + menu chế độ + vòng lặp chơi
│   ├── board.py          # Cấu hình bàn cờ, thắng/hòa, ô ứng viên (o_trong), độ sâu
│   ├── evaluation.py     # Hàm đánh giá (heuristic) cho AI
│   ├── ai_minimax.py     # Minimax + get_best_move1
│   ├── alpha_beta.py     # Alpha-Beta + get_best_move
│   └── Benchmark.py      # Giao diện đo / so sánh thuật toán (tùy chọn)
├── README.md
└── .gitignore
```

| File | Mô tả ngắn |
|------|------------|
| `main.py` | Khởi chạy `ui_pygame.main()`. |
| `ui_pygame.py` | Pygame: menu AI, bàn cờ, luồng người–máy. |
| `board.py` | `BOARD_SIZE`, `WIN_LEN`, `DEPTH`, `check_winner`, `draw`, `o_trong`. |
| `evaluation.py` | Đánh giá trạng thái (`chuoi4o`, …). |
| `ai_minimax.py` | Thuật toán Minimax. |
| `alpha_beta.py` | Alpha-Beta pruning. |
| `Benchmark.py` | Benchmark Minimax vs Alpha-Beta trên bàn mẫu. |

## Ghi chú nộp bài

- Nếu đề bài yêu cầu `report.pdf`, thêm file vào thư mục gốc và cập nhật danh sách nộp tương ứng.
- Có thể tạo `requirements.txt` với nội dung `pygame` để cài một lệnh: `pip install -r requirements.txt`.
