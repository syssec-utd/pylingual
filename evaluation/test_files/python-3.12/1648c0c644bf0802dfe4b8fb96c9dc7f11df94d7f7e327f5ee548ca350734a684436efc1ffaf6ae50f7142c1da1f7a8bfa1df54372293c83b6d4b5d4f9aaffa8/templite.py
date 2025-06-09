import sys
import os
import re

class Templite(object):
    autowrite = re.compile('(^[\'"])|(^[a-zA-Z0-9_\\.\\[\\]\'"]+$)')
    delimiters = ('${', '}$')
    cache = {}

    def __init__(self, text=None, filename=None, encoding='utf-8', delimiters=None, caching=False):
        """Loads a template from string or file."""
        if filename:
            filename = os.path.abspath(filename)
            mtime = os.path.getmtime(filename)
            self.file = key = filename
        elif text is not None:
            self.file = mtime = None
            key = hash(text)
        else:
            raise ValueError('either text or filename required')
        self.encoding = encoding
        self.caching = caching
        if delimiters:
            start, end = delimiters
            if len(start) != 2 or len(end) != 2:
                raise ValueError('each delimiter must be two characters long')
            self.delimiters = delimiters
        cache = self.cache
        if caching and key in cache and (cache[key][0] == mtime):
            self._code = cache[key][1]
            return
        if filename:
            with open(filename) as fh:
                text = fh.read()
        self._code = self._compile(text)
        if caching:
            cache[key] = (mtime, self._code)

    def _compile(self, source):
        offset = 0
        tokens = ['# -*- coding: %s -*-' % self.encoding]
        start, end = self.delimiters
        escaped = (re.escape(start), re.escape(end))
        regex = re.compile('%s(.*?)%s' % escaped, re.DOTALL)
        for i, part in enumerate(regex.split(source)):
            part = part.replace('\\'.join(start), start)
            part = part.replace('\\'.join(end), end)
            if i % 2 == 0:
                if not part:
                    continue
                lines = part.splitlines()
                if len(lines) > 1:
                    if all((not line.strip() for line in lines)):
                        continue
                part = part.replace('\\', '\\\\').replace('"', '\\"')
                part = '\t' * offset + 'write("""%s""")' % part
            else:
                part = part.rstrip()
                if not part:
                    continue
                part_stripped = part.lstrip()
                if part_stripped.startswith(':'):
                    if not offset:
                        raise SyntaxError('no block statement to terminate: ${%s}$' % part)
                    offset -= 1
                    part = part_stripped[1:]
                    if not part.endswith(':'):
                        continue
                elif self.autowrite.match(part_stripped):
                    part = 'write(%s)' % part_stripped
                lines = part.splitlines()
                margin = min((len(line) - len(line.lstrip()) for line in lines if line.strip()))
                part = '\n'.join(('\t' * offset + line[margin:] for line in lines))
                if part.endswith(':'):
                    offset += 1
            tokens.append(part)
        if offset:
            raise SyntaxError('%i block statement(s) not terminated' % offset)
        return compile('\n'.join(tokens), self.file or '<string>', 'exec')

    def render(self, **namespace):
        """Renders the template according to the given namespace."""
        stack = []
        namespace['__file__'] = self.file

        def write(*args):
            for value in args:
                stack.append(str(value))
        namespace['write'] = write

        def include(file):
            if not os.path.isabs(file):
                if self.file:
                    base = os.path.dirname(self.file)
                else:
                    base = os.path.dirname(sys.argv[0])
                file = os.path.join(base, file)
            t = Templite(None, file, self.encoding, self.delimiters, self.caching)
            stack.append(t.render(**namespace))
        namespace['include'] = include
        exec(self._code, namespace)
        return ''.join(stack)