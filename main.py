import pygame
import math
from board import Board
pygame.init()

width, height = 1080, 720
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game")

FPS = 60
clock = pygame.time.Clock()

color = {'black': (0, 0, 0), 'grey': (105, 105, 105), 'red': (255, 0, 0)}

# Создание игрового поля
hexagons = Board(screen, color=color)
hexagons.map_of_hexagons()
pygame.display.flip()

# Основной игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    clock.tick(FPS)

pygame.quit()
