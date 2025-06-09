import os
import unittest
from mock import patch
from liquid import Template
from liquid import Mode
from liquid.exceptions import LiquidValueError
from liquid.limits import MAX_STR_INT
from liquid.limits import _init_int_max_str_digits

class StrToIntTestCase(unittest.TestCase):

    def test_parse_long_integer_literal(self):
        """Test that we honour the maximum str to int length on integer literals."""
        Template(''.join(['{{', '1' * MAX_STR_INT, ' }}']))
        with self.assertRaises(LiquidValueError):
            Template(''.join(['{{', '1' * (MAX_STR_INT + 1), ' }}']))

    def test_math_filter_long_string_literal(self):
        """Test that we honour the maximum str to int length on string literals."""
        template = Template(''.join(["{{ '", '1' * MAX_STR_INT, "' | abs }}"]))
        self.assertEqual(template.render(), '1' * MAX_STR_INT)
        template = Template(''.join(["{{ '", '1' * (MAX_STR_INT + 1), "' | abs }}"]), tolerance=Mode.STRICT)
        with self.assertRaises(LiquidValueError):
            self.assertEqual(template.render(), '1' * (MAX_STR_INT + 1))

    @patch.dict(os.environ, {'LIQUIDINTMAXSTRDIGITS': 'hello'})
    def test_liquid_max_not_digit(self):
        """Test that we handle liquid environment variables that not digits."""
        with self.assertRaises(TypeError):
            _init_int_max_str_digits()

    @patch.dict(os.environ, {'LIQUIDINTMAXSTRDIGITS': '5'})
    def test_max_digits_too_small(self):
        """Test that we handle environment variables that are too small."""
        with self.assertRaises(ValueError):
            _init_int_max_str_digits()

    @patch.dict(os.environ, {'LIQUIDINTMAXSTRDIGITS': '1000'})
    def test_set_liquid_max(self):
        """Test that we can set LIQUIDINTMAXSTRDIGITS."""
        self.assertEqual(_init_int_max_str_digits(), 1000)

    @patch.dict(os.environ, {'LIQUIDINTMAXSTRDIGITS': '0'})
    def test_zero_is_ok(self):
        """Test that zero is OK"""
        self.assertEqual(_init_int_max_str_digits(), 0)