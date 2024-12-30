import pygame
pygame.init()
import random
import os
from  grid import * 
from  Setting import * 
from  Screen import * 
print("當前目錄中的檔案：", os.listdir("."))
# 主程式
show_start_screen()  # 顯示開始畫面
initialize_grid()  # 初始化遊戲棋盤
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
            remaining_steps -= 1
            process_matches()
            detect_game_over()
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
    draw_pedestrians()
    # 畫拖動的珠子
    if dragging and drag_start:
        mx, my = pygame.mouse.get_pos()
        sx, sy = drag_start[0] * TILE_SIZE, drag_start[1] * TILE_SIZE
        transport = grid[drag_start[1]][drag_start[0]]
        if transport:
            screen.blit(images[transport], (mx - TILE_SIZE // 2, my - TILE_SIZE // 2)) 
    detect_game_over()
    pygame.display.flip()
    clock.tick(30)

pygame.quit()