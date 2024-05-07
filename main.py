import pygame
from src.product.person import Person
from src.product.person import Board
pygame.init()


def main():
    width, height = 1080, 800
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Game")

    FPS = 60
    clock = pygame.time.Clock()
    # Создание игрока
    player = Person(screen, width, height)
    # Создание игрового поля!
    player.random_capture(who='player1')
    pygame.display.flip()

    # Основной игровой цикл
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                player.advance_phase()
                player.execute_phase('player1')

                
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    main()