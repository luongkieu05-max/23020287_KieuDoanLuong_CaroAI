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

def depth2():
    global DEPTH
    DEPTH = 2
    return DEPTH

def depth3():
    global DEPTH
    DEPTH = 3
    return DEPTH

def depth4():
    global DEPTH
    DEPTH = 4
    return DEPTH
# Kiểm tra chiến thắng
def check_winner(board, player):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            # Ngang
            if j <= BOARD_SIZE - WIN_LEN and all(board[i][j + k] == player for k in range(WIN_LEN)):
                return True
            # Dọc
            if i <= BOARD_SIZE - WIN_LEN and all(board[i + k][j] == player for k in range(WIN_LEN)):
                return True
            # Chéo xuống (\)
            if i <= BOARD_SIZE - WIN_LEN and j <= BOARD_SIZE - WIN_LEN and all(board[i + k][j + k] == player for k in range(WIN_LEN)):
                return True
            # Chéo lên (/)
            if i >= WIN_LEN - 1 and j <= BOARD_SIZE - WIN_LEN and all(board[i - k][j + k] == player for k in range(WIN_LEN)):
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