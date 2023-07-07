from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Iterable


class Bus:
    def __init__(self, size: int = 8):
        self.size = size
        self.__value = (0,) * size

    def __call__(self, value: Iterable[bool] = None):
        return self.read() if value is None else self.write(value)

    def __len__(self):
        return len(self.__value)

    def read(self) -> Iterable[bool]:
        return self.__value

    def write(self, value: Iterable[bool]):
        value_l, write_value_l = len(value), len(self.__value)

        if value_l > write_value_l:
            value = value[-(write_value_l):]
            pass
        elif value_l < write_value_l:
            value = [0] * (write_value_l - value_l)
            pass

        self.__value = value
        return self.__value

    def reset(self):
        self.write((0,) * self.size)
