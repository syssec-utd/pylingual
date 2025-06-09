def access_to_sympy(self, var_name, access):
    """
        Transform a (multidimensional) variable access to a flattend sympy expression.

        Also works with flat array accesses.
        """
    base_sizes = self.variables[var_name][1]
    expr = sympy.Number(0)
    for dimension, a in enumerate(access):
        base_size = reduce(operator.mul, base_sizes[dimension + 1:], sympy.Integer(1))
        expr += base_size * a
    return expr