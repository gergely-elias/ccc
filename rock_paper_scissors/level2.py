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

def next_round_fighting_styles(styles):
    nextStyles = ""
    for slice_start in range(0,len(styles),2):
        nextStyles += better_style(styles[slice_start:slice_start+2])
    return nextStyles

for line in input_lines[1:]:
    fightingStyles = line.strip()
    for round_index in range(2):
        fightingStyles = next_round_fighting_styles(fightingStyles)
    print(fightingStyles)
