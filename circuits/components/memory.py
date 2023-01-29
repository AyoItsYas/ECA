from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Callable
    from circuits.components.bus import Bus


from circuits.gates import gate_and, gate_or, gate_not


class Latch:
    """A latch circuit emulating the functionality of an AND-OR latch."""

    def __init__(self):
        self.__charge = False

    def __call__(self) -> bool:
        return self.__charge

    def __repr__(self) -> str:
        return str(int(self.__charge))

    def __bool__(self) -> bool:
        return self.__charge

    def circuit(self, set: bool = False, reset: bool = False):
        self.__charge = gate_and([gate_or([self.__charge, set]), gate_not(reset)])
        return self.__charge

    def set(self):
        self.circuit(True)

    def reset(self):
        self.circuit(False, True)


class Memory:
    def __init__(
        self, data_lines: Bus, address_lines: Bus, *, size: int, logger: Callable
    ):
        self.__log = logger

        self.__data_lines = data_lines
        self.__address_lines = address_lines

        get_latch = lambda: Latch()
        self.__memory_matrix = [[get_latch()] * size] * size

        self.__log("Start up complete!")

    def decode(self) -> tuple[bool]:
        address = self.__address_lines.read()
        address_inverse = [gate_not(x) for x in address]

        self.__log(f"Decoding address > {address}")

        decoder_lines = []

        i, step, size = 0, 1, 2 ** len(address)
        while step < size:
            line = [*[address[i]] * step, *[address_inverse[i]] * step]
            line = line * (size // len(line))

            decoder_lines += [line]

            i, step = i + 1, step * 2

        return (gate_and(line) for line in zip(*decoder_lines))


class RAM(Memory):
    def __init__(
        self, data_lines: Bus, address_lines: Bus, *, size: int, logger: Callable
    ):
        super().__init__(data_lines, address_lines, size=size, logger=logger)
