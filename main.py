import pygame
from board import Board
pygame.init()

width, height = 1080, 720
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game")

FPS = 60
clock = pygame.time.Clock()

color = {'black': (0, 0, 0), 'grey': (105, 105, 105), 'red': (255, 0, 0), 'blue': (0,0,255)}

# Создание игрового поля
hexagons = Board(screen, color=color)
hexagons.map_of_hexagons()
hexagons.draw_hexagon()
pygame.display.flip()

# Основной игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            hexagons.draw_hexagon(position=pygame.mouse.get_pos(), click=True)
            pygame.display.flip()
            print(pygame.mouse.get_pos())

    clock.tick(FPS)

pygame.quit()
