import collections
import fileinput
import itertools
import networkx

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

resource_graph = networkx.Graph()
for task_idx in range(numberOfTasks):
    line_index += 1
    line = input_lines[line_index]
    taskId, power, startInterval, endInterval = map(int, line.split())
    for timeslot in range(startInterval, endInterval+1):
        for taskPowerneed, timeslotPowerslot in itertools.product(range(power), range(maxPower)):
            resource_graph.add_edge(('task', taskId, taskPowerneed), ('minute', timeslot, timeslotPowerslot), weight=priceOverMinutes[timeslot])
matching = sorted([tuple(reversed(sorted(edge))) for edge in networkx.min_weight_matching(resource_graph)])

taskMinutePairs = []
for (_, task, _), (_, minute, _) in matching:
    taskMinutePairs.append((task, minute))
sortedTaskMinutePairs = sorted(taskMinutePairs)
taskMinutePowerTrips = [(t, m, s) for (t, m), s in collections.Counter(sortedTaskMinutePairs).items()]
groupedTMP = collections.defaultdict(list)
for t, *v in taskMinutePowerTrips:
    groupedTMP[t].append(v)
for task, minutePowerpairs in groupedTMP.items():
    print(f"{task}", end="")
    for minute, power in minutePowerpairs:
        print(f" {minute} {power}", end="")
    print()
