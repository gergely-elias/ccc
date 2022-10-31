import fileinput

input_lines = list(fileinput.input())

line_index = 0

line = input_lines[line_index]
gameCount, playerCount = map(int, line.split())
playerWins = [0] * playerCount
for game_idx in range(gameCount):
    line_index += 1
    line = input_lines[line_index]
    p1Id, p1Sc, p2Id, p2Sc = map(int, line.split())
    if p1Sc > p2Sc:
        playerWins[p1Id] += 1
    elif p2Sc > p1Sc:
        playerWins[p2Id] += 1
    else:
        raise ValueError

winsWithIds = [(-w,i) for i, w in enumerate(playerWins)]
for w, i in (sorted(winsWithIds)):
    print(f"{i} {-w}")
