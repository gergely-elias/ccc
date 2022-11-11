import fileinput

DIRECTIONS = {
    'N': (-1, 0),
    'E': (0, 1),
    'S': (1, 0),
    'W': (0, -1),
}

input_lines = list(fileinput.input())
split_input = (input_field for input_field in input_lines[0].strip().split(" "))

def transform_position(position):
    return (position-1) // cols + 1, (position-1) % cols + 1

def manhattan_distance(pointA, pointB):
    return sum([abs(coordA-coordB) for coordA, coordB in zip(pointA, pointB)])

def path_validity_with_step_index(path_color_with_offset, start_position, steps):
    path_color = path_color_with_offset - 1
    current_position = start_position
    cells_used_on_path = set([current_position])
    for step_idx, step in enumerate(steps):
        current_position = tuple([sum(coords) for coords in zip(current_position, step)])
        if current_position[0] < 1 or current_position[0] > rows or current_position[1] < 1 or current_position[1] > cols:
            return -1, step_idx+1
        if current_position in cells_used_on_path:
            return -1, step_idx+1
        if current_position in [point_position for point_position, point_color in points if point_color != path_color]:
            return -1, step_idx+1
        cells_used_on_path.add(current_position)
    return (1 if current_position in points_by_color[path_color] else -1), len(steps)

rows = int(next(split_input))
cols = int(next(split_input))
numberofpoints = int(next(split_input))
numberofcolors = numberofpoints//2
points = []
points_by_color = [[] for _ in range(numberofcolors)]
for point_idx in range(numberofpoints):
    position = transform_position(int(next(split_input)))
    color = int(next(split_input))-1
    points.append((position, color))
    points_by_color[color].append(position)
numberofpaths = int(next(split_input))
paths = []
paths_by_color = {}
for path_index in range(numberofpaths):
    path_color = int(next(split_input))
    start_position = transform_position(int(next(split_input)))
    path_length = int(next(split_input))
    steps = []
    for step_index in range(path_length):
        step = DIRECTIONS[next(split_input)]
        steps.append(step)
    paths.append((path_color, start_position, steps))
    paths_by_color[path_color] = (start_position, steps)

print(" ".join(map(str, [" ".join(map(str, path_validity_with_step_index(*path))) for path in paths])))
