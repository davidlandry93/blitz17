from random import choice
from game import Game, Board, FriesTile, BurgerTile
from food import FoodFinder
import random
import requests
from math import sqrt
from path_finder import find_path, direction
import time


training_map = """################################C1    C2############F-            F-########  @1        @4  ######    []  B-B-  []    ####    ##  ####  ##    ####    ##  ####  ##    ####    []  B-B-  []    ######  @2        @3  ########F-            F-############C3    C4################################"""

pathfinding_url = 'http://game.blitz.codes:8081/pathfinding/direction'

# Here state is the string of the map.

#old version
# def pathfinding(state, start, target, size):
#     payload = {'map': state, 'size': size, 'start': '(' + str(start[0]) + ',' + str(start[1]) + ')', 'target': '(' + str(target[0]) + ',' + str(target[1]) + ')'}

#     print('calling pathfinder...')

#     response = requests.get(pathfinding_url, params=payload)

#     print('Reponse is: ' + str(response.json()))

#     try:
#         direction = response.json()['direction']
#     except KeyError:
#         direction = None
#     return direction

# AStar
def pathfinding(state, start, target, size, avoid_forks=False):
    b = time.time()
    direction_ = direction(find_path(Board({'size': size, 'tiles': state}), start, target, avoid_forks))
    e = time.time()
    print('A Star returned ' + str(direction_) + ' in ' + str(e - b))

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

        nearby_food = self.nearby_food()
        if nearby_food:
            return nearby_food

        self.current_customer = self.smallest_order(self.game)
        self.objectives = self.create_objective_list(self.current_customer)

        if self.life < 25 and self.calorie > 30 and len(self.objectives) > 1:
            self.objectives.insert(0, self.food_finder.get_closest_soda(self.hero_pos))

        self.maybe_kill_someone()

        our_hero = None
        for h in self.game.heroes:
            if h.name == 'NullJS':
                our_hero = h
                break

        direction = pathfinding(state['game']['board']['tiles'], self.hero_pos, self.objectives[0], state['game']['board']['size'], our_hero.life < 30)

        if direction is None:
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
        start = self.hero_pos
        for i in range(len(objectives)):
            cost += self._dist(start, objectives[i])
            start = objectives[i]

        return cost

    def smallest_order(self, game):
        customers = game.customers

        for customer in customers:
            customer.loc = self.game.customers_locs[customer.id]

        customers = sorted(customers, key=lambda x: self._dist(self.hero_pos, x.loc))

        best = min(customers[:3], key=self.customer_cost_function)
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
                break

    def nearby_food(self):
        size = self.game.state['game']['board']['size']
        possible_locations = [(max(0, self.hero_pos[0] - 1), self.hero_pos[1], 'North'),
                              (min(self.hero_pos[0] + 1, size - 1), self.hero_pos[1], 'South'),
                              (self.hero_pos[0], max(self.hero_pos[1] - 1, 0), 'West'),
                              (self.hero_pos[0], min(self.hero_pos[1] + 1, size - 1), 'East')]

        for location in possible_locations:
            tile = self.game.board.tiles[int(location[0])][int(location[1])]
            if (type(tile) is FriesTile or type(tile) is BurgerTile) and str(tile.hero_id) != str(self.id):
                if tile.hero_id == '-':
                    if type(tile) is BurgerTile and random.uniform(0, 1) < 0.6:
                        return location[2]
                    elif random.uniform(0, 1) < 0.3:
                        return location[2]
                elif random.uniform(0, 1) < 0.8:
                    return location[2]
