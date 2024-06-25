from itertools import product
from typing import Callable, TypeAlias

from map import Map

Coordinate: TypeAlias = tuple[int, int]

INF = float("inf")


def reconstruct_path(
    path: dict[Coordinate, Coordinate], current: Coordinate
) -> list[Coordinate]:
    total_path = [current]
    while current in path.keys():
        current = path[current]
        total_path.insert(0, current)
    return total_path


def get_neighbours(current: Coordinate, map: Map) -> list[Coordinate]:
    """get all valid neighbours for a given point on a given map (walls are invalid)"""
    ret = [
        (current[0] + x, current[1] + y) for (x, y) in product([-1, 0, 1], [-1, 0, 1])
    ]
    return list(filter(map.is_valid, ret))


def squaredistance(p1: Coordinate, p2: Coordinate) -> int:
    w = p1[0] - p2[0]
    h = p1[1] - p2[1]
    return w * w + h * h


def a_star(
    start: Coordinate,
    goal: Coordinate,
    h: Callable[[Coordinate], float | int],
    map: Map,
):
    """from https://en.wikipedia.org/wiki/A*_search_algorithm#Pseudocode

    comments are in the Wikipedia article, this function is (practically) a direct translation into Python
    """

    open_set = {start}
    path: dict[Coordinate, Coordinate] = {}

    g_score: list[list[float | int]] = [
        [INF for _ in range(map.width)] for _ in range(map.height)
    ]
    g_score[start[1]][start[0]] = 0

    f_score: list[list[float | int]] = [
        [INF for _ in range(map.width)] for _ in range(map.height)
    ]
    f_score[start[1]][start[0]] = h(start)

    while open_set:
        current = min(open_set, key=lambda x: f_score[x[1]][x[0]])
        if current == goal:
            return reconstruct_path(path, current)

        open_set.remove(current)
        for neighbour in get_neighbours(current, map):
            tentative_g = g_score[current[1]][current[0]] + 1  # + d(current, neighbour)
            # d(current, neighbour) = the cost of the connection (or edge) between current and neighbour

            # For a straight line, the cost is 1
            # For a diagnol path (i.e. a path where the neighbour shares neither the x or y with the
            # current), the cost is sqrt(2)
            if neighbour[0] != current[0] and neighbour[1] != current[1]:
                tentative_g += 0.41421356237  # sqrt(2) - 1

            if tentative_g < g_score[neighbour[1]][neighbour[0]]:
                path[neighbour] = current
                g_score[neighbour[1]][neighbour[0]] = tentative_g
                f_score[neighbour[1]][neighbour[0]] = tentative_g + h(neighbour)
                open_set.add(neighbour)

    return []
