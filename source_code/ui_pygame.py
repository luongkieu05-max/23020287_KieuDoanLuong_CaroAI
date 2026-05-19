# ===============================
# File: ui_pygame.py
# ===============================
import pygame
import sys
from time import sleep
import threading  # Để AI tính toán ngầm không đơ máy
import copy       # Để nhân bản bàn cờ, che giấu bước đi thử nghiệm của AI
from dataclasses import dataclass
# Import cấu hình và các hàm thay đổi độ sâu từ board.py
import board as board_module
from board import BOARD_SIZE, depth2, depth3, depth4, check_winner, draw
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
    font_title = pygame.font.SysFont("arial", 40, bold=True)
    font_btn = pygame.font.SysFont("arial", 32, bold=True)
    
    selected_mode = None
    selected_depth = None

    # VÒNG LẶP 1: CHỌN THUẬT TOÁN (MODE)
    while selected_mode is None:
        screen.fill((50, 50, 50))
        
        title_text = font_title.render("SELECT AI", True, (255, 255, 255))
        screen.blit(title_text, title_text.get_rect(center=(WIDTH // 2, 120)))

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
                if mini_rect.collidepoint(mx, my): selected_mode = "minimax"
                if alpha_rect.collidepoint(mx, my): selected_mode = "alpha"

    # Đợi một chút để tránh nhận nhầm click từ menu trước chuyển sang menu sau
    sleep(0.1)

    # VÒNG LẶP 2: CHỌN ĐỘ SÂU (DEPTH)
    while selected_depth is None:
        screen.fill((40, 40, 40))
        
        title_text = font_title.render("SELECT AI DEPTH", True, (255, 255, 255))
        screen.blit(title_text, title_text.get_rect(center=(WIDTH // 2, 100)))

        d2_rect = pygame.Rect(0, 0, 300, 70)
        d2_rect.center = (WIDTH // 2, 220)
        pygame.draw.rect(screen, (255, 215, 0), d2_rect, border_radius=14)
        screen.blit(font_btn.render("DEPTH 2", True, (0, 0, 0)), font_btn.render("DEPTH 2", True, (0, 0, 0)).get_rect(center=d2_rect.center))

        d3_rect = pygame.Rect(0, 0, 300, 70)
        d3_rect.center = (WIDTH // 2, 310)
        pygame.draw.rect(screen, (255, 165, 0), d3_rect, border_radius=14)
        screen.blit(font_btn.render("DEPTH 3", True, (0, 0, 0)), font_btn.render("DEPTH 3", True, (0, 0, 0)).get_rect(center=d3_rect.center))

        d4_rect = pygame.Rect(0, 0, 300, 70)
        d4_rect.center = (WIDTH // 2, 400)
        pygame.draw.rect(screen, (255, 69, 0), d4_rect, border_radius=14)
        screen.blit(font_btn.render("DEPTH 4", True, (0, 0, 0)), font_btn.render("DEPTH 4", True, (0, 0, 0)).get_rect(center=d4_rect.center))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if d2_rect.collidepoint(mx, my): selected_depth = 2
                if d3_rect.collidepoint(mx, my): selected_depth = 3
                if d4_rect.collidepoint(mx, my): selected_depth = 4

    return selected_mode, selected_depth

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
@dataclass
class CaroPygame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("CARO AI")
        self.font = pygame.font.SysFont('arial', 24, bold=True)
        
        # Nhận chế độ và độ sâu người chơi đã chọn từ menu
        self.mode, self.depth_level = show_mode_menu(self.screen)
        
        # Cập nhật biến DEPTH toàn cục trong board.py ngay từ lúc khởi tạo
        board_module.DEPTH = self.depth_level
        
        # Định nghĩa các nút chọn độ sâu ở thanh trạng thái
        self.btn_d2 = pygame.Rect(380, BOARD_SIZE * CELL_SIZE + 12, 40, 36)
        self.btn_d3 = pygame.Rect(430, BOARD_SIZE * CELL_SIZE + 12, 40, 36)
        self.btn_d4 = pygame.Rect(480, BOARD_SIZE * CELL_SIZE + 12, 40, 36)
        
        self.reset_game()

    def reset_game(self):
        self.board = [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.game_over = False
        self.ai_thinking = False
        self.win_positions = None
        self.status_text = f"You(X)"

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
        # Vẽ nền thanh trạng thái
        pygame.draw.rect(self.screen, STATUS_BG, (0, BOARD_SIZE * CELL_SIZE, WIDTH, 60))
        pygame.draw.line(self.screen, (100, 100, 100), (0, BOARD_SIZE * CELL_SIZE), (WIDTH, BOARD_SIZE * CELL_SIZE), 3)
        
        # Vẽ text trạng thái (giới hạn chiều rộng để không đè lên nút độ sâu)
        text = self.font.render(self.status_text, True, TEXT_COLOR)
        self.screen.blit(text, text.get_rect(midleft=(15, BOARD_SIZE * CELL_SIZE + 30)))
        
        # Vẽ nhãn "Depth:"
        label_font = pygame.font.SysFont('arial', 18, bold=True)
        lbl = label_font.render("Depth:", True, TEXT_COLOR)
        self.screen.blit(lbl, lbl.get_rect(midleft=(310, BOARD_SIZE * CELL_SIZE + 30)))
        
        # Vẽ các nút chọn độ sâu
        btn_font = pygame.font.SysFont('arial', 20, bold=True)
        
        # Nút D2
        d2_color = (255, 215, 0) if self.depth_level == 2 else (255, 255, 255)
        pygame.draw.rect(self.screen, d2_color, self.btn_d2, border_radius=6)
        pygame.draw.rect(self.screen, (100, 100, 100), self.btn_d2, width=2, border_radius=6)
        txt2 = btn_font.render("2", True, (0, 0, 0))
        self.screen.blit(txt2, txt2.get_rect(center=self.btn_d2.center))
        
        # Nút D3
        d3_color = (255, 165, 0) if self.depth_level == 3 else (255, 255, 255)
        pygame.draw.rect(self.screen, d3_color, self.btn_d3, border_radius=6)
        pygame.draw.rect(self.screen, (100, 100, 100), self.btn_d3, width=2, border_radius=6)
        txt3 = btn_font.render("3", True, (0, 0, 0))
        self.screen.blit(txt3, txt3.get_rect(center=self.btn_d3.center))
        
        # Nút D4
        d4_color = (255, 69, 0) if self.depth_level == 4 else (255, 255, 255)
        pygame.draw.rect(self.screen, d4_color, self.btn_d4, border_radius=6)
        pygame.draw.rect(self.screen, (100, 100, 100), self.btn_d4, width=2, border_radius=6)
        txt4 = btn_font.render("4", True, (0, 0, 0))
        self.screen.blit(txt4, txt4.get_rect(center=self.btn_d4.center))

    def update_depth(self, d):
        self.depth_level = d
        board_module.DEPTH = d
        if not self.game_over:
            self.status_text = f"You(X)"

    def handle_click(self, pos):
        x, y = pos
        if y >= BOARD_SIZE * CELL_SIZE:
            # Click trên thanh trạng thái -> kiểm tra chọn độ sâu
            if not self.ai_thinking and not self.game_over:
                if self.btn_d2.collidepoint(pos):
                    self.update_depth(2)
                elif self.btn_d3.collidepoint(pos):
                    self.update_depth(3)
                elif self.btn_d4.collidepoint(pos):
                    self.update_depth(4)
            return

        if self.game_over or self.ai_thinking: return
        col, row = x // CELL_SIZE, y // CELL_SIZE
        if self.board[row][col] != ' ': return

        self.board[row][col] = 'X'
        if check_winner(self.board, 'X'):
            self.win_positions = get_win_positions(self.board, 'X')
            self.game_over = True
            return
        if draw(self.board):
            self.game_over = True
            self.status_text = "DRAW"
            return

        self.ai_thinking = True
        self.status_text = f"AI..."
        
        # Kích hoạt luồng ngầm xử lý AI
        ai_thread = threading.Thread(target=self.do_ai_turn)
        ai_thread.start()

    def do_ai_turn(self):
        board_copy = copy.deepcopy(self.board)

        # 1. GỌI HÀM TỪ FILE board.py ĐỂ THAY ĐỔI BIẾN DEPTH TOÀN CỤC
        if self.depth_level == 2:
            depth2()  # Gọi hàm đổi DEPTH = 2 trong board.py
        elif self.depth_level == 3:
            depth3()  # Gọi hàm đổi DEPTH = 3 trong board.py
        else:
            depth4()  # Gọi hàm đổi DEPTH = 4 trong board.py

        # 2. GỌI THUẬT TOÁN AI (AI sẽ tự động đọc giá trị DEPTH mới từ board.py)
        import time
        start_time = time.time()
        if self.mode == "alpha":
            move = get_best_move(board_copy)
        else:
            move = get_best_move1(board_copy)
        elapsed_time = time.time() - start_time

        # 3. Cập nhật nước đi lên bàn cờ chính và kiểm tra kết quả ván đấu
        if move and not self.game_over:
            r, c = move
            self.board[r][c] = 'O'

            if check_winner(self.board, 'O'):
                self.win_positions = get_win_positions(self.board, 'O')
                self.game_over = True
            elif draw(self.board):
                self.game_over = True
                self.status_text = "DRAW"
            else:
                self.status_text = f"You(X) | AI: {elapsed_time:.3f}s"
        
        self.ai_thinking = False

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
                # Vẽ lại bàn cờ lần cuối để chắc chắn nước đi cuối cùng được hiển thị đầy đủ
                self.draw_grid()
                self.draw_pieces()
                self.draw_status()
                pygame.display.update()
                
                if self.win_positions: sleep(0.7)
                txt = "YOU WIN" if self.win_positions and self.board[self.win_positions[0][0]][self.win_positions[0][1]] == 'X' else "AI WIN" if self.win_positions else "DRAW"
                result = show_game_over(self.screen, txt)
                if result == "restart": 
                    self.reset_game()
                else:
                    pygame.quit()
                    sys.exit()
            clock.tick(30)

def main():
    game = CaroPygame()
    game.game_loop()

if __name__ == '__main__':
    main()