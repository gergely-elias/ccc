import fileinput
import networkx

STEPCODE_TO_DIRECTION = {
    "L": (0, -1),
    "D": (1, 0),
    "R": (0, 1),
    "U": (-1, 0),
}
DIRECTION_TO_STEPCODE = {v: k for k,v in STEPCODE_TO_DIRECTION.items()}

# input parsing
input_lines = list(fileinput.input())
split_input = (input_line.strip() for input_line in input_lines)

size = int(next(split_input))
board = []
for row in range(size):
    line = next(split_input)
    board.append(list(line))

pacmanRow, pacmanColumn = map(lambda x: int(x)-1, next(split_input).split())

ghosts = []
numberOfGhosts = int(next(split_input))
for ghost_index in range(numberOfGhosts):
    ghostRow, ghostColumn = map(lambda x: int(x)-1, next(split_input).split())
    ghostSequenceLength = int(next(split_input))
    ghostSequence = next(split_input)
    ghosts.append(((ghostRow, ghostColumn), ghostSequence))

maxSequenceLength = int(next(split_input))

# helper functions
def positionafternextstep(current_position, step):
    step_direction = STEPCODE_TO_DIRECTION[step]
    return tuple(sum(coord_components) for coord_components in zip(current_position, step_direction))

def cellsvisited(start_position, sequence):
    current_position = start_position
    cells = [start_position]
    for step in sequence:
        current_position = positionafternextstep(current_position, step)
        cells.append(current_position)
    return cells

def cellsall():
    return [(y,x) for y in range(size) for x in range(size)]

def cellsofaspecifickind(celltype):
    return [(y,x) for y in range(size) for x in range(size) if board[y][x]==celltype]

# restructuring input data
ghostsCoordinates = []
for ghost_index in range(numberOfGhosts):
    ghostStartPosition, ghostMoveSequence = ghosts[ghost_index]
    ghostCoordinates = cellsvisited(ghostStartPosition, ghostMoveSequence)
    ghostCoordinates = ghostCoordinates + ghostCoordinates[-2:0:-1]
    ghostsCoordinates.append(ghostCoordinates)

# solve
sequence_found = False
time = 1
path_to_coin = None
pacmanstartcell = (pacmanRow, pacmanColumn)
walkablecells = set(cellsall()).difference(cellsofaspecifickind("W"))
coincells = cellsofaspecifickind("C")
assert pacmanstartcell not in coincells, ValueError("Pacman starts at coin, no moves needed")
assert pacmanstartcell not in cellsofaspecifickind("G"), ValueError("Pacman starts at ghost, no solution")

mazeovertimegraph = networkx.Graph()
availableatprevstep = set([pacmanstartcell])

while True:
    currentGhostPositions = [ghostCoords[time%len(ghostCoords)] for ghostCoords in ghostsCoordinates]
    currentWalkablePositions = walkablecells.difference(currentGhostPositions)
    availablethisstep = set()
    for prevpos in availableatprevstep:
        for stepcode, direction in STEPCODE_TO_DIRECTION.items():
            currentpos = positionafternextstep(prevpos, stepcode)
            if currentpos in currentWalkablePositions:
                mazeovertimegraph.add_edge((prevpos, time-1), (currentpos, time), stepcode=stepcode)
                availablethisstep.add(currentpos)
                if currentpos in coincells:
                    path_to_coin = networkx.shortest_path(mazeovertimegraph, (pacmanstartcell, 0), (currentpos, time))
                    edge_labels = networkx.get_edge_attributes(mazeovertimegraph, 'stepcode')
                    path_edges = [edge_labels.get(x, edge_labels.get((x[1],x[0]))) for x in zip(path_to_coin, path_to_coin[1:])]
                    print("".join(path_edges), flush=True)
                    exit()
    time += 1
    availableatprevstep = availablethisstep
