import pygame
from src.product.person import Person
from src.product.bots import RedBot, GreenBot, YellowBot
from src.product.board import Board
from src.product import global_variables

pygame.init()


def main():
    width, height = 1000, 800
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Game")
    board = Board(screen, width, height)

    FPS = 60
    clock = pygame.time.Clock()

    board.creating_map()
    # Создание игрока
    player = Person(screen, width, height, board)
    bot1 = RedBot(screen, width, height, board)
    # bot2 = RedBot(screen, width, height, board)
    # bot3 = RedBot(screen, width, height, board)

    # Создание игрового поля
    player.random_capture(who='player1')
    bot1.random_capture(who='bot1')
    # bot2.random_capture(who='bot2')
    # bot3.random_capture(who='bot3')
    pygame.display.flip()

    # Основной игровой цикл
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # print('phase:', global_variables.phase)
                if global_variables.phase == 1: player.phase1('player1')
                elif global_variables.phase == 2: player.phase2('player1')
                elif global_variables.phase == 3: player.phase3('player1')
                if global_variables.phase == 2:
                    print(len(player.my_hex)) 

                if global_variables.phase == 4: 
                    bot1.move('bot1', player_hex=player.my_hex)
                    # bot2.move('bot2', player_hex=player.my_hex)
                    # bot3.move('bot3', player_hex=player.my_hex)
                    global_variables.phase = 1

                
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    main()