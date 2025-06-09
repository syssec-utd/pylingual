import pytest
import units as u
from units.constants.time import *
from units.constants.length import *

def test_units_representation():
    assert str(u.Units(2, {'sec': -2})) == '2 1/sec^2'
    assert str(u.Units(2.0, {'sec': -2})) == '2 1/sec^2'
    assert str(u.Units(2.2, {'sec': -2})) == '2.2 1/sec^2'
    assert str(u.Units(2, {'m': 1, 'sec': -2})) == '2 m/sec^2'
    assert str(u.Units(2, {'m': 1, 'sec': 2})) == '2 (m*sec^2)'
    assert str(u.Units(2, {'m': -1, 'sec': -2})) == '2 1/(m*sec^2)'
    assert str(u.Units(2, {'s': 0, 'm': -1})) == '2 1/m'

def test_conversion():
    assert str(u._convert_unit(m, km)) == '0.001 km'
    assert str(u._convert_unit(m, 'km')) == '0.001 km'
    assert str(u._convert_unit(m, ['km'])) == '0.001 km'
    assert str(u._convert_unit(km, m)) == '1000 m'
    with pytest.raises(AssertionError):
        print(sec / m >> km / hr)

def test_unit_vector():
    test_unit = u.Units(1, {'m': 1, 'sec': -1})
    assert u._units_to_vector(test_unit) == [0, -1, 0, 0, 0, 0, 0, 0, 1, 0]

def test_multiplication():
    assert str(2 * m) == '2 m'
    assert str(m * m) == '1 m^2'
    assert str(m * km) == '1000 m^2'
    assert str(2 * m / (3 * m) / m) == '0.6666666666666666 1/m'
    assert str(m / sec * (m / sec)) == '1 m^2/sec^2'
    assert str(m / sec + m / sec) == '2 m/sec'
    assert str(m / sec - m / sec) == '0 m/sec'
    assert str(m / sec * m) == '1 m^2/sec'
    with pytest.raises((ValueError, AttributeError, AssertionError)):
        print(m / sec + m)
    assert str(m ** 2) == '1 m^2'
    with pytest.raises((ValueError, AttributeError, AssertionError)):
        print(2 ** m)

def test_single_unit_cast():
    assert str(km(2 * m)) == '0.002 km'
    assert str(2 * km >> m) == '2000 m'
    with pytest.raises(TypeError):
        print(2 * m >> 3 * km)
    assert str(2 >> km) == '2 km'

def test_align_method():
    assert str(m / sec + km / hr) == '1.2777777777777777 m/sec'
    assert str(km ** 2) == '1 km^2'
    assert str(23 * m / sec >> km / hr) == '82.8 km/hr'

def test_equal():
    assert 1000 * m == 1 * km
    assert 1 * min == 60 * sec
    d = dict()
    d[1 * min] = 'a'
    d[60 * sec] = 'b'
    assert str(d) == "{1 min: 'b'}"