# ===============================
# File: alpha_beta.py
# Chức năng:
# - Cài đặt thuật toán Alpha-Beta Pruning
# - Dùng cùng hàm đánh giá với Minimax
# - Chọn nước đi tốt nhất cho AI
# ===============================

import math
import time

from board import size, empty, player, Ai, is_draw, check_winner
from evaluation import evaluate


def alpha_beta(board, depth, maximizing, alpha, beta):
    """
    Thuật toán Alpha-Beta Pruning.
    """
    if check_winner(board, Ai):
        return 1000

    if check_winner(board, player):
        return -1000

    if is_draw(board):
        return 0

    if depth == 0:
        return evaluate(board)

    if maximizing:
        best = -math.inf

        for row in range(size):
            for col in range(size):
                if board[row][col] == empty:
                    board[row][col] = Ai

                    score = alpha_beta(board, depth - 1, False, alpha, beta)

                    board[row][col] = empty

                    best = max(best, score)
                    alpha = max(alpha, best)

                    if beta <= alpha:
                        return best

        return best

    best = math.inf

    for row in range(size):
        for col in range(size):
            if board[row][col] == empty:
                board[row][col] = player

                score = alpha_beta(board, depth - 1, True, alpha, beta)

                board[row][col] = empty

                best = min(best, score)
                beta = min(beta, best)

                if beta <= alpha:
                    return best

    return best


def best_move_alpha_beta(board, depth=3):
    """
    Chọn nước đi tốt nhất cho AI bằng Alpha-Beta Pruning.
    """
    best_score = -math.inf
    move = None

    start = time.time()

    for row in range(size):
        for col in range(size):
            if board[row][col] == empty:
                board[row][col] = Ai

                score = alpha_beta(
                    board,
                    depth - 1,
                    False,
                    -math.inf,
                    math.inf
                )

                board[row][col] = empty

                if score > best_score:
                    best_score = score
                    move = (row, col)

    end = time.time()
    print("Thoi gian Alpha-Beta:", end - start)
    print("Nuoc di tot nhat:", move, "diem:", best_score)

    return move
