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





class Bot:
    pass


class NullJsBot(Bot):

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

    def move(self, state):
        self.game = Game(state)
        self.food_finder = FoodFinder(self.game)
        self.hero_pos = (state['hero']['pos']['x'], state['hero']['pos']['y'])
        self.life = state['hero']['life']
        self.calorie = state['hero']['calories']

        if not self.current_customer:
            self.current_customer = self.smallest_order(self.game)
            self.objectives = self.create_objective_list(self.current_customer)

        if self.life < 25 and self.calorie > 30:
            self.objectives.insert(0, self.food_finder.get_closest_soda(self.hero_pos))

        objective = self.objectives[0]

        if self._dist(self.hero_pos, objective) == 1:
            self.objectives.pop(0)
            if len(self.objectives) == 0:
                self.objectives = []
                self.current_customer = None
                self.customer_number += 1

        return pathfinding(state['game']['board']['tiles'], self.hero_pos, objective, state['game']['board']['size'])

    def create_objective_list(self, customer):
        customer.loc = self.game.customers_locs[customer.id]
        objectives = []
        for _ in range(customer.burger):
            objectives.append(self.food_finder.get_closest_burger(self.hero_pos))

        for _ in range(customer.french_fries):
            objectives.append(self.food_finder.get_closest_fries(self.hero_pos))

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
