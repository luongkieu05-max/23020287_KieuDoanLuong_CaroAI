# ==========================================
# File: ui_benchmark.py
# ==========================================
import pygame
import sys
import time
import copy

# Import các hàm từ các file hiện tại của bạn
import board as board_module
from board import BOARD_SIZE, check_winner, draw
import ai_minimax
from ai_minimax import get_best_move1  # Hàm Minimax thuần túy
import alpha_beta
from alpha_beta import get_best_move    # Hàm Alpha-Beta Pruning

# CẤU HÌNH ĐỒ HỌA INTERFACE
CELL_SIZE = 40  # Thu nhỏ kích thước ô một chút để vừa màn hình tổng quan
GRID_SIZE = BOARD_SIZE * CELL_SIZE
WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 650

# MÀU SẮC
BG_COLOR = (240, 242, 245)
GRID_BG = (245, 239, 218)
LINE_COLOR = (139, 69, 19)
TEXT_COLOR = (33, 37, 41)
ACCENT_COLOR = (0, 80, 136)
GREEN_PANEL = (17, 202, 160)

# -----------------------------------------------------------------
# KHỞI TẠO 5 TRẠNG THÁI BÀN CỜ ĐỂ KIỂM THỬ (BENCHMARK BOARDS)
# -----------------------------------------------------------------
empty_board = [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

# Trạng thái 1: Khởi đầu (Mới đánh vài nước - 3 nước)
# O: (4, 4), (3, 4) | X: (4, 5)
b1 = copy.deepcopy(empty_board)
b1[4][4] = 'O'; b1[3][4] = 'O'
b1[4][5] = 'X'

# Trạng thái 2: Khai cuộc mở rộng (9 nước)
# Kế thừa Trạng thái 1 và phát triển thêm (không có bên nào thắng, chuỗi O dài nhất là 3)
b2 = copy.deepcopy(b1)
b2[2][4] = 'O'; b2[3][3] = 'O'; b2[3][5] = 'O'
b2[1][4] = 'X'; b2[3][2] = 'X'; b2[3][6] = 'X'

# Trạng thái 3: Thiết lập thế trận giằng co (14 nước)
# Kế thừa Trạng thái 2 và thêm các nước đi chặn đầu đuôi của cả 2 bên
b3 = copy.deepcopy(b2)
b3[2][3] = 'O'; b3[2][5] = 'O'
b3[5][4] = 'X'; b3[1][2] = 'X'; b3[1][6] = 'X'

# Trạng thái 4: Trung cuộc đan xen nhiều mối đe dọa (20 nước)
# Kế thừa Trạng thái 3 và thêm các chuỗi 3 quân nhưng đều bị chặn hợp lệ
b4 = copy.deepcopy(b3)
b4[4][3] = 'O'; b4[4][2] = 'O'; b4[4][6] = 'O'
b4[5][2] = 'X'; b4[4][1] = 'X'; b4[4][7] = 'X'

# Trạng thái 5: Tàn cuộc đỉnh điểm gay cấn nhưng CHƯA thắng (26 nước)
# Kế thừa Trạng thái 4 và tiếp tục cuộc đấu cực kỳ khốc liệt ở trung tâm
b5 = copy.deepcopy(b4)
b5[1][1] = 'O'; b5[5][0] = 'O'
b5[5][3] = 'X'; b5[1][5] = 'X'; b5[2][6] = 'X'; b5[0][3] = 'X'; b5[6][0] = 'X'

BENCHMARK_BOARDS = [b1, b2, b3, b4, b5]


class BenchmarkUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("CARO AI")
        self.clock = pygame.time.Clock()
        
        # Font chữ
        self.font_title = pygame.font.SysFont("arial", 22, bold=True)
        self.font_text = pygame.font.SysFont("arial", 16, bold=False)
        self.font_bold = pygame.font.SysFont("arial", 16, bold=True)
        
        # Quản lý trạng thái giao diện
        self.current_board_idx = 0
        self.current_depth = 2  # Độ sâu mặc định để test
        
        # Dữ liệu bảng kết quả
        self.results = {
            i: {
                "mm_time": "Not Tested", "mm_move": "N/A", "mm_states": "N/A",
                "ab_time": "Not Tested", "ab_move": "N/A", "ab_states": "N/A"
            }
            for i in range(5)
        }
        
        # Định nghĩa các nút bấm (Button Rects)
        self.btn_run = pygame.Rect(GRID_SIZE + 40, 80, 160, 40)
        self.btn_depth_up = pygame.Rect(GRID_SIZE + 320, 25, 40, 30)
        self.btn_depth_down = pygame.Rect(GRID_SIZE + 370, 25, 40, 30)
        
        self.btn_boards = []
        for i in range(5):
            self.btn_boards.append(pygame.Rect(GRID_SIZE + 40 + (i * 120), 140, 100, 35))

    def draw_grid(self):
        # Vẽ nền bàn cờ
        grid_rect = pygame.Rect(20, 80, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(self.screen, GRID_BG, grid_rect)
        
        # Vẽ các đường lưới đường biên
        board = BENCHMARK_BOARDS[self.current_board_idx]
        for i in range(BOARD_SIZE + 1):
            pygame.draw.line(self.screen, LINE_COLOR, (20 + i * CELL_SIZE, 80), (20 + i * CELL_SIZE, 80 + GRID_SIZE), 1)
            pygame.draw.line(self.screen, LINE_COLOR, (20, 80 + i * CELL_SIZE), (20 + GRID_SIZE, 80 + i * CELL_SIZE), 1)
            
        # Vẽ các quân cờ đang có sẵn ở trạng thái này
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                cx = 20 + c * CELL_SIZE + CELL_SIZE // 2
                cy = 80 + r * CELL_SIZE + CELL_SIZE // 2
                if board[r][c] == 'O':
                    pygame.draw.circle(self.screen, (0, 0, 200), (cx, cy), CELL_SIZE // 2 - 6, 3)
                elif board[r][c] == 'X':
                    offset = CELL_SIZE // 2 - 10
                    pygame.draw.line(self.screen, (200, 0, 0), (cx - offset, cy - offset), (cx + offset, cy + offset), 3)
                    pygame.draw.line(self.screen, (200, 0, 0), (cx + offset, cy - offset), (cx - offset, cy + offset), 3)

    def draw_dashboard(self):
        # Tiêu đề chính
        title = self.font_title.render("MINIMAX VS ALPHA-BETA", True, ACCENT_COLOR)
        self.screen.blit(title, (20, 25))
        
        # Hiển thị độ sâu hiện tại
        depth_txt = self.font_bold.render(f"Testing Depth (Depth): {self.current_depth}", True, TEXT_COLOR)
        self.screen.blit(depth_txt, (GRID_SIZE + 40, 30))
        
        # Nút tăng giảm depth
        pygame.draw.rect(self.screen, ACCENT_COLOR, self.btn_depth_up, border_radius=5)
        pygame.draw.rect(self.screen, ACCENT_COLOR, self.btn_depth_down, border_radius=5)
        self.screen.blit(self.font_bold.render("+", True, (255,255,255)), (self.btn_depth_up.x + 15, self.btn_depth_up.y + 5))
        self.screen.blit(self.font_bold.render("-", True, (255,255,255)), (self.btn_depth_down.x + 17, self.btn_depth_down.y + 5))

        # Nút Bấm "CHẠY THỰC NGHIỆM"
        pygame.draw.rect(self.screen, GREEN_PANEL, self.btn_run, border_radius=8)
        run_txt = self.font_bold.render("RUN TEST", True, (255, 255, 255))
        self.screen.blit(run_txt, run_txt.get_rect(center=self.btn_run.center))

        # Các nút chọn xem 5 Trạng thái bàn cờ
        for i, rect in enumerate(self.btn_boards):
            color = GREEN_PANEL if i == self.current_board_idx else (200, 200, 200)
            pygame.draw.rect(self.screen, color, rect, border_radius=5)
            b_txt = self.font_bold.render(f"Board {i+1}", True, (255, 255, 255) if i == self.current_board_idx else TEXT_COLOR)
            self.screen.blit(b_txt, b_txt.get_rect(center=rect.center))

        # -----------------------------------------------------------------
        # VẼ BẢNG KẾT QUẢ THỰC NGHIỆM (BENCHMARK TABLE)
        # -----------------------------------------------------------------
        table_start_y = 210
        pygame.draw.rect(self.screen, (255, 255, 255), (GRID_SIZE + 40, table_start_y, 620, 380), border_radius=10)
        
        # Tiêu đề cột
        headers = ["Sample", "MM Move", "MM Time", "MM States", "AB Move", "AB Time", "AB States"]
        col_widths = [65, 80, 85, 95, 80, 85, 95]
        start_x = GRID_SIZE + 45
        
        # Vẽ Header nền màu xanh đậm
        pygame.draw.rect(self.screen, ACCENT_COLOR, (GRID_SIZE + 40, table_start_y, 620, 40), border_top_left_radius=10, border_top_right_radius=10)
        for idx, header in enumerate(headers):
            h_x = start_x + sum(col_widths[:idx])
            txt = self.font_bold.render(header, True, (255, 255, 255))
            self.screen.blit(txt, (h_x, table_start_y + 10))
            
        # Đổ dữ liệu 5 hàng của 5 Board vào bảng
        for i in range(5):
            row_y = table_start_y + 40 + (i * 55)
            # Vẽ đường kẻ ngang phân tách
            pygame.draw.line(self.screen, (220, 220, 220), (GRID_SIZE + 40, row_y + 50), (GRID_SIZE + 660, row_y + 50), 1)
            
            # Highlight dòng đang được chọn xem cờ
            if i == self.current_board_idx:
                pygame.draw.rect(self.screen, (230, 242, 250), (GRID_SIZE + 41, row_y, 618, 50))

            res = self.results[i]
            row_data = [
                f"Board {i+1}",
                str(res["mm_move"]),
                f"{res['mm_time']:.4f}s" if isinstance(res['mm_time'], float) else res['mm_time'],
                str(res["mm_states"]),
                str(res["ab_move"]),
                f"{res['ab_time']:.4f}s" if isinstance(res['ab_time'], float) else res['ab_time'],
                str(res["ab_states"])
            ]
            
            for idx, data in enumerate(row_data):
                d_x = start_x + sum(col_widths[:idx])
                # Đổi màu chữ Alpha-Beta sang xanh lá nếu đã tính xong để làm nổi bật kết quả
                c = (11, 150, 100) if idx in (4, 5, 6) and isinstance(res['ab_time'], float) else TEXT_COLOR
                txt = self.font_text.render(data, True, c)
                self.screen.blit(txt, (d_x, row_y + 15))

    def run_benchmark(self):
        """Hàm quét qua trạng thái hiện tại, chạy cả 2 thuật toán và đo đạc dữ liệu"""
        board = BENCHMARK_BOARDS[self.current_board_idx]
        
        # Thiết lập độ sâu động vào board.py để AI tự đọc
        board_module.DEPTH = self.current_depth
        
        # 1. Đo hiệu năng Minimax thuần túy
        start_time = time.time()
        mm_move = get_best_move1(copy.deepcopy(board))
        mm_elapsed = time.time() - start_time
        mm_states = ai_minimax.visited_states
        
        # 2. Đo hiệu năng Alpha-Beta Pruning 
        start_time = time.time()
        ab_move = get_best_move(copy.deepcopy(board))
        ab_elapsed = time.time() - start_time
        ab_states = alpha_beta.visited_states
        
        # 3. Cập nhật dữ liệu lưu vào bảng
        self.results[self.current_board_idx] = {
            "mm_time": mm_elapsed,
            "mm_move": mm_move if mm_move else "Pass",
            "mm_states": mm_states,
            "ab_time": ab_elapsed,
            "ab_move": ab_move if ab_move else "Pass",
            "ab_states": ab_states
        }

    def main_loop(self):
        while True:
            self.screen.fill(BG_COLOR)
            
            # Vẽ các thành phần giao diện
            self.draw_grid()
            self.draw_dashboard()
            
            pygame.display.update()
            
            # Xử lý sự kiện tương tác chuột
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos
                    
                    # Click chọn tăng giảm độ sâu test
                    if self.btn_depth_up.collidepoint(mx, my) and self.current_depth < 4:
                        self.current_depth += 1
                    elif self.btn_depth_down.collidepoint(mx, my) and self.current_depth > 1:
                        self.current_depth -= 1
                        
                    # Click chọn xem cấu trúc các Bàn cờ 1 -> 5
                    for i, rect in enumerate(self.btn_boards):
                        if rect.collidepoint(mx, my):
                            self.current_board_idx = i
                            
                    # Click bấm nút "CHẠY TEST"
                    if self.btn_run.collidepoint(mx, my):
                        # Đổi text trạng thái tạm thời trong khi xử lý tính toán ngầm
                        self.results[self.current_board_idx]["mm_time"] = "Computing..."
                        self.results[self.current_board_idx]["ab_time"] = "Computing..."
                        self.draw_dashboard()
                        pygame.display.update()
                        
                        # Thực thi đo đạc cấu trúc thuật toán
                        self.run_benchmark()
            
            self.clock.tick(30)


if __name__ == "__main__":
    app = BenchmarkUI()
    app.main_loop()