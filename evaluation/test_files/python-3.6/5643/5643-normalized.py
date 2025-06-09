def _fix_dot_imports(not_consumed):
    """ Try to fix imports with multiple dots, by returning a dictionary
    with the import names expanded. The function unflattens root imports,
    like 'xml' (when we have both 'xml.etree' and 'xml.sax'), to 'xml.etree'
    and 'xml.sax' respectively.
    """
    names = {}
    for (name, stmts) in not_consumed.items():
        if any((isinstance(stmt, astroid.AssignName) and isinstance(stmt.assign_type(), astroid.AugAssign) for stmt in stmts)):
            continue
        for stmt in stmts:
            if not isinstance(stmt, (astroid.ImportFrom, astroid.Import)):
                continue
            for imports in stmt.names:
                second_name = None
                import_module_name = imports[0]
                if import_module_name == '*':
                    second_name = name
                else:
                    name_matches_dotted_import = False
                    if import_module_name.startswith(name) and import_module_name.find('.') > -1:
                        name_matches_dotted_import = True
                    if name_matches_dotted_import or name in imports:
                        second_name = import_module_name
                if second_name and second_name not in names:
                    names[second_name] = stmt
    return sorted(names.items(), key=lambda a: a[1].fromlineno)