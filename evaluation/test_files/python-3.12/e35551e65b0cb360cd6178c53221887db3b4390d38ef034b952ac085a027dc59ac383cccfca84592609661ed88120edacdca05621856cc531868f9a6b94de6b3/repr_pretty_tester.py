from typing import Any

class FakePrinter:
    """A fake of iPython's PrettyPrinter which captures text added to this printer.

    Can be used in tests to test a classes `_repr_pretty_` method:

    >>> p = FakePrinter()
    >>> s = object_under_test._repr_pretty(p, cycle=False)
    >>> p.text_pretty
    'my pretty_text'

    Prefer to use `assert_repr_pretty` below.
    """

    def __init__(self):
        self.text_pretty = ''

    def text(self, to_print):
        self.text_pretty += to_print

def assert_repr_pretty(val: Any, text: str, cycle: bool=False):
    """Assert that the given object has a `_repr_pretty_` method that produces the given text.

    Args:
            val: The object to test.
            text: The string that `_repr_pretty_` is expected to return.
            cycle: The value of `cycle` passed to `_repr_pretty_`.  `cycle` represents whether
                the call is made with a potential cycle. Typically one should handle the
                `cycle` equals `True` case by returning text that does not recursively call
                the `_repr_pretty_` to break this cycle.

    Raises:
        AssertionError: If `_repr_pretty_` does not pretty print the given text.
    """
    p = FakePrinter()
    val._repr_pretty_(p, cycle=cycle)
    assert p.text_pretty == text, f'{p.text_pretty} != {text}'

def assert_repr_pretty_contains(val: Any, substr: str, cycle: bool=False):
    """Assert that the given object has a `_repr_pretty_` output that contains the given text.

    Args:
            val: The object to test.
            substr: The string that `_repr_pretty_` is expected to contain.
            cycle: The value of `cycle` passed to `_repr_pretty_`.  `cycle` represents whether
                the call is made with a potential cycle. Typically one should handle the
                `cycle` equals `True` case by returning text that does not recursively call
                the `_repr_pretty_` to break this cycle.

    Raises:
        AssertionError: If `_repr_pretty_` does not pretty print the given text.
    """
    p = FakePrinter()
    val._repr_pretty_(p, cycle=cycle)
    assert substr in p.text_pretty, f'{substr} not in {p.text_pretty}'