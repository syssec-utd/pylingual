def visit_importfrom(self, node):
    """check modules attribute accesses"""
    if not self._analyse_fallback_blocks and utils.is_from_fallback_block(node):
        return
    name_parts = node.modname.split('.')
    try:
        module = node.do_import_module(name_parts[0])
    except astroid.AstroidBuildingException:
        return
    module = self._check_module_attrs(node, module, name_parts[1:])
    if not module:
        return
    for name, _ in node.names:
        if name == '*':
            continue
        self._check_module_attrs(node, module, name.split('.'))