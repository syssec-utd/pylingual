def parse_ast(ctx: ParserContext, form: ReaderForm) -> Node:
    """Take a Lisp form as an argument and produce a Basilisp syntax
    tree matching the clojure.tools.analyzer AST spec."""
    return _parse_ast(ctx, form).assoc(top_level=True)