import pygame
from product import color, whose_color


class Cell:
    def __init__(self, screen, surf_map, who_owns: str, num_of_points: int, position_in_matrix: tuple[int]) -> None:
        '''
        Класс для создания полигона.
            who_owns - Кому принадлежит этот полигон.
            num_of_points - Количество очков полигона.
            position_in_matrix - Позиция занимаемая полигоном в матрице.
            hexagon_center - Координаты центра полигона.
            amt_of_points - Хранит точки для отрисовки полигона [[points, points_edg]].
            neighbors - Соседи данного полигона. 
            font - Шрифт для цифр.
        '''
        self.screen = screen
        self.surf_map = surf_map
        self.who_owns = who_owns
        self.num_of_points = num_of_points
        self.position_in_matrix = position_in_matrix
        self.hexagon_center = ()
        self.amt_of_points = []
        self.neighbors = []
        self.font = pygame.font.Font(None, 24) 

    def draw_hexagon(self, who_owns='none'):
        '''
        Отрисовка полигона.
        Input:
            who_owns - Персонаж, который совершает действие.
        '''

        number = self.font.render(f'{self.num_of_points}', 1, color['black'], None)
        pygame.draw.polygon(self.surf_map, whose_color[who_owns], self.amt_of_points[0])
        pygame.draw.polygon(self.surf_map, whose_color[who_owns], self.amt_of_points[1], 1)

        if self.num_of_points >= 10: self.surf_map.blit(number, (self.hexagon_center[0], self.hexagon_center[1]-10))
        else: self.surf_map.blit(number, (self.hexagon_center[0], self.hexagon_center[1]))
        self.screen.blit(self.surf_map, (0, 0))

        self.who_owns = who_owns