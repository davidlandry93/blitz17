from random import choice
from game import Game
from food import FoodFinder
import requests
from math import sqrt
from path_finder import find_path, direction

training_map = """################################C1    C2############F-            F-########  @1        @4  ######    []  B-B-  []    ####    ##  ####  ##    ####    ##  ####  ##    ####    []  B-B-  []    ######  @2        @3  ########F-            F-############C3    C4################################"""

pathfinding_url = 'http://game.blitz.codes:8081/pathfinding/direction'

# Here state is the string of the map.

#old version
# def pathfinding(state, start, target, size):
#     payload = {'map': state, 'size': size, 'start': '(' + str(start[0]) + ',' + str(start[1]) + ')', 'target': '(' + str(target[0]) + ',' + str(target[1]) + ')'}

#     print('calling pathfinder...')

#     response = requests.get(pathfinding_url, params=payload)

#     print('Reponse is: ' + str(response.json()))

    # try:
    #     direction = response.json()['direction']
    # except KeyError:
    #     direction = None
    # return direction

# AStar
def pathfinding(state, start, target, size):
    print('calling pathfinder...')
    direction_ = direction(find_path(Board({'size': size, 'tiles': state}), start, target))
    print('A Star returned ' + direction_)
    if direction_ == 'Stay':
        direction_ = choice(['North', 'South', 'East', 'West'])

    print('Reponse is: ' + direction_)
    return direction_


class Bot:
    pass


class NullJsBot(Bot):
    KILL_DISTANCE = 1

    def __init__(self):
        self.current_customer = None  # {'burger': 1, 'fries': 2}
        self.inventory = {'burger': 0, 'fries': 0}
        self.hero_pos = None
        self.food_finder = None
        self.game = None
        self.objectives = []
        self.customer_number = 0
        self.life = 0
        self.calorie = 0
        self.id = 0

    def move(self, state):
        self.game = Game(state)
        self.food_finder = FoodFinder(self.game)
        self.hero_pos = (state['hero']['pos']['x'], state['hero']['pos']['y'])
        self.life = state['hero']['life']
        self.calorie = state['hero']['calories']
        self.id = state['hero']['id']
        self.inventory['burger'] = state['hero']['burgerCount']
        self.inventory['fries'] = state['hero']['frenchFriesCount']

        self.current_customer = self.smallest_order(self.game)
        self.objectives = self.create_objective_list(self.current_customer)

        if self.life < 25 and self.calorie > 30 and len(self.objectives) > 1:
            self.objectives.insert(0, self.food_finder.get_closest_soda(self.hero_pos))

        self.maybe_kill_someone()

        objective = self.objectives[0]

        direction = None
        tries = 0

        while direction is None and tries < min(len(self.objectives), 1):
            direction = pathfinding(state['game']['board']['tiles'], self.hero_pos, self.objectives[tries], state['game']['board']['size'])
            tries += 1

        if direction is None:
            print('RANDOM MOVE')
            direction = choice(['North', 'South', 'East', 'West'])

        return direction

    def create_objective_list(self, customer):
        customer.loc = self.game.customers_locs[customer.id]
        objectives = []
        last_pos = self.hero_pos
        burger_required = max(0, customer.burger - self.inventory['burger'])
        fries_required = max(0, customer.french_fries - self.inventory['fries'])

        total = burger_required + fries_required
        while total > 0:

            if fries_required > 0 and burger_required > 0:
                pos = self.food_finder.get_closest_burger_or_fries(last_pos, self.id, objectives)
                objectives.append(pos)
                last_pos = pos

            elif burger_required > 0:
                pos = self.food_finder.get_closest_burger(last_pos, self.id, objectives)
                objectives.append(pos)
                last_pos = pos

            elif fries_required > 0:
                pos = self.food_finder.get_closest_fries(last_pos, self.id, objectives)
                objectives.append(pos)
                last_pos = pos

            total -= 1

        objectives.append(customer.loc)
        return objectives

    def _dist(self, start, loc):
        return abs(start[0] - loc[0]) + abs(start[1] - loc[1])

    def customer_cost_function(self, customer):
        objectives = self.create_objective_list(customer)
        cost = 0
        for i in range(len(objectives) - 1):
            cost += self._dist(objectives[i], objectives[i + 1])
        return cost

    def smallest_order(self, game):
        customers = game.customers
        best = min(customers, key=self.customer_cost_function)
        return best

    def maybe_kill_someone(self):
        our_hero = None
        other_heros = []
        for h in self.game.heroes:
            if h.name != 'NullJS':
                other_heros.append(h)
            else:
                our_hero = h

        for h in other_heros:
            h_pos = (h.pos['x'], h.pos['y'])
            if h.life + 45 < our_hero.life and self._dist(self.hero_pos, h_pos) <= self.KILL_DISTANCE:
                self.objectives = [h_pos]
                print('ATTACK')
                break
