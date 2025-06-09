def Case(self, caseVal, *statements):
    """c-like case of switch statement"""
    assert self.parentStm is None
    caseVal = toHVal(caseVal, self.switchOn._dtype)
    assert isinstance(caseVal, Value), caseVal
    assert caseVal._isFullVld(), 'Cmp with invalid value'
    assert caseVal not in self._case_value_index, ('Switch statement already has case for value ', caseVal)
    self.rank += 1
    case = []
    self._case_value_index[caseVal] = len(self.cases)
    self.cases.append((caseVal, case))
    cond = self.switchOn._eq(caseVal)
    self._inputs.append(cond)
    cond.endpoints.append(self)
    self._register_stements(statements, case)
    return self