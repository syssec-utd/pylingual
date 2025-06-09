def get_by_return_type(self, tname: str) -> Scope:
    """ Retrieve a Set of all signature by (return) type """
    lst = []
    for s in self.values():
        if hasattr(s, 'tret') and s.tret == tname:
            lst.append(EvalCtx.from_sig(s))
    rscope = Scope(sig=lst, state=StateScope.LINKED, is_namespace=False)
    rscope.set_parent(self)
    return rscope