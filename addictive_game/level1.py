import fileinput

input_lines = list(fileinput.input())
rows, cols, numberofpositions, *positions = map(int, input_lines[0].strip().split(" "))

def transform_position(position):
    return (position-1) // cols + 1, (position-1) % cols + 1

print(" ".join([" ".join(map(str, transform_position(position))) for position in positions]))
