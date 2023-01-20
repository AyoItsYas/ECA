from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Callable, Iterable


from circuits.gates import gate_and, gate_or, gate_not


class Latch:
    def __init__(self):
        self.__charge = False

    def __call__(self) -> bool:
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
        self, *, matrix_size, multiplexer: Callable[[Iterable[bool]], Iterable[bool]]
    ):
        self.matrix_size = matrix_size

        self.__memory_matrix = None

        self.__buffer = None
        self.__buffer_size = matrix_size // 2
        self.__buffer_cut = self.__buffer_size // 2

        self.__multiplexer = multiplexer

        self.reset()

    def reset(self):
        self.__buffer = [0] * self.__buffer_size
        self.__memory_matrix: list[list[Latch]] = [
            [Latch()] * self.matrix_size
        ] * self.matrix_size

    def plex(self, set: bool, address: Iterable[bool]):
        row, col = address[0 : self.__buffer_cut], address[self.__buffer_cut :]
        self.__buffer = self.__multiplexer(set, row)
        self.__buffer = self.__multiplexer(set, col)

    def fetch(self, address: Iterable[bool]) -> Iterable[bool]:
        self.plex(address)
        return self.__buffer

    def read(self, address: Iterable[bool]) -> Iterable[bool]:
        return self.fetch(False, address)


class ReadOnlyMemeory(Memory):
    def write(self, *args, **kwargs) -> None:
        raise NotImplementedError


class RandomAccessMemory(Memory):
    def write(self, address: Iterable[bool]) -> Iterable[bool]:
        raise self.fetch(True, address)
