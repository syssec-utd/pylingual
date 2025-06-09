import cvcuda

def test_border_type():
    assert cvcuda.Border.CONSTANT != cvcuda.Border.REPLICATE
    assert cvcuda.Border.REPLICATE != cvcuda.Border.REFLECT
    assert cvcuda.Border.REFLECT != cvcuda.Border.WRAP
    assert cvcuda.Border.WRAP != cvcuda.Border.REFLECT101
    assert cvcuda.Border.REFLECT101 != cvcuda.Border.CONSTANT