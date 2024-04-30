import math
import pygame
import random
from .global_variables import color
from .cell import Cell
from .panel import Panel

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
            side_length - Размер внутреннего шестиугольника
            edging_length - Размер внешнего шестиугольника
            row_hex - Количество полигонов в ширину
            col_hex - Количество полигонов в высоту
            amount - Количество полигонов на поле
            hexagons - Матрица хранящая все полигоны поля 
            panel - Панель в нижней части экрана

            surf_map - Создание поверхности для карты
            surf_panel - Создание поверхности для панели
        '''

        self.screen = screen
        self.width = width
        self.height = height
        self.side_length = 12 
        self.edging_length = 20

        self.row_hex = (height // 40) - (((height // 35) // 10) + 1) * 2
        self.col_hex = (width // 30) - (((width // 30) // 10) + 1) * 2

        self.hex_width = self.edging_length * math.sqrt(3.5)
        self.hex_height = 2.2 * self.edging_length
        self.amount = 0 

        surf_map = pygame.Surface((self.width, self.height-80)) 
        surf_panel = pygame.Surface((self.width, self.height))

        # Матрица которая хранит все полигоны
        # Если полигон существует, то создается объект класса Cell, в ином случае Falls.
        self.hexagons = [] 
        for row in range(self.row_hex): 
            self.hexagons.append([])
            for col in range(self.col_hex): 
                cell = Cell(surf_map=surf_map, screen=screen, who_owns='none', num_of_points=0, position_in_matrix=(row, col))
                self.hexagons[row].append(cell)      

        self.panel = Panel(screen=screen, width=width, height=height, surf_panel=surf_panel)  



    def creating_hexagon_points(self, center: tuple, radius: int, radius_edg: int) -> tuple[tuple, tuple]:
        '''
        Создание точек, по которым будет строиться полигон.
        points - Точки внутреннего полигона
        points_edg - Точки внешнего полигона

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
        return points, points_edg
    

    def creating_hexagons_points(self) -> None:
        '''
        Создание точек, по которым будут строятся полигоны.
        '''

        for row in range(self.row_hex):
            for col in range(self.col_hex):
                if self.hexagons[row][col] == False: continue
                self.amount += 1

                x = col * self.hex_width * 1
                y = row * self.hex_height + (col % 2) * self.hex_height / 2

                points, points_edg = self.creating_hexagon_points((x + self.hex_width / 2, y + self.hex_height / 2), self.side_length, self.edging_length)
                hexagon_center = pygame.draw.polygon(self.screen, color['grey'], points).center

                self.hexagons[row][col].hexagon_center = (hexagon_center[0]-4, hexagon_center[1]-7) 
                self.hexagons[row][col].amt_of_points = [points, points_edg]
                

    def random_destruction(self):
        '''
        Рандомное удаление полигонов на карте.
        '''

        destroyed_hexagons = [(random.randint(0, self.row_hex-1), random.randint(0, self.col_hex-1)) for _ in range(150)]
        for row, col in destroyed_hexagons:
            self.hexagons[row][col] = False


    def creating_neighbors(self):
        for row in range(self.row_hex):
            for col in range(self.col_hex):
                count = 0
                if self.hexagons[row][col] == False: continue
                if (col+1) % 2 != 0:
                    if 0 < row < (self.row_hex-1):
                        if col != 0:
                            if self.hexagons[row][col-1] != False: 
                                self.hexagons[row][col].neighbors.append(self.hexagons[row][col-1])
                                count += 1    
                            if self.hexagons[row-1][col-1] != False: 
                                self.hexagons[row][col].neighbors.append(self.hexagons[row-1][col-1])
                                count += 1 
                        if col != (self.col_hex-1):
                            if self.hexagons[row][col+1] != False: 
                                self.hexagons[row][col].neighbors.append(self.hexagons[row][col+1])
                                count += 1
                            if self.hexagons[row-1][col+1] != False: 
                                self.hexagons[row][col].neighbors.append(self.hexagons[row-1][col+1])
                                count += 1  
                        if self.hexagons[row-1][col] != False: 
                            self.hexagons[row][col].neighbors.append(self.hexagons[row-1][col])
                            count += 1                       
                        if self.hexagons[row+1][col] != False: 
                            self.hexagons[row][col].neighbors.append(self.hexagons[row+1][col])
                            count += 1        
                    elif row == 0:
                        if col != 0:
                            if self.hexagons[row][col-1] != False: 
                                self.hexagons[row][col].neighbors.append(self.hexagons[row][col-1])
                                count += 1  
                        if col != (self.col_hex-1):
                            if self.hexagons[row][col+1] != False: 
                                self.hexagons[row][col].neighbors.append(self.hexagons[row][col+1])
                                count += 1 
                        if self.hexagons[row+1][col] != False: 
                            self.hexagons[row][col].neighbors.append(self.hexagons[row+1][col])
                            count += 1 
                    else:
                        if col != 0:
                            if self.hexagons[row][col-1] != False: 
                                self.hexagons[row][col].neighbors.append(self.hexagons[row][col-1])
                                count += 1    
                            if self.hexagons[row-1][col-1] != False: 
                                self.hexagons[row][col].neighbors.append(self.hexagons[row-1][col-1])
                                count += 1 
                        if col != (self.col_hex-1):
                            if self.hexagons[row][col+1] != False: 
                                self.hexagons[row][col].neighbors.append(self.hexagons[row][col+1])
                                count += 1
                            if self.hexagons[row-1][col+1] != False: 
                                self.hexagons[row][col].neighbors.append(self.hexagons[row-1][col+1])
                                count += 1  
                        if self.hexagons[row-1][col] != False: 
                            self.hexagons[row][col].neighbors.append(self.hexagons[row-1][col])
                            count += 1   
                elif (col+1) % 2 == 0:
                    if 0 < row < (self.row_hex-1):
                        if col != 0:
                            if self.hexagons[row][col-1] != False: 
                                self.hexagons[row][col].neighbors.append(self.hexagons[row][col-1])
                                count += 1    
                            if self.hexagons[row+1][col-1] != False: 
                                self.hexagons[row][col].neighbors.append(self.hexagons[row+1][col-1])
                                count += 1 
                        if col != (self.col_hex-1):
                            if self.hexagons[row][col+1] != False: 
                                self.hexagons[row][col].neighbors.append(self.hexagons[row][col+1])
                                count += 1
                            if self.hexagons[row+1][col+1] != False: 
                                self.hexagons[row][col].neighbors.append(self.hexagons[row+1][col+1])
                                count += 1  
                        if self.hexagons[row-1][col] != False: 
                            self.hexagons[row][col].neighbors.append(self.hexagons[row-1][col])
                            count += 1                       
                        if self.hexagons[row+1][col] != False: 
                            self.hexagons[row][col].neighbors.append(self.hexagons[row+1][col])
                            count += 1    
                    elif row == 0:
                        if col != 0:
                            if self.hexagons[row][col-1] != False: 
                                self.hexagons[row][col].neighbors.append(self.hexagons[row][col-1])
                                count += 1  
                            if self.hexagons[row+1][col-1] != False: 
                                self.hexagons[row][col].neighbors.append(self.hexagons[row+1][col-1])
                                count += 1  
                        if col != (self.col_hex-1):
                            if self.hexagons[row][col+1] != False: 
                                self.hexagons[row][col].neighbors.append(self.hexagons[row][col+1])
                                count += 1 
                            if self.hexagons[row+1][col+1] != False: 
                                self.hexagons[row][col].neighbors.append(self.hexagons[row+1][col+1])
                                count += 1 
                        if self.hexagons[row+1][col] != False: 
                            self.hexagons[row][col].neighbors.append(self.hexagons[row+1][col])
                            count += 1 
                    else:
                        if col != 0:
                            if self.hexagons[row][col-1] != False: 
                                self.hexagons[row][col].neighbors.append(self.hexagons[row][col-1])
                                count += 1    
                        if col != (self.col_hex-1):
                            if self.hexagons[row][col+1] != False: 
                                self.hexagons[row][col].neighbors.append(self.hexagons[row][col+1])
                                count += 1 
                        if self.hexagons[row-1][col] != False: 
                            self.hexagons[row][col].neighbors.append(self.hexagons[row-1][col])
                            count += 1  
                if 0 <= count <= 2: 
                    self.hexagons[row][col] = False 
                print(row, ' ', col, '=', count)


    def draw_hexagon(self, who_owns: str, position: tuple[int, int]) -> None:
        '''
        Создание или изменение полигонов.
        Input:
            position - позиция(x,y) нажатие мыши
        '''

        for row in range(self.row_hex):
            for col in range(self.col_hex):
                if self.hexagons[row][col] == False: continue
                if (self.hexagons[row][col].hexagon_center[0]-20 <= position[0] <= self.hexagons[row][col].hexagon_center[0]+20) and (self.hexagons[row][col].hexagon_center[1]-20 <= position[1] <= self.hexagons[row][col].hexagon_center[1]+20):
                    print(len(self.hexagons[row][col].neighbors))
                    self.hexagons[row][col].draw_hexagon(who_owns)
                    print(f'Полигон: {row}, {col}')

                
    def creating_map(self) -> None:
        '''
        Создание карты и панели в начале игры.
        '''
        # Рандомное удаление полигонов
        self.random_destruction()

        # Привязка соседей к полигону 
        self.creating_neighbors()

        # Создание точек полигонов
        self.creating_hexagons_points()

        # Создание карты
        for row in range(self.row_hex):
            for col in range(self.col_hex):
                if self.hexagons[row][col] == False: continue
                self.hexagons[row][col].draw_hexagon()

        # Создание панели
        self.panel.draw_panel(1)
