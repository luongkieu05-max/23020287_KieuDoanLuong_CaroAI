# ===============================
# File: board.py
# Chức năng:
# - Biểu diễn bàn cờ Caro
# - Tạo bàn cờ, in bàn cờ
# - Kiểm tra nước đi, thắng, hòa
# ===============================

size = 9
empty = "."
player = "X"
Ai = "O"


def create_board():
    """Tạo bàn cờ rỗng."""
    board = []

    for i in range(size):
        row = []

        for j in range(size):
            row.append(empty)

        board.append(row)

    return board


def print_board(board):
    """In bàn cờ ra console."""
    print()

    for i in range(size):
        for j in range(size):
            print(board[i][j], end=" ")

        print()

    print()


def player_move(board):
    """Nhận nước đi từ người chơi (console)."""
    while True:
        row = int(input("Nhap hang: "))
        col = int(input("Nhap cot: "))

        if valid_move(board, row, col):
            board[row][col] = player
            break

        print("Nuoc di khong hop le")


def valid_move(board, row, col):
    """Kiểm tra nước đi có hợp lệ hay không."""
    if row < 0 or row >= size:
        return False

    if col < 0 or col >= size:
        return False

    if board[row][col] != empty:
        return False

    return True


def make_move(board, row, col, symbol):
    """Đánh quân lên bàn cờ (dùng cho pygame và AI)."""
    if valid_move(board, row, col):
        board[row][col] = symbol
        return True

    return False


def check_winner(board, symbol):
    """Kiểm tra symbol đã thắng (4 quân liên tiếp) hay chưa."""
    # Ngang
    for i in range(size):
        for j in range(size - 3):
            if (
                board[i][j] == symbol
                and board[i][j + 1] == symbol
                and board[i][j + 2] == symbol
                and board[i][j + 3] == symbol
            ):
                return True

    # Dọc
    for i in range(size - 3):
        for j in range(size):
            if (
                board[i][j] == symbol
                and board[i + 1][j] == symbol
                and board[i + 2][j] == symbol
                and board[i + 3][j] == symbol
            ):
                return True

    # Chéo chính
    for i in range(size - 3):
        for j in range(size - 3):
            if (
                board[i][j] == symbol
                and board[i + 1][j + 1] == symbol
                and board[i + 2][j + 2] == symbol
                and board[i + 3][j + 3] == symbol
            ):
                return True

    # Chéo phụ
    for i in range(3, size):
        for j in range(size - 3):
            if (
                board[i][j] == symbol
                and board[i - 1][j + 1] == symbol
                and board[i - 2][j + 2] == symbol
                and board[i - 3][j + 3] == symbol
            ):
                return True

    return False


def is_draw(board):
    """Kiểm tra hòa (bàn cờ đã đầy)."""
    for row in board:
        if empty in row:
            return False

    return True
