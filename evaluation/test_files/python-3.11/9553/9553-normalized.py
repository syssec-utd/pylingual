def removeUnconnectedSignals(netlist):
    """
    If signal is not driving anything remove it
    """
    toDelete = set()
    toSearch = netlist.signals
    while toSearch:
        _toSearch = set()
        for sig in toSearch:
            if not sig.endpoints:
                try:
                    if sig._interface is not None:
                        continue
                except AttributeError:
                    pass
                for e in sig.drivers:
                    if isinstance(e, Operator):
                        inputs = e.operands
                        if e.result is sig:
                            e.result = None
                    else:
                        inputs = e._inputs
                        netlist.statements.discard(e)
                    for op in inputs:
                        if not isinstance(op, Value):
                            try:
                                op.endpoints.remove(e)
                            except KeyError:
                                continue
                            _toSearch.add(op)
                toDelete.add(sig)
        if toDelete:
            for sig in toDelete:
                if sig.ctx == netlist:
                    netlist.signals.remove(sig)
                _toSearch.discard(sig)
            toDelete = set()
        toSearch = _toSearch