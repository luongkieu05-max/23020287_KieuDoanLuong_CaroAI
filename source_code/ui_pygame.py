# ===============================
# File: ui_pygame.py
# Chức năng:
# - Giao diện đồ họa cho game Caro bằng pygame
# - Menu chọn chế độ AI trên cửa sổ pygame
# - Hiển thị bàn cờ 9x9, cho phép click để đánh X
# ===============================

import pygame

from board import create_board, make_move, valid_move, player, Ai, size
from game_rules import get_game_result
from ai_minimax import best_move
from alpha_beta import best_move_alpha_beta


CELL_SIZE = 60
BOARD_PIXEL_SIZE = size * CELL_SIZE
WINDOW_WIDTH = BOARD_PIXEL_SIZE
WINDOW_HEIGHT = BOARD_PIXEL_SIZE + 80

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
LIGHT_GRAY = (230, 230, 230)
BLUE = (70, 130, 180)
RED = (220, 50, 50)
HOVER = (100, 160, 220)

STATE_MENU = "MENU"
STATE_PLAYING = "PLAYING"
STATE_GAME_OVER = "GAME_OVER"

MENU_BUTTONS = [
    {"mode": "MINIMAX", "label": "Minimax"},
    {"mode": "ALPHA_BETA", "label": "Alpha-Beta Pruning"},
]


def get_mode_label(ai_mode):
    if ai_mode == "MINIMAX":
        return "Minimax"
    return "Alpha-Beta"


def get_ai_move(board, ai_mode):
    """Chọn nước đi cho máy theo chế độ AI đã chọn."""
    if ai_mode == "MINIMAX":
        return best_move(board, depth=2)

    if ai_mode == "ALPHA_BETA":
        return best_move_alpha_beta(board, depth=3)

    return None


def create_button_rects(labels, start_y, button_w=320, button_h=50, gap=16):
    """Tạo danh sách nút căn giữa cửa sổ."""
    buttons = []
    center_x = WINDOW_WIDTH // 2
    total_h = len(labels) * button_h + (len(labels) - 1) * gap
    y = start_y - total_h // 2

    for label in labels:
        rect = pygame.Rect(0, 0, button_w, button_h)
        rect.center = (center_x, y + button_h // 2)
        buttons.append({"label": label, "rect": rect})
        y += button_h + gap

    return buttons


def draw_button(screen, rect, label, font, hovered=False):
    """Vẽ một nút bấm."""
    color = HOVER if hovered else LIGHT_GRAY
    pygame.draw.rect(screen, color, rect, border_radius=8)
    pygame.draw.rect(screen, GRAY, rect, 2, border_radius=8)

    text = font.render(label, True, BLACK)
    text_rect = text.get_rect(center=rect.center)
    screen.blit(text, text_rect)


def handle_button_click(mouse_pos, buttons):
    """Trả về nút được click, hoặc None."""
    for btn in buttons:
        if btn["rect"].collidepoint(mouse_pos):
            return btn
    return None


def draw_mode_menu(screen, title_font, button_font, mouse_pos):
    """Vẽ màn hình chọn chế độ AI."""
    screen.fill(WHITE)

    title = title_font.render("CARO AI", True, BLACK)
    title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 70))
    screen.blit(title, title_rect)

    subtitle = button_font.render("Chon che do AI", True, GRAY)
    subtitle_rect = subtitle.get_rect(center=(WINDOW_WIDTH // 2, 115))
    screen.blit(subtitle, subtitle_rect)

    buttons = create_button_rects(
        [b["label"] for b in MENU_BUTTONS],
        start_y=WINDOW_HEIGHT // 2 + 20,
    )

    for i, btn_data in enumerate(buttons):
        hovered = btn_data["rect"].collidepoint(mouse_pos)
        draw_button(screen, btn_data["rect"], btn_data["label"], button_font, hovered)
        btn_data["mode"] = MENU_BUTTONS[i]["mode"]

    return buttons


def draw_board(screen, board, font):
    """Vẽ bàn cờ và quân cờ."""
    screen.fill(WHITE)

    for i in range(size + 1):
        pygame.draw.line(
            screen, GRAY,
            (0, i * CELL_SIZE), (BOARD_PIXEL_SIZE, i * CELL_SIZE), 2
        )
        pygame.draw.line(
            screen, GRAY,
            (i * CELL_SIZE, 0), (i * CELL_SIZE, BOARD_PIXEL_SIZE), 2
        )

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
    """Hiển thị thông báo ở phía dưới cửa sổ."""
    pygame.draw.rect(screen, WHITE, (0, BOARD_PIXEL_SIZE, WINDOW_WIDTH, 80))
    text = font.render(message, True, BLACK)
    text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, BOARD_PIXEL_SIZE + 40))
    screen.blit(text, text_rect)


def draw_game_over_bar(screen, button_font, mouse_pos):
    """Vẽ nút Chơi lại / Đổi chế độ khi kết thúc ván."""
    buttons = create_button_rects(
        ["Choi lai", "Doi che do"],
        start_y=BOARD_PIXEL_SIZE + 40,
        button_w=140,
        button_h=36,
        gap=20,
    )

    for btn in buttons:
        hovered = btn["rect"].collidepoint(mouse_pos)
        draw_button(screen, btn["rect"], btn["label"], button_font, hovered)

    return buttons


def show_result_message(result):
    if result == "PLAYER_WIN":
        return "Nguoi choi X thang!"
    if result == "AI_WIN":
        return "May O thang!"
    if result == "DRAW":
        return "Hoa!"
    return "Luot nguoi choi X"


def main():
    """Chạy pygame: menu chọn chế độ → chơi → chơi lại / đổi chế độ."""
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Caro AI")

    title_font = pygame.font.SysFont(None, 56)
    font = pygame.font.SysFont(None, 48)
    button_font = pygame.font.SysFont(None, 28)
    message_font = pygame.font.SysFont(None, 26)

    app_running = True
    state = STATE_MENU
    ai_mode = None
    mode_label = ""
    board = create_board()
    message = ""
    menu_buttons = []
    end_buttons = []

    while app_running:
        mouse_pos = pygame.mouse.get_pos()

        if state == STATE_MENU:
            menu_buttons = draw_mode_menu(screen, title_font, button_font, mouse_pos)

        elif state == STATE_PLAYING:
            draw_board(screen, board, font)
            draw_message(screen, message, message_font)

        elif state == STATE_GAME_OVER:
            draw_board(screen, board, font)
            draw_message(screen, message, message_font)
            end_buttons = draw_game_over_bar(screen, button_font, mouse_pos)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                app_running = False
                continue

            if event.type != pygame.MOUSEBUTTONDOWN:
                continue

            if state == STATE_MENU:
                clicked = handle_button_click(event.pos, menu_buttons)
                if clicked:
                    ai_mode = clicked["mode"]
                    mode_label = get_mode_label(ai_mode)
                    board = create_board()
                    message = f"Che do: {mode_label} | Luot nguoi choi X"
                    pygame.display.set_caption(f"Caro AI - {mode_label}")
                    state = STATE_PLAYING

            elif state == STATE_PLAYING:
                mouse_x, mouse_y = event.pos

                if mouse_y >= BOARD_PIXEL_SIZE:
                    continue

                col = mouse_x // CELL_SIZE
                row = mouse_y // CELL_SIZE

                if not valid_move(board, row, col):
                    message = "O nay da co quan. Hay chon o khac."
                    continue

                make_move(board, row, col, player)

                result = get_game_result(board)
                if result != "CONTINUE":
                    message = show_result_message(result)
                    state = STATE_GAME_OVER
                    continue

                ai_row, ai_col = get_ai_move(board, ai_mode)
                if ai_row is not None and ai_col is not None:
                    make_move(board, ai_row, ai_col, Ai)

                result = get_game_result(board)
                if result != "CONTINUE":
                    message = show_result_message(result)
                    state = STATE_GAME_OVER
                else:
                    message = f"Che do: {mode_label} | Luot nguoi choi X"

            elif state == STATE_GAME_OVER:
                clicked = handle_button_click(event.pos, end_buttons)
                if not clicked:
                    continue

                if clicked["label"] == "Choi lai":
                    board = create_board()
                    message = f"Che do: {mode_label} | Luot nguoi choi X"
                    state = STATE_PLAYING
                elif clicked["label"] == "Doi che do":
                    state = STATE_MENU
                    pygame.display.set_caption("Caro AI")

    pygame.quit()


if __name__ == "__main__":
    main()
