def _parse_lines(self, linesource):
    """ Parse lines of text for functions and classes """
    functions = []
    classes = []
    for line in linesource:
        if line.startswith('def ') and line.count('('):
            name = self._get_object_name(line)
            if not name.startswith('_'):
                functions.append(name)
        elif line.startswith('class '):
            name = self._get_object_name(line)
            if not name.startswith('_'):
                classes.append(name)
        else:
            pass
    functions.sort()
    classes.sort()
    return (functions, classes)