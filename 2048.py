import pygame
import numpy as np
import random
import sys

# 初始化Pygame
pygame.init()

# 配置游戏参数
SIZE = 6  # 6x6棋盘
WIDTH, HEIGHT = 600, 600  # 窗口大小
CELL_SIZE = WIDTH // SIZE  # 每个单元格大小
FONT = pygame.font.Font(None, 40)  # 字体大小
BACKGROUND_COLOR = (187, 173, 160)  # 背景颜色
CELL_COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}

# 初始化棋盘
def init_game():
    board = np.zeros((SIZE, SIZE), dtype=int)
    add_new_number(board)
    add_new_number(board)
    return board

# 随机在空白处添加数字
def add_new_number(board):
    empty_cells = [(i, j) for i in range(SIZE) for j in range(SIZE) if board[i][j] == 0]
    if empty_cells:
        x, y = random.choice(empty_cells)
        board[x][y] = random.choice([2, 4])

# 移动并合并行
def slide_and_merge(row):
    new_row = [i for i in row if i != 0]
    for i in range(len(new_row)-1):
        if new_row[i] == new_row[i+1]:  # 合并相同的数字
            new_row[i] *= 2
            new_row[i+1] = 0
    new_row = [i for i in new_row if i != 0]
    return new_row + [0] * (SIZE - len(new_row))

# 上下左右滑动
def move_left(board):
    new_board = np.zeros((SIZE, SIZE), dtype=int)
    for i in range(SIZE):
        new_board[i] = slide_and_merge(board[i])
    return new_board

def move_right(board):
    new_board = np.zeros((SIZE, SIZE), dtype=int)
    for i in range(SIZE):
        new_board[i] = slide_and_merge(board[i][::-1])[::-1]
    return new_board

def move_up(board):
    return np.transpose(move_left(np.transpose(board)))

def move_down(board):
    return np.transpose(move_right(np.transpose(board)))

# 绘制单元格
def draw_cell(screen, value, x, y):
    color = CELL_COLORS.get(value, (60, 58, 50))
    pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))
    if value != 0:
        text = FONT.render(str(value), True, (0, 0, 0) if value <= 4 else (255, 255, 255))
        text_rect = text.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
        screen.blit(text, text_rect)

# 绘制整个棋盘
def draw_board(screen, board):
    screen.fill(BACKGROUND_COLOR)
    for i in range(SIZE):
        for j in range(SIZE):
            draw_cell(screen, board[i][j], j * CELL_SIZE, i * CELL_SIZE)

# 检查游戏是否结束
def is_game_over(board):
    if np.any(board == 0):  # 仍有空位
        return False
    for i in range(SIZE):
        for j in range(SIZE - 1):
            if board[i][j] == board[i][j + 1] or board[j][i] == board[j + 1][i]:
                return False
    return True

# 主程序
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("2048 Game - 6x6")
    board = init_game()
    clock = pygame.time.Clock()

    while True:
        draw_board(screen, board)
        pygame.display.flip()

        # 检查游戏是否结束
        if is_game_over(board):
            print("Game Over!")
            pygame.quit()
            sys.exit()

        # 处理用户输入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    new_board = move_left(board)
                elif event.key == pygame.K_RIGHT:
                    new_board = move_right(board)
                elif event.key == pygame.K_UP:
                    new_board = move_up(board)
                elif event.key == pygame.K_DOWN:
                    new_board = move_down(board)
                else:
                    continue  # 跳过非方向键

                # 检查是否有效移动并添加新数字
                if not np.array_equal(board, new_board):
                    board = new_board
                    add_new_number(board)

        clock.tick(10)

if __name__ == "__main__":
    main()
