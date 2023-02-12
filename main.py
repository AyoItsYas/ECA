from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Callable

import time

from circuits.utils.logger import Logger

from circuits.components.bus import Bus
from circuits.components.memory import RAM
from circuits.components.processor import CPU


LOGGER = Logger()


class Computer:
    def __init__(
        self,
        size: int,
        *,
        logger: Callable[[str, str], None],
        start_up_hook: Callable[[Computer]] = None,
    ):
        self.__log = logger

        self.clock_speed = 1

        self.__data_lines = Bus(size)
        self.__address_lines = Bus(16 + 1)

        self.__primary_memory = RAM(
            self.__data_lines,
            self.__address_lines,
            logger=LOGGER.get_logger("RAM"),
        )
        self.__processing_unit = CPU(
            self.__data_lines,
            self.__address_lines,
            self.clock_speed,
            size=size,
            logger=LOGGER.get_logger("CPU"),
        )

        if start_up_hook:
            start_up_hook(self)

    def run(self):
        self.__processing_unit.cycle()

        cycle_hooks = (
            self.__primary_memory.cycle,
            self.__processing_unit.cycle,
        )
        if self.clock_speed > 0:
            while True:
                cycle_s = time.perf_counter()
                for hook in cycle_hooks:
                    hook()
                cycle_e = time.perf_counter()

                cycle_d = cycle_e - cycle_s

                if cycle_d > self.clock_speed:
                    self.clock_speed = cycle_d * 1.25
                else:
                    time.sleep(self.clock_speed - cycle_d)
        else:
            while True:
                for hook in cycle_hooks:
                    hook()

    def reset(self):
        self.__processing_unit.reset()


def main():
    computer = Computer(8, logger=LOGGER.get_logger("COM"))
    computer.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
