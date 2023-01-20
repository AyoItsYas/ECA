from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from memory import Memory

import time

from circuits.components.memory import RandomAccessMemory


class ArithmeticLogicUnit:
    def compute(
        self, opcode: list[bool], lines_in_A: list[bool], lines_in_B: list[bool]
    ) -> list[bool]:
        return


class CentralProcessingUnit:
    def __init__(self, clock_speed: float, *, size: int = 16):
        self.size = size
        self.clock_speed = clock_speed

        self.__instruction = 0
        self.__instruction_address = 0

        self.__memory: Memory = RandomAccessMemory(size=16)

    def fetch(self):
        self.__memory.read()
        pass

    def decode(self):
        pass

    def execute(self):
        pass

    def cycle(self):
        self.fetch()
        self.decode()
        self.execute()

    def run(self):
        self.__status = 0

        while True:
            cycle_s = time.perf_counter()
            self.cycle()
            cycle_e = time.perf_counter()

            cycle_d = cycle_e - cycle_s

            if cycle_d > self.clock_speed:
                pass  # raise a warning as the clock speed can't catch up
            else:
                time.sleep(self.clock_speed - cycle_d)
