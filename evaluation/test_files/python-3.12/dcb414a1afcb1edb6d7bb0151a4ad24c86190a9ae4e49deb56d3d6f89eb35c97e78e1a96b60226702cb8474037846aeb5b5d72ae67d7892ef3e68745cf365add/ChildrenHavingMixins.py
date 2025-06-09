"""Children having mixins

WARNING, this code is GENERATED. Modify the template ChildrenHavingMixin.py.j2 instead!

spell-checker: ignore append capitalize casefold center clear copy count decode encode endswith expandtabs extend find format formatmap fromkeys get haskey index insert isalnum isalpha isascii isdecimal isdigit isidentifier islower isnumeric isprintable isspace istitle isupper items iteritems iterkeys itervalues join keys ljust lower lstrip maketrans partition pop popitem prepare remove replace reverse rfind rindex rjust rpartition rsplit rstrip setdefault sort split splitlines startswith strip swapcase title translate update upper values viewitems viewkeys viewvalues zfill
spell-checker: ignore args chars count default delete encoding end errors fillchar index item iterable keepends key kwargs maxsplit new old pairs prefix sep start stop sub suffix table tabsize value width
"""
from .Checkers import checkStatementsSequenceOrNone, convertEmptyStrConstantToNone, convertNoneConstantToNone
from .NodeMakingHelpers import wrapExpressionWithSideEffects

class ModuleChildrenHavingBodyOptionalStatementsOrNoneFunctionsTupleMixin(object):
    __slots__ = ()

    def __init__(self, body, functions):
        body = checkStatementsSequenceOrNone(body)
        if body is not None:
            body.parent = self
        self.subnode_body = body
        assert type(functions) is tuple
        for val in functions:
            val.parent = self
        self.subnode_functions = functions

    def setChildBody(self, value):
        value = checkStatementsSequenceOrNone(value)
        if value is not None:
            value.parent = self
        self.subnode_body = value

    def setChildFunctions(self, value):
        assert type(value) is tuple, type(value)
        for val in value:
            val.parent = self
        self.subnode_functions = value

    def getVisitableNodes(self):
        """The visitable nodes, with tuple values flattened."""
        result = []
        value = self.subnode_body
        if value is None:
            pass
        else:
            result.append(value)
        result.extend(self.subnode_functions)
        return tuple(result)

    def getVisitableNodesNamed(self):
        """Named children dictionary.

        For use in cloning nodes, debugging and XML output.
        """
        return (('body', self.subnode_body), ('functions', self.subnode_functions))

    def replaceChild(self, old_node, new_node):
        value = self.subnode_body
        if old_node is value:
            new_node = checkStatementsSequenceOrNone(new_node)
            if new_node is not None:
                new_node.parent = self
            self.subnode_body = new_node
            return
        value = self.subnode_functions
        if old_node in value:
            if new_node is not None:
                new_node.parent = self
                self.subnode_functions = tuple((val if val is not old_node else new_node for val in value))
            else:
                self.subnode_functions = tuple((val for val in value if val is not old_node))
            return
        raise AssertionError("Didn't find child", old_node, 'in', self)

    def getCloneArgs(self):
        """Get clones of all children to pass for a new node.

        Needs to make clones of child nodes too.
        """
        values = {'body': self.subnode_body.makeClone() if self.subnode_body is not None else None, 'functions': tuple((v.makeClone() for v in self.subnode_functions))}
        values.update(self.getDetails())
        return values

    def finalize(self):
        del self.parent
        if self.subnode_body is not None:
            self.subnode_body.finalize()
        del self.subnode_body
        for c in self.subnode_functions:
            c.finalize()
        del self.subnode_functions

    def collectVariableAccesses(self, emit_read, emit_write):
        """Collect variable reads and writes of child nodes."""
        subnode_body = self.subnode_body
        if subnode_body is not None:
            self.subnode_body.collectVariableAccesses(emit_read, emit_write)
        for element in self.subnode_functions:
            element.collectVariableAccesses(emit_read, emit_write)
ChildrenCompiledPythonModuleMixin = ModuleChildrenHavingBodyOptionalStatementsOrNoneFunctionsTupleMixin
ChildrenCompiledPythonPackageMixin = ModuleChildrenHavingBodyOptionalStatementsOrNoneFunctionsTupleMixin
ChildrenPythonMainModuleMixin = ModuleChildrenHavingBodyOptionalStatementsOrNoneFunctionsTupleMixin

class ChildHavingAsyncgenRefMixin(object):
    __slots__ = ()

    def __init__(self, asyncgen_ref):
        asyncgen_ref.parent = self
        self.subnode_asyncgen_ref = asyncgen_ref

    def getVisitableNodes(self):
        """The visitable nodes, with tuple values flattened."""
        return (self.subnode_asyncgen_ref,)

    def getVisitableNodesNamed(self):
        """Named children dictionary.

        For use in cloning nodes, debugging and XML output.
        """
        return (('asyncgen_ref', self.subnode_asyncgen_ref),)

    def replaceChild(self, old_node, new_node):
        value = self.subnode_asyncgen_ref
        if old_node is value:
            new_node.parent = self
            self.subnode_asyncgen_ref = new_node
            return
        raise AssertionError("Didn't find child", old_node, 'in', self)

    def getCloneArgs(self):
        """Get clones of all children to pass for a new node.

        Needs to make clones of child nodes too.
        """
        values = {'asyncgen_ref': self.subnode_asyncgen_ref.makeClone()}
        values.update(self.getDetails())
        return values

    def finalize(self):
        del self.parent
        self.subnode_asyncgen_ref.finalize()
        del self.subnode_asyncgen_ref

    def computeExpressionRaw(self, trace_collection):
        """Compute an expression.

        Default behavior is to just visit the child expressions first, and
        then the node "computeExpression". For a few cases this needs to
        be overloaded, e.g. conditional expressions.
        """
        expression = trace_collection.onExpression(self.subnode_asyncgen_ref)
        if expression.willRaiseAnyException():
            return (expression, 'new_raise', lambda: "For '%s' the child expression '%s' will raise." % (self.getChildNameNice(), expression.getChildNameNice()))
        return self.computeExpression(trace_collection)

    def collectVariableAccesses(self, emit_read, emit_write):
        """Collect variable reads and writes of child nodes."""
        self.subnode_asyncgen_ref.collectVariableAccesses(emit_read, emit_write)
ChildrenExpressionMakeAsyncgenObjectMixin = ChildHavingAsyncgenRefMixin

class ChildHavingBodyOptionalMixin(object):
    __slots__ = ()

    def __init__(self, body):
        if body is not None:
            body.parent = self
        self.subnode_body = body

    def setChildBody(self, value):
        if value is not None:
            value.parent = self
        self.subnode_body = value

    def getVisitableNodes(self):
        """The visitable nodes, with tuple values flattened."""
        value = self.subnode_body
        if value is None:
            return ()
        else:
            return (value,)

    def getVisitableNodesNamed(self):
        """Named children dictionary.

        For use in cloning nodes, debugging and XML output.
        """
        return (('body', self.subnode_body),)

    def replaceChild(self, old_node, new_node):
        value = self.subnode_body
        if old_node is value:
            if new_node is not None:
                new_node.parent = self
            self.subnode_body = new_node
            return
        raise AssertionError("Didn't find child", old_node, 'in', self)

    def getCloneArgs(self):
        """Get clones of all children to pass for a new node.

        Needs to make clones of child nodes too.
        """
        values = {'body': self.subnode_body.makeClone() if self.subnode_body is not None else None}
        values.update(self.getDetails())
        return values

    def finalize(self):
        del self.parent
        if self.subnode_body is not None:
            self.subnode_body.finalize()
        del self.subnode_body

    def computeExpressionRaw(self, trace_collection):
        """Compute an expression.

        Default behavior is to just visit the child expressions first, and
        then the node "computeExpression". For a few cases this needs to
        be overloaded, e.g. conditional expressions.
        """
        expression = self.subnode_body
        if expression is not None:
            expression = trace_collection.onExpression(expression)
            if expression.willRaiseAnyException():
                return (expression, 'new_raise', lambda: "For '%s' the child expression '%s' will raise." % (self.getChildNameNice(), expression.getChildNameNice()))
        return self.computeExpression(trace_collection)

    def collectVariableAccesses(self, emit_read, emit_write):
        """Collect variable reads and writes of child nodes."""
        subnode_body = self.subnode_body
        if subnode_body is not None:
            self.subnode_body.collectVariableAccesses(emit_read, emit_write)
ChildrenExpressionAsyncgenObjectBodyMixin = ChildHavingBodyOptionalMixin
ChildrenExpressionClassBodyP2Mixin = ChildHavingBodyOptionalMixin
ChildrenExpressionClassBodyP3Mixin = ChildHavingBodyOptionalMixin
ChildrenExpressionCoroutineObjectBodyMixin = ChildHavingBodyOptionalMixin
ChildrenExpressionFunctionBodyMixin = ChildHavingBodyOptionalMixin
ChildrenExpressionFunctionPureBodyMixin = ChildHavingBodyOptionalMixin
ChildrenExpressionFunctionPureInlineConstBodyMixin = ChildHavingBodyOptionalMixin
ChildrenExpressionGeneratorObjectBodyMixin = ChildHavingBodyOptionalMixin
ChildrenExpressionOutlineBodyMixin = ChildHavingBodyOptionalMixin
ChildrenExpressionOutlineFunctionMixin = ChildHavingBodyOptionalMixin

class ChildHavingBytesArgMixin(object):
    __slots__ = ()

    def __init__(self, bytes_arg):
        bytes_arg.parent = self
        self.subnode_bytes_arg = bytes_arg

    def getVisitableNodes(self):
        """The visitable nodes, with tuple values flattened."""
        return (self.subnode_bytes_arg,)

    def getVisitableNodesNamed(self):
        """Named children dictionary.

        For use in cloning nodes, debugging and XML output.
        """
        return (('bytes_arg', self.subnode_bytes_arg),)

    def replaceChild(self, old_node, new_node):
        value = self.subnode_bytes_arg
        if old_node is value:
            new_node.parent = self
            self.subnode_bytes_arg = new_node
            return
        raise AssertionError("Didn't find child", old_node, 'in', self)

    def getCloneArgs(self):
        """Get clones of all children to pass for a new node.

        Needs to make clones of child nodes too.
        """
        values = {'bytes_arg': self.subnode_bytes_arg.makeClone()}
        values.update(self.getDetails())
        return values

    def finalize(self):
        del self.parent
        self.subnode_bytes_arg.finalize()
        del self.subnode_bytes_arg

    def computeExpressionRaw(self, trace_collection):
        """Compute an expression.

        Default behavior is to just visit the child expressions first, and
        then the node "computeExpression". For a few cases this needs to
        be overloaded, e.g. conditional expressions.
        """
        expression = trace_collection.onExpression(self.subnode_bytes_arg)
        if expression.willRaiseAnyException():
            return (expression, 'new_raise', lambda: "For '%s' the child expression '%s' will raise." % (self.getChildNameNice(), expression.getChildNameNice()))
        return self.computeExpression(trace_collection)

    def collectVariableAccesses(self, emit_read, emit_write):
        """Collect variable reads and writes of child nodes."""
        self.subnode_bytes_arg.collectVariableAccesses(emit_read, emit_write)
ChildrenExpressionBytesOperationCapitalizeMixin = ChildHavingBytesArgMixin
ChildrenExpressionBytesOperationCapitalizeBaseMixin = ChildHavingBytesArgMixin
ChildrenExpressionBytesOperationDecode1Mixin = ChildHavingBytesArgMixin
ChildrenExpressionBy