import fileinput
import math

input_lines = list(fileinput.input())

line_index = 0

mP, mSc = None, -math.inf
line = input_lines[line_index]
gameCount, playerCount = map(int, line.split())
for game_idx in range(gameCount):
    line_index += 1
    line = input_lines[line_index]
    p1Id, p1Sc, p2Id, p2Sc = map(int, line.split())
    if p1Sc > mSc or (p1Sc==mSc and p1Id<mP):
        mP, mSc = p1Id, p1Sc
    if p2Sc > mSc or (p2Sc==mSc and p2Id<mP):
        mP, mSc = p2Id, p2Sc

print(f"{mP} {mSc}")
