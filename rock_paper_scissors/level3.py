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

def get_styles_after_k_rounds(styles, k):
    for _round_index in range(k):
        styles = next_round_fighting_styles(styles)
    return styles

for line in input_lines[1:]:
    amountAllStyles = line.strip().split()
    amountR, amountP, amountS = map(lambda x: int(x[:-1]), amountAllStyles)
    fightingStyles = ""
    while amountR > 3:
        assert amountP > 0
        fightingStyles += 'PRRR'
        amountP -= 1
        amountR -= 3
    if amountR > 0:
        assert amountP > 0
        fightingStyles += 'P'
        fightingStyles += 'R'*amountR
        amountP -= 1
        amountR = 0
    fightingStyles += 'P'*amountP + 'S'*amountS
    amountP = 0
    amountS = 0
    stylesAfterTwoRounds = get_styles_after_k_rounds(fightingStyles, 2)
    assert stylesAfterTwoRounds.count('R') == 0 and stylesAfterTwoRounds.count('S') > 0
    print(fightingStyles)
