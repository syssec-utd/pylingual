from jinja2 import pass_context
from ..datatypes import Import
from .python_name import base_name, package_name, split_base_name, split_package_base_name, split_package_name

def sorted_imports(imports):
    imports = list(sorted(imports, key=lambda x: (x['import'], x.get('alias'))))
    return imports

def to_import_dict(import_object):
    if isinstance(import_object, Import):
        return {'import': import_object.import_path, 'alias': import_object.alias}
    return import_object

@pass_context
def generate_import(ctx, import_object, imported_part='class', alias=None, skip=False):
    if skip:
        return ''
    import_object = to_import_dict(import_object)
    if isinstance(import_object, list):
        import_object = [to_import_dict(x) for x in import_object]
        return '\n'.join([generate_import(ctx, x, None) for x in sorted_imports(import_object)])
    if isinstance(import_object, str):
        return generate_import(ctx, {'import': import_object, 'alias': alias}, None)
    if imported_part:
        if import_object.get('skip'):
            return ''
        return generate_import(ctx, import_object[imported_part], alias)
    import_name = import_object['import']
    if '.' in import_name:
        import_path, import_name = import_name.rsplit('.', maxsplit=1)
    else:
        import_path = None
    alias = import_object.get('alias')
    ret = []
    if import_path:
        if ctx['current_module'] == import_path:
            return ''
        ret.append(f'from {import_path} import {import_name}')
    else:
        ret.append(f'import {import_name}')
    if alias:
        ret.append(f'as {alias}')
    return ' '.join(ret)

def generate_list(data, separator=', ', start=False, end=False):
    if not data:
        return ''
    ret = []
    if start:
        ret.append(separator)
    for di, d in enumerate(data):
        if di:
            ret.append(separator)
        ret.append(d)
    if end:
        ret.append(separator)
    return ''.join(ret)

def in_different_package(current_module, value):
    return current_module != package_name(value)

def with_defined_prefix(always_defined_import_prefixes, value):
    return package_name(value) in always_defined_import_prefixes

def class_header(rec, class_name='class', base_classes_name='base-classes'):
    try:
        ret = [base_name(rec[class_name])]
    except KeyError:
        raise KeyError(f'Do not have "{class_name}" inside {rec}')
    base_classes = rec[base_classes_name]
    if base_classes:
        ret.append('(')
        for idx, cls in enumerate(base_classes):
            if idx > 0:
                ret.append(', ')
            ret.append(cls)
        ret.append(')')
    return ''.join(ret)