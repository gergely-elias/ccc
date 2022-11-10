import fileinput

input_lines = list(fileinput.input())
rows, cols, numberofpoints, *points = map(int, input_lines[0].strip().split(" "))

def transform_position(position):
    return (position-1) // cols + 1, (position-1) % cols + 1

def parse_pointlist(pointlist):
    point_chunksize = 2
    for chunk_offset in range(0, len(pointlist), point_chunksize):
        yield pointlist[chunk_offset:chunk_offset + point_chunksize]

def manhattan_distance(pointA, pointB):
    return sum([abs(coordA-coordB) for coordA, coordB in zip(pointA, pointB)])

points_by_color = [[] for _ in range(numberofpoints//2)]
for position, color in parse_pointlist(points):
    points_by_color[color-1].append(transform_position(position))

print(" ".join([str(manhattan_distance(*point_pair)) for point_pair in points_by_color]))
