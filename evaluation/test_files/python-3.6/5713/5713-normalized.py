def visit_functiondef(self, node):
    """check use of super"""
    if not node.is_method():
        return
    klass = node.parent.frame()
    for stmt in node.nodes_of_class(astroid.Call):
        if node_frame_class(stmt) != node_frame_class(node):
            continue
        expr = stmt.func
        if not isinstance(expr, astroid.Attribute):
            continue
        call = expr.expr
        if not (isinstance(call, astroid.Call) and isinstance(call.func, astroid.Name) and (call.func.name == 'super')):
            continue
        if not klass.newstyle and has_known_bases(klass):
            continue
        else:
            if not call.args:
                if sys.version_info[0] == 3:
                    continue
                else:
                    self.add_message('missing-super-argument', node=call)
                    continue
            arg0 = call.args[0]
            if isinstance(arg0, astroid.Call) and isinstance(arg0.func, astroid.Name) and (arg0.func.name == 'type'):
                self.add_message('bad-super-call', node=call, args=('type',))
                continue
            if len(call.args) >= 2 and isinstance(call.args[1], astroid.Name) and (call.args[1].name == 'self') and isinstance(arg0, astroid.Attribute) and (arg0.attrname == '__class__'):
                self.add_message('bad-super-call', node=call, args=('self.__class__',))
                continue
            try:
                supcls = call.args and next(call.args[0].infer(), None)
            except astroid.InferenceError:
                continue
            if klass is not supcls:
                name = None
                if supcls:
                    name = supcls.name
                elif call.args and hasattr(call.args[0], 'name'):
                    name = call.args[0].name
                if name:
                    self.add_message('bad-super-call', node=call, args=(name,))