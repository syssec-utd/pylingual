def get_compute_sig(self) -> Signature:
    """
        Compute a signature Using resolution!!!

        TODO: discuss of relevance of a final generation for a signature
        """
    tret = []
    tparams = []
    for t in self.tret.components:
        if t in self.resolution and self.resolution[t] is not None:
            tret.append(self.resolution[t]().show_name())
        else:
            tret.append(t)
    if hasattr(self, 'tparams'):
        for p in self.tparams:
            tp = []
            for t in p.components:
                if t in self.resolution and self.resolution[t] is not None:
                    tp.append(self.resolution[t]().show_name())
                else:
                    tp.append(t)
            tparams.append(' '.join(tp))
        if self.variadic:
            if self._variadic_types is None:
                raise ValueError("Can't compute the sig " + 'with unresolved variadic argument')
            for p in self._variadic_types:
                tp = []
                for t in p.components:
                    if t in self.resolution and self.resolution[t] is not None:
                        tp.append(self.resolution[t]().show_name())
                    else:
                        tp.append(t)
                tparams.append(' '.join(tp))
    ret = Fun(self.name, ' '.join(tret), tparams)
    ret.__class__ = self._sig.__class__
    return ret