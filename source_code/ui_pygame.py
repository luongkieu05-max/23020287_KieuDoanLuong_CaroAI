# ===============================
# File: ui_pygame.py
# ===============================
import pygame
import sys
from time import sleep
import threading  # Để AI tính toán ngầm không đơ máy
import copy       # Để nhân bản bàn cờ, che giấu bước đi thử nghiệm của AI

from board import BOARD_SIZE, check_winner, draw
from ai_minimax import get_best_move1
from alpha_beta import get_best_move  

# CẤU HÌNH ĐỒ HỌA
CELL_SIZE = 60
WIDTH = BOARD_SIZE * CELL_SIZE
HEIGHT = BOARD_SIZE * CELL_SIZE + 60
LINE_WIDTH = 2

BG_COLOR = (245, 245, 220)
LINE_COLOR = (139, 69, 19)
X_COLOR = (200, 0, 0)
O_COLOR = (0, 0, 200)
WIN_COLOR = (0, 200, 0)
STATUS_BG = (230, 230, 230)
TEXT_COLOR = (0, 0, 0)

def show_game_over(screen, text):
    width, height = screen.get_size()
    overlay = pygame.Surface((width, height))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    font_big = pygame.font.SysFont("arial", 60, bold=True)
    font_btn = pygame.font.SysFont("arial", 32, bold=True)

    msg = font_big.render(text, True, (255, 255, 255))
    screen.blit(msg, msg.get_rect(center=(width // 2, height // 2 - 80)))

    play_rect = pygame.Rect(0, 0, 260, 70)
    play_rect.center = (width // 2, height // 2 + 20)
    pygame.draw.rect(screen, (255, 255, 255), play_rect, border_radius=12)
    screen.blit(font_btn.render("RESTART", True, (0, 0, 0)), font_btn.render("RESTART", True, (0, 0, 0)).get_rect(center=play_rect.center))

    exit_rect = pygame.Rect(0, 0, 260, 70)
    exit_rect.center = (width // 2, height // 2 + 120)
    pygame.draw.rect(screen, (255, 255, 255), exit_rect, border_radius=12)
    screen.blit(font_btn.render("EXIT", True, (0, 0, 0)), font_btn.render("EXIT", True, (0, 0, 0)).get_rect(center=exit_rect.center))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if play_rect.collidepoint(mx, my): return "restart"
                if exit_rect.collidepoint(mx, my): return "exit"

def show_mode_menu(screen):
    font_btn = pygame.font.SysFont("arial", 32, bold=True)
    while True:
        screen.fill((50, 50, 50))
        mini_rect = pygame.Rect(0, 0, 300, 80)
        mini_rect.center = (WIDTH // 2, 250)
        pygame.draw.rect(screen, (255, 255, 255), mini_rect, border_radius=14)
        screen.blit(font_btn.render("MINIMAX", True, (0, 0, 0)), font_btn.render("MINIMAX", True, (0, 0, 0)).get_rect(center=mini_rect.center))

        alpha_rect = pygame.Rect(0, 0, 300, 80)
        alpha_rect.center = (WIDTH // 2, 360)
        pygame.draw.rect(screen, (255, 255, 255), alpha_rect, border_radius=14)
        screen.blit(font_btn.render("ALPHA - BETA", True, (0, 0, 0)), font_btn.render("ALPHA - BETA", True, (0, 0, 0)).get_rect(center=alpha_rect.center))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if mini_rect.collidepoint(mx, my): return "minimax"
                if alpha_rect.collidepoint(mx, my): return "alpha"

def get_win_positions(board, player):
    win_list = []
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if j <= BOARD_SIZE - 4 and all(board[i][j + k] == player for k in range(4)):
                win_list = [(i, j + k) for k in range(4)]
            elif i <= BOARD_SIZE - 4 and all(board[i + k][j] == player for k in range(4)):
                win_list = [(i + k, j) for k in range(4)]
            elif i <= BOARD_SIZE - 4 and j <= BOARD_SIZE - 4 and all(board[i + k][j + k] == player for k in range(4)):
                win_list = [(i + k, j + k) for k in range(4)]
            elif i >= 3 and j <= BOARD_SIZE - 4 and all(board[i - k][j + k] == player for k in range(4)):
                win_list = [(i - k, j + k) for k in range(4)]
            if win_list: return win_list
    return None

class CaroPygame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("CARO AI")
        self.font = pygame.font.SysFont('arial', 24, bold=True)
        self.mode = show_mode_menu(self.screen)
        self.reset_game()

    def reset_game(self):
        self.board = [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.game_over = False
        self.ai_thinking = False
        self.win_positions = None
        self.status_text = "You (O)"

    def draw_grid(self):
        self.screen.fill(BG_COLOR)
        for i in range(BOARD_SIZE + 1):
            pygame.draw.line(self.screen, LINE_COLOR, (i * CELL_SIZE, 0), (i * CELL_SIZE, BOARD_SIZE * CELL_SIZE), LINE_WIDTH)
            pygame.draw.line(self.screen, LINE_COLOR, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), LINE_WIDTH)

    def draw_pieces(self):
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                cx = x * CELL_SIZE + CELL_SIZE // 2
                cy = y * CELL_SIZE + CELL_SIZE // 2
                if self.win_positions and (y, x) in self.win_positions:
                    pygame.draw.rect(self.screen, WIN_COLOR, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                if self.board[y][x] == 'O':
                    pygame.draw.circle(self.screen, O_COLOR, (cx, cy), CELL_SIZE // 2 - 10, 4)
                elif self.board[y][x] == 'X':
                    offset = CELL_SIZE // 2 - 15
                    pygame.draw.line(self.screen, X_COLOR, (cx - offset, cy - offset), (cx + offset, cy + offset), 5)
                    pygame.draw.line(self.screen, X_COLOR, (cx + offset, cy - offset), (cx - offset, cy + offset), 5)

    def draw_status(self):
        pygame.draw.rect(self.screen, STATUS_BG, (0, BOARD_SIZE * CELL_SIZE, WIDTH, 60))
        pygame.draw.line(self.screen, (100, 100, 100), (0, BOARD_SIZE * CELL_SIZE), (WIDTH, BOARD_SIZE * CELL_SIZE), 3)
        text = self.font.render(self.status_text, True, TEXT_COLOR)
        self.screen.blit(text, text.get_rect(center=(WIDTH // 2, BOARD_SIZE * CELL_SIZE + 30)))

    def handle_click(self, pos):
        if self.game_over or self.ai_thinking: return
        x, y = pos
        if y >= BOARD_SIZE * CELL_SIZE: return
        col, row = x // CELL_SIZE, y // CELL_SIZE
        if self.board[row][col] != ' ': return

        self.board[row][col] = 'O'
        if check_winner(self.board, 'O'):
            self.win_positions = get_win_positions(self.board, 'O')
            self.game_over = True
            return
        if draw(self.board):
            self.game_over = True
            self.status_text = "DRAW"
            return

        self.ai_thinking = True
        self.status_text = "AI Thinking..."
        
        # Kích hoạt luồng ngầm xử lý AI
        ai_thread = threading.Thread(target=self.do_ai_turn)
        ai_thread.start()

    def do_ai_turn(self):
        # Chí mạng: Tạo bản sao sâu (deepcopy) để AI "thử nghiệm ngầm", không ảnh hưởng bàn cờ thật của UI
        board_copy = copy.deepcopy(self.board)

        if self.mode == "alpha":
            move = get_best_move(board_copy)
        else:
            move = get_best_move1(board_copy)

        if move and not self.game_over:
            r, c = move
            self.board[r][c] = 'X'  # Chốt nước cuối cùng lên màn hình thật

            if check_winner(self.board, 'X'):
                self.win_positions = get_win_positions(self.board, 'X')
                self.game_over = True
                return
            if draw(self.board):
                self.game_over = True
                self.status_text = "DRAW"
                return
            self.ai_thinking = False
            self.status_text = "You (O)"
        else:
            self.ai_thinking = False
            self.status_text = "You (O)"

    def game_loop(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if not self.game_over and event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)

            self.draw_grid()
            self.draw_pieces()
            self.draw_status()
            pygame.display.update()

            if self.game_over:
                if self.win_positions: sleep(0.7)
                txt = "YOU WIN" if self.win_positions and self.board[self.win_positions[0][0]][self.win_positions[0][1]] == 'O' else "AI WIN" if self.win_positions else "DRAW"
                result = show_game_over(self.screen, txt)
                if result == "restart": self.reset_game()
                else:
                    pygame.quit()
                    sys.exit()
            clock.tick(30)

def main():
    game = CaroPygame()
    game.game_loop()
