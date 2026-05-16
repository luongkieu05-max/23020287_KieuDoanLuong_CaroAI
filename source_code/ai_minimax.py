# ===============================
# File: ai_minimax.py
# Chức năng:
# - Cài đặt thuật toán Minimax
# - Chọn nước đi tốt nhất cho AI
# ===============================

import math
import time

from board import size, empty, player, Ai, is_draw, check_winner
from evaluation import evaluate


def minimax(board, depth, maximizing):
    """
    Thuật toán Minimax.
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
                    score = minimax(board, depth - 1, False)
                    board[row][col] = empty
                    best = max(best, score)

        return best

    best = math.inf

    for row in range(size):
        for col in range(size):
            if board[row][col] == empty:
                board[row][col] = player
                score = minimax(board, depth - 1, True)
                board[row][col] = empty
                best = min(best, score)

    return best


def best_move(board, depth=2):
    """
    Chọn nước đi tốt nhất cho AI bằng Minimax.
    """
    best_score = -math.inf
    move = None

    start = time.time()

    for row in range(size):
        for col in range(size):
            if board[row][col] == empty:
                board[row][col] = Ai
                score = minimax(board, depth - 1, False)
                board[row][col] = empty

                if score > best_score:
                    best_score = score
                    move = (row, col)

    end = time.time()
    print("Thoi gian Minimax:", end - start)
    print("Nuoc di tot nhat:", move, "diem:", best_score)

    return move
