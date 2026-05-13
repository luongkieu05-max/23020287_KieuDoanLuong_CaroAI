# ===============================
# File: ui_console.py
# Chức năng:
# - Xử lý giao diện nhập/xuất bằng console
# - Nhận nước đi từ người chơi
# ===============================


def get_player_move():
    """
    Nhận nước đi từ người chơi thông qua console.

    Người chơi nhập:
    - Hàng muốn đánh
    - Cột muốn đánh

    Hàm trả về:
    - row: chỉ số hàng
    - col: chỉ số cột

    Nếu người chơi nhập không phải số nguyên,
    chương trình sẽ yêu cầu nhập lại.
    """
    while True:
        try:
            row = int(input("Nhap hang: "))
            col = int(input("Nhap cot: "))
            return row, col

        except ValueError:
            print("Loi: Vui long nhap so nguyen.")
