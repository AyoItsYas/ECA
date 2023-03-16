from circuits.components.memory import Latch

instruction_set = {
    "NULL": "00000000",
    "JUMP": "00000001",
    "LOAD": "00000010",
    "ACCM": "00000011",
}

with open("test.asm", "r") as file:
    lines = file.readlines()


def sanitize(lines: list[str]):
    return [line.strip("\n") for line in lines]


def compile(lines: list[str]):
    result = []
    for line in lines:
        chunks = line.split()

        instruction = instruction_set.get(chunks.pop(0))
        result.append(instruction)

        if instruction is None:
            raise Exception(f"'{chunks[0]}' is an invalid instruction")

        for chunk in chunks:
            chunk = chunk.rjust(8, "0")
            result.append(chunk)

    return result


lines = sanitize(lines)
image = compile(lines)


def create_latch(charge: bool = False):
    return Latch(charge)


matrix = [[create_latch(x == "1") for x in row] for row in image]
