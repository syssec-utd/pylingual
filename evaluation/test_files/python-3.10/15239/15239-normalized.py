def visit_With(self, node):
    """
        with describe(thing) as it:
            ...

             |
             v

        class TestThing(TestCase):
            ...

        """
    (withitem,) = node.items
    context = withitem.context_expr
    if context.func.id == 'describe':
        describes = context.args[0].id
        example_group_name = withitem.optional_vars.id
        return self.transform_describe(node, describes, example_group_name)
    else:
        return node