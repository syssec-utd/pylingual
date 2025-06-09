def get_ids_by_expression(self, expression, threshold=0.001, func=np.sum):
    """ Use a PEG to parse expression and return study IDs."""
    lexer = lp.Lexer()
    lexer.build()
    parser = lp.Parser(lexer, self.dataset, threshold=threshold, func=func)
    parser.build()
    return parser.parse(expression).keys().values