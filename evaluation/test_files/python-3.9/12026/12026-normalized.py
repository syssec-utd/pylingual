def global_iterator(self):
    """
        Return global iterator sympy expression
        """
    global_iterator = sympy.Integer(0)
    total_length = sympy.Integer(1)
    for (var_name, start, end, incr) in reversed(self._loop_stack):
        loop_var = symbol_pos_int(var_name)
        length = end - start
        global_iterator += (loop_var - start) * total_length
        total_length *= length
    return global_iterator