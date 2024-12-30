import pygame
import random
import os
# 遊戲設定
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 800
GRID_SIZE = 6
TILE_SIZE = 60
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Puzzle Drag and Match")

# 音效
swap_sound = pygame.mixer.Sound("music/swap.wav")
eliminate_sound = pygame.mixer.Sound("music/eliminate.wav")
swap_sound.set_volume(0.25)
eliminate_sound.set_volume(0.25)

# 背景音樂
pygame.mixer.music.load("music/BGM.flac")  # 確保此檔案存在
pygame.mixer.music.set_volume(0.1)  # 設定音量（0.0 到 1.0）
pygame.mixer.music.play(-1)  # 循環播放背景音樂

# 圖片載入
images = {
    "car": pygame.transform.scale(pygame.image.load("image/car.png"), (TILE_SIZE, TILE_SIZE)),
    "bus": pygame.transform.scale(pygame.image.load("image/bus.png"), (TILE_SIZE, TILE_SIZE)),
    "train": pygame.transform.scale(pygame.image.load("image/train.png"), (TILE_SIZE, TILE_SIZE)),
    "plane": pygame.transform.scale(pygame.image.load("image/airplane.jpg"), (TILE_SIZE, TILE_SIZE)),
    "bike": pygame.transform.scale(pygame.image.load("image/bike.png"), (TILE_SIZE, TILE_SIZE)),
}

pedestrian_image = pygame.transform.scale(pygame.image.load("image/pedestrians.jpg"), (20, 20))

# 關卡設定
levels = [
    {"target": {"plane": 10}, "steps": 10, "pedestrians": 10},
    {"target": {"train": 10, "bus": 10}, "steps": 20, "pedestrians": 20},
    {"target": {"car": 10, "bus": 10, "bike": 10}, "steps": 30, "pedestrians": 30},
]
# 棋盤
transport_keys = list(images.keys())
grid = [[random.choice(transport_keys) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

elimination_count = {key: 0 for key in transport_keys}
dragging = False
drag_start = None
drag_current = None
eliminating = set()