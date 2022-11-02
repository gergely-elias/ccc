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
    taskId, power, startInterval, endInterval = map(int, line.split())
    priceInInterval = priceOverMinutes[startInterval:endInterval+1]
    minPriceInterval = min(priceInInterval)
    minPriceMinute = priceInInterval.index(minPriceInterval) + startInterval
    print(f"{taskId} {minPriceMinute} {power}")
