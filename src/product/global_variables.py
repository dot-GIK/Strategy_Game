'''
Глобальные переменные.
    color - Цвета
    characters - состояния персонажа
    phrases - Набор фраз.
'''

color = {'black': (0, 0, 0), 'grey': (105, 105, 105), 'red': (255, 0, 0), 'blue': (0,0,255), 'white': (255,255,255), 'bright_blue': (28, 170, 214), 'green': (0, 128, 0), 'yellow': (255,255,0), 'purple': (240, 230, 140)}
whose_color = {'player1': color['blue'], 'none': color['grey'], 'bot1': color['red'], 'bot2': color['green'], 'bot3': color['yellow'], 'bot4': color['purple']}
phrases = {1: 'Коснитесь вашей клетки', 2: 'Атакуйте соседнюю клетку', 3: 'Завершите атаку', 4: 'Усильте свои клетки', 5: 'Ожидайте свой ход'}
phase = 1
