import time
from pygame import Surface
from .person import Person
import random
from math import sqrt

class Bot(Person):
    def __init__(self, screen: Surface, width: int, height: int, board) -> None:
        super().__init__(screen, width, height, board)

    def phase2(self, who: str, attack_func):
        '''
        Фаза атаки (2)
        '''
        flag = True
        for row in range (self.board.row_hex):
            for col in range (self.board.col_hex):
                if (self.board.hexagons[row][col]!= False) and (self.board.hexagons[row][col].who_owns != who) and (self.board.hexagons[row][col].who_owns in  ['bot1', 'bot2', 'bot3', 'bot4','player1']):
                    flag = False

        if  flag: return True



        self.phase_gain_influence_points(who) # Из этой функции нам нужен self.points(Количество очков, которые мы можем распределить) и self.my_hex(В нем хранятся все клетки, которые принадлежат боту)
        self.bot_hexs = self.my_hex[:]


        
        
        print(f'БОТ - {who}')
        print(f'my_hex(1): {len(self.bot_hexs)}')
        for cell in self.bot_hexs:
            inner = False
            if cell == False: continue
            else: attack_func(cell)
            for neighbor in cell.neighbors:
                if neighbor.who_owns != who: break
            else: 
                inner = True
            if cell.num_of_points <= 1 or inner:
                self.bot_hexs.remove(cell)
        self.phase_gain_influence_points(who)
        print(f'self.points(1): {self.points}')


    def phase3(self, who: str, player_hex: list, distribution: str='regular'):
        '''
        Фаза распределения очков (3)
        '''
        self.phase_gain_influence_points(who)
        bot_cells = self.my_hex[:]

        
        # Принудительное распределение оставшихся очков.
        if self.points > 0 and len(bot_cells)>0:
            if distribution == 'regular':
                # Равномерное распределение оставшихся очков
                while self.points != 0:
                    for cell in bot_cells:
                        if self.points == 0: break
                        if cell.num_of_points + 1 == 16: continue
                        cell.num_of_points += 1
                        cell.draw_hexagon(who) 
                        self.points -= 1 

            elif distribution == 'random':
                # Рандомное распределение оставшихся очков
                timer = time.time()
                while self.points != 0:
                    if time.time() - timer > 0.1: break
                    idx = random.randint(0, len(bot_cells)-1)
                    cell = bot_cells[idx]

                    if cell.num_of_points + 1 == 16: continue
                    cell.num_of_points += 1
                    cell.draw_hexagon(who) 
                    self.points -= 1 
            
            elif distribution == 'closeness':
                # Усиление клеток, находящихся ближе всего к игроку
                while self.points != 0:
                    pl_cell = player_hex[0]

                    upgr_cells = set()
                    for cell in self.my_hex:
                        if len(upgr_cells) != 0.2*len(self.my_hex):
                            upgr_cells.add(cell)
            
            elif distribution == 'clever':

                necessary_cells = []
                secondary_cells = []
                bot_cells = []

                for row in range (self.board.row_hex):
                    for col in range (self.board.col_hex):
                        if self.board.hexagons[row][col]!= False and self.board.hexagons[row][col].who_owns == who:
                            bot_cells.append(self.board.hexagons[row][col])

                '''
                necessary_cells == [] здесь будут храниться клетки, которые граничат с противником
                secondary_cells == [] здесь будут храниться клетки, которые граничат с none
                bot_cells после циклов for здесь останутся только внутренние клетки
                '''

                for cell in bot_cells:
                    if cell == False: continue
                    else:
                        for neighbor in cell.neighbors:
                            if neighbor.who_owns != who and neighbor.who_owns != 'none': 
                                necessary_cells.append(cell)
                                bot_cells.remove(cell)
                                break

                for cell in bot_cells:
                    if cell == False: continue
                    else:
                        for neighbor in cell.neighbors:
                            if neighbor.who_owns != who: 
                                secondary_cells.append(cell)
                                bot_cells.remove(cell)
                                break

                #усиление клеток, находящихся рядом с противником
                timer = time.time()
                while self.points > 0 and necessary_cells != []:
                    if time.time() - timer > 0.1: break
                    for cell in necessary_cells:
                        if self.points == 0: break
                        if cell.num_of_points + 1 == 16: 
                            necessary_cells.remove(cell)
                            break
                        cell.num_of_points += 1
                        cell.draw_hexagon(who)
                        self.points -= 1

                #усиление клеток, находящихся рядом с пустыми клетками
                timer = time.time()
                while self.points > 0 and secondary_cells != []:
                    if time.time() - timer > 0.1: break
                    for cell in secondary_cells:
                        if self.points == 0: break
                        if cell.num_of_points + 1 == 16: 
                            secondary_cells.remove(cell)
                            break
                        cell.num_of_points += 1
                        cell.draw_hexagon(who)
                        self.points -= 1

                #усиление клеток, находящихся "внутри"
                timer = time.time()
                while self.points > 0 and bot_cells != []:
                    if time.time() - timer > 0.1: break
                    for cell in bot_cells:
                        if self.points == 0: break
                        if cell.num_of_points + 1 == 16: 
                            bot_cells.remove(cell)
                            break
                        cell.num_of_points += 1
                        cell.draw_hexagon(who)
                        self.points -= 1
                

        print(f'self.points(3): {self.points}')
        print(f'my_hex(2): {len(bot_cells)} \n')


    def prob_of_capture(self, invader, victim):
        '''
        Добавление и отрисовка новой(захваченной) клетки 
        Input:
            invader - захватчик, та клетка которая нападает на другую 
            victim - жертва, та клетка на которую нападают
        '''
        # Проверяем кому принадлежит наша victim(жертва) и в завистмости от этого переопределяем её очки
        if victim.who_owns == 'none':
            victim.num_of_points = invader.num_of_points - 1
            self.bot_hexs.append(victim)
            self.points += 1 
            victim.draw_hexagon(invader.who_owns)
        else:
            if invader.num_of_points - victim.num_of_points >= 2:
                victim.num_of_points = invader.num_of_points - victim.num_of_points
                self.bot_hexs.append(victim)
                self.points += 1 
                victim.draw_hexagon(invader.who_owns)

            elif invader.num_of_points == victim.num_of_points:
                if random.choices([True, False], weights=[50, 50])[0]:
                    self.bot_hexs.append(victim)
                    self.points += 1
                    victim.draw_hexagon(invader.who_owns)
                else:
                    victim.num_of_points = 1
                    victim.draw_hexagon(victim.who_owns)

            elif invader.num_of_points - victim.num_of_points == 1:
                if random.choices([True, False], weights=[75, 25])[0]:
                    self.bot_hexs.append(victim)
                    self.points += 1   
                    victim.draw_hexagon(invader.who_owns)
                else:
                    victim.num_of_points = invader.num_of_points - victim.num_of_points
                    victim.draw_hexagon(victim.who_owns)

            elif invader.num_of_points - victim.num_of_points == -1:
                if random.choices([True, False], weights=[25, 75])[0]:
                    self.bot_hexs.append(victim)
                    self.points += 1   
                    victim.draw_hexagon(invader.who_owns)
                else:
                    victim.num_of_points = victim.num_of_points - invader.num_of_points
                    victim.draw_hexagon(victim.who_owns)

            elif invader.num_of_points - victim.num_of_points == -2:
                victim.num_of_points = 1
                victim.draw_hexagon(victim.who_owns)
                
        invader.num_of_points = 1 # После атаки у invader(захватчик) автоматически количество очков равно 1
        invader.draw_hexagon(invader.who_owns)
    

    def cell_capture(self, cell, neighbor):
        '''
        Захват клетки
        Input:
            cell - захватчик
            neighbor - жертва
        '''
        self.prob_of_capture(cell, neighbor)
        

class RedBotRandom(Bot):
    def __init__(self, screen: Surface, width: int, height: int, board) -> None:
        super().__init__(screen, width, height, board)

    def attack_func(self, cell):
        cell_points = cell.num_of_points # очки на выбранном гексе до атаки
        cell_neighbours = cell.neighbors # соседи этого гекса
        for neighbor in cell_neighbours: # Проходимся по соседям клетки
            if cell_points > 1: 
                if neighbor.who_owns != cell.who_owns:
                    if neighbor.amt_of_points == []: continue
                    self.cell_capture(cell, neighbor)
                    break
            else: break
 
    def move(self, who: str, player_hex: list):
        game_over = self.phase2(who, self.attack_func)
        if game_over: return game_over
        self.phase3(who, player_hex, distribution='random')


class GreenBot(Bot):
    def __init__(self, screen: Surface, width: int, height: int, board) -> None:
        super().__init__(screen, width, height, board)

    def attack_func(self, cell):
        cell_points = cell.num_of_points # очки на выбранном гексе до атаки
        cell_neighbours = cell.neighbors # соседи этого гекса
        enemy_cells = []
        attack_cell = cell
        min_dist = [10**20, attack_cell]
        the_smallest_dist = [10**20, attack_cell]
 

        for row in range (self.board.row_hex):
            for col in range (self.board.col_hex):
                if (self.board.hexagons[row][col]!= False) and (self.board.hexagons[row][col].who_owns != cell.who_owns) and (self.board.hexagons[row][col].who_owns != 'none'):
                    enemy_cells.append(self.board.hexagons[row][col])


        for neighbor in cell_neighbours: # Проходимся по соседям клетки
            if cell_points > 1:
                if len(neighbor.hexagon_center) < 2: continue
                for enemy_cell in enemy_cells:         #dist = sqrt((x2-x1)**2-(y2-y1)**2)
                    if neighbor != False and enemy_cell != False and enemy_cell.who_owns != cell.who_owns and sqrt((neighbor.hexagon_center[0]-enemy_cell.hexagon_center[0])**2 + (neighbor.hexagon_center[1]-enemy_cell.hexagon_center[1])**2) < min_dist[0] :
                        min_dist = [sqrt((neighbor.hexagon_center[0]-enemy_cell.hexagon_center[0])**2 + (neighbor.hexagon_center[1]-enemy_cell.hexagon_center[1])**2), neighbor]
                if min_dist[1].amt_of_points != [] and min_dist[0] < the_smallest_dist[0]:
                    the_smallest_dist = min_dist
            else: break
        
        self.cell_capture(cell, the_smallest_dist[1])
  

    def move(self, who: str, player_hex: list):
        game_over = self.phase2(who, self.attack_func)
        if game_over: return game_over
        self.phase3(who, player_hex, distribution='clever')


class YellowBot(Bot):
    def __init__(self, screen: Surface, width: int, height: int, board) -> None:
        super().__init__(screen, width, height, board)

    def attack_func(self, cell):
        cell_points = cell.num_of_points # очки на выбранном гексе до атаки
        cell_neighbours = cell.neighbors # соседи этого гекса
        enemy_cells = []
        attack_cell = cell
        min_dist = [10**20, attack_cell]
        the_biggest_dist = [0, attack_cell]

        for row in range (self.board.row_hex):
            for col in range (self.board.col_hex):
                if (self.board.hexagons[row][col]!= False) and (self.board.hexagons[row][col].who_owns != cell.who_owns) and (self.board.hexagons[row][col].who_owns != 'none'):
                    enemy_cells.append(self.board.hexagons[row][col])


        for neighbor in cell_neighbours: # Проходимся по соседям клетки
            if cell_points > 1:
                if len(neighbor.hexagon_center) < 2: continue
                for enemy_cell in enemy_cells:
                    if (neighbor != False)  and  (enemy_cell != False)  and  (enemy_cell.who_owns != cell.who_owns)  and  (sqrt((neighbor.hexagon_center[0]-enemy_cell.hexagon_center[0])**2 + (neighbor.hexagon_center[1]-enemy_cell.hexagon_center[1])**2) < min_dist[0]) :
                        min_dist = [sqrt((neighbor.hexagon_center[0]-enemy_cell.hexagon_center[0])**2 + (neighbor.hexagon_center[1]-enemy_cell.hexagon_center[1])**2), neighbor]
                if min_dist[1].amt_of_points != [] and min_dist[0] > the_biggest_dist[0]:
                    the_biggest_dist = min_dist
            else: break
        self.cell_capture(cell, the_biggest_dist[1])
  

    def move(self, who: str, player_hex: list):
        game_over = self.phase2(who, self.attack_func)
        if game_over: return game_over
        self.phase3(who, player_hex, distribution='clever')


class PurpleBot(Bot):
    def __init__(self, screen: Surface, width: int, height: int, board) -> None:
        super().__init__(screen, width, height, board)

    def attack_func(self, cell):
        cell_points = cell.num_of_points # очки на выбранном гексе до атаки
        cell_neighbours = cell.neighbors # соседи этого гекса
        enemy_cells = []
        attack_cell = cell
        min_dist = [10**20, attack_cell]
        the_smallest_dist = [10**20, attack_cell]
 

        for row in range (self.board.row_hex):
            for col in range (self.board.col_hex):
                if (self.board.hexagons[row][col]!= False) and (self.board.hexagons[row][col].who_owns != cell.who_owns) and (self.board.hexagons[row][col].who_owns != 'none'):
                    enemy_cells.append(self.board.hexagons[row][col])


        for neighbor in cell_neighbours: # Проходимся по соседям клетки
            if cell_points > 1:
                if len(neighbor.hexagon_center) < 2: continue
                for enemy_cell in enemy_cells:         #dist = sqrt((x2-x1)**2-(y2-y1)**2)
                    if neighbor != False and enemy_cell != False and enemy_cell.who_owns != cell.who_owns and sqrt((neighbor.hexagon_center[0]-enemy_cell.hexagon_center[0])**2 + (neighbor.hexagon_center[1]-enemy_cell.hexagon_center[1])**2) < min_dist[0] :
                        min_dist = [sqrt((neighbor.hexagon_center[0]-enemy_cell.hexagon_center[0])**2 + (neighbor.hexagon_center[1]-enemy_cell.hexagon_center[1])**2), neighbor]
                if min_dist[1].amt_of_points != [] and min_dist[0] < the_smallest_dist[0]:
                    the_smallest_dist = min_dist
            else: break
        
        self.cell_capture(cell, the_smallest_dist[1])
  

    def move(self, who: str, player_hex: list):
        game_over = self.phase2(who, self.attack_func)
        if game_over: return game_over
        self.phase3(who, player_hex, distribution='random')


class RedBotClever(Bot):
    def __init__(self, screen: Surface, width: int, height: int, board) -> None:
        super().__init__(screen, width, height, board)

    def attack_func(self, cell):
        cell_points = cell.num_of_points # очки на выбранном гексе до атаки
        cell_neighbours = cell.neighbors # соседи этого гекса
        for neighbor in cell_neighbours: # Проходимся по соседям клетки
            if cell_points > 1: 
                if neighbor.who_owns != cell.who_owns:
                    if neighbor.amt_of_points == []: continue
                    self.cell_capture(cell, neighbor)
                    break
            else: break
 
    def move(self, who: str, player_hex: list):
        game_over = self.phase2(who, self.attack_func)
        if game_over: return game_over
        self.phase3(who, player_hex, distribution='clever')
