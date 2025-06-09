def _to_bits(nqbits, ncbits=0, func=None):
    """Convert gate arguments to [qu|cl]bits from integers, slices, ranges, etc.
    For example circuit.h(0) -> circuit.h(QuantumRegister(2)[0]) """
    if func is None:
        return functools.partial(_to_bits, nqbits, ncbits)

    @functools.wraps(func)
    def wrapper(self, *args):
        qbits = self.qubits()
        cbits = self.clbits()
        nparams = len(args) - nqbits - ncbits
        params = args[:nparams]
        qb_args = args[nparams:nparams + nqbits]
        cl_args = args[nparams + nqbits:]
        args = list(params) + _convert_to_bits(qb_args, qbits) + _convert_to_bits(cl_args, cbits)
        return func(self, *args)
    return wrapper