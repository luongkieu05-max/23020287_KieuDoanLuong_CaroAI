# ===============================
# File: board.py
# Chức năng:
# - Biểu diễn bàn cờ Caro
# - Tạo bàn cờ
# - In bàn cờ ra console
# - Kiểm tra nước đi hợp lệ
# - Đánh quân lên bàn cờ
# - Kiểm tra bàn cờ đầy
# ===============================

# Kích thước bàn cờ theo yêu cầu đề bài: tối thiểu 9x9
BOARD_SIZE = 9

# Ký hiệu các ô trên bàn cờ
EMPTY = "."      # Ô trống
PLAYER = "X"    # Người chơi
AI = "O"        # Máy tính


def create_board():
    """
    Tạo bàn cờ rỗng kích thước BOARD_SIZE x BOARD_SIZE.

    Bàn cờ được biểu diễn bằng danh sách 2 chiều.
    Mỗi phần tử trong danh sách là một ô cờ.

    Ví dụ:
    [
        ['.', '.', '.', ...],
        ['.', '.', '.', ...],
        ...
    ]
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

    Hàm này hiển thị thêm chỉ số hàng và cột
    để người chơi dễ nhập vị trí muốn đánh.
    """
    print()

    # In chỉ số cột
    print("   ", end="")
    for col in range(BOARD_SIZE):
        print(col, end=" ")
    print()

    # In từng hàng của bàn cờ
    for row in range(BOARD_SIZE):
        print(row, " ", end="")

        for col in range(BOARD_SIZE):
            print(board[row][col], end=" ")

        print()

    print()


def is_valid_move(board, row, col):
    """
    Kiểm tra nước đi có hợp lệ hay không.

    Một nước đi hợp lệ khi:
    - Chỉ số hàng nằm trong bàn cờ
    - Chỉ số cột nằm trong bàn cờ
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
    Đánh quân vào bàn cờ.

    Tham số:
    - board: bàn cờ hiện tại
    - row: hàng muốn đánh
    - col: cột muốn đánh
    - symbol: quân cờ, có thể là X hoặc O

    Trả về:
    - True nếu đánh thành công
    - False nếu nước đi không hợp lệ
    """
    if is_valid_move(board, row, col):
        board[row][col] = symbol
        return True

    return False


def is_board_full(board):
    """
    Kiểm tra bàn cờ đã đầy hay chưa.

    Nếu không còn ô trống EMPTY thì bàn cờ đầy.
    Khi bàn cờ đầy mà không có người thắng thì kết quả là hòa.
    """
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == EMPTY:
                return False

    return True
