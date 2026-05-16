# ===============================
# File: ui_pygame.py
# Chức năng:
# - Giao diện đồ họa cho game Caro bằng pygame
# - Hiển thị bàn cờ 9x9
# - Cho phép người chơi click chuột để đánh X
# ===============================

import pygame

from board import create_board, make_move, valid_move, player, Ai, size
from game_rules import get_game_result
from ai_minimax import best_move
from alpha_beta import best_move_alpha_beta


# Kích thước mỗi ô cờ
CELL_SIZE = 60

# Kích thước vùng bàn cờ
BOARD_PIXEL_SIZE = size * CELL_SIZE

# Kích thước cửa sổ
WINDOW_WIDTH = BOARD_PIXEL_SIZE
WINDOW_HEIGHT = BOARD_PIXEL_SIZE + 80

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
BLUE = (70, 130, 180)
RED = (220, 50, 50)


def get_ai_move(board, ai_mode):
    """
    Chọn nước đi cho máy theo chế độ AI đã chọn.
    """
    if ai_mode == "MINIMAX":
        return best_move(board, depth=2)

    if ai_mode == "ALPHA_BETA":
        return best_move_alpha_beta(board, depth=3)

    return None


def draw_board(screen, board, font):
    """
    Vẽ bàn cờ và quân cờ lên cửa sổ pygame.
    """

    screen.fill(WHITE)

    # Vẽ các đường kẻ bàn cờ
    for i in range(size + 1):
        # Đường ngang
        pygame.draw.line(
            screen,
            GRAY,
            (0, i * CELL_SIZE),
            (BOARD_PIXEL_SIZE, i * CELL_SIZE),
            2
        )

        # Đường dọc
        pygame.draw.line(
            screen,
            GRAY,
            (i * CELL_SIZE, 0),
            (i * CELL_SIZE, BOARD_PIXEL_SIZE),
            2
        )

    # Vẽ quân X và O
    for row in range(size):
        for col in range(size):
            symbol = board[row][col]

            center_x = col * CELL_SIZE + CELL_SIZE // 2
            center_y = row * CELL_SIZE + CELL_SIZE // 2

            if symbol == player:
                text = font.render("X", True, BLUE)
                text_rect = text.get_rect(center=(center_x, center_y))
                screen.blit(text, text_rect)

            elif symbol == Ai:
                text = font.render("O", True, RED)
                text_rect = text.get_rect(center=(center_x, center_y))
                screen.blit(text, text_rect)


def draw_message(screen, message, font):
    """
    Hiển thị thông báo ở phía dưới cửa sổ.
    """
    pygame.draw.rect(
        screen,
        WHITE,
        (0, BOARD_PIXEL_SIZE, WINDOW_WIDTH, 80)
    )

    text = font.render(message, True, BLACK)
    text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, BOARD_PIXEL_SIZE + 40))
    screen.blit(text, text_rect)


def show_result_message(result):
    """
    Chuyển kết quả game thành chuỗi thông báo.
    """
    if result == "PLAYER_WIN":
        return "Nguoi choi X thang!"

    if result == "AI_WIN":
        return "May O thang!"

    if result == "DRAW":
        return "Hoa!"

    return "Luot nguoi choi X"


def main(ai_mode="ALPHA_BETA"):
    """
    Hàm chính chạy giao diện pygame.

    Tham số:
    - ai_mode: "MINIMAX" hoặc "ALPHA_BETA"
    """

    pygame.init()

    mode_label = "Minimax" if ai_mode == "MINIMAX" else "Alpha-Beta"
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(f"Caro AI - {mode_label}")

    font = pygame.font.SysFont(None, 48)
    message_font = pygame.font.SysFont(None, 32)

    board = create_board()
    running = True
    game_over = False
    message = f"Che do: {mode_label} | Luot nguoi choi X"

    while running:
        draw_board(screen, board, font)
        draw_message(screen, message, message_font)
        pygame.display.update()

        for event in pygame.event.get():

            # Bấm nút X để tắt cửa sổ
            if event.type == pygame.QUIT:
                running = False

            # Người chơi click chuột để đánh
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Chỉ xử lý click trong vùng bàn cờ
                if mouse_y < BOARD_PIXEL_SIZE:
                    col = mouse_x // CELL_SIZE
                    row = mouse_y // CELL_SIZE

                    if valid_move(board, row, col):
                        make_move(board, row, col, player)

                        result = get_game_result(board)
                        if result != "CONTINUE":
                            message = show_result_message(result)
                            game_over = True
                            continue

                        # Máy đánh
                        ai_row, ai_col = get_ai_move(board, ai_mode)

                        if ai_row is not None and ai_col is not None:
                            make_move(board, ai_row, ai_col, Ai)

                        result = get_game_result(board)
                        if result != "CONTINUE":
                            message = show_result_message(result)
                            game_over = True
                        else:
                            message = f"Che do: {mode_label} | Luot nguoi choi X"

                    else:
                        message = "O nay da co quan. Hay chon o khac."

    pygame.quit()


if __name__ == "__main__":
    main()