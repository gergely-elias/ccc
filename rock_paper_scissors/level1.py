import fileinput

input_lines = list(fileinput.input())

styleorder = "RPS"

def better_style(styles):
    a, b = styles
    if a == b:
        return a
    a_index, b_index = (styleorder.index(x) for x in styles)
    if (a_index - b_index)%len(styleorder) == 1:
        return a
    return b

assert better_style("RR") == "R"
assert better_style("RS") == "R"
assert better_style("SP") == "S"
assert better_style("PS") == "S"

for line in input_lines[1:]:
    fightingStyles = line.strip()
    print(better_style(fightingStyles))