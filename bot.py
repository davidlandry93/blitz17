from random import choice
from game import Game
from food import FoodFinder


class Bot:
    pass


class NullJsBot(Bot):

    def __init__(self):
        self.current_order = None  # {'burger': 1, 'fries': 2}

    def move(self, state):
        game = Game(state)
        food_finder = FoodFinder(game)
        hero_pos = state['hero']['pos']

        if not self.current_order:
            self.current_order = {'burger': game.customers[0].burger, 'fries': game.customers[1].french_fries}

        objective = None
        if self.current_order['burger'] > 1:
            objective = food_finder.get_closest_burger(hero_pos)
        else:
            objective = food_finder.get_closest_fries(hero_pos)

        dirs = ['Stay', 'North', 'South', 'East', 'West']
        return choice(dirs)


