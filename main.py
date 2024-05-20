import time
import pandas as pd
import pygame
from src.product.initial_window import InitialWindow
from src.product.person import Person
from src.product.bots import RedBotRandom, RedBotClever, GreenBot, YellowBot, PurpleBot
from src.product.board import Board
from src.product import global_variables
from src.product.GameOver import GameOverScreen
pygame.init()


def main():
    width, height = 1000, 800
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Game")

    board = Board(screen, width, height)
    initial_window = InitialWindow(screen, width, height, board)
    game_over_screen = GameOverScreen(screen, width, height, board)
    
    FPS = 60
    clock = pygame.time.Clock()

    sel_bots = []
    only_bots = None
    init_wind_st = 0
    running = True
    # Цикл начального окна
    while running:
        if init_wind_st <= FPS:
            init_wind_st+=1
            initial_window.appearance_window()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if initial_window.update(position=pygame.mouse.get_pos(), mode='buttondown') == False:
                    running = False
                    sel_bots = initial_window.get_bots()
                    only_bots = initial_window.get_mode()
        pygame.display.flip()
        clock.tick(FPS)
    
    # Создание карты
    board.creating_map()

    # Создание игрока
    player = Person(screen, width, height, board)

    # Создание ботов
    bots = []
    for bot in sel_bots:
        if bot == 'bot1':
            bot1 = RedBotClever(screen, width, height, board)
            bots.append([bot1, 'bot1'])
        elif bot == 'bot2':
            bot2 = RedBotRandom(screen, width, height, board)
            bots.append([bot2, 'bot2'])
        elif bot == 'bot3':
            bot3 = RedBotRandom(screen, width, height, board)
            bots.append([bot3, 'bot3'])
        elif bot == 'bot4':
            bot4 = RedBotRandom(screen, width, height, board)
            bots.append([bot4, 'bot4'])
    
    # Создание начальных гексов ботов
    for bot, who in bots:
        bot.random_capture(who=who)

    pygame.display.flip()
    game_over = False
    game_over_scr = False

    if only_bots == False: player.random_capture(who='player1')
    else: timer = time.time()
    # Главный цикл
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and only_bots == False:
                if global_variables.phase == 1: player.phase1('player1')
                elif global_variables.phase == 2: player.phase2('player1')
                elif global_variables.phase == 3: player.phase3('player1')

                if global_variables.phase == 4:
                    for bot, who in bots:
                        game_over = bot.move(who, player_hex=player.my_hex)
                        if game_over:
                            break
                    global_variables.phase = 1
                if player.my_hex_count()==0 or player.check_bot() == False: game_over=True

        if game_over:
            all_hexs = len([cell for row in board.hexagons for cell in row if cell!=False])
            table = {'игроки': [who for bot, who in bots],
                     'кол. клеток': [len(bot.my_hex) for bot, who in bots],
                     'кол. клеток в %': [f"{'{:.2f}'.format(100 * len(bot.my_hex) / all_hexs)} %" for bot, who in bots]}
            
            table = pd.DataFrame(table, index=range(1, len(bots)+1))
            table.sort_values(by='кол. клеток', ascending=False, inplace=True)
            table.index = range(1, len(bots)+1)
            print(f'ТАБЛИЦА ИГРОКОВ: \n {table.head()}')
            game_over_scr = True
            only_bots = False
            game_over = False


        if game_over_scr:
            if table.loc[1, 'кол. клеток']<=player.my_hex_count() and only_bots == False:
                winner = 'player1'
            else:
                winner = table.loc[1, 'игроки']
            game_over_screen.update(winner)

        elif only_bots:
            for bot, who in bots: 
                if bot.move(who, player_hex=player.my_hex) or time.time() - timer > 5:
                    game_over = True            
                    break

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    main()