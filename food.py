from math import sqrt, inf


class FoodFinder:

    def __init__(self, game):
        self.game = game

    def get_closest_burger(self, player_loc):
        return self._get_closest_food(list(self.game.burger_locs), player_loc)

    def get_closest_fries(self, player_loc):
        return self._get_closest_food(list(self.game.fries_locs), player_loc)

    def _get_closest_food(self, food_list, player_loc):
        best = {"dist": inf, "loc": None}
        for food_loc in food_list:
            dist = sqrt((player_loc['x'] - food_loc[0]) ** 2 + (player_loc['y'] + food_loc[1]) ** 2)
            if dist < best['dist']:
                best['dist'] = dist
                best['loc'] = food_loc

        return best['loc']