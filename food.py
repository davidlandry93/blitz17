from math import sqrt, inf


class FoodFinder:

    def __init__(self, game):
        self.game = game

    def get_closest_burger(self, player_loc, player_id):
        burger_list = []
        for key, val in self.game.burger_locs.items():
            if val != player_id:
                burger_list.append(key)
        return self._get_closest(list(self.game.burger_locs), player_loc)

    def get_closest_fries(self, player_loc, player_id):
        fries_list = []
        for key, val in self.game.fries_locs.items():
            if val != player_id:
                fries_list.append(key)
        return self._get_closest(fries_list, player_loc)

    def get_closest_soda(self, player_loc):
        return self._get_closest(list(self.game.taverns_locs), player_loc)

    def _get_closest(self, food_list, player_loc):
        best = {"dist": inf, "loc": None}
        for food_loc in food_list:
            dist = abs(player_loc[0] - food_loc[0]) + abs(player_loc[1] + food_loc[1])
            if dist < best['dist']:
                best['dist'] = dist
                best['loc'] = food_loc

        return best['loc']