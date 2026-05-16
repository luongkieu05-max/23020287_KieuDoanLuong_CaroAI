# ===============================
# File: main.py
# Chức năng:
# - File chạy chính của chương trình
# - Kết nối các phần:
#   + Biểu diễn bàn cờ
#   + Luật chơi
#   + Giao diện console
#   + Nước đi tạm thời của máy
# ===============================

from board import create_board, print_board, make_move, is_valid_move, PLAYER, AI
from game_rules import get_game_result
from ui_console import (
    show_welcome,
    get_player_move,
    show_invalid_move,
    show_ai_move,
    show_turn_player,
    show_turn_ai,
    show_result
)


def get_ai_move(board):
    """
    Hàm chọn nước đi cho máy.

    Hiện tại đây chỉ là hàm tạm thời:
    Máy sẽ đánh vào ô trống đầu tiên tìm được.

    Sau này nhóm sẽ thay hàm này bằng:
    - Minimax
    - Alpha-Beta Pruning
    - Hàm đánh giá trạng thái
    """
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == ".":
                return row, col

    return None, None


def main():
    """
    Hàm chính điều khiển toàn bộ luồng chơi.

    Thứ tự chơi:
    1. Tạo bàn cờ rỗng
    2. Người chơi đánh X
    3. Kiểm tra kết quả
    4. Máy đánh O
    5. Kiểm tra kết quả
    6. Lặp lại cho đến khi thắng, thua hoặc hòa
    """

    show_welcome()

    # Tạo bàn cờ ban đầu
    board = create_board()

    while True:
        # In bàn cờ hiện tại
        print_board(board)

        # ===============================
        # Lượt người chơi
        # ===============================
        show_turn_player()
        row, col = get_player_move()

        # Kiểm tra nước đi của người chơi
        if not is_valid_move(board, row, col):
            show_invalid_move()
            continue

        # Đánh quân X vào bàn cờ
        make_move(board, row, col, PLAYER)

        # Kiểm tra sau lượt người chơi
        result = get_game_result(board)
        if result != "CONTINUE":
            print_board(board)
            show_result(result)
            break

        # ===============================
        # Lượt máy
        # ===============================
        show_turn_ai()
        ai_row, ai_col = get_ai_move(board)

        # Nếu còn ô trống thì máy đánh
        if ai_row is not None and ai_col is not None:
            make_move(board, ai_row, ai_col, AI)
            show_ai_move(ai_row, ai_col)

        # Kiểm tra sau lượt máy
        result = get_game_result(board)
        if result != "CONTINUE":
            print_board(board)
            show_result(result)
            break


# Chỉ chạy hàm main khi file này được chạy trực tiếp
if __name__ == "__main__":
    main()