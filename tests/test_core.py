"""Tests for roman_numerals_tools.core.

Run with: PYTHONPATH=src python -m unittest discover -s tests
"""

import unittest

from roman_numerals_tools import from_roman, to_roman


class ToRomanTests(unittest.TestCase):
    def test_single_symbols(self):
        cases = {
            1: "I",
            5: "V",
            10: "X",
            50: "L",
            100: "C",
            500: "D",
            1000: "M",
        }
        for number, expected in cases.items():
            with self.subTest(number=number):
                self.assertEqual(to_roman(number), expected)

    def test_subtractive_pairs(self):
        cases = {
            4: "IV",
            9: "IX",
            40: "XL",
            90: "XC",
            400: "CD",
            900: "CM",
        }
        for number, expected in cases.items():
            with self.subTest(number=number):
                self.assertEqual(to_roman(number), expected)

    def test_additive_forms(self):
        cases = {
            2: "II",
            3: "III",
            8: "VIII",
            14: "XIV",
            38: "XXXVIII",
            1987: "MCMLXXXVII",
            2024: "MMXXIV",
            3999: "MMMCMXCIX",
        }
        for number, expected in cases.items():
            with self.subTest(number=number):
                self.assertEqual(to_roman(number), expected)

    def test_lower_bound(self):
        self.assertEqual(to_roman(1), "I")

    def test_upper_bound(self):
        self.assertEqual(to_roman(3999), "MMMCMXCIX")

    def test_zero_is_rejected(self):
        with self.assertRaises(ValueError):
            to_roman(0)

    def test_negative_is_rejected(self):
        with self.assertRaises(ValueError):
            to_roman(-1)

    def test_above_upper_bound_is_rejected(self):
        with self.assertRaises(ValueError):
            to_roman(4000)

    def test_bool_is_rejected(self):
        # bool is a subclass of int, but True/False are almost certainly a
        # mistake at a call site that expects a number.
        with self.assertRaises(TypeError):
            to_roman(True)

    def test_non_int_is_rejected(self):
        for bad in ("1", 1.0, None):
            with self.subTest(bad=bad):
                with self.assertRaises(TypeError):
                    to_roman(bad)


class FromRomanTests(unittest.TestCase):
    def test_round_trip(self):
        for number in range(1, 4000):
            with self.subTest(number=number):
                self.assertEqual(from_roman(to_roman(number)), number)

    def test_known_values(self):
        cases = {
            "I": 1,
            "IV": 4,
            "IX": 9,
            "XL": 40,
            "XC": 90,
            "CD": 400,
            "CM": 900,
            "MCMLXXXVII": 1987,
            "MMXXIV": 2024,
            "MMMCMXCIX": 3999,
        }
        for text, expected in cases.items():
            with self.subTest(text=text):
                self.assertEqual(from_roman(text), expected)

    def test_empty_string_is_rejected(self):
        with self.assertRaises(ValueError):
            from_roman("")

    def test_invalid_character_is_rejected(self):
        for bad in ("A", "i", "X1", "MMM "):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    from_roman(bad)

    def test_non_canonical_forms_are_rejected(self):
        # These all have a valid arithmetic interpretation under a naive
        # left-to-right parser, but they are not the shortest representation
        # of their value and so are rejected.
        for bad in ("IIII", "VV", "IC", "IM", "XXXX", "CMCM", "MCMC"):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    from_roman(bad)

    def test_non_string_is_rejected(self):
        for bad in (1, None, ["X"]):
            with self.subTest(bad=bad):
                with self.assertRaises(TypeError):
                    from_roman(bad)


if __name__ == "__main__":
    unittest.main()
