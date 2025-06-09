import pytest
from wpiutil_test import module
import array

def test_span_load_int():
    assert module.load_span_int([1, 2, 3, 4]) == [1, 2, 3, 4]

def test_span_load_int():
    assert module.load_span_int([1, 2, 3]) == [1, 2, 3]

def test_span_load_bool():
    assert module.load_span_bool([True, False, True]) == [True, False, True]

def test_span_load_string():
    assert module.load_span_string(['a', 'b', 'c']) == ['a', 'b', 'c']

def test_span_load_string_const():
    assert module.load_span_string_const(['a', 'b', 'c']) == ['a', 'b', 'c']

def test_span_load_stringview():
    assert module.load_span_string_view(['a', 'b', 'c']) == ['a', 'b', 'c']

def test_span_load_vector():
    assert module.load_span_vector([['a'], ['b'], ['c']]) == [['a'], ['b'], ['c']]

def test_span_load_buffer_bytes():
    assert module.load_span_bytes(b'abc') == b'abc'

def test_span_modify_buffer_bytes():
    b = b'abc'
    with pytest.raises(BufferError):
        module.modify_span_buffer(b)

def test_span_load_buffer_bytearray():
    assert module.load_span_bytes(bytearray([1, 2, 3])) == b'\x01\x02\x03'

def test_span_modify_buffer_bytearray():
    b = bytearray([1, 2, 3])
    module.modify_span_buffer(b)
    assert b == bytearray([4, 2, 3])

def test_span_load_buffer_array():
    a = array.array('l')
    a.append(1)
    a2 = array.array('l')
    a2.frombytes(module.load_span_bytes(a))
    assert len(a2) == 1
    assert a2[0] == 1

def test_span_cast():
    assert module.cast_span() == [1, 2, 3]

def test_string_span():
    assert module.cast_string_span() == ['hi', 'there']

def test_fixed_double_span():
    assert module.load_span_fixed_double([1, 2, 3]) == (1, 2, 3)
    with pytest.raises(TypeError):
        assert module.load_span_fixed_double([1, 2, 3, 4])