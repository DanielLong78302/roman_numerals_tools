"""Conversion between integers and Roman numerals.

Scope decisions (documented so callers are not surprised):

* Only values in ``1..3999`` are supported. Classical Roman numerals do not
  have a zero, and the subtractive notation is only well defined up to 3999;
  larger numbers require overbars or other conventions that this library does
  not implement.
* Output is always canonical: the shortest representation using the standard
  subtractive pairs (IV, IX, XL, XC, CD, CM).
* Input is validated strictly. ``from_roman`` rejects empty strings,
  non-canonical forms such as ``IIII`` or ``VX``, and values outside the
  supported range. Strictness is deliberate: silently accepting ``IIII``
  would make round-tripping ambiguous.
"""

from __future__ import annotations

__all__ = ["to_roman", "from_roman"]

# Ordered from largest to smallest. The subtractive pairs (900, 400, 90, 40,
# 9, 4) are placed before the symbols they subtract from so a single greedy
# pass produces the canonical form.
_VALUE_SYMBOLS: tuple[tuple[int, str], ...] = (
    (1000, "M"),
    (900, "CM"),
    (500, "D"),
    (400, "CD"),
    (100, "C"),
    (90, "XC"),
    (50, "L"),
    (40, "XL"),
    (10, "X"),
    (9, "IX"),
    (5, "V"),
    (4, "IV"),
    (1, "I"),
)

_SYMBOL_VALUES: dict[str, int] = {
    "I": 1,
    "V": 5,
    "X": 10,
    "L": 50,
    "C": 100,
    "D": 500,
    "M": 1000,
}

_MIN_VALUE = 1
_MAX_VALUE = 3999


def to_roman(number: int) -> str:
    """Return the canonical Roman numeral for ``number``.

    ``number`` must be an ``int`` in ``1..3999``. ``bool`` is rejected even
    though it is a subclass of ``int`` because ``True``/``False`` are almost
    certainly a caller bug here.

    Raises ``TypeError`` for non-integers and ``ValueError`` for out-of-range
    values.
    """
    if isinstance(number, bool) or not isinstance(number, int):
        raise TypeError(f"number must be an int, got {type(number).__name__}")
    if not _MIN_VALUE <= number <= _MAX_VALUE:
        raise ValueError(
            f"number must be between {_MIN_VALUE} and {_MAX_VALUE}, got {number}"
        )

    parts: list[str] = []
    remaining = number
    for value, symbol in _VALUE_SYMBOLS:
        # Integer division avoids float issues entirely; the loop terminates
        # because each value is strictly positive.
        count, remaining = divmod(remaining, value)
        if count:
            parts.append(symbol * count)
    return "".join(parts)


def from_roman(text: str) -> int:
    """Parse a canonical Roman numeral and return its integer value.

    ``text`` must be a non-empty ``str`` containing only the symbols
    ``I V X L C D M`` in a canonical arrangement. The result is in
    ``1..3999``.

    Raises ``TypeError`` for non-strings and ``ValueError`` for malformed or
    non-canonical input.
    """
    if not isinstance(text, str):
        raise TypeError(f"text must be a str, got {type(text).__name__}")
    if not text:
        raise ValueError("text must not be empty")

    total = 0
    previous_value = 0
    for char in text:
        value = _SYMBOL_VALUES.get(char)
        if value is None:
            raise ValueError(f"invalid Roman numeral character: {char!r}")
        if value > previous_value:
            # Subtractive pair: the previous symbol was smaller and must be
            # undone. Only a single preceding symbol can be subtracted in
            # canonical Roman numerals, which the canonicality check below
            # enforces.
            total -= 2 * previous_value
        total += value
        previous_value = value

    if not _MIN_VALUE <= total <= _MAX_VALUE:
        raise ValueError(f"value out of supported range: {total}")
    # Re-encoding is the simplest reliable canonicality check: any string that
    # does not round-trip is not the shortest representation of its value.
    if to_roman(total) != text:
        raise ValueError(f"non-canonical Roman numeral: {text!r}")
    return total
