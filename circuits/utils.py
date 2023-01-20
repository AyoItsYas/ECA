def generate_line_map(lines_count: int) -> list[list[bool]]:
    lines_power = pow(2, lines_count)

    lines = []

    i = lines_power
    while lines_power > 1:
        repeat = i // lines_power
        lines_power = lines_power // 2

        lines += [(([False] * lines_power) + ([True] * lines_power)) * repeat]

    return lines
