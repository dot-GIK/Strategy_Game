import os
import pygame
from .global_variables import color, phrases

class Panel:
    def __init__(self, screen: pygame.Surface, width: int, height: int, surf_panel: pygame.Surface) -> None:
        '''
        Класс для создания панели в нижней части экрана.
            width_rect - Ширина панели.
            width_small_rect - Ширина прямоугольников.
            font_for_panel - Шрифт для текста.
        '''

        self.screen = screen
        self.width = width
        self.height = height
        self.surf_panel = surf_panel
        self.width_rect = 80
        self.width_small_rect = 10 
        self.font_for_panel = pygame.font.Font(os.path.abspath('src/font/minecraft-ten-font-cyrillic.ttf'), 18)

    def draw_panel(self, phase: int) -> None:
        '''
        Отрисовка панели.
        Input:
            phase - Фаза текста (1-5).
        '''

        text = self.font_for_panel.render(phrases[phase], 1, color['white'], None)
        pygame.draw.rect(self.surf_panel, color['red'], (0, 0, self.width, self.width_small_rect))
        pygame.draw.rect(self.surf_panel, color['blue'], (0, (self.width_rect - self.width_small_rect), self.width, self.width_small_rect))

        self.screen.blit(self.surf_panel, (0, self.height - self.width_rect))
        self.screen.blit(text, ((self.width // 2) - 145, self.height - 55))