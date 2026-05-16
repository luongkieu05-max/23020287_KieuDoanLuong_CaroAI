# ===============================
# File: game_rules.py
# Chức năng:
# - Tổng hợp trạng thái trò chơi (thắng / thua / hòa / tiếp tục)
# ===============================

from board import player, Ai, check_winner, is_draw


def get_game_result(board):
    """
    Kiểm tra trạng thái hiện tại của trò chơi.

    Trả về:
    - "PLAYER_WIN" nếu người chơi X thắng
    - "AI_WIN" nếu máy O thắng
    - "DRAW" nếu hòa
    - "CONTINUE" nếu trò chơi chưa kết thúc
    """
    if check_winner(board, player):
        return "PLAYER_WIN"

    if check_winner(board, Ai):
        return "AI_WIN"

    if is_draw(board):
        return "DRAW"

    return "CONTINUE"
