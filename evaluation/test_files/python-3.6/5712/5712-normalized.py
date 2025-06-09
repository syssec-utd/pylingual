def visit_tryexcept(self, node):
    """check for empty except"""
    self._check_try_except_raise(node)
    exceptions_classes = []
    nb_handlers = len(node.handlers)
    for (index, handler) in enumerate(node.handlers):
        if handler.type is None:
            if not _is_raising(handler.body):
                self.add_message('bare-except', node=handler)
            if index < nb_handlers - 1:
                msg = 'empty except clause should always appear last'
                self.add_message('bad-except-order', node=node, args=msg)
        elif isinstance(handler.type, astroid.BoolOp):
            self.add_message('binary-op-exception', node=handler, args=handler.type.op)
        else:
            try:
                excs = list(_annotated_unpack_infer(handler.type))
            except astroid.InferenceError:
                continue
            for (part, exc) in excs:
                if exc is astroid.Uninferable:
                    continue
                if isinstance(exc, astroid.Instance) and utils.inherit_from_std_ex(exc):
                    exc = exc._proxied
                self._check_catching_non_exception(handler, exc, part)
                if not isinstance(exc, astroid.ClassDef):
                    continue
                exc_ancestors = [anc for anc in exc.ancestors() if isinstance(anc, astroid.ClassDef)]
                for previous_exc in exceptions_classes:
                    if previous_exc in exc_ancestors:
                        msg = '%s is an ancestor class of %s' % (previous_exc.name, exc.name)
                        self.add_message('bad-except-order', node=handler.type, args=msg)
                if exc.name in self.config.overgeneral_exceptions and exc.root().name == utils.EXCEPTIONS_MODULE and (not _is_raising(handler.body)):
                    self.add_message('broad-except', args=exc.name, node=handler.type)
                if exc in exceptions_classes:
                    self.add_message('duplicate-except', args=exc.name, node=handler.type)
            exceptions_classes += [exc for (_, exc) in excs]