import os
import pygame
from .global_variables import color
from .panel import Panel


class Button(Panel):
    def __init__(self, screen, surf_panel, width: int, height: int) -> None:
        super().__init__(screen, width, height, surf_panel)
        
    def draw_button(self, phase: int, num_of_points='-'):
        '''
        Отрисовка кнопки
        Input:
            phase - Фаза, от нее зависит, что будет показываться на кнопке: '-' - (1,2,3,5); 'num_of_points' - (4).
            num_of_points - Количество очков, которые можно распределить по полю.
        '''
        pygame.draw.circle(self.screen, color['blue'], (self.width-100, self.height-40), 26, 7)

        number = self.font_for_panel.render(f'{num_of_points}', 1, color['white'], None)
        if phase == 4:
            if num_of_points >= 10: self.screen.blit(number, (self.width-112, self.height-55))
            else: self.screen.blit(number, (self.width-106, self.height-56))
        else: self.screen.blit(number, (self.width-105, self.height-55))