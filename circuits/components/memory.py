from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Callable
    from circuits.components.bus import Bus


from circuits.utils.formatting import bits_to_string

from circuits.gates import gate_and, gate_or, gate_not


class Latch:
    """A latch circuit emulating the functionality of an AND-OR latch."""

    def __init__(self, charge: bool = False):
        self.__charge = charge

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
        return self.__call__()

    def reset(self):
        self.circuit(False, True)
        return self.__call__()


class Memory:
    def __init__(
        self,
        data_lines: Bus,
        address_lines: Bus,
        *,
        logger: Callable[[str, str], None],
    ):
        self.__log = logger

        self.__data_lines = data_lines
        self.__address_lines = address_lines

        get_latch = lambda: Latch()
        self.__memory_matrix = [[get_latch()] * 8] * (2 ** len(address_lines))

        self.__log(f"Memory size {len(self.__memory_matrix):,} bytes")

    def decode(self) -> tuple[bool]:
        address = _raw_address = self.__address_lines.read()

        address, reset = address[1:], address[0]
        address_inverse = [gate_not(x) for x in address]

        decoder_lines = []

        i, step, size = 0, 1, 2 ** len(address)
        while step < size:
            line = [*[address[i]] * step, *[address_inverse[i]] * step]
            line = line * (size // len(line))

            decoder_lines += [line]

            i, step = i + 1, step * 2

        decoder_lines = [gate_and(line) for line in zip(*decoder_lines)]
        decoder_lines.reverse()

        latches = []
        for decode, chunk in zip(decoder_lines, self.__memory_matrix):
            if decode:
                latches = chunk
                break

        data = []
        for latch, new_data in zip(latches, self.__data_lines.read()):
            data.append(latch.reset() if reset and new_data else latch())

        self.__data_lines.write(data)
        format_spec = "DEC {} >>> {}".format(
            bits_to_string(_raw_address, "addr"), bits_to_string(data)
        )
        self.__log(format_spec)

    def cycle(self):
        self.decode()


class RAM(Memory):
    def __init__(self, data_lines: Bus, address_lines: Bus, *, logger: Callable):
        super().__init__(data_lines, address_lines, logger=logger)
