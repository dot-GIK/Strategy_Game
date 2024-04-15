import math
import pygame
import random
from global_variables import color, phrases

class Board:
    '''
    Это Данила
    '''
    def __init__(self, screen: pygame.Surface, width: int, height: int) -> None:
        '''
        Input:
            screen - Основная поверхность(экран)
            width - Ширина экрана
            height - Высота экрана
        '''

        self.screen = screen
        self.width = width
        self.height = height
        self.side_length = 12 # Размер внутреннего шестиугольника
        self.edging_length = 20 # Размер внешнего шестиугольника

        self.row_hex = (height // 40) - (((height // 35) // 10) + 1) * 2
        self.col_hex = (width // 30) - (((width // 30) // 10) + 1) * 2
        print(self.row_hex)

        self.hex_width= self.edging_length * math.sqrt(3.5)
        self.hex_height = 2.2 * self.edging_length
        self.hexagons = [] # Содержит [[Центер каждого полигона: tuple, Очко: int, Кому этот полигон принадлежит={me, none, enemy}] * n]
        self.points = [] # Содержит [[Все точки внутреннего полигона: tuple, Все точки внешнего полигона: tuple] * n]
        self.amount = 0 # Количество полигонов на поле
        self.font = pygame.font.Font(None, 24) # Шрифт для цифр
        self.font_for_panel = pygame.font.Font('font/minecraft-ten-font-cyrillic.ttf', 18) # Шрифт для текста


    def create_points(self, center: tuple, radius: int, radius_edg: int, row_col) -> tuple[tuple, tuple]:
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
        self.points.append([points, points_edg, row_col])
    

    def map_of_hexagons(self) -> None:
        '''
        Создание точек, по которым будут строятся полигоны.
        '''

        destroyed_polygons = self.random_destruction()
        for row in range(self.row_hex):
            for col in range(self.col_hex):
                if (row, col) in destroyed_polygons:
                    continue
                self.amount += 1
                x = col * self.hex_width * 1
                y = row * self.hex_height + (col % 2) * self.hex_height / 2
                self.create_points((x + self.hex_width / 2, y + self.hex_height / 2), self.side_length, self.edging_length, (row, col))
                

    def random_destruction(self) -> list[tuple]:
        '''
        Рандомное удаление полигонов на карте.
        Output: Кортеж из позиций полигонов, которые будут удаленны
        '''

        return [(random.randint(0, self.row_hex), random.randint(0, self.col_hex)) for _ in range(100)]
    

    def draw_hexagon(self, who: str, position=None, click=False, start=False) -> None:
        '''
        Создание или изменение полигонов.
        Input:
            position - позиция(x,y) нажатие мыши
            click - нажатие кнопки мыши
            start - создание персонажей в начале игры
        '''

        if click or start:
            for i in range(len(self.hexagons)):
                if (self.hexagons[i][0][0]-20 <= position[0] <= self.hexagons[i][0][0]+20) and (self.hexagons[i][0][1]-20 <= position[1] <= self.hexagons[i][0][1]+20):
                    self.hexagons[i][1] += 1

                    number = self.font.render(f'{self.hexagons[i][1]}', 1, color['black'], None)
                    hex = pygame.draw.polygon(self.surf_map, color['blue'], self.points[i][0])
                    pygame.draw.polygon(self.surf_map, color['blue'], self.points[i][1], 1)

                    if self.hexagons[i][1] >= 10: self.surf_map.blit(number, (hex[0]+4, hex[1]+4))
                    else: self.surf_map.blit(number, (hex[0]+8, hex[1]+4))
                    self.screen.blit(self.surf_map, (0, 0))
                    self.hexagons[i][2] = who
                    break

                
    def create_map(self) -> None:
        '''
        Создание карты и панели в начале игры.
        '''

        # Создание точек полигонов
        self.map_of_hexagons()

        # Создание карты
        self.surf_map = pygame.Surface((self.width, self.height-80)) # Создание поверхности для карты

        for i in range(len(self.points)):
            number = self.font.render('0', 1, color['black'], None)
            hex = pygame.draw.polygon(self.surf_map, color['grey'], self.points[i][0])
            pygame.draw.polygon(self.surf_map, color['grey'], self.points[i][1], 1)

            self.surf_map.blit(number, (hex[0]+8, hex[1]+4))
            self.screen.blit(self.surf_map, (0, 0))
            self.hexagons.append([hex.center, 0, 'none']) 


        # Создание панели
        self.width_rect = 80 # Ширина панели
        self.width_small_rect = 10 # Ширина прямоугольников
        self.surf_panel = pygame.Surface((self.width, self.height)) # Создание поверхности для панели

        text = self.font_for_panel.render(phrases[1], 1, color['white'], None)
        pygame.draw.rect(self.surf_panel, color['red'], (0, 0, self.width, self.width_small_rect))
        pygame.draw.rect(self.surf_panel, color['blue'], (0, (self.width_rect - self.width_small_rect), self.width, self.width_small_rect))

        self.screen.blit(self.surf_panel, (0, self.height - self.width_rect))
        self.screen.blit(text, ((self.width // 2) - 145, self.height - 55))

    def create_panel(self, phase: int) -> None:
        '''
        Input:
            phase - Фаза хода игрока 1-5.
        '''

        text = self.font_for_panel.render(phrases[phase], 1, color['white'], None)
        self.screen.blit(self.surf_panel, (0, self.height - self.width_rect))

        # shift - Сдвиг текста.
        if phase in (1, 2): shift = 145
        elif phase == 3: shift = 110
        else: shift = 140
        self.screen.blit(text, ((self.width // 2) - shift, self.height - 55))