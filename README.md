# 23020287_KieuDoanLuong_CaroAI
Caro AI using Minimax and Alpha-Beta Pruning
## Thành viên nhóm

| STT | Họ tên | MSSV | Vai trò |
|---|---|---|---|
| 1 | Kiều Doãn Lượng | 23020287 | GitHub, biểu diễn bàn cờ, quy tắc trò chơi, giao diện   |
| 2 | Nguyễn Văn Hưng | 23020280 | Cài đặt thuật toán gốc, cải tiến thuật toán, hàm đánh giá, tích hợp, kiểm thử |
| 3 | Nguyễn Duy Mạnh | 23020289 | Cài đặt thuật toán gốc, cải tiến thuật toán, hàm đánh giá, tích hợp, kiểm thử |

## Cấu trúc thư mục

| File/Thư mục | Chức năng |
|---|---|
| `source_code/main.py` | File chạy chính, mở pygame |
| `source_code/board.py` | Biểu diễn bàn cờ, tạo bàn cờ, in bàn cờ, kiểm tra ô hợp lệ |
| `source_code/game_rules.py` | Quy tắc trò chơi, kiểm tra thắng/thua/hòa |
| `source_code/evaluation.py` | Hàm đánh giá trạng thái bàn cờ |
| `source_code/ai_minimax.py` | Thuật toán Minimax |
| `source_code/alpha_beta.py` | Thuật toán Alpha-Beta Pruning |
| `source_code/ui_pygame.py` | Giao diện đồ họa pygame |
| `requirements.txt` | Thư viện cần cài (pygame) |

```text
23020287_KieuDoanLuong_CaroAI/
│
├── source_code/
│   ├── board.py
│   ├── game_rules.py
│   ├── evaluation.py
│   ├── ai_minimax.py
│   ├── alpha_beta.py
│   ├── main.py
│   └── ui_pygame.py
│
├── README.md
├── requirements.txt
├── .gitignore
└── report.pdf
```

## Cách chạy chương trình

Cài thư viện (nếu dùng pygame):

```bash
pip install -r requirements.txt
```

Chạy chương trình (chọn Minimax / Alpha-Beta trên cửa sổ pygame):

```bash
python source_code/main.py
```
