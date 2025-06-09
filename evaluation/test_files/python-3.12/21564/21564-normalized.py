def expand_aliases(self, fn, rest):
    """Expand multiple levels of aliases:

        if:

        alias foo bar /tmp
        alias baz foo

        then:

        baz huhhahhei -> bar /tmp huhhahhei
        """
    line = fn + ' ' + rest
    done = set()
    while 1:
        pre, _, fn, rest = split_user_input(line, shell_line_split)
        if fn in self.alias_table:
            if fn in done:
                warn("Cyclic alias definition, repeated '%s'" % fn)
                return ''
            done.add(fn)
            l2 = self.transform_alias(fn, rest)
            if l2 == line:
                break
            if l2.split(None, 1)[0] == line.split(None, 1)[0]:
                line = l2
                break
            line = l2
        else:
            break
    return line