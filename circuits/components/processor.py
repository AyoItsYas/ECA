from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Callable

import time

from circuits.utils.formatting import bits_to_string

from circuits.components.bus import Bus
from circuits.adders import dynamic_adder


class CPU:
    def __init__(
        self,
        data_lines: Bus,
        address_lines: Bus,
        clock: float,
        *,
        logger: Callable[[str, str], None],
        hooks_fetch: list[Callable] = None,
        hooks_decode: list[Callable] = None,
        hooks_execute: list[Callable] = None,
    ):
        self.clock = clock

        self.__log = lambda *x, **y: logger(*x, origin=__name__, **y)

        self.__data_lines = data_lines
        self.__address_lines = address_lines
        self.__program_counter = Bus(len(address_lines))

        self.__register_A = Bus()  # 00
        self.__register_B = Bus()  # 01
        self.__register_C = Bus()  # 10
        self.__register_D = Bus()  # 11

        self.__instruction_set = {
            "0b00000000": self.NULL,
            "0b00000001": self.JUMP,
            "0b00000010": self.LOAD,
            "0b00000011": self.ACCM,
        }

        self.__hooks_fetch = hooks_fetch
        self.__hooks_decode = hooks_decode
        self.__hooks_execute = hooks_execute

        self.__circuit: Callable = lambda: None

    def fetch(self):
        if self.__hooks_fetch:
            [hook() for hook in self.__hooks_fetch]

        data = self.__data_lines.read()
        addr = self.__address_lines.read()
        self.__log(
            f"FET {bits_to_string(addr, 'addr')} >>> {bits_to_string(data)}", "DEBG"
        )

    def decode(self):
        if self.__hooks_decode:
            [hook() for hook in self.__hooks_decode]

        data = self.__data_lines.read()
        op_code = bits_to_string(data)

        self.__circuit: Callable = self.__instruction_set.get(op_code, self.NULL)

        self.__log(
            f"DEC {op_code} ({bits_to_string(data, 'h')}) >>> {self.__circuit.__name__}",
            "DEBG",
        )

    def execute(self):
        if self.__hooks_execute:
            [hook() for hook in self.__hooks_execute]

        self.__log(f"EXE {self.__circuit.__name__}", "DEBG")

        self.__circuit()  # execute the insturction circuit

        self.__address_lines.write(self.__program_counter.read())

    def increment_program(self):
        program_counter = self.__program_counter.read()
        new_program_counter, carry = dynamic_adder(
            program_counter, (0,) * len(program_counter) + (1,)
        )

        new_program_counter = (
            self.__program_counter.write((0,) * len(program_counter))
            if carry
            else new_program_counter
        )

        self.__program_counter.write(new_program_counter)

    def cycle(self):
        cycle_s = time.perf_counter()

        self.fetch()
        self.decode()
        self.execute()

        cycle_e = time.perf_counter()

        cycle_d = cycle_e - cycle_s

        if cycle_d > self.clock:
            self.__log(f"Falling behind clock! {cycle_d * 1000}ms", "WARN")
        else:
            time.sleep(self.clock - cycle_d)

    def register_instruction(function):
        def wrapper(self):
            function(self)

        x = wrapper
        x.__name__ = function.__name__

        return x

    def NULL(self):
        self.increment_program()

    def JUMP(self):
        self.__address_lines.write(self.__program_counter.read())
        self.fetch()

        self.__program_counter.write(self.__data_lines.read())

        self.increment_program()

    def LOAD(self):
        self.increment_program()
        self.__address_lines.write(self.__program_counter.read())
        self.fetch()

        data = self.__data_lines.read()
        x, y = data[-2:]

        if not x and not y:
            register = self.__register_A
        elif not x and y:
            register = self.__register_B
        elif x and not y:
            register = self.__register_C
        else:
            register = self.__register_D

        self.increment_program()
        self.__address_lines.write(self.__program_counter.read())
        self.fetch()

        data = self.__data_lines.read()
        register.write(data)

    def ACCM(self):
        pass
