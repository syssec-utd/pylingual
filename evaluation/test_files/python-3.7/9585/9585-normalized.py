def eval(self, operator, simulator=None):
    """Load all operands and process them by self._evalFn"""

    def getVal(v):
        while not isinstance(v, Value):
            v = v._val
        return v
    operands = list(map(getVal, operator.operands))
    if isEventDependentOp(operator.operator):
        operands.append(simulator.now)
    elif operator.operator == AllOps.IntToBits:
        operands.append(operator.result._dtype)
    return self._evalFn(*operands)