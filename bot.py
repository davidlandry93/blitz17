from random import choice
from game import Game
from food import FoodFinder
import requests
from math import sqrt

training_map = """################################C1    C2############F-            F-########  @1        @4  ######    []  B-B-  []    ####    ##  ####  ##    ####    ##  ####  ##    ####    []  B-B-  []    ######  @2        @3  ########F-            F-############C3    C4################################"""

pathfinding_url = 'http://game.blitz.codes:8081/pathfinding/direction'

def pathfinding(state, start, target):
    payload = {'map': state, 'size': int(sqrt(len(training_map) / 2)), 'start': '(' + str(start[0]) + ',' + str(start[1]) + ')', 'target': '(' + str(target[0]) + ',' + str(target[1]) + ')'}
    response = requests.get(pathfinding_url, params=payload)
    return response.json()['direction']

class Bot:
    pass


class NullJsBot(Bot):

    def __init__(self):
        self.current_order = None  # {'burger': 1, 'fries': 2}
        self.inventory = {'burger': 0, 'fries': 0}

    def move(self, state):
        game = Game(state)
        food_finder = FoodFinder(game)
        hero_pos = (state['hero']['pos']['x'], state['hero']['pos']['y'])

        if not self.current_order:
            self.current_order = {'burger': game.customers[0].burger, 'fries': game.customers[0].french_fries}

        objective = None
        if self.current_order['burger'] > 1:
            objective = food_finder.get_closest_burger(hero_pos)
        else:
            objective = food_finder.get_closest_fries(hero_pos)

        return pathfinding(state['game']['board']['tiles'], hero_pos, objective)


