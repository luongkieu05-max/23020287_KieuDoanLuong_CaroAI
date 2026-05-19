# ===============================
# File: alpha_beta.py
# Chức năng:
# - Cài đặt thuật toán Alpha-Beta Pruning
# - Dùng cùng hàm đánh giá với Minimax
# - Chọn nước đi tốt nhất cho AI
# ===============================



import math

import board as board_module
from board import check_winner, o_trong, draw
from evaluation import chuoi4o

def minimax(board, depth, alpha, beta, is_maximizing):
    if check_winner(board, 'O'): return 5000000
    if check_winner(board, 'X'): return -4000000
    if draw(board): return 0
    
    # Khi đạt tới độ sâu giới hạn, dùng hàm đánh giá để chấm điểm
    if depth == 0: return chuoi4o(board)

    danh_sach_o_trong = o_trong(board)

    if is_maximizing:
        max_eval = -math.inf
        for move in danh_sach_o_trong:
            board[move[0]][move[1]] = 'O'
            eval = minimax(board, depth - 1, alpha, beta, False)
            board[move[0]][move[1]] = ' '
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = math.inf
        for move in danh_sach_o_trong:
            board[move[0]][move[1]] = 'X'
            eval = minimax(board, depth - 1, alpha, beta, True)
            board[move[0]][move[1]] = ' '
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha: 
                break
        return min_eval

def get_best_move(board):
    best_score = -math.inf
    best_move = None
    possible_moves = o_trong(board)
    alpha = -math.inf
    beta = math.inf

    for move in possible_moves:
        board[move[0]][move[1]] = 'O'
        score = minimax(board, board_module.DEPTH - 1, alpha, beta, False)
        board[move[0]][move[1]] = ' '
        if score > best_score:
            best_score = score
            best_move = move
        alpha = max(alpha, best_score)
        
    return best_move
