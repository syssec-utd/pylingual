def parserrule_topython(parser: parsing.BasicParser, rulename: str) -> ast.FunctionDef:
    """Generates code for a rule.

    def rulename(self):
        <code for the rule>
        return True
    """
    visitor = RuleVisitor()
    rule = parser._rules[rulename]
    fn_args = ast.arguments([ast.arg('self', None)], None, None, [], None, None, [], [])
    body = visitor._clause(rule_topython(rule))
    body.append(ast.Return(ast.Name('True', ast.Load())))
    return ast.FunctionDef(rulename, fn_args, body, [], None)