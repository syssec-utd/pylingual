def staticEval(self):
    """
        Recursively statistically evaluate result of this operator
        """
    for o in self.operands:
        o.staticEval()
    self.result._val = self.evalFn()