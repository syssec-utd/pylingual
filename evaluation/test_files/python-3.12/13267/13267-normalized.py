def _process_syntax_quoted_form(ctx: ReaderContext, form: ReaderForm) -> ReaderForm:
    """Post-process syntax quoted forms to generate forms that can be assembled
    into the correct types at runtime.

    Lists are turned into:
        (basilisp.core/seq
         (basilisp.core/concat [& rest]))

    Vectors are turned into:
        (basilisp.core/apply
         basilisp.core/vector
         (basilisp.core/concat [& rest]))

    Sets are turned into:
        (basilisp.core/apply
         basilisp.core/hash-set
         (basilisp.core/concat [& rest]))

    Maps are turned into:
        (basilisp.core/apply
         basilisp.core/hash-map
         (basilisp.core/concat [& rest]))

    The child forms (called rest above) are processed by _expand_syntax_quote.

    All other forms are passed through without modification."""
    lconcat = lambda v: llist.list(v).cons(_CONCAT)
    if _is_unquote(form):
        return form[1]
    elif _is_unquote_splicing(form):
        raise SyntaxError('Cannot splice outside collection')
    elif isinstance(form, llist.List):
        return llist.l(_SEQ, lconcat(_expand_syntax_quote(ctx, form)))
    elif isinstance(form, vector.Vector):
        return llist.l(_APPLY, _VECTOR, lconcat(_expand_syntax_quote(ctx, form)))
    elif isinstance(form, lset.Set):
        return llist.l(_APPLY, _HASH_SET, lconcat(_expand_syntax_quote(ctx, form)))
    elif isinstance(form, lmap.Map):
        flat_kvs = seq(form.items()).flatten().to_list()
        return llist.l(_APPLY, _HASH_MAP, lconcat(_expand_syntax_quote(ctx, flat_kvs)))
    elif isinstance(form, symbol.Symbol):
        if form.ns is None and form.name.endswith('#'):
            try:
                return llist.l(_QUOTE, ctx.gensym_env[form.name])
            except KeyError:
                genned = symbol.symbol(langutil.genname(form.name[:-1])).with_meta(form.meta)
                ctx.gensym_env[form.name] = genned
                return llist.l(_QUOTE, genned)
        return llist.l(_QUOTE, form)
    else:
        return form