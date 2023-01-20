from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Callable


from circuits.gates import gate_and, gate_xor


def half_adder(line_in_A: bool, line_in_B: bool) -> tuple[bool, bool]:
    return gate_xor(line_in_A, line_in_B), gate_and([line_in_A, line_in_B])


def dynamic_adder(
    lines_in_A: list[bool],
    lines_in_B: list[bool],
    *,
    adder: Callable[[bool, bool], tuple[bool, bool]] = half_adder,
) -> tuple[list[bool], bool]:
    result = []
    add_carry = None
    for line_in_A, line_in_B in zip(lines_in_A[::-1], lines_in_B[::-1]):

        sum, carry = adder(line_in_A, line_in_B)

        if add_carry:
            sum, _ = adder(sum, True)
            add_carry = False

        if carry:
            add_carry = True

        result.append(sum)

    result.reverse()
    return result, add_carry


dynamic_adder([0, 0, 1, 0], [0, 0, 1, 0])
dynamic_adder([0, 1, 0, 1], [0, 1, 0, 1])
dynamic_adder([1, 1, 1, 1], [1, 1, 1, 1])
dynamic_adder([1, 1, 1, 1, 1], [1, 1, 1, 1, 1])
