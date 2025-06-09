def reinterpretBits(self, sigOrVal, toType):
    """
    Cast object of same bit size between to other type
    (f.e. bits to struct, union or array)
    """
    if isinstance(sigOrVal, Value):
        return reinterpretBits__val(self, sigOrVal, toType)
    elif isinstance(toType, Bits):
        return fitTo_t(sigOrVal, toType)
    elif sigOrVal._dtype.bit_length() == toType.bit_length():
        if isinstance(toType, HStruct):
            raise reinterpret_bits_to_hstruct(sigOrVal, toType)
        elif isinstance(toType, HUnion):
            raise NotImplementedError()
        elif isinstance(toType, HArray):
            reinterpret_bits_to_harray(sigOrVal, toType)
    return default_auto_cast_fn(self, sigOrVal, toType)