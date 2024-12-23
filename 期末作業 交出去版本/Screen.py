import pygame
import random
import os
from  Setting import * 
def game_over_screen():
    font = pygame.font.SysFont(None, 48)
    screen.fill((0, 0, 0))
    text = font.render("Game Over!", True, (255, 255, 255))
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
    pygame.display.flip()
    pygame.time.delay(2000)
    pygame.quit()
    exit()

def victory_screen():
    font = pygame.font.SysFont(None, 48)
    screen.fill((0, 0, 0))
    text = font.render("You Win!", True, (255, 255, 255))
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
    pygame.display.flip()
    pygame.time.delay(2000)
    pygame.quit()
    exit()

def show_start_screen():
    #font = pygame.font.Font("msjh.ttc", 24)#本文主角
    font_title = pygame.font.Font("msjh.ttc", 36)
    font_text = pygame.font.Font("msjh.ttc", 18)
    font_button = pygame.font.Font("msjh.ttc", 24)

    button_width, button_height = 200, 50
    button_x = (SCREEN_WIDTH - button_width) // 2
    button_y = SCREEN_HEIGHT // 2

    while True:
        screen.fill((0, 0, 0))

        # 遊戲名稱
        title_text = font_title.render("交通管理員", True, (255, 255, 255))
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))

        # 遊戲說明
        instruction_text = [
            "歡迎來到交通管理員！",
            "為了減少行人的數量，",
            "達成每一場景的需求，",
            "消除指定數量的交通工具。",
            "滑動方塊以匹配三個或更多相同的圖案。",
            "按下以下按鈕開始遊戲！"
        ]
        for i, line in enumerate(instruction_text):
            text_surface = font_text.render(line, True, (200, 200, 200))
            screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, 200 + i * 40))

        # 畫按鈕
        pygame.draw.rect(screen, (100, 200, 100), (button_x, button_y, button_width, button_height))
        button_text = font_button.render("開始遊戲", True, (0, 0, 0))
        screen.blit(button_text, (button_x + (button_width - button_text.get_width()) // 2, button_y + (button_height - button_text.get_height()) // 2))

        pygame.display.flip()

        # 檢查事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if button_x <= mx <= button_x + button_width and button_y <= my <= button_y + button_height:
                    return  # 離開此函數，開始遊戲

