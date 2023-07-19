from __future__ import annotations

import sys

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Callable


from circuits.utils.logger import Logger

from circuits.components.bus import Bus
from circuits.components.memory import RAM
from circuits.components.processor import CPU


from circuits.components.memory import Latch


def create_latch(charge: bool = False):
    return Latch(charge)


with open(sys.argv[1], "r") as file:
    lines = file.readlines()

image = [[create_latch(x == "1") for x in row.strip("\n")] for row in lines]

print(image)


LOGGER = Logger()


class Computer:
    def __init__(
        self,
        *,
        logger: Callable[[str, str], None],
    ):
        self.clock = 1

        self.__log = lambda *x, **y: logger(*x, origin=__name__, **y)

        self.__data_lines = Bus()
        self.__address_lines = Bus(5)

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
            memory_module=self.__primary_memory,
            logger=LOGGER.get_logger("CPU"),
            hooks_fetch=hooks_fetch,
        )

    def run(self):
        while True:
            self.__processing_unit.cycle()


def main():
    computer = Computer(logger=LOGGER.get_logger("COM"))
    computer.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
