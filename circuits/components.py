import time


class ALU:
    def compute(
        self, opcode: list[bool], lines_in_A: list[bool], lines_in_B: list[bool]
    ) -> list[bool]:
        return


class CPU:
    def __init__(self, clock_speed: float):
        self.clock_speed = clock_speed

    def cycle(self):
        pass

    def run(self):
        while True:
            cycle_s = time.perf_counter()
            self.cycle()
            cycle_e = time.perf_counter()

            cycle_d = cycle_e - cycle_s

            if cycle_d > self.clock_speed:
                pass  # raise a warning as the clock speed can't catch up
            else:
                time.sleep(self.clock_speed - cycle_d)
