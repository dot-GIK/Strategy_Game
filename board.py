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
        self.hexagons = [] 
        self.font = pygame.font.Font(None, 24)

    def draw_hexagon(self, center: int, radius: int, radius_edg: int) -> tuple[tuple, tuple]:
        points = []
        points_edg = []
        for i in range(6):
            x = center[0] + radius * math.cos(math.pi/3 * i) + 15
            y = center[1] + radius * math.sin(math.pi/3 * i) + 20
            x_edg = center[0] + radius_edg * math.cos(math.pi/3 * i) + 15
            y_edg = center[1] + radius_edg * math.sin(math.pi/3 * i) + 20
            points.append((x, y))
            points_edg.append((x_edg, y_edg))
        number = self.font.render('0', 1, (0,0,0), None)
        hex = pygame.draw.polygon(self.screen, self.color['grey'], points)
        hex_edg = pygame.draw.polygon(self.screen, self.color['grey'], points_edg, 1)
        self.screen.blit(number, (hex[0]+8, hex[1]+4))
        return (hex, hex_edg)
    
    def map_of_hexagons(self) -> None:
        destroyed_polygons = self.random_destruction()
        for row in range(self.row_hex):
            for col in range(self.col_hex):
                if (row, col) in destroyed_polygons:
                    continue
                x = col * self.hex_width * 1
                y = row * self.hex_height + (col % 2) * self.hex_height / 2
                hexs = self.draw_hexagon((x + self.hex_width / 2, y + self.hex_height / 2), self.side_length, self.edging_length)
                self.hexagons.append([(row, col), hexs])

    def random_destruction(self) -> list[tuple]:
        return [(random.randint(0, self.row_hex), random.randint(0, self.col_hex)) for i in range(100)]
    
