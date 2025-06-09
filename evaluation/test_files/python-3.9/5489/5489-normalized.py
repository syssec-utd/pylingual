def _check_open_mode(self, node):
    """Check that the mode argument of an open or file call is valid."""
    try:
        mode_arg = utils.get_argument_from_call(node, position=1, keyword='mode')
    except utils.NoSuchArgumentError:
        return
    if mode_arg:
        mode_arg = utils.safe_infer(mode_arg)
        if isinstance(mode_arg, astroid.Const) and (not _check_mode_str(mode_arg.value)):
            self.add_message('bad-open-mode', node=node, args=mode_arg.value)