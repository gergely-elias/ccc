import fileinput

input_lines = list(fileinput.input())

line_index = 0

line = input_lines[line_index]
maxPower = int(line)
line_index += 1
line = input_lines[line_index]
maxElectricityBill = int(line)
line_index += 1
line = input_lines[line_index]
maxConcurrentTasks = int(line)
line_index += 1
line = input_lines[line_index]
numMinutes = int(line)
priceOverMinutes = []
for minute_idx in range(numMinutes):
    line_index += 1
    line = input_lines[line_index]
    price = int(line)
    priceOverMinutes.append(price)
minutesInPriceOrder = [x[0] for x in sorted(enumerate(priceOverMinutes), key = lambda x: x[1])]

line_index += 1
line = input_lines[line_index]
numberOfTasks = int(line)

print(f"{numberOfTasks}")

tasks = []
for task_idx in range(numberOfTasks):
    line_index += 1
    line = input_lines[line_index]
    shiftedTaskId, power, startInterval, endInterval = tuple(map(int, line.split()))
    priciestMinuteOfTask = max(minutesInPriceOrder.index(timeslot) for timeslot in range(startInterval, endInterval+1))
    tasks.append((shiftedTaskId-1, power, startInterval, endInterval, priciestMinuteOfTask))
tasksSorted = sorted(tasks, key = lambda x: (x[4]))

resourceSetup = [[0 for _ in range(numberOfTasks)] for _ in range(numMinutes)]

for taskId, power, startInterval, endInterval, _ in tasksSorted:
    tasksTimeSlotsInPriceOrder = [x for x in minutesInPriceOrder if x >= startInterval and x <= endInterval]
    timeslot_index = 0
    timeslot = tasksTimeSlotsInPriceOrder[timeslot_index]
    while power > 0:
        resourceLeftInTimeslot = maxPower - sum(resourceSetup[timeslot])
        roomLeftInTimeslot = maxConcurrentTasks > sum([x>0 for x in resourceSetup[timeslot]])
        if power > resourceLeftInTimeslot:
            if resourceLeftInTimeslot > 0 and roomLeftInTimeslot:
                resourceSetup[timeslot][taskId] += resourceLeftInTimeslot
                power -= resourceLeftInTimeslot
        else:
            if roomLeftInTimeslot:
                resourceSetup[timeslot][taskId] += power
                break
        timeslot_index += 1
        timeslot = tasksTimeSlotsInPriceOrder[timeslot_index]
        if timeslot_index >= len(tasksTimeSlotsInPriceOrder):
            raise Exception(f"no time left for task {taskId}")

for taskId, _, startInterval, endInterval, _ in tasksSorted:
    print(f"{taskId+1}", end="")
    for timeslot in range(startInterval, endInterval+1):
        if resourceSetup[timeslot][taskId] > 0:
            print(f" {timeslot} {resourceSetup[timeslot][taskId]}", end="")
    print()
