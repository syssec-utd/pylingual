def getExprVal(self, val, do_eval=False):
    """
        :see: doc of method on parent class
        """
    ctx = VhdlSerializer.getBaseContext()

    def createTmpVar(suggestedName, dtype):
        raise NotImplementedError('Width value can not be converted do ipcore format (%r)', val)
    ctx.createTmpVarFn = createTmpVar
    if do_eval:
        val = val.staticEval()
    val = VivadoTclExpressionSerializer.asHdl(val, ctx)
    return val