def _check_inputs(self):
    """ make some basic checks on the inputs to make sure they are valid"""
    try:
        _ = self._inputs[0]
    except TypeError:
        raise RuntimeError("inputs should be iterable but found type='{0}', value='{1}'".format(type(self._inputs), str(self._inputs)))
    from melody.inputs import Input
    for check_input in self._inputs:
        if not isinstance(check_input, Input):
            raise RuntimeError("input should be a subclass of the Input class but found type='{0}', value='{1}'".format(type(check_input), str(check_input)))