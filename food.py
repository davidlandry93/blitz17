from math import sqrt, inf


class FoodFinder:

    def __init__(self, game):
        self.game = game

    def get_closest_burger_or_fries(self, player_loc, player_id, objective_list):
        food_list = []
        for key, val in self.game.burger_locs.items() + self.game.fries_locs.items():
            if val != player_id and key not in objective_list:
                food_list.append(key)
        return self._get_closest(food_list, player_loc)

    def get_closest_burger(self, player_loc, player_id, objective_list):
        burger_list = []
        for key, val in self.game.burger_locs.items():
            if val != player_id and key not in objective_list:
                burger_list.append(key)
        return self._get_closest(burger_list, player_loc)

    def get_closest_fries(self, player_loc, player_id, objective_list):
        fries_list = []
        for key, val in self.game.fries_locs.items():
            if val != player_id and key not in objective_list:
                fries_list.append(key)
        return self._get_closest(fries_list, player_loc)

    def get_closest_soda(self, player_loc):
        return self._get_closest(list(self.game.taverns_locs), player_loc)

    def _get_closest(self, food_list, player_loc):
        best = {"dist": inf, "loc": None}
        for food_loc in food_list:
            dist = abs(player_loc[0] - food_loc[0]) + abs(player_loc[1] - food_loc[1])
            if dist < best['dist']:
                best['dist'] = dist
                best['loc'] = food_loc

        return best['loc']
