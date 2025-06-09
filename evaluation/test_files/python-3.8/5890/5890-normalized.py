def modules(self):
    """return all module nodes in the diagram"""
    return [o for o in self.objects if isinstance(o.node, astroid.Module)]