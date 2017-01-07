from queue import PriorityQueue
#from game import Board

class SquareGrid:
    def __init__(self, board):
        self.board = board

    def in_bounds(self, id):
        (x, y) = id
        return 0 <= x < self.board.size and 0 <= y < self.board.size

    def passable(self, id):
        return self.board.passable(id)

    def cost(self, _from, _to):
        return 1

    def neighbors(self, id):
        (x, y) = id
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        if (x + y) % 2 == 0: results.reverse() # aesthetics
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results


def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)

def a_star_search(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                frontier.put(next, priority)
                came_from[next] = current

    return came_from, cost_so_far

def reconstruct_path(came_from, start, goal):
    current = goal
    path = [current]
    while current != start:
        current = came_from[current]
        path.append(current)
    path.reverse() # optional
    return path


def find_path(board, start, goal):
    try:
        graph = SquareGrid(board)
        came_from, cost_so_far = a_star_search(graph, start, goal)
        path = reconstruct_path(came_from, start, goal)
        return path
    except:
        return []

def direction(path):
    if len(path) < 2:
        return 'Stay'

    x0 = path[0][0]
    y0 = path[0][1]
    x1 = path[1][0]
    y1 = path[1][1]

    if y1 - y0 > 0:
        return 'East'
    if y1 - y0 < 0:
        return 'West'
    if x1 - x0 > 0:
        return 'South'
    if x1 - x0 < 0:
        return 'North'

    return 'Stay'


# if __name__ == '__main__':
#     training_map = """################################C1    C2############F-            F-########  @1        @4  ######    []  B-B-  []    ####    ##  ####  ##    ####    ##  ####  ##    ####    []  B-B-  []    ######  @2        @3  ########F-            F-############C3    C4################################"""

#     board = Board({'size': 12, 'tiles': training_map})
#     path = find_path(board, (2, 7), (9, 7))

#     print(path)
#     print(direction(path))
