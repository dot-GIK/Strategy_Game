from pygame import Surface
from .person import Person
import random

class Bot(Person):
    def __init__(self, screen: Surface, width: int, height: int, board) -> None:
        super().__init__(screen, width, height, board)

    def phase2(self, who: str, attack_func):
        '''
        Фаза атаки (2)
        '''
        self.new_hexs = [] # В нем будут храниться все новые захваченные клетки
        self.phase_gain_influence_points(who) # Из этой функции нам нужен self.points(Количество очков, которые мы можем распределить) и self.my_hex(В нем хранятся все клетки, которые принадлежат боту)
        print(f'my_hex(1): {len(self.my_hex)}')
        for cell in self.my_hex:
            if cell == False: continue
            else: attack_func(cell)   
        print(f'self.points(1): {self.points}')

    def phase3(self, who: str, player_hex: list, distribution: str='regular'):
        '''
        Фаза распределения очков (3)
        '''
        if len(self.my_hex) > 0: #грубо говоря, проверяем, что клетки бота существуют, то есть его пока не победили
            while self.points > 0: 
                for cell in self.new_hexs: 
                    # Добавление новых(захваченных) клеток в наш основной массив self.my_hex
                    if self.points > 0 and cell.amt_of_points != [] and cell.num_of_points + 1 != 16: 
                        if cell not in self.my_hex: self.my_hex.append(cell) 
                        cell.num_of_points += 1
                        cell.draw_hexagon(who) 
                        self.points -= 1              
                print(f'self.points(2): {self.points}')
                break
        
        # Принудительное распределение оставшихся очков.
        if self.points > 0:
            if distribution == 'regular':
                # Равномерное распределение оставшихся очков
                while self.points != 0:
                    for cell in self.my_hex:
                        if self.points == 0: break
                        if cell.num_of_points + 1 == 15: continue
                        cell.num_of_points += 1
                        cell.draw_hexagon(who) 
                        self.points -= 1 

            elif distribution == 'random':
                # Рандомное распределение оставшихся очков
                while self.points != 0:
                    idx = random.randint(0, len(self.my_hex)-1)
                    cell = self.my_hex[idx]

                    if cell.num_of_points + 1 == 15: continue
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

        print(f'self.points(3): {self.points}')
        print(f'my_hex(2): {len(self.my_hex)}')

    def add_new_cell(self, invader, victim):
        '''
        Добавление и отрисовка новой(захваченной) клетки 
        Input:
            invader - захватчик, та клетка которая нападает на другую 
            victim - жертва, та клетка на которую нападают
        '''

        # Проверяем кому принадлежит наша victim(жертва) и в завистмости от этого переопределяем её очки
        if victim.who_owns == 'none':
            victim.num_of_points = invader.num_of_points - 1
        else:
            if invader.num_of_points == victim.num_of_points:
                victim.num_of_points = 1
            else:
                victim.num_of_points = abs(invader.num_of_points - victim.num_of_points)

        invader.num_of_points = 1 # После атаки у invader(захватчик) автоматически количество очков равно 1
        self.new_hexs.append(victim)
        self.points += 1 
        invader.draw_hexagon(invader.who_owns)
        victim.draw_hexagon(invader.who_owns)

    def prob_of_capture(self, cell_1, cell_2):
        '''
        Вероятность захвата клетки
        Output:
            Возвращает список: [победитель, проигравший]
        '''
        if max(cell_1.num_of_points, cell_2.num_of_points) == cell_1.num_of_points:
            members = [cell_1, cell_2]
        else:
            members = [cell_2, cell_1]
        
        # Разница в 2 очка
        if abs(cell_1.num_of_points - cell_2.num_of_points) >= 2:  
            return members    
        # Разница в 1 очка
        elif abs(cell_1.num_of_points - cell_2.num_of_points) == 1:
            winner = random.choices(members, weights=[75, 25])[0]  
        # Разница в 0 очка
        else:
            winner = random.choices(members, weights=[50, 50])[0]

        members.remove(winner)
        loser = members[0]
        return winner, loser

    def cell_capture(self, cell, neighbor):
        '''
        Захват клетки
        Input:
            cell - захватчик
            neighbor - жертва
        '''
        winner, loser = self.prob_of_capture(cell, neighbor)
        self.add_new_cell(winner, loser)
        

class RedBot(Bot):
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
        self.phase2(who, self.attack_func)
        self.phase3(who, player_hex, distribution='random')


class GreenBot(Bot):
    def __init__(self, screen: Surface, width: int, height: int, board) -> None:
        super().__init__(screen, width, height, board)

    def attack_func(self, who: str):
        pass

    def move(self, who: str):
        self.phase2(who, self.attack_func)
        self.phase3(who, distribution='random')


class YellowBot(Bot):
    def __init__(self, screen: Surface, width: int, height: int, board) -> None:
        super().__init__(screen, width, height, board)

    def attack_func(self, who: str):
        pass

    def move(self, who: str):
        self.phase2(who, self.attack_func)
        self.phase3(who, distribution='random')