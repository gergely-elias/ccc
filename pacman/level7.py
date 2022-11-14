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
    ghosts.append((ghostRow, ghostColumn))

coins = {}
numberOfCoins = int(next(split_input))
for coin_index in range(numberOfCoins):
    coinRow_offset, coinColumn_offset, coinValue = map(int, next(split_input).split())
    coinRow, coinColumn = map(lambda x: x-1, (coinRow_offset, coinColumn_offset))
    coins[(coinRow, coinColumn)] = coinValue

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

def lexfirstshortestpath(startpos, finalpos):
    time = 1
    walkablecells = set(cellsall()).difference(cellsofaspecifickind("W"))
    bestpaths_prevstep = {
        startpos: "",
    }

    shortest_path_found = False
    while not shortest_path_found:
        bestpaths_thisstep = dict()
        for prevpos, prevpathsequence in bestpaths_prevstep.items():
            for stepcode in STEPCODE_TO_DIRECTION.keys():
                currentpos = positionafternextstep(prevpos, stepcode)
                if currentpos in walkablecells:
                    currentpathsequence = prevpathsequence + stepcode
                    if currentpos not in bestpaths_thisstep.keys() or currentpathsequence < bestpaths_thisstep[currentpos]:
                        bestpaths_thisstep[currentpos] = currentpathsequence
                    if currentpos == finalpos:
                        shortest_path_found = True
        time += 1
        bestpaths_prevstep = bestpaths_thisstep
    lex_first_shortest_path = min([path for pos, path in bestpaths_thisstep.items() if pos==finalpos])
    return lex_first_shortest_path

# restructuring input data
ghostsCoordinates = []
for ghost_index in range(numberOfGhosts):
    ghostStartPosition = ghosts[ghost_index]
    ghostMoveSequence = lexfirstshortestpath(ghostStartPosition, (pacmanRow, pacmanColumn))
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

bestpaths_prevstep = {
    pacmanstartcell: 0,
}

shortest_path_found = False
for time in range(1, maxSequenceLength+1):
    currentGhostPositions = [ghostCoords[time%len(ghostCoords)] for ghostCoords in ghostsCoordinates]
    currentWalkablePositions = walkablecells.difference(currentGhostPositions)
    bestpaths_thisstep = dict()
    for prevpos, prevscore in bestpaths_prevstep.items():
        for stepcode, direction in STEPCODE_TO_DIRECTION.items():
            currentpos = positionafternextstep(prevpos, stepcode)
            if currentpos in currentWalkablePositions:
                if currentpos in coincells:
                    currentscore = prevscore + coins[currentpos]
                else:
                    currentscore = prevscore
                if currentpos not in bestpaths_thisstep.keys() or currentscore > bestpaths_thisstep[currentpos]:
                    bestpaths_thisstep[currentpos] = currentscore
    time += 1
    bestpaths_prevstep = bestpaths_thisstep
max_score = max(bestpaths_thisstep.values())
print(max_score)
