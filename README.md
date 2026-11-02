# roman_numerals_tools

Convert between integers in `1..3999` and canonical Roman numerals.

```python
from roman_numerals_tools import from_roman, to_roman

to_roman(1987)        # 'MCMLXXXVII'
from_roman('MMXXIV')  # 2024
```

## Why this exists

Roman numerals have no zero and no single widely agreed notation above 3999,
and many strings of `I`, `V`, `X`, `L`, `C`, `D`, `M` are not the canonical
form of any number (`IIII`, `VV`, `IC`). Rather than guess what a caller
meant, this library picks one interpretation and sticks to it: it only
produces and accepts the shortest representation, and it rejects anything
else with `ValueError`. That means `from_roman('IIII')` raises instead of
returning `4`, and `to_roman(4000)` raises instead of inventing an overbar
convention. The trade-off is strictness for predictability: every accepted
input round-trips exactly, and every rejected input is rejected for a
reason the caller can act on.

## API

- `to_roman(number: int) -> str` — returns the canonical Roman numeral for
  `number`. Raises `TypeError` if `number` is not an `int` (and `bool` is
  rejected even though it is a subclass of `int`), and `ValueError` if it is
  outside `1..3999`.
- `from_roman(text: str) -> int` — parses a canonical Roman numeral and
  returns its integer value. Raises `TypeError` for non-strings, and
  `ValueError` for empty strings, unknown characters, and non-canonical
  forms such as `IIII` or `VX`.

## The awkward edge

The one that surprises people is `from_roman('IIII')`. A left-to-right
parser will happily compute `4`, but `4` is written `IV`. Because this
library defines its input language as "canonical Roman numerals only",
`IIII` is not a valid input and raises `ValueError`. If you need to accept
non-canonical input, normalise it first (for example by parsing to an int
with your own rules and calling `to_roman`).
