from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Callable


from circuits.utils import Logger

from circuits.components.bus import Bus
from circuits.components.memory import RAM
from circuits.components.processor import CPU


LOGGER = Logger()


class Computer:
    def __init__(
        self, size: int, *, logger: Callable, start_up_hook: Callable[[Computer]] = None
    ):
        self.__log = logger

        self.__data_lines = Bus(size)
        self.__address_lines = Bus()

        self.__primary_memory = RAM(
            self.__data_lines,
            self.__address_lines,
            size=size,
            logger=LOGGER.get_logger("RAM"),
        )
        self.__processing_unit = CPU(
            self.__data_lines,
            self.__address_lines,
            1,
            size=size,
            logger=LOGGER.get_logger("CPU"),
        )

        if start_up_hook:
            start_up_hook(self)

        self.__log("Start up complete!")

    def run(self):
        self.__processing_unit.run()

    def reset(self):
        self.__processing_unit.reset()


def start_up(computer: Computer):
    computer.run()


def main():
    logger = LOGGER.get_logger("MAIN")
    logger("Starting up")

    computer = Computer(8, logger=LOGGER.get_logger("COM"), start_up_hook=start_up)

    logger("Exitting")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
