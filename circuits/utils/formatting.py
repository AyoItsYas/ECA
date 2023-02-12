from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Iterable, Union


def bits_to_string(
    bit_stream: Iterable[bool],
    format: str = "b",
    format_spec: str = None,
    return_args: bool = False,
) -> Union[str, tuple[str]]:
    if format == "b":
        format_spec = format_spec or "0b{}"
        format_args = ("".join("1" if x else "0" for x in bit_stream),)
    elif format == "h":
        format_spec = format_spec or "{}"
        format_args = (str(hex(int("".join("1" if x else "0" for x in bit_stream)))),)
    elif format == "o":
        format_spec = format_spec or "{}"
        format_args = (str(oct(int("".join("1" if x else "0" for x in bit_stream)))),)
    elif format == "addr":
        format_spec = format_spec or "{} {} ({})"
        format_args = (
            "W" if bit_stream[0] else "R",
            bits_to_string(bit_stream[1:]),
            bits_to_string(bit_stream[1:], "h"),
        )
    else:
        format_spec, format_args = None, None

    return format_args if return_args else format_spec.format(*format_args)
