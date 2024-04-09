import math
import pygame
import random

class Board:
    '''
    Это Данила
    '''
    def __init__(self, screen: pygame.Surface, color: dict) -> None:
        self.screen = screen
        self.side_length = 12 # Размер внутреннего шестиугольника
        self.edging_length = 20 # Размер внешнего шестиугольника
        self.row_hex = 15
        self.col_hex = 28
        self.color = color
        self.hex_width= self.edging_length * math.sqrt(3.5)
        self.hex_height = 2.2 * self.edging_length
        self.hexagons = [] # Содержит [[Центер каждого полигона: tuple, Очко: int, Кому этот полигон принадлежит={my, none, enemy}] * n]
        self.points = [] # Содержит [[Все точки внутреннего полигона: tuple, Все точки внешнего полигона: tuple] * n]
        self.num = 0
        self.font = pygame.font.Font(None, 24)


    def create_points(self, center: int, radius: int, radius_edg: int) -> tuple[tuple, tuple]:
        '''
        Создание точек, по которым будут строятся полигоны.
        points - Точки внутреннего полигона
        points - Точки внешнего полигона

        Output: Кортеж из всех точек полигонов 
        '''

        points = []
        points_edg = []
        for i in range(6):
            x = center[0] + radius * math.cos(math.pi/3 * i) + 15
            y = center[1] + radius * math.sin(math.pi/3 * i) + 20
            x_edg = center[0] + radius_edg * math.cos(math.pi/3 * i) + 15
            y_edg = center[1] + radius_edg * math.sin(math.pi/3 * i) + 20
            points.append((x, y))
            points_edg.append((x_edg, y_edg))
        self.points.append([points, points_edg])
    

    def map_of_hexagons(self) -> None:
        destroyed_polygons = self.random_destruction()
        for row in range(self.row_hex):
            for col in range(self.col_hex):
                if (row, col) in destroyed_polygons:
                    continue
                x = col * self.hex_width * 1
                y = row * self.hex_height + (col % 2) * self.hex_height / 2
                self.create_points((x + self.hex_width / 2, y + self.hex_height / 2), self.side_length, self.edging_length)
                

    def random_destruction(self) -> list[tuple]:
        '''
        Рандомное удаление полигонов на карте.
        Output: Кортеж из позиций полигонов, которые будут удаленны
        '''

        return [(random.randint(0, self.row_hex), random.randint(0, self.col_hex)) for _ in range(100)]
    

    def draw_hexagon(self, position=None, click=False, start=False) -> None:
        '''
        Создание или изменение полигонов.
        Input:
            position - позиция(x,y) нажатие мыши
            click - нажатие кнопки мыши
        '''

        if click == True or start == True:
            for i in range(len(self.hexagons)):
                if (self.hexagons[i][0][0]-20 <= position[0] <= self.hexagons[i][0][0]+20) and (self.hexagons[i][0][1]-20 <= position[1] <= self.hexagons[i][0][1]+20) and self.hexagons[i][2] != 'enemy':
                    self.hexagons[i][1] += 1

                    number = self.font.render(f'{self.hexagons[i][1]}', 1, (0,0,0), None)
                    hex = pygame.draw.polygon(self.screen, self.color['blue'], self.points[i][0])
                    pygame.draw.polygon(self.screen, self.color['blue'], self.points[i][1], 1)

                    if self.hexagons[i][1] >= 10: self.screen.blit(number, (hex[0]+4, hex[1]+4))
                    else: self.screen.blit(number, (hex[0]+8, hex[1]+4))
                    self.hexagons[i][2] = 'my'
                    break
        else:
            '''
            Создание карты в начале игры.
            '''

            for i in range(len(self.points)):
                number = self.font.render('0', 1, (0,0,0), None)
                hex = pygame.draw.polygon(self.screen, self.color['grey'], self.points[i][0])
                pygame.draw.polygon(self.screen, self.color['grey'], self.points[i][1], 1)
                self.screen.blit(number, (hex[0]+8, hex[1]+4))
