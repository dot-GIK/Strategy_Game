import pygame
from person import Person
from global_variables import characters
pygame.init()

width, height = 1080, 1000
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game")

FPS = 60
clock = pygame.time.Clock()

# Создание игрока
player = Person(screen, width, height)
# Создание игрового поля
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
            if player.phase==3:
                for _ in range(player.points):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        player.execute_phase(characters[1])
            else:
                player.execute_phase(characters[1])

            
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

