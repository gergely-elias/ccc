import fileinput

input_lines = list(fileinput.input())

line_index = 0

line = input_lines[line_index]
winIncrement, lossDecrement = map(int, line.split())
line_index += 1
line = input_lines[line_index]
gameCount, playerCount = map(int, line.split())
playerScores = [0] * playerCount
for game_idx in range(gameCount):
    line_index += 1
    line = input_lines[line_index]
    p1Id, p1Sc, p2Id, p2Sc = map(int, line.split())
    if p1Sc > p2Sc:
        playerScores[p1Id] += winIncrement
        playerScores[p2Id] -= lossDecrement
    elif p2Sc > p1Sc:
        playerScores[p2Id] += winIncrement
        playerScores[p1Id] -= lossDecrement
    else:
        raise ValueError

scoresWithIds = [(-s,i) for i, s in enumerate(playerScores)]
for s, i in (sorted(scoresWithIds)):
    print(f"{i} {-s}")
