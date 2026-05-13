# Kích thước bàn cờ Caro theo đề bài: tối thiểu 9x9
BOARD_SIZE = 9

# Ký hiệu các trạng thái trên bàn cờ
EMPTY = "."
PLAYER = "X"
AI = "O"


def create_board():
    """
    Tạo bàn cờ rỗng kích thước BOARD_SIZE x BOARD_SIZE.
    Mỗi ô ban đầu có giá trị EMPTY.
    """
    board = []

    for row in range(BOARD_SIZE):
        current_row = []

        for col in range(BOARD_SIZE):
            current_row.append(EMPTY)

        board.append(current_row)

    return board


def print_board(board):
    """
    In bàn cờ ra màn hình console.
    Có hiển thị chỉ số hàng và cột để người chơi nhập nước đi.
    """
    print()
    print("   ", end="")

    for col in range(BOARD_SIZE):
        print(col, end=" ")

    print()

    for row in range(BOARD_SIZE):
        print(row, " ", end="")

        for col in range(BOARD_SIZE):
            print(board[row][col], end=" ")

        print()

    print()


def is_valid_move(board, row, col):
    """
    Kiểm tra nước đi có hợp lệ không.
    Nước đi hợp lệ khi:
    - Hàng và cột nằm trong bàn cờ
    - Ô được chọn đang trống
    """
    if row < 0 or row >= BOARD_SIZE:
        return False

    if col < 0 or col >= BOARD_SIZE:
        return False

    if board[row][col] != EMPTY:
        return False

    return True


def make_move(board, row, col, symbol):
    """
    Đánh quân symbol vào vị trí row, col nếu nước đi hợp lệ.
    Trả về True nếu đánh thành công, False nếu không hợp lệ.
    """
    if is_valid_move(board, row, col):
        board[row][col] = symbol
        return True

    return False


def is_board_full(board):
    """
    Kiểm tra bàn cờ đã đầy chưa.
    Nếu không còn ô EMPTY thì bàn cờ đầy.
    """
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == EMPTY:
                return False

    return True
