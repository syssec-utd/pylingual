def compileActions(self):
    """Build the action table from the text above
        """
    import re
    self.actionList = actions = [None] * 121
    actions[73] = "b' the '+w+b' of the '"
    actionLines = self.actionTable.splitlines()
    colonPositions = [m.start() for m in re.finditer(':', actionLines[1])] + [100]
    columns = [(colonPositions[i] - 3, colonPositions[i + 1] - 3) for i in range(len(colonPositions) - 1)]
    for line in self.actionTable.splitlines(keepends=False):
        for (start, end) in columns:
            action = line[start:end]
            if not action or action.isspace():
                continue
            (index, colon, action) = (action[:3], action[3], action[4:])
            assert colon == ':'
            action = action.rstrip()
            action = action.replace('_', ' ')
            wPos = action.index('w')
            action = re.sub('^(.*)(?=\\+[U(]*w)', "b'\\1'", action)
            action = re.sub('(w[[:\\-1\\]).U]*)\\+(.*)$', "\\1+b'\\2'", action)
            action = action.replace('.U', '.upper()')
            actions[int(index)] = action