from copy import deepcopy
import fileinput
import math
import random
import sys

input_lines = list(fileinput.input())

line_index = 0

line = input_lines[line_index]
maxPower = int(line)
line_index += 1
line = input_lines[line_index]
maxElectricityBill = int(line)
line_index += 1
line = input_lines[line_index]
numMinutes = int(line)
priceOverMinutes = []
for minute_idx in range(numMinutes):
    line_index += 1
    line = input_lines[line_index]
    price = int(line)
    priceOverMinutes.append(price)
line_index += 1
line = input_lines[line_index]
numberOfTasks = int(line)

print(f"{numberOfTasks}")

tasks = []
for task_idx in range(numberOfTasks):
    line_index += 1
    line = input_lines[line_index]
    shiftedTaskId, *taskTuple = tuple(map(int, line.split()))
    tasks.append((shiftedTaskId-1, *taskTuple))
tasksSorted = sorted(tasks, key = lambda x: (x[3], x[2]))

# creating a power usage schedule that fulfills the power resource limits of each minute
# it might not fit in the electricity bill limit, we shall improve the costs later
resourceSetup = [[0 for task in range(numberOfTasks)] for timeslot in range(numMinutes)]

for taskId, power, startInterval, endInterval in tasksSorted:
    timeslot = startInterval
    while power > 0:
        resourceLeftInTimeslot = maxPower - sum(resourceSetup[timeslot])
        if power > resourceLeftInTimeslot:
            if resourceLeftInTimeslot > 0:
                resourceSetup[timeslot][taskId] += resourceLeftInTimeslot
                power -= resourceLeftInTimeslot
            timeslot += 1
            if timeslot > endInterval:
                raise Exception(f"no time left for task {taskId}")
        else:
            resourceSetup[timeslot][taskId] += power
            break

# using simplified ideas of simulated annealing to decrease the costs by adjusting the 
#  power usage schedule, step by step, starting with the setup calculated above

# analogy of energy function - electricity bill calculation
def electricityBill(schedule):
    return sum(priceOverMinutes[minute]*sum(schedule[minute]) for minute in range(numMinutes))

# analogy of state perturbation - assign another timeslot for one unit of power usage
def perturbateSchedule(resourceSetup):
    taskId, _, startInterval, endInterval = random.choice(tasksSorted)
    possibleOriginalTimeslots = [timeslot for timeslot in range(startInterval, endInterval+1) if resourceSetup[timeslot][taskId] > 0]
    oldTimeslot = random.choice(possibleOriginalTimeslots)
    possibleRescheduleTimeslots = [timeslot for timeslot in range(startInterval, endInterval+1) if timeslot != oldTimeslot and sum(resourceSetup[timeslot]) < maxPower]
    if len(possibleRescheduleTimeslots) > 0:
        newTimeslot = random.choice(possibleRescheduleTimeslots)
        newResourceSetup = deepcopy(resourceSetup)
        resourcesToMove = min(resourceSetup[oldTimeslot][taskId], maxPower - sum(resourceSetup[newTimeslot]))
        newResourceSetup[oldTimeslot][taskId] -= resourcesToMove
        newResourceSetup[newTimeslot][taskId] += resourcesToMove
        return newResourceSetup
    else:
        return resourceSetup

acceptance_factor = 1000000
mitigation = 0.98

while not electricityBill(resourceSetup) < maxElectricityBill:
    acceptance_factor *= mitigation
    print(electricityBill(resourceSetup), file=sys.stderr)
    newResourceSetup = perturbateSchedule(resourceSetup)
    scoreImprovement = electricityBill(newResourceSetup) - electricityBill(resourceSetup)
    if scoreImprovement < 0 or random.random() < math.exp(-scoreImprovement/acceptance_factor)/2:
        resourceSetup = newResourceSetup
print(electricityBill(resourceSetup), file=sys.stderr)

for taskId, _, startInterval, endInterval in tasksSorted:
    print(f"{taskId+1}", end="")
    for timeslot in range(startInterval, endInterval+1):
        if resourceSetup[timeslot][taskId] > 0:
            print(f" {timeslot} {resourceSetup[timeslot][taskId]}", end="")
    print()
