"""
generate the python code from AST tree
AST -> Abstract Syntax Tree... thank you Jesus!

THIS FILE IS FULL OF GOD'S GRACE AND MAGIC CODE :)))
"""
import json
from .importer import get
' NOTE: Let all blocks be like this:\n    if [COND] {\n\n        [EXPRESSION]\n    \n}\n    Asin, the curly braces should be at the end of everyline\n'
word_ops = {'and': 'and', 'or': 'or', 'is': '=', 'not': '!=', 'in': 'in', 'plus': '+', 'minus': '-', 'times': '*', 'dividedby': '/'}

def handle_operators(op: str) -> str:
    """ convert custom operators to python operators... """
    if op.isalpha():
        return word_ops.get(op)
    else:
        return op

def is_in_parents_props(prop_name: str, parent_props) -> bool:
    """For every prop in parent check if that prop is same as the passed prop
        if so, stop searching and return found
    """
    found = False
    i = 0
    if len(parent_props) <= 0:
        return found
    while not found and i < len(parent_props):
        p = parent_props[i]
        if p.get('value', None) == prop_name or p.get('left', None) == prop_name:
            found = True
        i += 1
    return found

def make_py(token, local: bool=False):
    """local is if this file is a local file"""

    def pythonise(token):
        switch = {'num': py_atom, 'str': py_atom, 'bool': py_atom, 'var': py_var, 'module': py_var, 'binary': py_binary, 'membership': py_binary, 'assign': py_assign, 'access': py_access, 'function': py_function, 'import': py_import, 'return': py_return, 'if': py_if, 'list': py_list, 'dict': py_dict, 'while': py_while, 'for': py_forloop, 'call': py_call, 'prog': py_prog, 'class': py_class, 'class_property': py_class_prop}
        doer = switch.get(token['type'], None)
        if not doer:
            raise Exception('Invalid Hapy code: %s' % json.dumps(token))
        return doer(token)

    def py_atom(tok):
        """return the value of a token"""
        if tok['type'] == 'bool':
            return '%s' % tok['value']
        return json.dumps(tok['value'])

    def py_var(tok):
        """return a plain variable value"""
        return tok['value']

    def py_class_prop(tok):
        """return a plain variable value"""
        if 'default_value' in tok:
            return '{left}{op}{right}'.format(**{'left': pythonise(tok['value']), 'op': '=', 'right': pythonise(tok['default_value'])})
        return tok['value']

    def py_binary(tok):
        """return a binary statement"""
        " this is because we make '.' a binary operator :)\n                        and we are using this different notation cuz I don't want space\n                        between the operands... 'foo.bar' over 'foo . bar'\n        "
        s1 = s2 = ' '
        (left_key, right_key) = ('left', 'right')
        if tok['operator'] == '.':
            s1 = s2 = ''
        if tok['operator'] == ':':
            (left_key, right_key) = ('key', 'value')
            s1 = ''
        'if this is a regular binary operator, then give space!'
        return '{left}{s1}{op}{s2}{right}'.format(**{'left': pythonise(tok[left_key]), 'op': handle_operators(tok['operator']), 'right': pythonise(tok[right_key]), 's1': s1, 's2': s2})

    def py_assign(tok):
        """return an assign function"""
        return py_binary(tok)

    def py_access(tok):
        """return dot access statement: foo.bar """
        return py_binary(tok)

    def py_function(tok, class_method=False, custom_name=None):
        """return a Python function definition"""
        function_name = pythonise(tok['name']) if not custom_name else custom_name
        args = ''
        if class_method:
            sep = ',' if len(tok['vars']) > 0 else ''
            args = ' (self' + sep + '{args})'.format(**{'args': ', '.join(list(map(lambda x: pythonise(x), tok['vars'])))})
        else:
            args = ' ({args})'.format(**{'args': ', '.join(list(map(lambda x: pythonise(x), tok['vars'])))})
        o = 'def ' + function_name + args + '{\n' + pythonise(tok['body']) + '\n}'
        return o

    def py_list(tok):
        """return a Python list definition"""
        o = ' [{args}]'.format(**{'args': ','.join(list(map(lambda x: pythonise(x), tok['elements'])))})
        return o

    def py_dict(tok):
        """This turns a dictionary AST into a dictionary with boundary definition like this `<<<| |>>>` """
        o = '<<<|{args}|>>>'.format(**{'args': ', '.join(list(map(lambda x: py_binary(x), tok['content'])))})
        return o
    ' NOTE: Let all blocks be like this:\n        if [COND] {\n\n            [EXPRESSION]\n        \n}\n        Asin, the curly braces should be at the end of everyline\n    '

    def py_if(tok):
        """creates a Python if statement"""
        o = 'if (' + pythonise(tok['cond']) + ') {\n' + pythonise(tok['then']) + '\n}' + ('\nelse {\n' + pythonise(tok['else']) + '\n}' if tok.get('else', None) else '')
        return o

    def py_while(tok):
        """while loop, returns python while loop!"""
        o = 'while (' + pythonise(tok['cond']) + ') {\n'
        +pythonise(tok['then']) + '\n}'
        return o

    def py_forloop(tok):
        """forloop, returns python for loop!"""
        o = 'for ' + pythonise(tok['header']) + ' {\n' + pythonise(tok['body']) + '\n}'
        return o

    def py_call(tok):
        return pythonise(tok['func']) + '({args})'.format(**{'args': ', '.join(list(map(lambda x: pythonise(x), tok['args'])))})

    def py_class(tok):
        """generate python class"""
        class_header = 'class ' + pythonise(tok['name']) + ('(%s) {\n' % tok['inherits']['value'] if 'inherits' in tok else ' {\n')
        init = ''
        for t in tok['class_special_methods']:
            if t['name']['value'] == 'when_created':
                init += py_class_init(tok, t)
            elif t['name']['value'] == 'when_string':
                init += py_function(t, class_method=True, custom_name='__str__') + ';\n'
            elif t['name']['value'] == 'when_printed':
                init += py_function(t, class_method=True, custom_name='__repr__') + ';\n'
            else:
                init += '#invalid special method\n'
        methods = ''
        if 'class_methods' in tok:
            methods = ';\n'.join(list(map(lambda x: py_function(x, class_method=True), tok['class_methods'])))
        class_body = ''
        if 'body' in tok:
            class_body = 'pass'
        o = class_header + init + methods + class_body + '\n}'
        return o

    def py_class_init(tok, init_token):
        """return __init__ definition"""
        init_header = 'def __init__(self, {args})'.format(**{'args': ', '.join(list(map(lambda x: pythonise(x), tok['class_properties'])))}) + ' {\n'
        init_body = ''
        if 'inherits' in tok:
            args = ''
            if 'init_parent' in tok and tok['init_parent'].get('args', None):
                args = ', '.join(list(map(lambda x: pythonise(x), tok['init_parent']['args'])))
            init_body += 'super().__init__({});\n'.format(args)
        if len(tok['class_properties']) > 0:
            for p in tok['class_properties']:
                if p['type'] == 'var' and (not is_in_parents_props(p['value'], tok.get('init_parent', {}).get('args', []))):
                    init_body += 'self.{prop_name} = {prop_name}'.format(**{'prop_name': p['value']}) + ';\n'
                elif p['type'] == 'assign' and (not is_in_parents_props(p['left']['value'], tok.get('init_parent', {}).get('args', []))):
                    init_body += 'self.{prop_name} = {prop_name}'.format(**{'prop_name': p['left']['value']}) + ';\n'
        if init_token.get('body', None):
            init_body += '\n' + pythonise(init_token['body']) + ';\n'
        o = '\n' + init_header + init_body + '}\n'
        return o

    def py_return(tok):
        o = 'return ' + pythonise(tok['expression'])
        return o

    def py_import(tok):
        """paste import statement in code
        Importing in Hapy. You can import:
        - Another .hapy "module"
        - A "custom" builtin module, see popo and test lol
        - Actual Python builtin modules, no restrictions for now!

        It was challenging at first, but thank God we achieved it.
        :)
        """
        (status, imp_type, result) = get(tok['module']['value'], is_local=local)
        if status and imp_type in (1, 2):
            o = result + '\n'
        elif status and imp_type == 3:
            o = 'import {module}\n'.format(**{'module': result})
        elif not status:
            o = '# !!! Hapy cannot import {module}. Sorry :/ !!!\n'.format(**{'module': tok['module']['value']})
        return o

    def py_prog(tok):
        return ';\n'.join(list(map(lambda x: pythonise(x), tok['prog'])))
    return pythonise(token)
if __name__ == '__main__':
    code = 'class Cow {\n        has name = {};\n\n       def when_created() {\n\n        };\n    };'
    inputs = InputStream(code)
    tokens = TokenStream(inputs)
    ast = parse(tokens)
    python_code = make_py(ast)
    print(python_code)