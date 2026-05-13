# ===============================
# File: game_rules.py
# Chức năng:
# - Cài đặt luật chơi Caro
# - Kiểm tra thắng/thua/hòa
# - Kiểm tra 4 quân liên tiếp theo 4 hướng
# ===============================

from board import BOARD_SIZE, PLAYER, AI, is_board_full

# Theo đề bài, người thắng là người có 4 quân liên tiếp
WIN_LENGTH = 4


def check_winner(board, symbol):
    """
    Kiểm tra một người chơi đã thắng hay chưa.

    Tham số:
    - board: bàn cờ hiện tại
    - symbol: quân cần kiểm tra, X hoặc O

    Luật thắng:
    Có 4 quân liên tiếp theo một trong các hướng:
    - Ngang
    - Dọc
    - Chéo xuống phải
    - Chéo xuống trái

    Đề bài không xét luật chặn hai đầu.
    """

    # Các hướng cần kiểm tra
    directions = [
        (0, 1),    # Hướng ngang: sang phải
        (1, 0),    # Hướng dọc: đi xuống
        (1, 1),    # Hướng chéo chính: xuống phải
        (1, -1)    # Hướng chéo phụ: xuống trái
    ]

    # Duyệt qua từng ô trên bàn cờ
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):

            # Nếu ô hiện tại không phải quân cần kiểm tra thì bỏ qua
            if board[row][col] != symbol:
                continue

            # Nếu gặp quân cần kiểm tra, thử kiểm tra theo 4 hướng
            for dr, dc in directions:
                count = 0

                # Kiểm tra 4 ô liên tiếp
                for step in range(WIN_LENGTH):
                    new_row = row + dr * step
                    new_col = col + dc * step

                    # Kiểm tra vị trí mới có nằm trong bàn cờ không
                    if 0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE:

                        # Nếu ô đó cùng ký hiệu thì tăng biến đếm
                        if board[new_row][new_col] == symbol:
                            count += 1
                        else:
                            break
                    else:
                        break

                # Nếu đủ 4 quân liên tiếp thì người chơi đó thắng
                if count == WIN_LENGTH:
                    return True

    return False


def get_game_result(board):
    """
    Kiểm tra trạng thái hiện tại của trò chơi.

    Trả về:
    - "PLAYER_WIN" nếu người chơi X thắng
    - "AI_WIN" nếu máy O thắng
    - "DRAW" nếu bàn cờ đầy và không ai thắng
    - "CONTINUE" nếu trò chơi chưa kết thúc
    """
    if check_winner(board, PLAYER):
        return "PLAYER_WIN"

    if check_winner(board, AI):
        return "AI_WIN"

    if is_board_full(board):
        return "DRAW"

    return "CONTINUE"
