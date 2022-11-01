import fileinput
import math
import random
from copy import deepcopy

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
line_index += 1
line = input_lines[line_index]
maxEloDiff, scoreThreshold = map(int, line.split())
line_index += 1
line = input_lines[line_index]
queueSize = int(line)
playersQueue = []
for queue_idx in range(queueSize):
    line_index += 1
    line = input_lines[line_index]
    playerIndex = int(line)
    playersQueue.append(playerIndex)

queuedPlayersWithRating = [(i, r) for i, r in enumerate(playerRatings) if i in playersQueue]
sortedPlayers = sorted(queuedPlayersWithRating, key=lambda x: (-x[1], x[0]))

initPairing = []

for match_idx in range(len(sortedPlayers)//(2*playersPerTeam)):
    teamA = []
    teamB = []
    for offset, player_count in enumerate(range(2*playersPerTeam*match_idx, 2*playersPerTeam*(match_idx+1))):
        if offset%4==0 or offset%4==3:
            teamA.append(sortedPlayers[player_count])
        else:
            teamB.append(sortedPlayers[player_count])
    initPairing.append([teamA, teamB])

def evalMatch(match):
    teamA, teamB = match
    return abs(sum([x[1] for x in teamA]) - sum([x[1] for x in teamB]))

def evalPairing(pairing):
    return sum([evalMatch(match) for match in pairing])

def validateMatch(match):
    participantRatings = [member[1] for team in match for member in team]
    return max(participantRatings) - min(participantRatings) <= maxEloDiff

def perturbatePairing(pairing):
    newPairing = deepcopy(pairing)
    numberOfMatches = len(pairing)
    randomMatches = [random.randrange(numberOfMatches) for _ in range(2)]
    randomMatchParticipants = [random.randrange(2*playersPerTeam) for _ in range(2)]
    teamIndices = [0 if participant < playersPerTeam else 1 for participant in randomMatchParticipants]
    memberIndices = [participant%playersPerTeam for participant in randomMatchParticipants]
    newPairing[randomMatches[0]][teamIndices[0]][memberIndices[0]] = pairing[randomMatches[1]][teamIndices[1]][memberIndices[1]]
    newPairing[randomMatches[1]][teamIndices[1]][memberIndices[1]] = pairing[randomMatches[0]][teamIndices[0]][memberIndices[0]]
    if validateMatch(newPairing[randomMatches[0]]) and validateMatch(newPairing[randomMatches[1]]):
        return newPairing
    else:
        return pairing

pairing = initPairing
acceptance_factor = 0.3

while not evalPairing(pairing) < scoreThreshold:
    newPairing = perturbatePairing(pairing)
    scoreImprovement = evalPairing(newPairing) - evalPairing(pairing)
    if scoreImprovement < 0 or random.random() < math.exp(-scoreImprovement/acceptance_factor)/2:
        pairing = newPairing

for match in pairing:
    print(" ".join([" ".join(str(member[0]) for member in team) for team in match]))
