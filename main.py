from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Callable


from circuits.utils.logger import Logger

from circuits.components.bus import Bus
from circuits.components.memory import RAM
from circuits.components.processor import CPU


from circuits.components.memory import Latch

instruction_set = {
    "NULL": "00000000",
    "JUMP": "00000001",
    "LOAD": "00000010",
    "ACCM": "00000011",
}

with open("test.eca", "r") as file:
    lines = file.readlines()


def sanitize(lines: list[str]):
    return [line.strip("\n") for line in lines]


def compile(lines: list[str]):
    result = []
    for line in lines:
        chunks = line.split()

        instruction = instruction_set.get(chunks.pop(0))
        if instruction is None:
            raise Exception(f"'{chunks[0]}' is an invalid instruction")

        result.append(instruction)

        for chunk in chunks:
            chunk = chunk.rjust(8, "0")
            result.append(chunk)

    return result


lines = sanitize(lines)
lines = compile(lines)


def create_latch(charge: bool = False):
    return Latch(charge)


image = [[create_latch(x == "1") for x in row] for row in lines]


LOGGER = Logger()


class Computer:
    def __init__(
        self,
        *,
        logger: Callable[[str, str], None],
    ):
        self.clock = 4

        self.__log = logger

        self.__data_lines = Bus()
        self.__address_lines = Bus(4)

        self.__primary_memory = RAM(
            self.__data_lines,
            self.__address_lines,
            logger=LOGGER.get_logger("RAM"),
        )
        self.__primary_memory.set_memory_image(image)

        hooks_fetch = (self.__primary_memory.decode_hook,)
        self.__processing_unit = CPU(
            self.__data_lines,
            self.__address_lines,
            clock=self.clock,
            logger=LOGGER.get_logger("CPU"),
            hooks_fetch=hooks_fetch,
        )

    def run(self):
        while True:
            self.__log("Running cycle!")
            self.__processing_unit.cycle()


def main():
    computer = Computer(logger=LOGGER.get_logger("COM"))
    computer.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
