import fileinput

input_lines = list(fileinput.input())
for line in input_lines[1:]:
    x, y = map(int, line.strip().split())
    print(x * y // 3)
