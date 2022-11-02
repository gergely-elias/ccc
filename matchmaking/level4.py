import fileinput
import math

input_lines = list(fileinput.input())

line_index = 0

line = input_lines[line_index]
gameCount, playerCount = map(int, line.split())
playerRatings = [1000] * playerCount
k = 32
for game_idx in range(gameCount):
    line_index += 1
    line = input_lines[line_index]
    p1Id, p1Sc, p2Id, p2Sc = map(int, line.split())
    exp1 = 1 / (1+10**((playerRatings[p2Id]-playerRatings[p1Id])/400))
    exp2 = 1 - exp1
    if p1Sc > p2Sc:
        s1, s2 = 1, 0
    elif p2Sc > p1Sc:
        s1, s2 = 0, 1
    else:
        raise ValueError
    playerRatings[p1Id] += math.floor(k * (s1-exp1))
    playerRatings[p2Id] += math.floor(k * (s2-exp2))

ratingsWithIds = [(-s,i) for i, s in enumerate(playerRatings)]
for s, i in (sorted(ratingsWithIds)):
    print(f"{i} {-s}")
