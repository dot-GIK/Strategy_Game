from math import *
import pygame
import random
from board import Board
from global_variables import color, characters

class Person:
    '''
    Это Макса
    '''
    def __init__(self, screen: pygame.Surface) -> None:
        '''
        board - карта, на которой все происходит
        phase - всего есть три фазы:
            1) Нажатие на клетку, которой совершаем ход
            2) Распределение очков
            3) Атака или распространение
        '''
        
        self.board = Board(screen)
        self.phase = 0 

    def advance_phase(self) -> None:
        self.phase += 1
        print('Phase:', self.phase)

    def execute_phase(self, who: str) -> None:
        if self.phase == 1:
            self.phase_attack(who, clicked_position=pygame.mouse.get_pos())
            self.phase_gain_influence_points()
        if self.phase == 2:
            self.phase_distribute_influence_points()
            self.phase = 0

    def phase_attack(self, who: str, clicked_position=None) -> None:
        '''
        Фаза атаки: атакуем и захватываем полигон, на который кликнули мышью, если у нашего полигона больше одного очка.
        '''
        # Проходим по всем полигонам на доске
        for i in range(len(self.board.hexagons)):
            # Получаем центр текущего полигона
            hex_center = self.board.hexagons[i][0]
            # Вычисляем расстояние от центра текущего полигона до позиции, на которую кликнули мышью
            distance =  sqrt(abs(hex_center[0] - clicked_position[0]) ** 2 + abs(hex_center[1] - clicked_position[1]) ** 2)
            # Если расстояние меньше определенного порога (например, 20 пикселей), это означает, что мы кликнули на этот полигон
            if distance < 50:
                # Проверяем, принадлежит ли полигон текущему игроку и имеет ли он больше одного очка!
                if self.board.hexagons[i][2] == characters[1] and self.board.hexagons[i][1] > 1 and self.board.hexagons[i][1] > 1:
                    self.board.draw_hexagon(who, position=clicked_position, click=True)
                    # Проходим по всем полигонам еще раз
                    for j in range(len(self.board.hexagons)):
                        # Если соседний полигон принадлежит противнику, захватываем его
                        if i != j and ((self.board.hexagons[i][0][0] - self.board.hexagons[j][0][0]) ** 2 + (
                                self.board.hexagons[i][0][1] - self.board.hexagons[j][0][1]) ** 2) ** 0.5 <= 30:
                            # Устанавливаем захваченный полигон в качестве нашего и увеличиваем количество очков на 1
                            self.board.draw_hexagon(who, position=clicked_position, click=True)
                            return

    def phase_gain_influence_points(self) -> None:
        '''
        Фаза получения очков усиления: количество очков зависит от числа подконтрольных гексов.
        '''
        points = 0
        for i in range(len(self.board.hexagons)):
            if self.board.hexagons[i][2] == characters[1]:
                points+=1
        print('Points:', points)

    def phase_distribute_influence_points(self) -> None:
        '''
        Фаза распределения очков усиления между подконтрольными гексами.
        '''
        for i in range(len(self.board.hexagons)):
            if self.board.hexagons[i][2] == characters[1]:
                self.board.hexagons[i][1] += 1

    def random_capture(self, who: str) -> None:
        '''
        Рандомный захват одного полигона на старте игры.
        '''

        # Генерируем случайный индекс полигона
        self.board.map_of_hexagons()
        self.board.create_map()
        random_index = random.randint(0, self.board.amount)
        # Получаем координаты центра захватываемого полигона
        position = self.board.hexagons[random_index][0]
        # Устанавливаем цвет полигона как синий (0, 0, 255), чтобы подсветить его
        self.board.hexagons[random_index][1] = 1
        self.board.draw_hexagon(who, position, start=True)
