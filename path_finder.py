from queue import PriorityQueue
from game import Board

class SquareGrid:
    def __init__(self, board):
        self.board = board

    def in_bounds(self, id):
        (x, y) = id
        return 0 <= x < self.board.size and 0 <= y < self.board.size

    def passable(self, id):
        return self.board.passable(id)

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
    #frontier.put(start, 0)
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get() #frontier.get()

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
    path.append(start) # optional
    path.reverse() # optional
    return path


def find_path(board, start, goal):
    graph = SquareGrid(board)
    came_from, cost_so_far = a_star_search(graph, start, goal)
    print(came_from)
    print(cost_so_far)
    path = reconstruct_path(came_from, start, goal)
    return path


if __name__ == '__main__':
    training_map = """################################C1    C2############F-            F-########  @1        @4  ######    []  B-B-  []    ####    ##  ####  ##    ####    ##  ####  ##    ####    []  B-B-  []    ######  @2        @3  ########F-            F-############C3    C4################################"""

    board = Board({'size': 12, 'tiles': training_map})

    print(board.tiles)

    for x, y in enumerate(range(12)):
        if board.passable((x,y)):
            print((x,y))

#    print(board.passable((2,5)))
 #   print(board.passable((2,6)))

    print(find_path(board, (2, 3), (2, 6)))
