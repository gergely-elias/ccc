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

def positionafternextstep(current_position, step):
    step_direction = STEPCODE_TO_DIRECTION[step]
    return tuple(sum(coord_components) for coord_components in zip(current_position, step_direction))

numofcoins = 0
current_position = (pacmanRow, pacmanColumn)
for step in sequence:
    current_position = positionafternextstep(current_position, step)
    cy, cx = current_position
    if board[cy][cx] == 'C':
        numofcoins += 1
        board[cy][cx] = ' '
print(numofcoins)
