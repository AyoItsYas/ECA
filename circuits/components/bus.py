from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Iterable


class Bus:
    def __init__(self, size: int = 8):
        self.__value = (0,) * size

    def __call__(self, value: Iterable[bool] = None):
        return self.read() if value is None else self.write(value)

    def __len__(self):
        return len(self.__value)

    def read(self) -> Iterable[bool]:
        return self.__value

    def write(self, value: Iterable[bool]):
        if len(value) != len(self.__value):
            return

        self.__value = value
        return self.__value
