# ===============================
# File: board.py
# Chức năng:
# - Biểu diễn bàn cờ Caro
# - Tạo bàn cờ
# - Kiểm tra nước đi, thắng, hòa
# - Xử lí các trạng thái bàn cờ
# ===============================

# CẤU HÌNH
BOARD_SIZE = 9
WIN_LEN = 4  # Điều kiện thắng
DEPTH = 4    # Độ sâu
lui_o = WIN_LEN - 1

# Kiểm tra chiến thắng
def check_winner(board, player):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            a = b = c = d = 0
            for e in range(WIN_LEN):
            # Ngang
                if j < BOARD_SIZE - lui_o:
                    if board[i][j+e] == player:
                        a += 1
            # Dọc
                if i < BOARD_SIZE - lui_o:
                    if board[i+e][j] == player:
                        b += 1
            # Chéo xuống (\)
                if i < BOARD_SIZE - lui_o and j < BOARD_SIZE - lui_o:
                    if board[i+e][j+e] == player:
                        c += 1
            # Chéo lên (/)
                if i < BOARD_SIZE - lui_o and j >= lui_o:
                    if board[i+e][j-e] == player:
                        d += 1
            if a==4 or b==4 or c==4 or d==4:
                    return True
            
    return False

# Kiểm tra hòa
def draw(board):
    for row in board:
        if ' ' in row: 
            return False
    return True

# tìm kiếm các ô trống tiếp giáp với các ô đánh rồi
def o_trong(board):
    moves = set() # hàm chứa các phần tử không trùng lặp với nhau
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] != ' ': # xét tìm các ô trống tiếp giáp với ô đã được đánh
                for m in [-1, 0, 1]:
                    for n in [-1, 0, 1]:
                        if m == 0 and n == 0: 
                            continue
                        doc = i + m
                        ngang = j + n
                        if 0 <= doc < BOARD_SIZE and 0 <= ngang < BOARD_SIZE and board[doc][ngang] == ' ':
                            moves.add((doc, ngang))
    if not moves: # nếu ban đầu chưa đánh gì hết chưa có ô trống nào thì lấy vị trí giữa bàn cờ
        return [(BOARD_SIZE // 2, BOARD_SIZE // 2)]
    return list(moves)