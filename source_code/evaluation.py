# ===============================
# File: evaluation.py
# Chức năng:
# - Hàm đánh giá trạng thái bàn cờ
# - Dùng chung cho Minimax và Alpha-Beta
# ===============================

from board import BOARD_SIZE, WIN_LEN, lui_o
# Hàm đánh giá
def tinh_diem(window, AI, player):
    score = 0
    AI_count = window.count(AI) # trả về số lượng lượt đánh của AI trong window
    Play_count = window.count(player) # trả về số lượng lượt đánh của Người trong window

    # Đánh giá lợi thế của AI
    if AI_count > 0 and Play_count == 0:
        if AI_count == 4: score += 100000    # Chắc chắn thắng
        elif AI_count == 3: score += 10000   # Cơ hội rất cao
        elif AI_count == 2: score += 100     # Bắt đầu tạo thế
        elif AI_count == 1: score += 10
    
    # Đánh giá nước đi của Player
    elif Play_count > 0 and AI_count == 0:
        if Play_count == 4: score -= 100000    # Chắc chắn thua
        elif Play_count == 3: score -= 10000   # Rất nguy hiểm, phải chặn
        elif Play_count == 2: score -= 100     # Người chơi đang tạo thế
        elif Play_count == 1: score -= 10
        
    return score

def chuoi4o(board):
    score = 0
    # Lập tổ hợp 4 ô liên tiếp khắp bàn cơ
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            # Ngang
            if j < BOARD_SIZE - lui_o:
                window = []
                for e in range(WIN_LEN):
                    window.append(board[i][j+e])
                score += tinh_diem(window, 'X', 'O')

            # Dọc
            if i < BOARD_SIZE - lui_o:
                window = []
                for e in range(WIN_LEN):
                    window.append(board[i+e][j])
                score += tinh_diem(window, 'X', 'O')

            # Chéo xuống (\)
            if i < BOARD_SIZE - lui_o and j < BOARD_SIZE - lui_o:
                window = []
                for e in range(WIN_LEN):
                    window.append(board[i+e][j+e])
                score += tinh_diem(window, 'X', 'O')

            # Chéo lên (/)
            if i < BOARD_SIZE - lui_o and j >= lui_o:
                window = []
                for e in range(WIN_LEN):
                    window.append(board[i+e][j-e])
                score += tinh_diem(window, 'X', 'O')
    return score