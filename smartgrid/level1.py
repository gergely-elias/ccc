import fileinput
import math

input_lines = list(fileinput.input())

line_index = 0

minPrice, minPriceMinute = math.inf, None
line = input_lines[line_index]
numMinutes = int(line)
for minute_idx in range(numMinutes):
    line_index += 1
    line = input_lines[line_index]
    price = int(line)
    if price < minPrice:
        minPrice, minPriceMinute = price, minute_idx

print(f"{minPriceMinute}")
