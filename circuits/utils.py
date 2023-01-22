def generate_line_map(lines_count: int) -> list[list[bool]]:
    """Generates a map of inputs that accounts for all the possible combinations of logic for a given number of input lines.

    Args:
        lines_count (int): Number of input lines.

    Returns:
        list[list[bool]]: Map of all the possible combinations of logic for the given input lines.
    """
    lines_power = pow(2, lines_count)

    lines = []

    i = lines_power
    while lines_power > 1:
        repeat = i // lines_power
        lines_power = lines_power // 2

        lines += [(([False] * lines_power) + ([True] * lines_power)) * repeat]

    return lines
