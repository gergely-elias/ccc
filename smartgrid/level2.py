import fileinput
import math

input_lines = list(fileinput.input())

line_index = 0

minPrice, minPriceMinute = math.inf, None
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

for task_idx in range(numberOfTasks):
    line_index += 1
    line = input_lines[line_index]
    taskId, completionTime = map(int, line.split())
    windowPrice = sum(priceOverMinutes[:completionTime])
    minSumPrice, minSumPriceStartTime = windowPrice, 0
    for possibleStartTime in range(1, numMinutes-completionTime+1):
        windowPrice += priceOverMinutes[possibleStartTime+completionTime-1] - priceOverMinutes[possibleStartTime-1]
        if windowPrice < minSumPrice:
            minSumPrice, minSumPriceStartTime = windowPrice, possibleStartTime
    print(f"{taskId} {minSumPriceStartTime}")
