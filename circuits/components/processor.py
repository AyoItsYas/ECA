from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Callable

from circuits.utils.formatting import bits_to_string

from circuits.components.bus import Bus
from circuits.adders import dynamic_adder


class CPU:
    def __init__(
        self,
        data_lines: Bus,
        address_lines: Bus,
        clock_speed: float,
        *,
        size: int = 8,
        logger: Callable[[str, str], None],
    ):
        self.__log = logger

        self.size = size
        self.clock_speed = clock_speed

        self.__data_lines = data_lines
        self.__address_lines = address_lines
        self.__program_counter = Bus(len(address_lines))

        self.__run_flag = True

        self.__instruction_set = {
            "0b00000000": self.NULL,
            "0b00000001": self.JMP_,
            "0b00000010": self.LDA_,
        }

    def fetch(self):
        addr = self.__address_lines.read()
        data = self.__data_lines.read()
        self.__log(f"FET {bits_to_string(addr, 'addr')} >>> {bits_to_string(data)}")

    def decode(self):
        data = self.__data_lines.read()
        op_code = bits_to_string(data)

        self.__circuit: Callable = self.__instruction_set.get(op_code, lambda x: None)

        self.__log(
            f"DEC {op_code} ({bits_to_string(data, 'h')}) >>> {self.__circuit.__name__}"
        )

    def execute(self):
        value = self.__circuit()
        self.__log(f"EXE {self.__circuit.__name__} >>> {value}")

    def increment_program(self):
        program_counter = self.__program_counter.read()
        new_program_counter, carry = dynamic_adder(
            program_counter, (0,) * len(program_counter) + (1,)
        )

        if carry:
            self.__program_counter.write((0,) * 3)
        else:
            self.__program_counter.write(new_program_counter)

        self.__data_lines.write((1,) * 8)
        self.__address_lines.write((1, *self.__program_counter.read()))

    def cycle(self):
        if not self.__run_flag:
            return

        self.fetch()
        self.decode()
        self.execute()

    def reset(self):
        self.__run_flag = False

    def NULL(self):
        return None

    def JMP_(self):
        return False

    def LDA_(self):
        return False
