from enum import Enum, IntEnum

class Color(Enum):
    red = 1
    green = 2
    blue = 3

class Shake(Enum):
    vanilla = 7
    chocolate = 4
    cookies = 9
    mint = 3

class Planet(Enum):
    MERCURY = (3.303e+23, 2439700.0)
    VENUS = (4.869e+24, 6051800.0)
    EARTH = (5.976e+24, 6378140.0)
    MARS = (6.421e+23, 3397200.0)
    JUPITER = (1.9e+27, 71492000.0)
    SATURN = (5.688e+26, 60268000.0)
    URANUS = (8.686e+25, 25559000.0)
    NEPTUNE = (1.024e+26, 24746000.0)

class HeterogeneousEnum(Enum):
    red = 1.0
    green = 2.0
    blue = 3j

class Shape(IntEnum):
    circle = 2
    square = 500

class RequestError(IntEnum):
    dummy = 2
    not_found = 404
    internal_error = 500

class IntEnumWithNegatives(IntEnum):
    one = 1
    two = 2
    too = 2
    three = 3
    negone = -1
    negtwo = -2
    negthree = -3