import fileinput

input_lines = list(fileinput.input())
TABLE_LENGTH = 3
EXTENDED_TABLE_LENGTH = TABLE_LENGTH + 1
for line in input_lines[1:]:
    width, height, number_of_tables = map(int, line.strip().split())
    extended_width = width + 1
    extended_height = height + 1
    room = [["." for x in range(extended_width)] for y in range(extended_height)]
    table_index = 0
    for y in range(0, extended_height - 1, 2):
        for x in range(
            0, extended_width - EXTENDED_TABLE_LENGTH + 1, EXTENDED_TABLE_LENGTH
        ):
            table_index += 1
            for table_part_offset in range(TABLE_LENGTH):
                room[y][x + table_part_offset] = "X"
    for x in range(
        extended_width - extended_width % (EXTENDED_TABLE_LENGTH), extended_width - 1, 2
    ):
        for y in range(
            0, extended_height - EXTENDED_TABLE_LENGTH + 1, EXTENDED_TABLE_LENGTH
        ):
            table_index += 1
            for table_part_offset in range(TABLE_LENGTH):
                room[y + table_part_offset][x] = "X"
    for row in room[:-1]:
        print("".join(map(str, row[:-1])))
    assert table_index == number_of_tables
    print()
