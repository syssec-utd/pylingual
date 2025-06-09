def _check_consider_merging_isinstance(self, node):
    """Check isinstance calls which can be merged together."""
    if node.op != 'or':
        return
    first_args = self._duplicated_isinstance_types(node)
    for duplicated_name, class_names in first_args.items():
        names = sorted((name for name in class_names))
        self.add_message('consider-merging-isinstance', node=node, args=(duplicated_name, ', '.join(names)))