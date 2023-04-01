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

def get_final_winner(styles):
    while len(styles) > 1:
        styles = next_round_fighting_styles(styles)
    return styles[0]

def fill_bracket(bracketSize):
    global amountR, amountP, amountS
    stylesInBracket = ""
    slotsLeft = bracketSize
    if amountR >= slotsLeft:
        assert amountP > 0
        stylesInBracket += "P" + "R"*(slotsLeft-1)
        amountP -= 1
        amountR -= slotsLeft-1
        slotsLeft = 0
        return stylesInBracket
    if amountR > 0:
        assert amountP > 0
        stylesInBracket += "P" + "R"*amountR
        slotsLeft -= 1+amountR
        amountP -= 1
        amountR = 0
    if amountP >= slotsLeft:
        stylesInBracket += "P"*slotsLeft
        amountP -= slotsLeft
        slotsLeft = 0
        return stylesInBracket
    stylesInBracket += "P"*amountP
    slotsLeft -= amountP
    amountP = 0
    if amountS >= slotsLeft:
        stylesInBracket += "S"*slotsLeft
        amountS -= slotsLeft
        slotsLeft = 0
    return stylesInBracket

_n, m = map(int, input_lines[0].strip().split())
for line in input_lines[1:]:
    amountAllStyles = line.strip().split()
    amountR, amountP, amountS = map(lambda x: int(x[:-1]), amountAllStyles)
    originalAmounts = {
        "R": amountR,
        "P": amountP,
        "S": amountS,
    }
    bracketSize = m//2
    fightingStyles = ""
    while bracketSize > 0:
        fightingStyles += fill_bracket(bracketSize)
        bracketSize //= 2
    fightingStyles += "S"
    assert get_final_winner(fightingStyles) == "S"
    assert all(originalAmounts[style] == fightingStyles.count(style) for style in originalAmounts)
    print(fightingStyles)
