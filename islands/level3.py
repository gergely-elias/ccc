import fileinput
import networkx

input_lines = list(fileinput.input())
map_size = int(input_lines[0].strip())
input_lines = input_lines[1:]
area_map = [line.strip() for line in input_lines[:map_size]]
input_lines = input_lines[map_size:]
number_of_queries = int(input_lines[0].strip())
input_lines = input_lines[1:]
routes = [
    list(map(lambda coord: tuple(map(int, coord.split(","))), line.strip().split(" ")))
    for line in input_lines[:number_of_queries]
]
input_lines = input_lines[number_of_queries:]
assert len(input_lines) == 0


class TileType:
    LAND = "L"
    WATER = "W"


sea = networkx.Graph()
for y in range(map_size):
    for x in range(map_size):
        if area_map[y][x] == TileType.WATER:
            sea.add_node((x, y))
            if y > 0:
                if area_map[y - 1][x] == TileType.WATER:
                    sea.add_edge((x, y), (x, y - 1))
            if x > 0:
                if area_map[y][x - 1] == TileType.WATER:
                    sea.add_edge((x, y), (x - 1, y))
            if x > 0 and y > 0:
                if area_map[y - 1][x - 1] == TileType.WATER:
                    sea.add_edge((x, y), (x - 1, y - 1))
            if x > 0 and y < map_size - 1:
                if area_map[y + 1][x - 1] == TileType.WATER:
                    sea.add_edge((x, y), (x - 1, y + 1))


def tuple_sum(*ts):
    assert all(len(t) == len(ts[0]) for t in ts[1:])
    return tuple(sum(c) for c in zip(*ts))


def tuple_scalar(t, s):
    return tuple(c * s for c in t)


def tuple_diff(t1, t2):
    return tuple_sum(t1, tuple_scalar(t2, -1))


def self_crossing(route):
    route_length = len(route)
    for route_element_index in range(1, route_length):
        prev_route_element, route_element = route[
            route_element_index - 1 : route_element_index + 1
        ]
        if route_element in route[:route_element_index]:
            return True
        direction = tuple_diff(route_element, prev_route_element)
        assert max(abs(c) for c in direction) <= 1
        if min(abs(c) for c in direction) == 1:
            opposing_diagonals1 = (prev_route_element[0], route_element[1])
            opposing_diagonals2 = (route_element[0], prev_route_element[1])
            if (
                opposing_diagonals1 in route[: route_element_index - 1]
                and opposing_diagonals2 in route[: route_element_index - 1]
            ):
                opposing_diagonals_indices = [
                    route.index(od) for od in [opposing_diagonals1, opposing_diagonals2]
                ]
                if (
                    abs(opposing_diagonals_indices[0] - opposing_diagonals_indices[1])
                    == 1
                ):
                    return True
    return False


for route in routes:
    print("INVALID" if self_crossing(route) else "VALID")
