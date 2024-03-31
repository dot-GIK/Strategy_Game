import pygame
from board import Board
from person import Person
pygame.init()

'''
PS: Над этим дерьмом работали: Данил, Гоша и Макс
'''

W = 1080
H = 500

sc = pygame.display.set_mode((W, H))
pygame.display.set_caption('Game')

FPS = 60
clock = pygame.time.Clock()

while True:   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    
    clock.tick(FPS)