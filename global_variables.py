'''
Глобальные переменные.
    color - Цвета
    characters - состояния персонажа
    phrases - Набор фраз.
'''

color = {'black': (0, 0, 0), 'grey': (105, 105, 105), 'red': (255, 0, 0), 'blue': (0,0,255), 'white': (255,255,255)}
phrases = {1: 'Коснитесь вашей клетки', 2: 'Атакуйте соседнюю клетку', 3: 'Завершите атаку', 4: 'Усильте свои клетки', 5: 'Ожидайте свой ход'}
characters = {1: 'me', 2: 'none', 3: 'enemy', 4: 'empty'}