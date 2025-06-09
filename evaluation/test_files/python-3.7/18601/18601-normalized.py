def visit_Rule(self, node: parsing.Rule) -> ast.expr:
    """Generates python code calling a rule.

        self.evalRule('rulename')
        """
    return ast.Call(ast.Attribute(ast.Name('self', ast.Load()), 'evalRule', ast.Load()), [ast.Str(node.name)], [], None, None)