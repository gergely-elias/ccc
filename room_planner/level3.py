import fileinput

input_lines = list(fileinput.input())
TABLE_LENGTH = 3
for line in input_lines[1:]:
    width, height, number_of_tables = map(int, line.strip().split())
    assert width % 3 != 2 or height % 3 != 2
    room = [[0 for x in range(width)] for y in range(height)]
    table_index = 0
    for y in range(height):
        for x in range(0, width - TABLE_LENGTH + 1, TABLE_LENGTH):
            table_index += 1
            for table_part_offset in range(TABLE_LENGTH):
                room[y][x + table_part_offset] = table_index
    for x in range(width - width % TABLE_LENGTH, width):
        for y in range(0, height - TABLE_LENGTH + 1, TABLE_LENGTH):
            table_index += 1
            for table_part_offset in range(TABLE_LENGTH):
                room[y + table_part_offset][x] = table_index
    for row in room:
        print(" ".join(map(str, row)))
    assert table_index == number_of_tables
    print()
