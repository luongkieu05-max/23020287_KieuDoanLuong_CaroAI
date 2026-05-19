# ===============================
# File: evaluation.py
# Chức năng:
# - Hàm đánh giá trạng thái bàn cờ tối ưu tốc độ
# - Dùng chung cho Minimax và Alpha-Beta
# ===============================

from board import BOARD_SIZE, WIN_LEN, lui_o

def tinh_diem(window, AI, player):
    score = 0
    AI_count = window.count(AI)
    Play_count = window.count(player)

    # --- ĐÁNH GIÁ LỢI THẾ CỦA AI ('O') ---
    if AI_count > 0 and Play_count == 0:
        if AI_count == 4: return 500000     # Thắng tuyệt đối
        elif AI_count == 3: score += 15000   # Thế trận cực mạnh (3 ô thoáng)
        elif AI_count == 2: score += 200     # Bắt đầu tạo thế đôi
        elif AI_count == 1: score += 10      # Điểm khuyến khích ô đơn

    # --- ĐÁNH GIÁ NƯỚC ĐI CỦA PLAYER ('X') ---
    elif Play_count > 0 and AI_count == 0:
        if Play_count == 4: return -400000    # Phải chặn ngay lập tức nếu không sẽ thua
        elif Play_count == 3: score -= 20000   # Player có 3 ô nguy hiểm, ưu tiên chặn cao hơn tự công
        elif Play_count == 2: score -= 300     # Ngăn chặn Player tạo thế đôi
        elif Play_count == 1: score -= 15      # Chặn bớt các ô lẻ

    return score

def chuoi4o(board):
    score = 0

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            
            # Ngang
            if j < BOARD_SIZE - lui_o:
                window = board[i][j : j + WIN_LEN]
                score += tinh_diem(window, 'O', 'X')

            # Dọc
            if i < BOARD_SIZE - lui_o:
                window = [board[i + e][j] for e in range(WIN_LEN)]
                score += tinh_diem(window, 'O', 'X')

            # Chéo xuống (\)
            if i < BOARD_SIZE - lui_o and j < BOARD_SIZE - lui_o:
                window = [board[i + e][j + e] for e in range(WIN_LEN)]
                score += tinh_diem(window, 'O', 'X')

            # Chéo lên (/)
            if i < BOARD_SIZE - lui_o and j >= lui_o:
                window = [board[i + e][j - e] for e in range(WIN_LEN)]
                score += tinh_diem(window, 'O', 'X')
                
    return score