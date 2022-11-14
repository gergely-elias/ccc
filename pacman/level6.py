import fileinput

STEPCODE_TO_DIRECTION = {
    "L": (0, -1),
    "D": (1, 0),
    "R": (0, 1),
    "U": (-1, 0),
}

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
time = 1
path_to_coin = None
pacmanstartcell = (pacmanRow, pacmanColumn)
walkablecells = set(cellsall()).difference(cellsofaspecifickind("W"))
coincells = cellsofaspecifickind("C")
assert pacmanstartcell not in coincells, ValueError("Pacman starts at coin, no moves needed")
assert pacmanstartcell not in cellsofaspecifickind("G"), ValueError("Pacman starts at ghost, no solution")

availableatprevstep = set([pacmanstartcell])
bestpaths_prevstep = {
    (pacmanstartcell, tuple(False for _ in coincells)): "",
}

shortest_path_found = False
while not shortest_path_found:
    currentGhostPositions = [ghostCoords[time%len(ghostCoords)] for ghostCoords in ghostsCoordinates]
    currentWalkablePositions = walkablecells.difference(currentGhostPositions)
    availablethisstep = set()
    bestpaths_thisstep = dict()
    for (prevpos, prevcoins), prevpathsequence in bestpaths_prevstep.items():
        for stepcode in STEPCODE_TO_DIRECTION.keys():
            currentpos = positionafternextstep(prevpos, stepcode)
            if currentpos in currentWalkablePositions:
                currentcoins_lst = list(prevcoins)
                if currentpos in coincells:
                    currentcoins_lst[coincells.index(currentpos)] = True
                currentcoins = tuple(currentcoins_lst)
                currentpathsequence = prevpathsequence + stepcode
                if (currentpos, currentcoins) not in bestpaths_thisstep.keys() or currentpathsequence < bestpaths_thisstep[(currentpos, currentcoins)]:
                    bestpaths_thisstep[(currentpos, currentcoins)] = currentpathsequence
                if all(currentcoins):
                    shortest_path_found = True
    time += 1
    availableatprevstep = availablethisstep
    bestpaths_prevstep = bestpaths_thisstep
lex_first_shortest_path = min([path for (_, coins), path in bestpaths_thisstep.items() if all(coins)])
print(lex_first_shortest_path)
