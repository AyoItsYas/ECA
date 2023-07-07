from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Iterable


def transistor(
    control: bool, line_in: bool, *, grounded_out: bool = False, return_line: int = 2
) -> bool:
    """Emulates the functionality of a transistor.

    Args:
        control (bool): Line in for control
        line_in (bool): Line in for input
        grounded_out (bool, optional): Grounds the output line if set. Defaults to False.
        return_line (int, optional): What the returning line is defaults to the output line. Defaults to 2.

    Returns:
        bool: Line out for the returning line.
    """
    if grounded_out and control:
        line_out = line_in
        line_in = False
    else:
        line_out = line_in if control else False

    return_lines = (control, line_in, line_out)

    if return_line:
        return return_lines[return_line]
    else:
        return return_lines


def gate_not(line_in: bool) -> bool:
    """Emulates the functionality of a NOT gate.

    Args:
        line_in (bool): Line in for the gate.

    Returns:
        bool: Line out for the gate.
    """
    return transistor(line_in, True, grounded_out=True, return_line=1)


def gate_and(lines_in: Iterable[bool]) -> bool:
    """Emulates the functionality of an AND gate.

    Args:
        lines_in (Iterable[bool]): Line in(s) for the gate.

    Returns:
        bool: Line out for the gate.
    """
    result = True

    for line_in in lines_in:
        result = transistor(line_in, result)

    return result


def gate_or(lines_in: Iterable[bool]) -> bool:
    """Emulates the functionality of an OR gate.

    Args:
        lines_in (Iterable[bool]): Line in(s) for the gate.

    Returns:
        bool: Line out for the gate.
    """
    result = True

    for line_in in lines_in:
        result = transistor(line_in, True)

        if result:
            break

    return result


def gate_nand(lines_in: Iterable[bool]) -> bool:
    """Emulated the functionality of a NAND gate.

    Args:
        lines_in (Iterable[bool]): Line in(s) for the gate.

    Returns:
        bool: Line out for the gate.
    """
    return gate_not(gate_and(lines_in))


def gate_xor(line_in_A: bool, line_in_B: bool) -> bool:
    """Emulates the functionality of an XOR gate.

    Args:
        line_in_A (bool): Line A for the gate.
        line_in_B (bool): Line B for the gate.

    Returns:
        bool: Line out for the gate.
    """
    return gate_and(
        (gate_or((line_in_A, line_in_B)), gate_nand((line_in_A, line_in_B)))
    )
