import sys

instruction_set = {
    "NULL": "00000000",
    "JUMP": "00000001",
    "LDAV": "00000010",
    "DMPM": "00000011",
    "ACCM": "00000100",
    "PRNT": "00000101",
}

input_file = sys.argv[1]

with open(input_file, "r") as file:
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


with open(input_file + ".bin", "w") as file:
    file.write("\n".join(image))
