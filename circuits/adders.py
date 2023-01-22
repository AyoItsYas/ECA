from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Callable


from circuits.gates import gate_and, gate_xor


def half_adder(line_in_A: bool, line_in_B: bool) -> tuple[bool, bool]:
    """Half adder circuit to perform bianary additions.

    Args:
        line_in_A (bool): Line A for the circuit.
        line_in_B (bool): Line B for the circuit.

    Returns:
        tuple[bool, bool]: Line out carrying the sum and carry respectively.
    """
    return gate_xor(line_in_A, line_in_B), gate_and([line_in_A, line_in_B])


def dynamic_adder(
    lines_in_A: list[bool],
    lines_in_B: list[bool],
    *,
    adder: Callable[[bool, bool], tuple[bool, bool]] = half_adder,
) -> tuple[list[bool], bool]:
    """A dynamic adder that can be used to perform bianry addition while handling the bit size.

    Args:
        lines_in_A (list[bool]): Line A bits.
        lines_in_B (list[bool]): Line B bits.
        adder (Callable[[bool, bool], tuple[bool, bool]], optional):
            A callable adder circuit that returns the sum and carry for given two bits.
            Defaults to half_adder.

    Returns:
        tuple[list[bool], bool]: Returns the sum and carry for the given bits respectively.
    """
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
