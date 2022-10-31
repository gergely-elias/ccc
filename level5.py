import fileinput
import math

input_lines = list(fileinput.input())

line_index = 0

line = input_lines[line_index]
gameCount, playerCount, playersPerTeam = map(int, line.split())
playerRatings = [1000] * playerCount
k = 32
for game_idx in range(gameCount):
    line_index += 1
    line = input_lines[line_index]
    allPlayersAndScores = list(map(int, line.split()))
    team1PandS = allPlayersAndScores[:2*playersPerTeam]
    team2PandS = allPlayersAndScores[2*playersPerTeam:]
    team1Members = [x for i,x in enumerate(team1PandS) if i%2==0]
    team2Members = [x for i,x in enumerate(team2PandS) if i%2==0]
    team1totalScore = sum([x for i,x in enumerate(team1PandS) if i%2==1])
    team2totalScore = sum([x for i,x in enumerate(team2PandS) if i%2==1])
    ratingDiff = sum(playerRatings[x] for x in team2Members) - sum(playerRatings[x] for x in team1Members)
    exp1 = 1 / (1+10**(ratingDiff/400))
    exp2 = 1 - exp1
    if team1totalScore > team2totalScore:
        s1, s2 = 1, 0
    elif team2totalScore > team1totalScore:
        s1, s2 = 0, 1
    else:
        raise ValueError
    for p1Id in team1Members:
        playerRatings[p1Id] += math.floor(k * (s1-exp1))
    for p2Id in team2Members:
        playerRatings[p2Id] += math.floor(k * (s2-exp2))

ratingsWithIds = [(-s,i) for i, s in enumerate(playerRatings)]
for s, i in (sorted(ratingsWithIds)):
    print(f"{i} {-s}")
