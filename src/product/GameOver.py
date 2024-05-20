import pygame
import os

from .board import Board

class GameOverScreen:
    def __init__(self, screen, width: int, height: int, board, fade_speed=5) -> None:
        self.board = board
        self.screen = screen
        self.fade_speed = fade_speed
        self.font_for_over = pygame.font.Font(os.path.abspath('src/font/minecraft-ten-font-cyrillic.ttf'), 18)
        self.alpha = 0

        # self.text = self.font_for_over.render("Game Over", True, (255, 255, 255))
        # self.text_rect = self.text.get_rect(center=self.screen.get_rect().center)
        # self.text_overlay = pygame.Surface(self.text.get_size(), pygame.SRCALPHA)
        # self.text_overlay.blit(self.text, (0, 0))

        self.overlay = pygame.Surface(screen.get_size())
        self.overlay.fill((0, 0, 0))

    def update(self, winner):
            text="WINNER: " + winner
            self.text2 = self.font_for_over.render(text, True, (255, 255, 255))
            self.text2_rect = self.text2.get_rect(center=self.screen.get_rect().center)
            self.text2_overlay = pygame.Surface(self.text2.get_size(), pygame.SRCALPHA)
            self.text2_overlay.blit(self.text2, (0, 0))

            if self.alpha < 255:
                self.alpha += self.fade_speed
                self.overlay.set_alpha(self.alpha)
            self.screen.blit(self.overlay, (0, 0))

            if self.alpha >= 128:
                text_alpha = (self.alpha - 128) * 2
                text_alpha = min(text_alpha, 255)
                self.text2_overlay.set_alpha(text_alpha)
                self.screen.blit(self.text2_overlay, self.text2_rect)

                # self.text_overlay.set_alpha(text_alpha)
                # self.screen.blit(self.text_overlay, self.text_rect)