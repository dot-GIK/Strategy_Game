import pygame
from board import Board
from person import Person
from global_variables import color, characters
pygame.init()

width, height = 1080, 720
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game")

FPS = 60
clock = pygame.time.Clock()

# Создание игрока
player = Person(screen)

# Создание игрового поля
hexagons = Board(screen)
player.random_capture(who=characters[1])
pygame.display.flip()

# Основной игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            player.advance_phase()
            player.execute_phase(characters[1])
            
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

