def ascii_art(self, strict=False, show_internal=True):
    """
        Return a unicode string representing a tree in ASCII art fashion.

        :param strict: Use ASCII characters strictly (for the tree symbols).
        :param show_internal: Show labels of internal nodes.
        :return: unicode string

        >>> node = loads('((A,B)C,((D,E)F,G,H)I)J;')[0]
        >>> print(node.ascii_art(show_internal=False, strict=True))
                /-A
            /---|
            |   \\-B
        ----|       /-D
            |   /---|
            |   |   \\-E
            \\---|
                |-G
                \\-H
        """
    cmap = {'─': '-', '│': '|', '┌': '/', '└': '\\', '├': '|', '┤': '|', '┼': '+'}

    def normalize(line):
        m = re.compile('(?<=│)(?P<s>\\s+)(?=[┌└│])')
        line = m.sub(lambda m: m.group('s')[1:], line)
        line = re.sub('─│', '─┤', line)
        line = re.sub('│─', '├', line)
        line = re.sub('┤─', '┼', line)
        if strict:
            for u, a in cmap.items():
                line = line.replace(u, a)
        return line
    return '\n'.join((normalize(l) for l in self._ascii_art(show_internal=show_internal)[0] if set(l) != {' ', '│'}))