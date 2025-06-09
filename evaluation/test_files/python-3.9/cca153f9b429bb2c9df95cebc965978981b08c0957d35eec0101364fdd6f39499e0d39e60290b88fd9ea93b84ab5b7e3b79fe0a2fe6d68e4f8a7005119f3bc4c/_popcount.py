import bitstring

def popcount(val: int) -> int:
    """Count the number of set bits in the binary representation of a
    non-negative int.
    """
    assert val >= 0
    try:
        return val.bit_count()
    except AttributeError:
        return bitstring.Bits(uint=val, length=(val + 1).bit_length()).count(1)