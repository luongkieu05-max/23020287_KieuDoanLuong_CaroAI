# ===============================
# File: evaluation.py
# Chức năng:
# - Hàm đánh giá trạng thái bàn cờ
# - Dùng chung cho Minimax và Alpha-Beta
# ===============================

from board import size, player, Ai, check_winner


def count_row(board, symbol, length):
    """
    Đếm số chuỗi liên tiếp theo hàng ngang có độ dài length.
    """
    count = 0

    for row in range(size):
        for col in range(size - length + 1):
            ok = True

            for k in range(length):
                if board[row][col + k] != symbol:
                    ok = False
                    break

            if ok:
                count += 1

    return count


def evaluate(board):
    """
    Hàm đánh giá trạng thái bàn cờ.

    AI là O nên điểm dương có lợi cho AI.
    Người chơi là X nên điểm âm có lợi cho người chơi.
    """
    if check_winner(board, Ai):
        return 1000

    if check_winner(board, player):
        return -1000

    score = 0
    score += count_row(board, Ai, 2) * 10
    score += count_row(board, Ai, 3) * 100
    score -= count_row(board, player, 2) * 10
    score -= count_row(board, player, 3) * 100

    return score
