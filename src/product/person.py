from math import *
import pygame
import random
from .global_variables import color, phrases
from .board import Board


class Person:
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

    def advance_phase(self) -> None:
        self.phase += 1
        print('Phase:', self.phase)

    def execute_phase(self, who: str) -> None:
        if self.phase == 1:  # Выбор гекса
            print('Выделите гекс')
            self.board.panel.draw_panel(2)
            self.choose_hex(who, clicked_position=pygame.mouse.get_pos())
        if self.phase == 2:  # Атака
            self.board.panel.draw_panel(4)
            print('Атакуйте')
            self.phase_attack(who, clicked_position=pygame.mouse.get_pos())
            self.phase_gain_influence_points()
        if self.phase > 2:  # Распределение очков
            print('Распределите очки')
            self.phase_distribute_influence_points(who, clicked_position=pygame.mouse.get_pos())
            if self.points == 0:
                self.phase = 0
                self.board.panel.draw_panel(1)

    def choose_hex(self, who: str, clicked_position=None) -> None:
        for i in range(len(self.board.hexagons)):
            hex_center = self.board.hexagons[i][0]
            if who == 'me' and sqrt(abs(hex_center[0] - clicked_position[0]) ** 2 + abs(
                    hex_center[1] - clicked_position[1]) ** 2) <= 20:
                self.hex_y = hex_center[1]
                self.hex_x = hex_center[0]
                print('Выделен:', self.hex_x, self.hex_y)

    def phase_attack(self, who: str, clicked_position=None) -> None:
        '''
        Фаза атаки: атакуем и захватываем полигон, на который кликнули мышью, если у нашего полигона больше одного очка.
        '''
        for i in range(len(self.board.hexagons)):
            # Вычисляем расстояние от центра текущего полигона до позиции, на которую кликнули мышью
            distance = sqrt(abs(self.hex_x - clicked_position[0]) ** 2 + abs(self.hex_y - clicked_position[1]) ** 2)
            if distance < 50 and self.hex_x == self.board.hexagons[i][0][0] and self.hex_y == self.board.hexagons[i][0][
                1]:
                # Проверяем, принадлежит ли полигон текущему игроку и имеет ли он больше одного очка!!!!
                if self.board.hexagons[i][2] == 'player1' and self.board.hexagons[i][1] > 1 and \
                        self.board.hexagons[i][1] > 1:
                    me_hex = (self.hex_x, self.hex_y)
                    self.board.draw_hexagon(who, position=clicked_position)
                    for l in range(len(self.board.hexagons)):
                        if self.hex_x == self.board.hexagons[l][0][0] and self.hex_y == self.board.hexagons[l][0][1]:
                            self.board.hexagons[l][1] -= 2
                    self.board.draw_hexagon(who, position=me_hex)

                    # Проходим по всем полигонам еще раз
                    for j in range(len(self.board.hexagons)):
                        # (ТУТ ДОЛЖНА БЫТЬ ТАКТИКА)
                        if i != j and ((self.board.hexagons[i][0][0] - self.board.hexagons[j][0][0]) ** 2 + (
                                self.board.hexagons[i][0][1] - self.board.hexagons[j][0][1]) ** 2) ** 0.5 <= 30:
                            # Устанавливаем захваченный полигон в качестве нашего и увеличиваем количество очков на 1
                            self.board.draw_hexagon(who, position=clicked_position)
                            return

    def phase_gain_influence_points(self) -> None:
        '''
        Фаза получения очков усиления: количество очков зависит от числа подконтрольных гексов.
        '''
        self.points = 0
        for i in range(len(self.board.hexagons)):
            if self.board.hexagons[i][2] == 'player1':
                self.points += 1
        print('У вас:', self.points, 'очков')

    def phase_distribute_influence_points(self, who: str, clicked_position=None) -> None:
        '''
        Фаза распределения очков усиления между подконтрольными гексами.
        '''
        for i in range(len(self.board.hexagons)):
            # Вычисляем расстояние от центра текущего полигона до позиции, на которую кликнули мышью
            distance = sqrt(abs(self.board.hexagons[i][0][0] - clicked_position[0]) ** 2 + abs(
                self.board.hexagons[i][0][1] - clicked_position[1]) ** 2)
            if distance < 20 and self.board.hexagons[i][2] == 'player1':
                self.board.draw_hexagon(who, position=clicked_position)
                self.points -= 1
                print(self.points)

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