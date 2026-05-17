# ===============================
# File: ai_minimax.py
# Chức năng:
# - Cài đặt thuật toán Minimax
# - Chọn nước đi tốt nhất cho AI
# ===============================

import math

from board import DEPTH, check_winner, o_trong, draw
from evaluation import chuoi4o

def minimax(board, depth, is_maximizing):
    if check_winner(board, 'X'): return 10000000
    if check_winner(board, 'O'): return -10000000
    if draw(board): return 0
    
    # Khi đạt tới độ sâu giới hạn, dùng hàm đánh giá để chấm điểm
    if depth == 0: return chuoi4o(board)

    danh_sach_o_trong = o_trong(board)

    if is_maximizing:
        max_eval = -math.inf
        for move in danh_sach_o_trong:
            board[move[0]][move[1]] = 'X'
            eval = minimax(board, depth - 1, False)
            board[move[0]][move[1]] = ' '
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = math.inf
        for move in danh_sach_o_trong:
            board[move[0]][move[1]] = 'O'
            eval = minimax(board, depth - 1, True)
            board[move[0]][move[1]] = ' '
            min_eval = min(min_eval, eval)
        return min_eval

def get_best_move1(board):
    best_score = -math.inf
    best_move = None
    possible_moves = o_trong(board)

    for move in possible_moves:
        board[move[0]][move[1]] = 'X'
        score = minimax(board, DEPTH - 1, False)
        board[move[0]][move[1]] = ' '
        
        if score > best_score:
            best_score = score
            best_move = move  
    return best_move