import pygame
import random
import os
import Setting
from  Screen import * 


############################

background_images = [
    "image/background_level_1.jpg",
    "image/background_level_2.jpg",
    "image/background_level_3.jpg",
]
current_level = 0
remaining_steps = levels[current_level]["steps"]
pedestrians = sum(levels[current_level]["target"].values())  # 計算目標的總和
background_image = pygame.transform.scale(pygame.image.load(background_images[current_level]), (SCREEN_WIDTH, SCREEN_HEIGHT - 470))
##############################4


def draw_grid():
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if (x, y) not in eliminating:
                transport = grid[y][x]
                if transport:
                    screen.blit(images[transport], (x * TILE_SIZE, y * TILE_SIZE))
                pygame.draw.rect(screen, (0, 0, 0), (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 2)

def swap_tiles(pos1, pos2):
    swap_sound.play()
    grid[pos1[1]][pos1[0]], grid[pos2[1]][pos2[0]] = grid[pos2[1]][pos2[0]], grid[pos1[1]][pos1[0]]

def check_matches():
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
    global pedestrians
    target = levels[current_level]["target"]
    for x, y in matches:
        transport = grid[y][x]
        elimination_count[transport] += 1
        if transport and transport in target:  # 只有當前目標才計算
            if elimination_count[transport] <= target[transport]:  # 確保不超出目標數量
                pedestrians -= 1  # 減少行人數量
    eliminate_sound.play()
    for x, y in matches:
        grid[y][x] = None

def refill_grid():
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE-1, -1, -1):
            if grid[y][x] is None:
                for above_y in range(y-1, -1, -1):
                    if grid[above_y][x]:
                        grid[y][x] = grid[above_y][x]
                        grid[above_y][x] = None
                        break
                else:
                    grid[y][x] = random.choice(transport_keys)


def draw_statistics():
    font = pygame.font.SysFont(None, 24)
    y_offset = 370
    text = f"Level: {current_level+1}"
    text_surface = font.render(text, True, (255, 255, 255))
    screen.blit(text_surface, (100, y_offset))
    y_offset += 20
    text = f"Target:"
    text_surface = font.render(text, True, (255, 255, 255))
    screen.blit(text_surface, (100, y_offset))
    y_offset += 20
    
    
    current_target = levels[current_level]["target"]
    for transport, count in current_target.items():
        # 計算剩餘數量
        remaining = max(0, count - elimination_count.get(transport, 0))
        text = f"{transport} ------  {remaining}"  # 顯示名稱和剩餘數量
        text_surface = font.render(text, True, (255, 255, 255))
        screen.blit(text_surface, (100, y_offset))
        y_offset += 20
        
    y_offset = 370
    for transport, count in elimination_count.items():
        text = f"{transport.capitalize()}: {count}"
        text_surface = font.render(text, True, (255, 255, 255))
        screen.blit(text_surface, (10, y_offset))
        y_offset += 20

def draw_pedestrians():
    target_total = sum(levels[current_level]["target"].values())
    bar_width = 200
    bar_height = 20
    bar_x = (SCREEN_WIDTH - bar_width) // 2
    bar_y = SCREEN_HEIGHT - 50
    health_ratio = pedestrians / target_total if target_total > 0 else 0  # 避免除以零
    health_width = int(bar_width * health_ratio)
    
        # 繪製血量文字
    font = pygame.font.SysFont(None, 24)
    text = f"{pedestrians}/{target_total}"  # 格式為 "剩餘數量/總數量"
    text_surface = font.render(text, True, (255, 255, 255))
    text_x = bar_x + bar_width // 2 - text_surface.get_width() // 2  # 文字置中
    text_y = bar_y + 25  # 文字在血條上方
    screen.blit(text_surface, (text_x, text_y))
    #print(health_ratio,health_width)
    for i in range(pedestrians):
        x_offset = 20 + (i % 10) * 25
        y_offset = SCREEN_HEIGHT - 80 - (i // 10) * 25
        screen.blit(pedestrian_image, (x_offset, y_offset))
    pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
    pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, health_width, bar_height))

def animate_removal(matches):
    steps = 10
    alpha_grid = [[255] * GRID_SIZE for _ in range(GRID_SIZE)]
    for x, y in matches:
        eliminating.add((x, y))
    for step in range(steps):
        screen.fill((0, 0, 0))
        draw_background()
        draw_grid()
        draw_statistics()
        draw_pedestrians()
        for x, y in matches:
            alpha_grid[y][x] = max(0, 255 - (step + 1) * (255 // steps))
            transport = grid[y][x]
            if transport in images:
                image = images[transport].copy()
                image.set_alpha(alpha_grid[y][x])
                screen.blit(image, (x * TILE_SIZE, y * TILE_SIZE))
        pygame.display.flip()
        pygame.time.delay(5)
    for x, y in matches:
        grid[y][x] = None
    eliminating.clear()

def process_matches():
    while True:
        matches = check_matches()
        if not matches:
            break
        remove_matches(matches)
        animate_removal(matches)
        refill_grid()
        pygame.time.delay(200)
        draw_statistics()


def initialize_grid():
    while True:
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                grid[y][x] = random.choice(transport_keys)
        if not check_matches():
            break

def detect_game_over():
    global current_level, pedestrians, remaining_steps,background_images, background_image
    targets = levels[current_level]["target"]
    
    
    if all(elimination_count[transport] >= count for transport, count in targets.items()):
        current_level += 1
        if current_level >= len(levels):
            victory_screen()
        else:
            background_image = pygame.transform.scale(pygame.image.load(background_images[current_level]), (SCREEN_WIDTH, SCREEN_HEIGHT - 470))
            pedestrians = levels[current_level]["pedestrians"]
            remaining_steps = levels[current_level]["steps"]
            elimination_count.update({key: 0 for key in elimination_count})
            initialize_grid()
    elif remaining_steps <= 0:
        game_over_screen()

def draw_background():
    screen.blit(background_image, (0, 470))