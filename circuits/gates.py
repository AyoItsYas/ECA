from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Iterable


def transistor(
    control: bool, line_in: bool, *, grounded_out: bool = False, return_line: int = 2
) -> bool:
    if grounded_out and control:
        line_out = line_in
        line_in = False
    else:
        line_out = line_in if control else False

    return (control, line_in, line_out)[return_line]


def gate_not(line_in: bool) -> bool:
    return transistor(line_in, True, grounded_out=True, return_line=1)


def gate_and(lines_in: Iterable[bool]) -> bool:
    result = True

    for line_in in lines_in:
        result = transistor(line_in, result)

    return result


def gate_or(lines_in: Iterable[bool]) -> bool:
    result = True

    for line_in in lines_in:
        result = transistor(line_in, True)

        if result:
            break

    return result


def gate_nand(lines_in: Iterable[bool]):
    return gate_not(gate_and(lines_in))


def gate_xor(line_in_A: bool, line_in_B: bool) -> bool:
    return gate_and(
        (gate_or((line_in_A, line_in_B)), gate_nand((line_in_A, line_in_B)))
    )
