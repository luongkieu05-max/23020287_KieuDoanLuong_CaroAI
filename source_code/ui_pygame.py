# ===============================
# File: ui_pygame.py
# Chức năng:
# - Giao diện đồ họa cho game Caro bằng pygame
# - Hiển thị bàn cờ 9x9
# - Cho phép người chơi click chuột để đánh X
# ===============================

import pygame

from board import create_board, make_move, is_valid_move, PLAYER, AI, BOARD_SIZE
from game_rules import get_game_result


# Kích thước mỗi ô cờ
CELL_SIZE = 60

# Kích thước vùng bàn cờ
BOARD_PIXEL_SIZE = BOARD_SIZE * CELL_SIZE

# Kích thước cửa sổ
WINDOW_WIDTH = BOARD_PIXEL_SIZE
WINDOW_HEIGHT = BOARD_PIXEL_SIZE + 80

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
BLUE = (70, 130, 180)
RED = (220, 50, 50)


def get_ai_move(board):
    """
    Hàm chọn nước đi tạm thời cho máy.

    Hiện tại máy đánh vào ô trống đầu tiên tìm được.
    Sau này nhóm sẽ thay bằng Minimax hoặc Alpha-Beta.
    """
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == ".":
                return row, col

    return None, None


def draw_board(screen, board, font):
    """
    Vẽ bàn cờ và quân cờ lên cửa sổ pygame.
    """

    screen.fill(WHITE)

    # Vẽ các đường kẻ bàn cờ
    for i in range(BOARD_SIZE + 1):
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
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            symbol = board[row][col]

            center_x = col * CELL_SIZE + CELL_SIZE // 2
            center_y = row * CELL_SIZE + CELL_SIZE // 2

            if symbol == PLAYER:
                text = font.render("X", True, BLUE)
                text_rect = text.get_rect(center=(center_x, center_y))
                screen.blit(text, text_rect)

            elif symbol == AI:
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


def main():
    """
    Hàm chính chạy giao diện pygame.
    """

    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Caro AI - Minimax Alpha-Beta")

    font = pygame.font.SysFont(None, 48)
    message_font = pygame.font.SysFont(None, 32)

    board = create_board()
    running = True
    game_over = False
    message = "Luot nguoi choi X"

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

                    if is_valid_move(board, row, col):
                        make_move(board, row, col, PLAYER)

                        result = get_game_result(board)
                        if result != "CONTINUE":
                            message = show_result_message(result)
                            game_over = True
                            continue

                        # Máy đánh
                        ai_row, ai_col = get_ai_move(board)

                        if ai_row is not None and ai_col is not None:
                            make_move(board, ai_row, ai_col, AI)

                        result = get_game_result(board)
                        if result != "CONTINUE":
                            message = show_result_message(result)
                            game_over = True
                        else:
                            message = "Luot nguoi choi X"

                    else:
                        message = "O nay da co quan. Hay chon o khac."

    pygame.quit()


if __name__ == "__main__":
    main()