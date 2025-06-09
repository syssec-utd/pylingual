def eval_str(s: str, ctx: compiler.CompilerContext, module: types.ModuleType, eof: Any):
    """Evaluate the forms in a string into a Python module AST node."""
    last = eof
    for form in reader.read_str(s, resolver=runtime.resolve_alias, eof=eof):
        last = compiler.compile_and_exec_form(form, ctx, module)
    return last