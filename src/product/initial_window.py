import pygame
import os
from .global_variables import whose_color

class InitialWindow:
    def __init__(self, screen, width, height, board, fade_speed: int=5) -> None:
        self.screen = screen
        self.width = width
        self.height = height
        self.fade_speed = fade_speed
        self.alpha = 0
        self.only_bots = None

        # Шрифты для тестов
        self.font = pygame.font.Font(os.path.abspath('src/font/minecraft-ten-font-cyrillic.ttf'), 22)
        self.font_modes = pygame.font.Font(os.path.abspath('src/font/minecraft-ten-font-cyrillic.ttf'), 16)

        # Главное окно начального экрана
        self.window = pygame.Surface([self.width, self.height], pygame.SRCALPHA)
        self.window_rect = self.window.get_rect()
        self.window_center = self.window_rect.center
        self.x = self.window_center[0]
        self.y = self.window_center[0]

        # Перекрывающая поверхность
        self.overlay = pygame.Surface(screen.get_size())
        self.overlay.fill((0, 0, 0))
        
        # Текст
        self.modes = self.font.render("ВЫБОР РЕЖИМА", True, (66,170,255))
        self.choose_bots = self.font.render("ВЫБЕРИТЕ БОТОВ", True, (227,38,54))
        self.standard_mode = self.font_modes.render("ОБЫЧНЫЙ РЕЖИМ", True, (255,255,255))
        self.mode_only_bots = self.font_modes.render("БИТВА БОТОВ", True, (255,255,255))
        self.bot1_txt = self.font_modes.render("BOT1", True, (0,0,0))
        self.bot2_txt = self.font_modes.render("BOT2", True, (0,0,0))
        self.bot3_txt = self.font_modes.render("BOT3", True, (0,0,0))
        self.bot4_txt = self.font_modes.render("BOT4", True, (0,0,0))
        self.start = self.font.render("START", True, (255,255,255))

        # Поверхность для текста
        self.modes_surf = pygame.Surface(self.modes.get_size(), pygame.SRCALPHA)
        self.choose_bots_surf = pygame.Surface(self.choose_bots.get_size(), pygame.SRCALPHA)
        self.standard_mode_surf = pygame.Surface(self.standard_mode.get_size(), pygame.SRCALPHA)
        self.mode_only_bots_surf = pygame.Surface(self.mode_only_bots.get_size(), pygame.SRCALPHA)
        self.start_surf = pygame.Surface(self.start.get_size(), pygame.SRCALPHA)
        self.start_surf.set_alpha(128)
        
        # Список со всеми выбранными ботами
        self.bots = []

        # Кружки с ботами(внутренние)
        self.bot1_crl = pygame.draw.circle(self.window, [255,255,255], [self.x-210, self.y-10], 50)
        pygame.draw.circle(self.window, whose_color['bot1'], [self.x-210, self.y-10], 50, 10)
        self.bot2_crl = pygame.draw.circle(self.window, [255,255,255], [self.x-70, self.y-10], 50)
        pygame.draw.circle(self.window, whose_color['bot2'], [self.x-70, self.y-10], 50, 10)
        self.bot3_crl = pygame.draw.circle(self.window, [255,255,255], [self.x+70, self.y-10], 50)
        pygame.draw.circle(self.window, whose_color['bot3'], [self.x+70, self.y-10], 50, 10)
        self.bot4_crl = pygame.draw.circle(self.window, [255,255,255], [self.x+210, self.y-10], 50)
        pygame.draw.circle(self.window, whose_color['bot4'], [self.x+210, self.y-10], 50, 10)
        self.bots_center = {'bot1': self.bot1_crl.center, 'bot2': self.bot2_crl.center,
                            'bot3': self.bot3_crl.center, 'bot4': self.bot4_crl.center}


    def update(self, position: tuple, mode: str):
        x = self.window_center[0]
        y = self.window_center[1]

        x_std, y_std = self.standard_mode.get_size()[0], self.standard_mode.get_size()[1]
        x_bot, y_bot = self.mode_only_bots.get_size()[0], self.mode_only_bots.get_size()[1]
        x_str, y_str = self.start.get_size()[0], self.start.get_size()[1]

        if x-95 <= position[0] <= x-95+x_std and y-130 <= position[1] <= y-130+y_std: # ОБЫЧНЫЙ РЕЖИМ
            if mode == 'buttondown': 
                self.blackout_text(self.standard_mode, self.standard_mode_surf)
                self.only_bots = False
        elif x-70 <= position[0] <= x-70+x_bot and y-105 <= position[1] <= y-105+y_bot: # БИТВА БОТОВ
            if mode == 'buttondown': 
                self.blackout_text(self.mode_only_bots, self.mode_only_bots_surf)
                self.only_bots = True

        elif x-210-50 <= position[0] <= x-210+50 and y+50 <= position[1] <= y+100+30: # bot1
            self.draw_circle('bot1', self.bot1_txt, self.bot1_crl.center)
            self.bots.append('bot1')
        elif x-70-50 <= position[0] <= x-70+50 and y+50 <= position[1] <= y+100+30: # bot2
            self.draw_circle('bot2', self.bot2_txt, self.bot2_crl.center)
            self.bots.append('bot2')
        elif x+70-50 <= position[0] <= x+70+50 and y+50 <= position[1] <= y+100+30: # bot3
            self.draw_circle('bot3',self.bot3_txt, self.bot3_crl.center)
            self.bots.append('bot3')
        elif x+210-50 <= position[0] <= x+210+50 and y+50 <= position[1] <= y+100+30: # bot4
            self.draw_circle('bot4',self.bot4_txt, self.bot4_crl.center)
            self.bots.append('bot4')

        elif x-50 <= position[0] <= x-50+x_str and y+180 <= position[1] <= y+180+y_str: # bot4
            return False


    def appearance_window(self): 
        if self.alpha < 255:
            self.alpha += self.fade_speed
        self.screen.blit(self.overlay, (0, 0))

        if self.alpha >= 128:
            text_alpha = (self.alpha - 128) * 2
            text_alpha = min(text_alpha, 255)
            self.window.set_alpha(text_alpha)
            self.window.blit(self.modes, [self.window_center[0]-115, self.window_center[1]-200])
            self.window.blit(self.choose_bots, [self.window_center[0]-125, self.window_center[1]-40])
            self.window.blit(self.standard_mode, [self.window_center[0]-95, self.window_center[1]-130])
            self.window.blit(self.mode_only_bots, [self.window_center[0]-70, self.window_center[1]-105])
            self.window.blit(self.bot1_txt, [self.bot1_crl.center[0]-24, self.bot1_crl.center[1]-13])
            self.window.blit(self.bot2_txt, [self.bot2_crl.center[0]-24, self.bot1_crl.center[1]-13])
            self.window.blit(self.bot3_txt, [self.bot3_crl.center[0]-24, self.bot1_crl.center[1]-13])
            self.window.blit(self.bot4_txt, [self.bot4_crl.center[0]-24, self.bot1_crl.center[1]-13])
            self.window.blit(self.start, [self.window_center[0]-50, self.window_center[1]+180])
            self.screen.blit(self.window, (0, 0))


    def draw_data(self, dataset, text_alpha: int=255):
        self.window.set_alpha(text_alpha)
        for data in dataset:
            if data in [self.modes, self.modes_surf]:
                self.window.blit(data, [self.window_center[0]-115, self.window_center[1]-200])
            elif data in [self.standard_mode, self.standard_mode_surf]:
                self.window.blit(data, [self.window_center[0]-95, self.window_center[1]-130])
            elif data in [self.mode_only_bots, self.mode_only_bots_surf]:
                self.window.blit(data, [self.window_center[0]-70, self.window_center[1]-105])
            elif data == 'bot1':
                self.window.blit(data, [self.window_center[0], self.window_center[1]])
        self.screen.blit(self.window, (0, 0))


    def blackout_text(self, text: pygame.Surface, surf: pygame.Surface):
        surf.fill((0,0,0))
        text.set_alpha(128)
        self.draw_data(dataset=[surf, text])
        self.screen.blit(self.window, (0, 0))


    def draw_circle(self, who: str, text: str, srf):
        pygame.draw.circle(self.window, (128,128,128), self.bots_center[who], 50)
        pygame.draw.circle(self.window, whose_color[who], self.bots_center[who], 50, 10)
        self.window.blit(text, [srf[0]-24, srf[1]-13])
        self.screen.blit(self.window, (0, 0))


    def get_bots(self):
        return self.bots
    

    def get_mode(self):
        return self.only_bots