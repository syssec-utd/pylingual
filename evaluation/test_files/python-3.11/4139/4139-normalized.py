def _check_wiremap_validity(self, wire_map, keymap, valmap):
    """Check that the wiremap is consistent.

        Check that the wiremap refers to valid wires and that
        those wires have consistent types.

        Args:
            wire_map (dict): map from (register,idx) in keymap to
                (register,idx) in valmap
            keymap (dict): a map whose keys are wire_map keys
            valmap (dict): a map whose keys are wire_map values

        Raises:
            DAGCircuitError: if wire_map not valid
        """
    for k, v in wire_map.items():
        kname = '%s[%d]' % (k[0].name, k[1])
        vname = '%s[%d]' % (v[0].name, v[1])
        if k not in keymap:
            raise DAGCircuitError('invalid wire mapping key %s' % kname)
        if v not in valmap:
            raise DAGCircuitError('invalid wire mapping value %s' % vname)
        if type(k) is not type(v):
            raise DAGCircuitError('inconsistent wire_map at (%s,%s)' % (kname, vname))