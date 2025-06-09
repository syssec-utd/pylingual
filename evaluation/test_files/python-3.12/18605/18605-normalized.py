def visit_Seq(self, node: parsing.Seq) -> [ast.stmt] or ast.expr:
    """Generates python code for clauses.

        #Continuous clauses which can can be inlined are combined with and
        clause and clause

        if not clause:
            return False
        if not clause:
            return False
        """
    exprs, stmts = ([], [])
    for clause in node.ptlist:
        clause_ast = self.visit(clause)
        if isinstance(clause_ast, ast.expr):
            exprs.append(clause_ast)
        else:
            if exprs:
                stmts.extend(self.combine_exprs_for_clauses(exprs))
                exprs = []
            stmts.extend(self._clause(clause_ast))
    if not stmts:
        return ast.BoolOp(ast.And(), exprs)
    if exprs:
        stmts.extend(self.combine_exprs_for_clauses(exprs))
    return stmts