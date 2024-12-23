import pygame
import random
import os
print("Current working directory:", os.getcwd())

# 初始化 Pygame
pygame.init()

# 遊戲設定
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 800
GRID_SIZE = 6
TILE_SIZE = 60
#COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0)]
grid_offset_y = SCREEN_HEIGHT - (GRID_SIZE * TILE_SIZE)  # 將棋盤移到畫面下半部

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Puzzle Drag and Match")

# 載入音效
swap_sound = pygame.mixer.Sound("swap.wav")  # 轉珠音效
eliminate_sound = pygame.mixer.Sound("eliminate.wav")  # 消除音效
swap_sound.set_volume(0.25)
eliminate_sound.set_volume(0.25)

# 載入交通工具圖片並縮放到棋盤大小
images = {
    "car": pygame.transform.scale(pygame.image.load("car.png"), (TILE_SIZE, TILE_SIZE)),
    "bus": pygame.transform.scale(pygame.image.load("bus.png"), (TILE_SIZE, TILE_SIZE)),
    "train": pygame.transform.scale(pygame.image.load("train.png"), (TILE_SIZE, TILE_SIZE)),
    "plane": pygame.transform.scale(pygame.image.load("airplane.jpg"), (TILE_SIZE, TILE_SIZE)),
    "bike": pygame.transform.scale(pygame.image.load("bike.png"), (TILE_SIZE, TILE_SIZE)),
}
# 載入背景圖片並縮放到需要的尺寸
background_image = pygame.transform.scale(pygame.image.load("background.jpg"), (SCREEN_WIDTH, SCREEN_HEIGHT - 470))

# 隨機初始化棋盤，使用交通工具名稱代替顏色
transport_keys = list(images.keys())
# 記錄每種交通工具的消除數量
elimination_count = {key: 0 for key in transport_keys}

grid = [[random.choice(transport_keys) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
dragging = False
drag_start = None
drag_current = None
def draw_background():
    """繪製下方的背景圖"""
    screen.blit(background_image, (0, 470))  # 在 (0, 470) 開始繪製背景圖
def draw_grid():
    """繪製遊戲盤格，使用圖片代替顏色方塊"""
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if (x, y) not in eliminating:  # 檢查該格子是否在消除列表中
                transport = grid[y][x]
                if transport:
                    # 繪製圖片
                    screen.blit(images[transport], (x * TILE_SIZE, y * TILE_SIZE))
                # 繪製邊框
                pygame.draw.rect(screen, (0, 0, 0), (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 2)




def swap_tiles(pos1, pos2):
    """交換兩個位置的珠子"""
    # 播放轉珠音效
    swap_sound.play()
    
    # 交換棋盤格子
    grid[pos1[1]][pos1[0]], grid[pos2[1]][pos2[0]] = grid[pos2[1]][pos2[0]], grid[pos1[1]][pos1[0]]


def check_matches():
    """檢查是否有三消的匹配"""
    matches = set()
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE - 2):
            if grid[y][x] == grid[y][x+1] == grid[y][x+2]:
                matches.update([(x, y), (x+1, y), (x+2, y)])
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE - 2):
            if grid[y][x] == grid[y+1][x] == grid[y+2][x]:
                matches.update([(x, y), (x, y+1), (x, y+2)])
    return matches

def remove_matches(matches):
    """移除匹配的交通工具並更新計數"""
    # 先更新消除數量，避免在 grid[y][x] 是 None 時計數
    for x, y in matches:
        transport = grid[y][x]
        if transport:
            elimination_count[transport] += 1  # 更新消除數量
    # 播放消除音效
    eliminate_sound.play()
    # 等動畫完成後清空格子
    for x, y in matches:
        grid[y][x] = None  # 將該位置設為 None



def refill_grid():
    """補充空缺的交通工具"""
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE-1, -1, -1):
            if grid[y][x] is None:
                for above_y in range(y-1, -1, -1):
                    if grid[above_y][x]:
                        grid[y][x] = grid[above_y][x]
                        grid[above_y][x] = None
                        break
                else:
                    grid[y][x] = random.choice(transport_keys)  # 補充新的交通工具
eliminating = set()  # 用來儲存需要消除的格子的座標
def animate_removal(matches):
    """動畫效果：讓匹配的圖片漸漸透明，僅影響被消除的部分"""
    steps = 10  # 動畫分成 10 個步驟
    alpha_grid = [[255] * GRID_SIZE for _ in range(GRID_SIZE)]  # 初始化透明度為255（完全不透明）

    # 標記消除的格子
    for x, y in matches:
        eliminating.add((x, y))  # 將該格子加入消除清單

    for step in range(steps):
        screen.fill((0, 0, 0))  # 清空畫面
        draw_background()       # 繪製背景
        draw_grid()             # 繪製棋盤
        draw_statistics()

        for x, y in matches:
            # 逐步降低透明度
            alpha_grid[y][x] = max(0, 255 - (step + 1) * (255 // steps))
            transport = grid[y][x]
            if transport in images:
                # 創建一個透明度調整後的圖片
                image = images[transport].copy()
                image.set_alpha(alpha_grid[y][x])  # 設定 Alpha 值
                screen.blit(image, (x * TILE_SIZE, y * TILE_SIZE))

        pygame.display.flip()
        pygame.time.delay(50)  # 每步延遲 50 毫秒

    # 動畫結束後，清空消除格子
    for x, y in matches:
        grid[y][x] = None  # 將該位置設為 None
    eliminating.clear()  # 清空消除格子標記


def process_matches():
    """反覆檢查並移除三消匹配，直到沒有新的匹配"""
    while True:
        matches = check_matches()
        if not matches:
            break
        # 先更新消除數量
        remove_matches(matches)
        # 然後才是動畫
        animate_removal(matches)  # 僅針對匹配部分進行動畫
        # 更新格子並補充新的交通工具
        refill_grid()             
        pygame.time.delay(200)    # 動畫與補充之間的小延遲
        draw_statistics()         # 更新統計




def initialize_grid():
    """初始化棋盤，避免出現初始匹配的情況"""
    transport_keys = list(images.keys())  # 提取字典的鍵作為列表
    while True:
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                grid[y][x] = random.choice(transport_keys)  # 隨機選擇鍵名
        if not check_matches():  # 確保初始化時沒有匹配
            break

def draw_statistics():
    """在畫面上方顯示消除的交通工具統計"""
    font = pygame.font.SysFont(None, 24)  # 使用系統字體
    y_offset = 370
    for transport, count in elimination_count.items():
        text = f"{transport.capitalize()}: {count}"
        text_surface = font.render(text, True, (255, 255, 255))  # 白色字體
        screen.blit(text_surface, (10, y_offset))
        y_offset += 20  # 每行向下移動 20 像素

# 偵測結束條件 可根據目前關卡目標修改now_target
now_target = "car"
def detect_over():
    if elimination_count[now_target] >10:
        game_over_screen()

def game_over_screen():
    """顯示遊戲結束畫面"""
    font = pygame.font.SysFont(None, 48)
    screen.fill((0, 0, 0))
    text = font.render("Game Over!", True, (255, 255, 255))
    score_text = font.render(f"Cars Eliminated: {elimination_count['car']}", True, (255, 255, 255))
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 + 10))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()  # 確保程式完全退出
            if event.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):
                waiting = False  # 退出結束畫面



# 初始化遊戲棋盤
initialize_grid()


clock = pygame.time.Clock()

running = True
while running:
    screen.fill((0, 0, 0))
    draw_background()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            drag_start = (mx // TILE_SIZE, my // TILE_SIZE)
            dragging = True
        if event.type == pygame.MOUSEBUTTONUP:
            dragging = False
            process_matches()  # 呼叫函式處理連續消除
            drag_start = None
            drag_current = None

    if dragging and drag_start:
        mx, my = pygame.mouse.get_pos()
        grid_x, grid_y = mx // TILE_SIZE, my // TILE_SIZE
        if (0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE and 
            (grid_x, grid_y) != drag_start and (abs(grid_x - drag_start[0]) + abs(grid_y - drag_start[1]) == 1)):
            swap_tiles(drag_start, (grid_x, grid_y))
            drag_start = (grid_x, grid_y)

    draw_grid()
    draw_statistics()  # 在每一幀中都繪製統計信息
    # 畫拖動的珠子
    if dragging and drag_start:
        mx, my = pygame.mouse.get_pos()
        sx, sy = drag_start[0] * TILE_SIZE, drag_start[1] * TILE_SIZE
        transport = grid[drag_start[1]][drag_start[0]]
        if transport:
            screen.blit(images[transport], (mx - TILE_SIZE // 2, my - TILE_SIZE // 2))
    
    
    detect_over()
    pygame.display.flip()
    clock.tick(30)


pygame.quit()
