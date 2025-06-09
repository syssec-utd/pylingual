import re

class JamlError(Exception):
    pass

def readfile(name, encoding='utf8'):
    with open(name, encoding=encoding) as f:
        return read(f.read())

def read(text):
    return readlines(text.splitlines())

def readlines(lines):
    from trubar.messages import MsgNode

    def error(msg, line=None):
        raise JamlError(f'Line {line or lineno}: {msg}') from None

    def read_quoted(line):
        nonlocal lineno
        start_line = lineno
        block = ''
        q, line = (line[0], line[1:])
        while (mo := re.match(f'((?:[^{q}]|(?:{q}{q}))*){q}(?!{q})(.*)', line)) is None:
            block += line + '\n'
            try:
                lineno, line = next(linegen)
            except StopIteration:
                error('file ends before the end of quoted string', start_line)
        inside, after = mo.groups()
        block += inside
        return (block.replace(2 * q, q), after)

    def check_no_comments():
        if comments:
            error('stray comment', comment_start)
    items = {}
    stack = [(-1, items, True)]
    comments = []
    comment_start = None
    linegen = enumerate(lines, start=1)
    for lineno, line in linegen:
        if not line.strip():
            continue
        sline = line.lstrip()
        indent = len(line) - len(sline)
        line = sline
        last_indent, _, indent_expected = stack[-1]
        if indent_expected:
            if indent <= last_indent:
                error('indent expected')
            stack.append((indent, stack.pop()[1], False))
        elif indent > last_indent:
            error('unexpected indent')
        elif indent < last_indent:
            check_no_comments()
            while stack and indent != stack[-1][0]:
                stack.pop()
            if not stack:
                error('unindent does not match any outer level')
        if line[0] == '#':
            comments.append(line)
            comment_start = comment_start or lineno
            continue
        if line[0] in '\'"':
            key, after = read_quoted(line)
            if after[:2] != ': ':
                error("quoted key must be followed by a ': '")
            else:
                value = after[2:].lstrip()
        else:
            mo = re.match('(.*?):(?:\\s+|$)(.*)', line)
            if mo is None:
                if ':' in line:
                    raise error('colon at the end of the key should be followed by a space or a new line')
                else:
                    raise error('key followed by colon expected')
            key, value = mo.groups()
        if value.strip():
            if value[0] in '\'"':
                value, after = read_quoted(value)
                if after.strip():
                    error('quoted value must be followed by end of line')
            else:
                value = {'true': True, 'false': False, 'null': None}.get(value.strip(), value)
            stack[-1][1][key] = MsgNode(value, comments or None)
        else:
            space = {}
            stack[-1][1][key] = MsgNode(space, comments or None)
            stack.append((indent, space, True))
        comments = []
        comment_start = None
    if stack[-1][-1]:
        raise error('unexpected end of file')
    check_no_comments()
    return items

def dump(d, indent=''):

    def quotescape(s, allow_colon):
        if '\n' in s or (': ' in s and (not allow_colon)) or s[0] in ' #"\'|' or (s[-1] in ' \t\n'):
            q = '"' if "'" in s else "'"
            return f'{q}{s.replace(q, 2 * q)}{q}'
        return s

    def dumpval(s):
        trans = {True: 'true', False: 'false', None: 'null', '': '""'}
        if s in trans:
            return trans[s]
        return quotescape(s, True)
    res = ''
    for key, node in d.items():
        if node.comments is not None:
            res += ''.join((f'{indent}{comment}\n' for comment in node.comments))
        if isinstance(node.value, dict):
            res += f"{indent}{key}:\n{dump(node.value, indent + '    ')}"
        else:
            res += f'{indent}{quotescape(key, False)}: {dumpval(node.value)}\n'
    return res