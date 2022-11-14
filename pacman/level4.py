import fileinput
import networkx

STEPCODE_TO_DIRECTION = {
    "L": (0, -1),
    "D": (1, 0),
    "R": (0, 1),
    "U": (-1, 0),
}
DIRECTION_TO_STEPCODE = {v: k for k,v in STEPCODE_TO_DIRECTION.items()}

input_lines = list(fileinput.input())
split_input = (input_line.strip() for input_line in input_lines)

size = int(next(split_input))
board = []
for row in range(size):
    line = next(split_input)
    board.append(list(line))

pacmanRow, pacmanColumn = map(lambda x: int(x)-1, next(split_input).split())

maxSequenceLength = int(next(split_input))

def firstcoinposition():
    for y in range(size):
        for x in range(size):
            if board[y][x] == "C":
                return (y,x)
    return None

mazegraph = networkx.Graph()
current_position = (pacmanRow, pacmanColumn)
for y in range(size):
    for x in range(size):
        if x > 0 and board[y][x] not in ["W", "G"] and board[y][x-1] not in ["W", "G"]:
            mazegraph.add_edge((y,x), (y,x-1))
        if y > 0 and board[y][x] not in ["W", "G"] and board[y-1][x] not in ["W", "G"]:
            mazegraph.add_edge((y,x), (y-1,x))

allsteps = ""
nextcointarget = firstcoinposition()
while nextcointarget is not None:
    path = networkx.shortest_path(mazegraph, current_position, nextcointarget)[1:]
    for y, x in path:
        currenty, currentx = current_position
        direction = (y-currenty, x-currentx)
        stepcode = DIRECTION_TO_STEPCODE[direction]
        allsteps += stepcode
        current_position = y, x
        if board[y][x] == 'C':
            board[y][x] = ' '
    nextcointarget = firstcoinposition()
print(allsteps)
