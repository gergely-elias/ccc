import fileinput

input_lines = list(fileinput.input())
map_size = int(input_lines[0].strip())
input_lines = input_lines[1:]
area_map = [line.strip() for line in input_lines[:map_size]]
input_lines = input_lines[map_size:]
number_of_queries = int(input_lines[0].strip())
input_lines = input_lines[1:]
coordinates = [
    tuple(map(int, line.strip().split(","))) for line in input_lines[:number_of_queries]
]
input_lines = input_lines[number_of_queries:]
assert len(input_lines) == 0

for x, y in coordinates:
    print(area_map[y][x])
