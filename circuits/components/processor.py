from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Callable, Iterable
    from circuits.components.memory import Memory, Latch

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
        memory_module: Memory,
        *,
        logger: Callable[[str, str], None],
        hooks_fetch: list[Callable] = None,
        hooks_decode: list[Callable] = None,
        hooks_execute: list[Callable] = None,
    ):
        self.clock = clock
        self.memory = memory_module

        self.__log = lambda *x, **y: logger(*x, origin=__name__, **y)

        self.__data_lines = data_lines
        self.__address_lines = address_lines
        self.__program_counter = Bus(8)

        self.__register_A = Bus()  # 00
        self.__register_B = Bus()  # 01

        self.__instruction_set = {
            "0b00000000": self.NULL,
            "0b00000001": self.JUMP,
            "0b00000010": self.LDAV,
            "0b00000011": self.DMPM,
            "0b00000100": self.ACCM,
            "0b00000101": self.PRNT,
        }

        self.__hooks_fetch = hooks_fetch
        self.__hooks_decode = hooks_decode
        self.__hooks_execute = hooks_execute

        self.__circuit: Callable = lambda: None

    def fetch(self):
        """Read the data lines and address lines"""
        if self.__hooks_fetch:
            [hook() for hook in self.__hooks_fetch]

        self.memory.decode_hook()

        data = self.__data_lines.read()
        addr = self.__address_lines.read()
        self.__log(
            f"FET {bits_to_string(addr, 'addr')} >>> {bits_to_string(data)}", "DEBG"
        )

    def decode(self):
        """Decode instruction and set the processor cicuit to peform the instruction"""
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

        self.__circuit()  # execute the insturction circuit

        self.__log(f"EXE {self.__circuit.__name__}", "DEBG")

        self.__address_lines.write(self.__program_counter.read())

    def increment_program(self, increment: int = 1):
        """Increment the program counter"""

        increment = bin(increment)
        increment = [int(x) for x in increment[2:]]

        program_counter = self.__program_counter.read()
        new_program_counter, carry = dynamic_adder(
            program_counter, (0,) * (len(program_counter) - len(increment)) + increment
        )

        new_program_counter = (
            self.__program_counter.write((0,) * len(program_counter))
            if carry
            else new_program_counter
        )

        self.__program_counter.write(new_program_counter)

    def cycle(self):
        self.__log("Start of cycle!")
        cycle_s = time.perf_counter()

        self.fetch()
        self.decode()
        self.execute()

        cycle_e = time.perf_counter()

        cycle_d = cycle_e - cycle_s

        self.__log("End of cycle!")

        if cycle_d > self.clock:
            self.__log(f"Falling behind clock! {cycle_d * 1000}ms", "WARN")
        else:
            time.sleep(self.clock - cycle_d)

    def decode_register(self, index: Iterable[bool]):
        if not index[-1]:
            register = self.__register_A
        else:
            register = self.__register_B

        return register

    def decode_parameter(self, index: Iterable[bool] = None):
        crnt_addr = index or self.__address_lines.read()  # current address
        prmt_addr, _ = dynamic_adder(
            crnt_addr, (0,) * len(crnt_addr) + (1,)
        )  # parameter address
        prmt_addr[0] = False  # set the first bit to 0 to read

        self.__address_lines.write(prmt_addr)
        self.fetch()
        prmt_value = self.__data_lines.read()

        return prmt_value, prmt_addr

    def NULL(self):
        self.increment_program()

    def JUMP(self):  # Jump the program counter
        jump_addr, _ = self.decode_parameter()

        self.__program_counter.write(jump_addr)

    def LDAV(self):  # Load a value to a register
        para_1, para_n = self.decode_parameter()  # register to load to
        para_2, para_n = self.decode_parameter(para_n)  # value to load

        register: Bus = self.decode_register(para_1)
        register.write(para_2)

        self.increment_program(3)

    def LDVM(self):  # Load a memory value to a register
        para_1, para_n = self.decode_parameter()  # register to load to
        para_2, para_n = self.decode_parameter(para_n)  # value to load

        self.__address_lines.write(para_2)
        self.fetch()
        value = self.__data_lines.read()

        register: Bus = self.decode_register(para_1)
        register.write(value)

        self.increment_program(3)

    def DMPM(self):
        self.increment_program()

    def ACCM(self):
        self.increment_program()

    def PRNT(self):
        para_1, _ = self.decode_parameter()

        self.__address_lines.write(para_1)
        self.fetch()
        value: list[Latch] = self.__data_lines.read()

        self.__log(f"{value}", "INFO")

        self.increment_program(2)
