from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Callable

import time

from circuits.components.bus import Bus


class ArithmeticLogicUnit:
    def compute(
        self, opcode: list[bool], lines_in_A: list[bool], lines_in_B: list[bool]
    ) -> list[bool]:
        return


class CPU:
    def __init__(
        self,
        data_lines: Bus,
        address_lines: Bus,
        clock_speed: float,
        *,
        size: int = 8,
        logger: Callable,
    ):
        self.__log = logger

        self.size = size
        self.clock_speed = clock_speed

        self.__instruction = 0
        self.__instruction_address = 0

        self.__data_lines = data_lines
        self.__address_lines = address_lines

        self.__run_flag = True

        self.__log("Start up complete!")

    def fetch(self):
        self.__log("Fetching")
        pass

    def decode(self):
        self.__log("Decoding")
        pass

    def execute(self):
        self.__log("Executing")
        pass

    def cycle(self):
        self.__log("Cycle start")

        self.fetch()
        self.decode()
        self.execute()

        self.__log("Cycle end")

    def run(self):
        self.__log("Starting processor cycle")
        while self.__run_flag:
            cycle_s = time.perf_counter()
            self.cycle()
            cycle_e = time.perf_counter()

            cycle_d = cycle_e - cycle_s

            if cycle_d > self.clock_speed:
                pass  # raise a warning as the clock speed can't catch up
            else:
                time.sleep(self.clock_speed - cycle_d)

        self.__log("Ending processor cycle")

    def reset(self):
        self.__run_flag = False
