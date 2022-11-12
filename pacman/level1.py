import fileinput

input_lines = list(fileinput.input())
split_input = (input_line.strip() for input_line in input_lines)

size = int(next(split_input))
numofcoins = 0

for row in range(size):
    line = next(split_input)
    linecoins = line.count("C")
    numofcoins += linecoins
print(numofcoins)
