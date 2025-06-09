def __resolve_namespaced_symbol(ctx: ParserContext, form: sym.Symbol) -> Union[MaybeClass, MaybeHostForm, VarRef]:
    """Resolve a namespaced symbol into a Python name or Basilisp Var."""
    assert form.ns is not None
    if form.ns == ctx.current_ns.name:
        v = ctx.current_ns.find(sym.symbol(form.name))
        if v is not None:
            return VarRef(form=form, var=v, env=ctx.get_node_env())
    elif form.ns == _BUILTINS_NS:
        class_ = munge(form.name, allow_builtins=True)
        target = getattr(builtins, class_, None)
        if target is None:
            raise ParserException(f"cannot resolve builtin function '{class_}'", form=form)
        return MaybeClass(form=form, class_=class_, target=target, env=ctx.get_node_env())
    if '.' in form.name:
        raise ParserException("symbol names may not contain the '.' operator", form=form)
    ns_sym = sym.symbol(form.ns)
    if ns_sym in ctx.current_ns.imports or ns_sym in ctx.current_ns.import_aliases:
        v = Var.find(form)
        if v is not None:
            return VarRef(form=form, var=v, env=ctx.get_node_env())
        if ns_sym in ctx.current_ns.import_aliases:
            ns = ctx.current_ns.import_aliases[ns_sym]
            assert ns is not None
            ns_name = ns.name
        else:
            ns_name = ns_sym.name
        safe_module_name = munge(ns_name)
        assert safe_module_name in sys.modules, f"Module '{safe_module_name}' is not imported"
        ns_module = sys.modules[safe_module_name]
        safe_name = munge(form.name)
        if safe_name in vars(ns_module):
            return MaybeHostForm(form=form, class_=munge(ns_sym.name), field=safe_name, target=vars(ns_module)[safe_name], env=ctx.get_node_env())
        safe_name = munge(form.name, allow_builtins=True)
        if safe_name not in vars(ns_module):
            raise ParserException("can't identify aliased form", form=form)
        return MaybeHostForm(form=form, class_=munge(ns_sym.name), field=safe_name, target=vars(ns_module)[safe_name], env=ctx.get_node_env())
    elif ns_sym in ctx.current_ns.aliases:
        aliased_ns: runtime.Namespace = ctx.current_ns.aliases[ns_sym]
        v = Var.find(sym.symbol(form.name, ns=aliased_ns.name))
        if v is None:
            raise ParserException(f"unable to resolve symbol '{sym.symbol(form.name, ns_sym.name)}' in this context", form=form)
        return VarRef(form=form, var=v, env=ctx.get_node_env())
    else:
        raise ParserException(f"unable to resolve symbol '{form}' in this context", form=form)