"""Public API for roman_numerals_tools.

Exports two functions:

    to_roman(n: int) -> str
    from_roman(s: str) -> int

They are intentionally strict: the library converts between integers in
range 1..3999 and canonical (shortest) Roman numerals only. See README for
the reasoning.
"""

from .core import from_roman, to_roman

__all__ = ["to_roman", "from_roman"]
