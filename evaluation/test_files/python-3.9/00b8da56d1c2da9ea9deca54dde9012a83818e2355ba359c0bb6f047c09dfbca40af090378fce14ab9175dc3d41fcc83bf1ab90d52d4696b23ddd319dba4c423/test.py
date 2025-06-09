import unittest

def assert_almost_equal(first, second, places=7, delta=None, msg=None):
    return unittest.TestCase().assertAlmostEqual(first, second, places=places, msg=msg, delta=delta)

def assert_dict_equal(first, second, msg=None):
    return unittest.TestCase().assertDictEqual(first, second, msg)

def assert_equal(first, second, msg=None):
    return unittest.TestCase().assertEqual(first, second, msg)

def assert_false(expr, msg=None):
    return unittest.TestCase().assertFalse(expr, msg)

def assert_is(first, second, msg=None):
    return unittest.TestCase().assertIs(first, second, msg)

def assert_is_instance(obj, cls, msg=None):
    return unittest.TestCase().assertIsInstance(obj, cls, msg)

def assert_is_none(expr, msg=None):
    return unittest.TestCase().assertIsNone(expr, msg)

def assert_logs(logger=None, level=None):
    return unittest.TestCase().assertLogs(logger, level)

def assert_no_logs(logger=None, level=None):
    return unittest.TestCase().assertNoLogs(logger, level)

def assert_raises(exception, *, msg=None):
    return unittest.TestCase().assertRaises(exception, msg)

def assert_sequence_equal(first, second, msg=None, seq_type=None):
    return unittest.TestCase().assertSequenceEqual(first, second, msg, seq_type)

def assert_true(expr, msg=None):
    return unittest.TestCase().assertTrue(expr, msg)