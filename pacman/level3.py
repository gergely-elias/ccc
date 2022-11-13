import fileinput

STEPCODE_TO_DIRECTION = {
    "L": (0, -1),
    "D": (1, 0),
    "R": (0, 1),
    "U": (-1, 0),
}

input_lines = list(fileinput.input())
split_input = (input_line.strip() for input_line in input_lines)

size = int(next(split_input))
board = []
for row in range(size):
    line = next(split_input)
    board.append(list(line))

pacmanRow, pacmanColumn = map(lambda x: int(x)-1, next(split_input).split())

sequenceLength = int(next(split_input))
sequence = next(split_input)

ghosts = []
numberOfGhosts = int(next(split_input))
for ghost_index in range(numberOfGhosts):
    ghostRow, ghostColumn = map(lambda x: int(x)-1, next(split_input).split())
    ghostSequenceLength = int(next(split_input))
    ghostSequence = next(split_input)
    ghosts.append(((ghostRow, ghostColumn), ghostSequence))

def positionafternextstep(current_position, step):
    step_direction = STEPCODE_TO_DIRECTION[step]
    return tuple(sum(coord_components) for coord_components in zip(current_position, step_direction))

survive = True
numofcoins = 0
current_pacmanposition = (pacmanRow, pacmanColumn)
current_ghostpositions, ghostmovesequences = list(map(list, zip(*ghosts)))
for time in range(sequenceLength):
    current_pacmanposition = positionafternextstep(current_pacmanposition, sequence[time])
    current_ghostpositions = [positionafternextstep(current_ghostpositions[ghost_idx], ghostmovesequences[ghost_idx][time]) for ghost_idx in range(numberOfGhosts)]
    cy, cx = current_pacmanposition
    if board[cy][cx] == 'W':
        survive = False
        break
    elif current_pacmanposition in current_ghostpositions:
        survive = False
        break
    elif board[cy][cx] == 'C':
        numofcoins += 1
        board[cy][cx] = ' '

print(numofcoins, "YES" if survive else "NO")
