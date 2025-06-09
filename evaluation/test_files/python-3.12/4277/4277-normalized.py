def p_gate_op_2(self, program):
    """
        gate_op : id id_list ';'
        """
    program[0] = node.CustomUnitary([program[1], program[2]])
    self.verify_as_gate(program[1], program[2])
    self.verify_bit_list(program[2])
    self.verify_distinct([program[2]])