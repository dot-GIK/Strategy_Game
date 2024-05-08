from math import *
import pygame
import random
from .board import Board
from .panel import Panel
from .button import Button


class Person():
    '''
    Это Макса
    '''

    def __init__(self, screen: pygame.Surface, width: int, height: int) -> None:
        '''
        board - карта, на которой все происходит
        phase - всего есть три фазы:
            1) Нажатие на клетку, которой совершаем ход
            2) Атака
            3) Распределение
        '''

        self.board = Board(screen, width, height)
        self.board.creating_map()  # Создание поля
        self.phase = 0
        self.but_x = width-100 #центр кнопки по оси абсцисс
        self.but_y = height-40 #центр по оси ординат

    def advance_phase(self) -> None: #фактическое переключение фазы
        self.phase += 1
        print('Phase:', self.phase)

    def execute_phase(self, who: str) -> None: #Реализация фазы

        if self.phase == 1:  # Выбор гекса
            self.hex_x=0
            self.hex_y=0
            print('Выделите гекс')
            clicked_position = pygame.mouse.get_pos() #Считывание позиции мыши
            self.board.panel.draw_panel(2) #Рисуем панель
            self.choose_hex(who, clicked_position=pygame.mouse.get_pos()) #Функция выбора Гекса
            self.board.button.draw_button(1) #Рисуем кнопку для переключения фазы
            distance = sqrt(abs(self.but_x - clicked_position[0]) ** 2 + abs(self.but_y - clicked_position[1]) ** 2) #Дистанция от мыши до кнопки
            if distance <= 32: #Если кликнули по кнопке, то переходим к распределению очков
                self.phase_gain_influence_points() #Функция начисления очков
                self.phase = 2
                self.board.panel.draw_panel(2)
                self.board.button.draw_button(4, num_of_points=self.points) #Рисуем кнопку с очками

        if self.phase == 2:  # Атака
            self.board.panel.draw_panel(4)
            print('Атакуйте')
            clicked_position = pygame.mouse.get_pos()
            self.phase_attack(who, clicked_position) #ФАЗА АТАААКИ ТИТАНОВ
            distance=sqrt(abs(self.but_x - clicked_position[0]) ** 2 + abs(self.but_y- clicked_position[1]) ** 2)
            if distance>32:
                self.phase = 0
                self.board.panel.draw_panel(1)
                self.board.button.draw_button(1)
            if distance <= 32:
                self.phase_gain_influence_points()
                self.board.panel.draw_panel(4)
                self.board.button.draw_button(4, num_of_points=self.points)

        if self.phase > 2:  # Распределение очков
            print('Распределите очки', self.points)
            clicked_position = pygame.mouse.get_pos()

            if self.points>0:
                distance = sqrt(abs(self.but_x - clicked_position[0]) ** 2 + abs(self.but_y - clicked_position[1]) ** 2)
                if distance > 32:
                    self.phase_distribute_influence_points(who, clicked_position=pygame.mouse.get_pos())
                    self.board.panel.draw_panel(4)
                    self.board.button.draw_button(4, num_of_points=self.points)
                if distance <= 32:
                    self.board.button.draw_button(1)
                    self.phase=0
                    self.board.panel.draw_panel(1)
            if self.points==0:
                self.phase = 0
                self.board.panel.draw_panel(1)
    def choose_hex(self, who: str, clicked_position=None) -> None: #ФАЗА ВЫБОРА ГЕКСАГОНА
        for row in range(self.board.row_hex):
            for col in range(self.board.col_hex):
                if self.board.hexagons[row][col] == False: continue
                else:
                    hex_center = self.board.hexagons[row][col].hexagon_center #Считаем центр гекса
                    if self.board.hexagons[row][col].who_owns == 'player1' and sqrt(abs(hex_center[0] - clicked_position[0]) ** 2 + abs(
                            hex_center[1] - clicked_position[1]) ** 2) <= 20:
                        self.hex_y = hex_center[1]
                        self.hex_x = hex_center[0]
                        print('Выделен:', self.hex_x, self.hex_y)
                        break
        if self.hex_x==0 and self.hex_y==0:
                self.phase = 0
                self.board.panel.draw_panel(1)
                self.board.button.draw_button(1)

    def phase_attack(self, who: str, clicked_position=None) -> None:
        '''
        Фаза атаки: атакуем и захватываем полигон, на который кликнули мышью, если у нашего полигона больше одного очка.
        '''
        for row in range(self.board.row_hex):
            for col in range(self.board.col_hex):
                if self.board.hexagons[row][col] == False: continue
                # Вычисляем расстояние от центра текущего полигона до позиции, на которую кликнули мышью
                distance = sqrt(abs(self.hex_x - clicked_position[0]) ** 2 + abs(self.hex_y - clicked_position[1]) ** 2)
                if distance < 65 and self.hex_x == self.board.hexagons[row][col].hexagon_center[0] and self.hex_y == self.board.hexagons[row][col].hexagon_center[1]:
                    # Проверяем, принадлежит ли полигон текущему игроку и имеет ли он больше одного очка!!!!
                    if self.board.hexagons[row][col].who_owns == 'player1' and self.board.hexagons[row][col].num_of_points > 1:
                        me_hex = (self.hex_x, self.hex_y)
                        first_points=self.board.hexagons[row][col].num_of_points
                        self.board.hexagons[row][col].num_of_points = 1
                        for row in range(self.board.row_hex):
                            for col in range(self.board.col_hex):
                                if self.board.hexagons[row][col] == False: continue
                                if sqrt(abs(self.board.hexagons[row][col].hexagon_center[0] - clicked_position[0]) ** 2 + abs(self.board.hexagons[row][col].hexagon_center[1] - clicked_position[1]) ** 2) <= 20 and self.board.hexagons[row][col].who_owns == 'none':
                                    self.board.hexagons[row][col].num_of_points = first_points-1
                                    print(first_points, 'FIRST')
                        who_owns=who
                        self.board.draw_hexagon(who_owns, position=clicked_position)
                        # for row in range(self.board.row_hex):
                        #     for col in range(self.board.col_hex):
                        #         if self.board.hexagons[row][col] == False: continue
                        #         if self.hex_x == self.board.hexagons[row][col].hexagon_center[0] and self.hex_y == self.board.hexagons[row][col].hexagon_center[1]:
                        #             self.board.hexagons[row][col].num_of_points == 1

                        self.board.draw_hexagon(who_owns, position=me_hex)

                        # Проходим по всем полигонам еще раз
                        # for row in range(self.board.row_hex):
                        #     for col in range(self.board.col_hex):
                        #         if self.board.hexagons[row][col] == False: continue
                        #             # (ТУТ ДОЛЖНА БЫТЬ ТАКТИКА)
                        #             if ((self.board.hexagons[i][0][0] - self.board.hexagons[j][0][0]) ** 2 + (
                        #                     self.board.hexagons[i][0][1] - self.board.hexagons[j][0][1]) ** 2) ** 0.5 <= 30:
                        #                 # Устанавливаем захваченный полигон в качестве нашего и увеличиваем количество очков на 1
                        #                 self.board.draw_hexagon(who, position=clicked_position)
                        #                 return

    def phase_gain_influence_points(self) -> None:
        '''
        Фаза получения очков усиления: количество очков зависит от числа подконтрольных гексов.
        '''
        self.points = 0
        for row in range(self.board.row_hex):
            for col in range(self.board.col_hex):
                if self.board.hexagons[row][col] == False: continue
                if self.board.hexagons[row][col].who_owns == 'player1':
                    self.points += 1
        print('У вас:', self.points, 'очков')

    def phase_distribute_influence_points(self, who: str, clicked_position=None) -> None:
        '''
        Фаза распределения очков усиления между подконтрольными гексами.
        '''
        for row in range(self.board.row_hex):
            for col in range(self.board.col_hex):
                if self.board.hexagons[row][col] == False: continue
                distance = sqrt(abs(self.board.hexagons[row][col].hexagon_center[0] - clicked_position[0]) ** 2 + abs(self.board.hexagons[row][col].hexagon_center[1] - clicked_position[1]) ** 2)
                if self.board.hexagons[row][col].who_owns == 'player1' and distance < 20:
                    self.board.hexagons[row][col].num_of_points+=1
                    self.board.draw_hexagon(who, position=clicked_position)
                    self.points -= 1
                    print(self.points, "UPDATE POINTS")

    def random_capture(self, who: str) -> None:
        '''
        Рандомный захват одного полигона на старте игры.
        '''
        row, col = random.randint(0, self.board.row_hex-1), random.randint(0, self.board.col_hex-1)
        if self.board.hexagons[row][col] == False:
            while self.board.hexagons[row][col] == False:
                row, col = random.randint(0, self.board.row_hex-1), random.randint(0, self.board.col_hex-1)

        position = self.board.hexagons[row][col].hexagon_center
        self.board.hexagons[row][col].num_of_points = 2
        self.board.draw_hexagon(who, position)