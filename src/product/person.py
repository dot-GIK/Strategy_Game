from math import *
import pygame
import random
from .board import Board
from src.product import global_variables


class Person():
    '''
    Это Макса
    '''

    def __init__(self, screen: pygame.Surface, width: int, height: int, board) -> None:
        '''
        board - карта, на которой все происходит
        phase - всего есть три фазы:
            1) Нажатие на клетку, которой совершаем ход
            2) Атака
            3) Распределение
        '''
        self.board=board
        self.my_hex = []  #Мои гексы
        self.but_x = width-100 #центр кнопки по оси абсцисс
        self.but_y = height-40 #центр по оси ординат


    def phase1(self, who: str) -> None: #Обобщенная фаза выбора гекса

        # print('ФАЗА 1')
        self.choose_hex(who, clicked_position=pygame.mouse.get_pos()) #Функция выбора Гекса

        self.f_button('player1', 1)

    def phase2(self, who: str) -> None: #Обобщенная фаза атаки
        if who == 'player1':
            clicked_position = pygame.mouse.get_pos()

        self.phase_attack(who, clicked_position) #ФАЗА АТАААКИ ТИТАНОВ
        self.f_button('player1', 2)



    def phase3(self, who:str):  # Распределение очков
        self.f_button('player1', 3)


    def choose_hex(self, who: str, clicked_position=None) -> None: #ФАЗА ВЫБОРА ГЕКСАГОНА
        self.hex_x = 0
        self.hex_y = 0
        for row in range(self.board.row_hex):
            for col in range(self.board.col_hex):
                if self.board.hexagons[row][col] == False: continue
                else:
                    hex_center = self.board.hexagons[row][col].hexagon_center #Считаем центр гекса
                    if self.board.hexagons[row][col].who_owns == who and sqrt(abs(hex_center[0] - clicked_position[0]) ** 2 + abs(
                            hex_center[1] - clicked_position[1]) ** 2) <= 20 and self.board.hexagons[row][col].num_of_points >= 2:
                        self.hex_y = hex_center[1]
                        self.hex_x = hex_center[0]
                        self.player_choose = self.board.hexagons[row][col]
                        global_variables.phase = 2
                        break
        if self.hex_x==0 and self.hex_y==0:
            global_variables.phase = 1

    def phase_attack(self, who: str, clicked_position=None) -> None:
        '''
        Фаза атаки: атакуем и захватываем полигон, на который кликнули мышью, если у нашего полигона больше одного очка.
        '''
                # Вычисляем расстояние от центра текущего полигона до позиции, на которую кликнули мышью
        distance = sqrt(abs(self.hex_x - clicked_position[0]) ** 2 + abs(self.hex_y - clicked_position[1]) ** 2)
        if distance < 65:
            # Проверяем, принадлежит ли полигон текущему игроку и имеет ли он больше одного очка!!!!
                me_hex = (self.hex_x, self.hex_y)
                for row in range(self.board.row_hex):
                    for col in range(self.board.col_hex):
                        if self.board.hexagons[row][col] == False: continue
                        distance2 = sqrt(abs(self.board.hexagons[row][col].hexagon_center[0] - clicked_position[0]) ** 2 + abs(self.board.hexagons[row][col].hexagon_center[1] - clicked_position[1]) ** 2) <= 20
                        if (self.board.hexagons[row][col].who_owns=='player1') and distance2 and self.board.hexagons[row][col]!=self.player_choose:
                            print("По своему кликнул")
                            self.board.hexagons[row][col].num_of_points += self.player_choose.num_of_points - 2
                            self.player_choose.num_of_points = 1
                            self.board.hexagons[row][col].who_owns='player1'
                            self.board.draw_hexagon(who, position=clicked_position)
                            self.board.draw_hexagon(who, position=me_hex)

                        if distance2 and (self.board.hexagons[row][col].who_owns == 'none' or self.board.hexagons[row][col].num_of_points == 0):
                            print("Пустой")
                            self.board.hexagons[row][col].num_of_points += self.player_choose.num_of_points - 1
                            self.player_choose.num_of_points = 1
                            self.board.hexagons[row][col].who_owns = 'player1'
                            if who == 'player1': self.my_hex.append(self.board.hexagons[row][col])
                            self.board.draw_hexagon(who, position=clicked_position)
                            self.board.draw_hexagon(who, position=me_hex)

                        #БОЙ С БОТОМ
                        if distance2 and (self.board.hexagons[row][col].num_of_points>0 or (self.board.hexagons[row][col].who_owns != 'player1' and self.board.hexagons[row][col].who_owns != 'none')) and self.board.hexagons[row][col].who_owns != 'player1':
                            bot = self.board.hexagons[row][col]
                            print("Рубеж Пройден")

                            if (self.player_choose.num_of_points - bot.num_of_points)>=2:
                                print("Больше 2х очков")
                                bot.num_of_points=self.player_choose.num_of_points - bot.num_of_points
                                self.player_choose.num_of_points = 1
                                bot.who_owns='player1'
                                self.my_hex.append(bot)
                                self.board.draw_hexagon('player1', position=clicked_position, sel_hex=False)
                                self.board.draw_hexagon('player1', position=self.player_choose.hexagon_center, sel_hex=False)
                            if (self.player_choose.num_of_points - bot.num_of_points)==1:
                                print("+1 очко")
                                if random.choices([True, False], weights=[75, 25])[0]:
                                    bot.num_of_points=1
                                    self.player_choose.num_of_points = 1
                                    bot.who_owns='player1'
                                    self.my_hex.append(bot)
                                    self.board.draw_hexagon('player1', position=clicked_position, sel_hex=False)
                                    self.board.draw_hexagon('player1', position=self.player_choose.hexagon_center, sel_hex=False)
                                else:
                                    self.player_choose.num_of_points = 1
                                    self.board.draw_hexagon('player1', position=self.player_choose.hexagon_center, sel_hex=False)
                            if (self.player_choose.num_of_points - bot.num_of_points)==0:
                                print("0 очков")
                                if random.choices([True, False], weights=[50, 50])[0]:
                                    bot.num_of_points=1
                                    self.player_choose.num_of_points = 1
                                    bot.who_owns='player1'
                                    self.my_hex.append(bot)
                                    self.board.draw_hexagon('player1', position=clicked_position, sel_hex=False)
                                    self.board.draw_hexagon('player1', position=self.player_choose.hexagon_center, sel_hex=False)
                                else:
                                    self.player_choose.num_of_points = 1
                                    self.board.draw_hexagon('player1', position=self.player_choose.hexagon_center, sel_hex=False)
                            if (self.player_choose.num_of_points - bot.num_of_points)==-1:
                                print("-1 очко")
                                if random.choices([True, False], weights=[25, 75])[0]:
                                    bot.num_of_points=1
                                    self.player_choose.num_of_points = 1
                                    bot.who_owns='player1'
                                    self.my_hex.append(bot)
                                    self.board.draw_hexagon('player1', position=clicked_position, sel_hex=False)
                                    self.board.draw_hexagon('player1', position=self.player_choose.hexagon_center, sel_hex=False)
                                else:
                                    self.player_choose.num_of_points = 1
                                    self.board.draw_hexagon('player1', position=self.player_choose.hexagon_center, sel_hex=False)
                            if (self.player_choose.num_of_points - bot.num_of_points)<=-2:
                                print("-2 очка")
                                self.player_choose.num_of_points = 1
                                self.board.draw_hexagon('player1', position=self.player_choose.hexagon_center, sel_hex=False)


                        if self.board.hexagons[row][col]==self.player_choose:
                            print('Выбор игрока')
                            self.board.draw_hexagon(who, position=self.player_choose.hexagon_center, sel_hex=False)
        if distance>=65:
            print('Дистанция велика')
            self.board.draw_hexagon(who, position=(self.hex_x, self.hex_y), sel_hex=False)

        for row in range(self.board.row_hex):
            for col in range(self.board.col_hex):
                if self.board.hexagons[row][col] == False: continue
                if self.board.hexagons[row][col].who_owns == who and self.board.hexagons[row][col].num_of_points == 0:
                    self.board.hexagons[row][col].num_of_points=1
                    position = self.board.hexagons[row][col].hexagon_center
                    self.board.draw_hexagon(who, position)



    def phase_gain_influence_points(self, who) -> None:
        '''
        Фаза получения очков усиления: количество очков зависит от числа подконтрольных гексов.
        '''
        self.points = 0
        if who in ['bot1', 'bot2', 'bot3', 'bot4', 'bot5']: 
            self.my_hex = []
        for row in range(self.board.row_hex):
            for col in range(self.board.col_hex):
                if self.board.hexagons[row][col] == False: continue
                if self.board.hexagons[row][col].who_owns == who:
                    self.points += 1
                    if who in ['bot1', 'bot2', 'bot3', 'bot4', 'bot5'] and self.board.hexagons[row][col] not in self.my_hex:
                        self.my_hex.append(self.board.hexagons[row][col])

    def phase_distribute_influence_points(self, who: str, clicked_position=None) -> None:
        '''
        Фаза распределения очков усиления между подконтрольными гексами.
        '''
        for row in range(self.board.row_hex):
            for col in range(self.board.col_hex):
                if self.board.hexagons[row][col] == False: continue
                distance = sqrt(abs(self.board.hexagons[row][col].hexagon_center[0] - clicked_position[0]) ** 2 + abs(self.board.hexagons[row][col].hexagon_center[1] - clicked_position[1]) ** 2)
                if self.board.hexagons[row][col].who_owns == who and distance < 20 and self.board.hexagons[row][col].num_of_points<15:
                    self.board.hexagons[row][col].num_of_points+=1
                    self.board.draw_hexagon(who, position=clicked_position)
                    self.points -= 1
    def random_capture(self, who: str) -> None:
        '''
        Рандомный захват одного полигона на старте игры.
        '''
        row, col = random.randint(0, self.board.row_hex-1), random.randint(0, self.board.col_hex-1)
        if self.board.hexagons[row][col] == False:
            while self.board.hexagons[row][col] == False:
                row, col = random.randint(0, self.board.row_hex-1), random.randint(0, self.board.col_hex-1)

        if who == 'player1': self.my_hex.append(self.board.hexagons[row][col])
        position = self.board.hexagons[row][col].hexagon_center
        self.board.hexagons[row][col].num_of_points = 2
        self.board.hexagons[row][col].who_owns = who
        self.board.draw_hexagon(who, position)

    def f_button(self, who, phase):
        if who=='player1':
            if phase==1:
                clicked_position = pygame.mouse.get_pos()
                if self.affiliation_check(who=who, position=clicked_position) and self.hex_x!=0 and self.hex_y!=0:
                    self.board.draw_hexagon(who_owns=who, position=clicked_position, sel_hex=True)
                if self.hex_x!=0 and self.hex_y!=0:
                    self.board.panel.draw_panel(2)  # Рисуем панель
                self.board.button.draw_button(1)  # Рисуем кнопку для переключения фазы
                distance = sqrt(abs(self.but_x - clicked_position[0]) ** 2 + abs(
                    self.but_y - clicked_position[1]) ** 2)  # Дистанция от мыши до кнопки
                if distance <= 32:  # Если кликнули по кнопке, то переходим к распределению очков
                    self.phase_gain_influence_points('player1')  # Функция начисления очков
                    global_variables.phase = 3
                    self.board.panel.draw_panel(4)
                    self.board.button.draw_button(4, num_of_points=self.points)  # Рисуем кнопку с очками
            if phase==2:
                count = 0
                for i in range(len(self.my_hex)):
                    if self.my_hex[i].num_of_points == 1:
                        count += 1
                clicked_position = pygame.mouse.get_pos()
                self.board.panel.draw_panel(4)
                # print('ФАЗА 2')
                distance = sqrt(abs(self.but_x - clicked_position[0]) ** 2 + abs(self.but_y - clicked_position[1]) ** 2)
                if distance > 32:
                    global_variables.phase = 1
                    self.board.panel.draw_panel(1)
                    self.board.button.draw_button(1)
                if distance <= 32 or len(self.my_hex)==count:
                    self.phase_gain_influence_points('player1')
                    self.board.panel.draw_panel(4)
                    self.board.button.draw_button(4, num_of_points=self.points)
                    global_variables.phase=3
            if phase==3:
                clicked_position = pygame.mouse.get_pos()
                if self.points > 0:
                    self.board.panel.draw_panel(4)
                    distance = sqrt(
                        abs(self.but_x - clicked_position[0]) ** 2 + abs(self.but_y - clicked_position[1]) ** 2)
                    if distance > 32:
                        self.phase_distribute_influence_points(who, clicked_position=pygame.mouse.get_pos())
                        self.board.panel.draw_panel(4)
                        self.board.button.draw_button(4, num_of_points=self.points)
                    if distance <= 32:
                        global_variables.phase = 4
                        self.board.panel.draw_panel(1)
                        self.board.button.draw_button(1)
                if self.points == 0:
                    global_variables.phase = 4
                    self.board.panel.draw_panel(1)
                    self.board.button.draw_button(1)

    def affiliation_check(self, who: str, position: tuple=None, coordinate_method: bool=True) -> bool:
        if coordinate_method:
            for row in range(self.board.row_hex):
                for col in range(self.board.col_hex):
                    if self.board.hexagons[row][col] == False: continue
    
                    if (self.board.hexagons[row][col].hexagon_center[0]-20 <= position[0] <= self.board.hexagons[row][col].hexagon_center[0]+20) and \
                    (self.board.hexagons[row][col].hexagon_center[1]-20 <= position[1] <= self.board.hexagons[row][col].hexagon_center[1]+20):
                        return who == self.board.hexagons[row][col].who_owns

    def my_hex_count(self):
        player_hex = 0
        for row in range(self.board.row_hex):
            for col in range(self.board.col_hex):
                if self.board.hexagons[row][col] == False:
                    continue
                else:
                    if self.board.hexagons[row][col].who_owns == 'player1':
                        player_hex += 1
        return player_hex