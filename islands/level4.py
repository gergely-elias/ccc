import fileinput
import networkx

input_lines = list(fileinput.input())
map_size = int(input_lines[0].strip())
input_lines = input_lines[1:]
area_map = [line.strip() for line in input_lines[:map_size]]
input_lines = input_lines[map_size:]
number_of_queries = int(input_lines[0].strip())
input_lines = input_lines[1:]
coordinate_pairs = [
    tuple(map(lambda coord: tuple(map(int, coord.split(","))), line.strip().split(" ")))
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


def tile_presentation(tile):
    return ",".join(str(coord) for coord in tile)


def route_presentation(route):
    return " ".join(tile_presentation(tile) for tile in route)


for coord1, coord2 in coordinate_pairs:
    print(route_presentation(networkx.shortest_path(sea, coord1, coord2)))
