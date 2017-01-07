from random import choice
from game import Game
from food import FoodFinder
import requests
from math import sqrt

training_map = """################################C1    C2############F-            F-########  @1        @4  ######    []  B-B-  []    ####    ##  ####  ##    ####    ##  ####  ##    ####    []  B-B-  []    ######  @2        @3  ########F-            F-############C3    C4################################"""

pathfinding_url = 'http://game.blitz.codes:8081/pathfinding/direction'

# Here state is the string of the map.
def pathfinding(state, start, target, size):
    payload = {'map': state, 'size': size, 'start': '(' + str(start[0]) + ',' + str(start[1]) + ')', 'target': '(' + str(target[0]) + ',' + str(target[1]) + ')'}
    response = requests.get(pathfinding_url, params=payload)
    try:
        direction = response.json()['direction']
        return direction
    except KeyError:
        print('Random move')
        return choice(['North', 'South', 'East', 'West'])

def customer_cost_function(customer):
    return customer.burger + customer.french_fries

def smallest_order(game):
    customers = game.customers

    print(customers[0].french_fries)

    best = min(customers, key=customer_cost_function)
    print('smallest order' + str(best))

    return best

class Bot:
    pass


class NullJsBot(Bot):

    def __init__(self):
        self.current_order = None  # {'burger': 1, 'fries': 2}
        self.inventory = {'burger': 0, 'fries': 0}
        self.hero_pos = None
        self.food_finder = None
        self.game = None
        self.objectives = []
        self.customer_number = 0
        self.life = 0
        self.calorie = 0

    def move(self, state):
        self.game = Game(state)
        self.food_finder = FoodFinder(self.game)
        self.hero_pos = (state['hero']['pos']['x'], state['hero']['pos']['y'])
        self.life = state['hero']['life']
        self.life = state['hero']

        smallest_order(self.game)

        if not self.current_order:
            self.current_order = smallest_order(self.game)
            self.current_order.loc = self.game.customers[self.current_order.id].id
            print(self.current_order.loc)

        if self.life < 25 and self.calorie > 30:
            self.objectives.insert(0, self.food_finder.get_closest_soda(self.hero_pos))

        objective = self.objectives[0]

        if self._dist(objective) == 1:
            self.objectives.pop(0)
            if len(self.objectives) == 0:
                self.objectives = []
                self.current_order = None
                self.customer_number += 1

        return pathfinding(state['game']['board']['tiles'], self.hero_pos, objective, state['game']['board']['size'])

    def create_objective_list(self):
        objectives = []
        for _ in range(self.current_order['burger']):
            objectives.append(self.food_finder.get_closest_burger(self.hero_pos))

        for _ in range(self.current_order['fries']):
            objectives.append(self.food_finder.get_closest_fries(self.hero_pos))

        objectives.append(self.game.customers_locs[self.game.customers[self.customer_number].id])
        self.objectives = objectives

    def _dist(self, loc):
        return abs(self.hero_pos[0] - loc[0]) + abs(self.hero_pos[1] - loc[1])
