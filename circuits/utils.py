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


class Logger:
    def __init__(self):
        self.__streams = []
        self.__streams_offset = 0

    def log(self, stream: str, content: str):
        print(stream.ljust(self.__streams_offset), ":", content)

    def get_logger(self, stream: str):
        self.register_stream(stream)
        return lambda x: self.log(stream, x)

    def register_stream(self, stream: str):
        self.__streams.append(stream)
        self.__streams_offset = max(len(x) for x in self.__streams)
