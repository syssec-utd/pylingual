def p_barrier(self, program):
    """
        barrier : BARRIER primary_list
        """
    program[0] = node.Barrier([program[2]])
    self.verify_reg_list(program[2], 'qreg')
    self.verify_distinct([program[2]])