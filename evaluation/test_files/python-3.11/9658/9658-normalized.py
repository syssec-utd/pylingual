def Architecture_var(cls, v, serializerVars, extraTypes, extraTypes_serialized, ctx, childCtx):
    """
        :return: list of extra discovered processes
        """
    t = v._dtype
    if isinstance(t, HArray) and v.defVal.vldMask:
        if v.drivers:
            raise SerializerException('Verilog does not support RAMs with initialized value')
        eProcs, eVars = cls.hardcodeRomIntoProcess(v)
        for _v in eVars:
            _procs = cls.Architecture_var(_v, serializerVars, extraTypes, extraTypes_serialized, ctx, childCtx)
            eProcs.extend(_procs)
        return eProcs
    v.name = ctx.scope.checkedName(v.name, v)
    serializedVar = cls.SignalItem(v, childCtx, declaration=True)
    serializerVars.append(serializedVar)
    return []