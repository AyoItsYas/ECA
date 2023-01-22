from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Callable, Iterable


from circuits.gates import gate_and, gate_or, gate_not


class Latch:
    """A latch circuit emulating the functionality of an AND-OR latch."""

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
        """An abstract class to base any type of memory.

        Args:
            matrix_size (_type_): Matrix size of the memory.
            multiplexer (Callable[[Iterable[bool]], Iterable[bool]]): Multiplexer circuit handling the selction of rows, columns of the matrix.
        """
        self.__matrix_size = matrix_size

        self.__memory_matrix = None

        self.__buffer = None
        self.__buffer_size = matrix_size // 2
        self.__buffer_cut = self.__buffer_size // 2

        self.__multiplexer = multiplexer

        self.reset()

    def reset(self):
        """Rests the memory matrix and the buffer lines."""
        self.__buffer = [0] * self.__buffer_size
        self.__memory_matrix: list[list[Latch]] = [
            [Latch()] * self.__matrix_size
        ] * self.__matrix_size

    def plex(self, set: bool, address: Iterable[bool]):
        """Calls the multiplexer citcuit and dumps the data line values into the memeory buffer lines.

        Args:
            set (bool): Line in for setting or reseting the latches.
            address (Iterable[bool]): Memory address the size of the buffer size.
        """
        row, col = address[0 : self.__buffer_cut], address[self.__buffer_cut :]
        self.__buffer = self.__multiplexer(set, row)
        self.__buffer = self.__multiplexer(set, col)

    def fetch(
        self, address: Iterable[bool], value: Iterable[bool] = None
    ) -> Iterable[bool]:
        """Fetches the values at a given address.

        Args:
            address (Iterable[bool]): Memory address the size of the buffer size.

        Returns:
            Iterable[bool]: Stored values on the given address.
        """
        self.plex(address)
        return self.__buffer

    def read(self, address: Iterable[bool]) -> Iterable[bool]:
        """Reads the values at a given address.

        Args:
            address (Iterable[bool]): Memory address the size of the buffer size.

        Returns:
            Iterable[bool]: Stored values on the given address.
        """
        return self.fetch(False, address)


class ReadOnlyMemeory(Memory):
    def write(self, *args, **kwargs) -> None:
        """
        Raises:
            NotImplementedError: Unsupported.
        """
        raise NotImplementedError


class RandomAccessMemory(Memory):
    def write(self, address: Iterable[bool], value: Iterable[bool]) -> None:
        """Writes the giiven values to a given address.

        Args:
            address (Iterable[bool]): Memory address the size of the buffer size.
        """
        self.fetch(True, address, value)
