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
        self.__log = lambda *x, **y: logger(*x, origin=__name__, **y)

        self.__data_lines = data_lines
        self.__address_lines = address_lines

        # make a memory matrix

        matrix = []
        for _ in range(2 ** (len(address_lines) - 1)):
            matrix.append([Latch() for _ in range(8)])

        self.__memory_matrix = matrix

        self.__memory_matrix

        self.__log(f"Memory size {len(self.__memory_matrix):,} bytes")

    def decode_hook(self):
        data = self.__data_lines.read()
        addr_o = self.__address_lines.read()  # storing the address

        ctrl, addr = addr_o[0], addr_o[1:]
        addr_inv = [gate_not(x) for x in addr]

        # preping decoder lines and logic

        size = 2 ** len(addr)
        decoder_lines: list[
            list
        ] = []  # arranging the lines in the form of a truth table for the decoder

        i = 0
        x = size // 2
        while x > 0:
            y = 0
            deck = False
            for _ in range(size // x):
                for _ in range(x):
                    decoder_lines.append(addr[i] if deck else addr_inv[i])
                    y += 1

                deck = not deck

            i += 1
            x = x // 2

        decoder_lines = [
            decoder_lines[i : i + size] for i in range(0, len(decoder_lines), size)
        ]  # arranging the lines to be fed into logic

        decoder_lines = [
            gate_and(x) for x in zip(*decoder_lines)
        ]  # feeding the lines into logic and finalizing the address select

        # decode the address and perform action

        for decode, byte in zip(decoder_lines, self.__memory_matrix):
            if decode:
                self.__data_lines.write(byte)
                if ctrl:
                    for latch, value in zip(byte, data):
                        latch.circuit(value)

        # logging

        format_skel = "DEC {} >>> {}".format(
            bits_to_string(addr_o, "addr"), bits_to_string(data)
        )
        self.__log(format_skel, "DEBG")

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
