def p_bit_list_1(self, program):
    """
           bit_list : bit_list ',' id
        """
    program[0] = program[1]
    program[0].add_child(program[3])
    program[3].is_bit = True
    self.update_symtab(program[3])