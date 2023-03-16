from __future__ import annotations

import copy
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Callable, Iterable
    from circuits.components.bus import Bus

from circuits.gates import gate_and, gate_not, gate_or
from circuits.utils.formatting import bits_to_string


class UniqueCopy(object):
    def __init__(self, body, coppier=copy.deepcopy):
        self.body = body
        self.coppier = coppier

    def __mul__(self, n):
        return [self.coppier(x) for x in (self.body * n)]


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

    def circuit(self, set: bool = False, reset: bool = False) -> bool:
        self.__charge = gate_and([gate_or([self.__charge, set]), gate_not(reset)])
        return self.__charge

    def set(self) -> Latch:
        self.circuit(True)
        return self

    def reset(self) -> Latch:
        self.circuit(False, True)
        return self


class Memory:
    __memory_matrix: list[list[Latch]]

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

        self.__memory_matrix = UniqueCopy(UniqueCopy([UniqueCopy([Latch()]) * 8])) * (
            2 ** (len(address_lines) - 1)
        )

        self.__log(f"Memory size {len(self.__memory_matrix):,} bytes")

    def decode_hook(self):
        data = self.__data_lines.read()
        addr_o = self.__address_lines.read()

        ctrl, addr = addr_o[0], addr_o[1:]

        # preparing the lines that feed the decoder circuit

        decoder_lines = []
        addr_i = [gate_not(x) for x in addr]
        i, step, size = 0, 1, 2 ** len(addr)
        while step < size:
            line = [*[addr[i]] * step, *[addr_i[i]] * step]
            line = line * (size // len(line))

            decoder_lines += [line]

            i, step = i + 1, step * 2

        # feeding the decoder the data and address values

        decoder_lines = [gate_and(line) for line in zip(*decoder_lines)]
        decoder_lines.reverse()

        # isolating the latches responsible for the address

        latches: list[Latch] = None
        for decode, latches in zip(decoder_lines, self.__memory_matrix):
            if decode:
                break

        data = []
        for latch, new_value in zip(latches, self.__data_lines.read()):
            data.append(latch.circuit(new_value, ctrl) if ctrl and new_value else latch())

        self.__data_lines.write(data)

        # logging

        format_skel = "DEC {} >>> {}".format(
            bits_to_string(addr_o, "addr"), bits_to_string(data)
        )
        self.__log(format_skel)

    def set_memory_image(self, memory_image: Iterable[Iterable[Latch]]):
        from circuits.adders import dynamic_adder

        memory_image += UniqueCopy(UniqueCopy([UniqueCopy([Latch()]) * 8])) * (
            (2 ** (len(self.__address_lines) - 1)) - len(memory_image)
        )

        addr = self.__address_lines.read()
        incr = ([0] * (len(self.__address_lines) - 1)) + [1]  # address increment

        for latches in memory_image:
            self.__data_lines.write([latch() for latch in latches])
            addr, _ = dynamic_adder(addr, incr)
            addr[0] = 1  # setting the first bit as control to write to memory
            self.__address_lines.write(addr)

            self.decode_hook()

        for x, (image_latches, matrix_latches) in enumerate(
            zip(memory_image, self.__memory_matrix)
        ):
            for y, (image_latch, _) in enumerate(zip(image_latches, matrix_latches)):
                if image_latch():
                    self.__memory_matrix[x][y].set()

        self.__data_lines.reset()
        self.__address_lines.reset()

        self.__log("Memory image written!")


class RAM(Memory):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
