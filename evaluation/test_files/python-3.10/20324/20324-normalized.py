def _check_table(self):
    """Ensure that an incorrect table doesn't exist

        If a bad (old) table does exist, return False
        """
    cursor = self._db.execute('PRAGMA table_info(%s)' % self.table)
    lines = cursor.fetchall()
    if not lines:
        return True
    types = {}
    keys = []
    for line in lines:
        keys.append(line[1])
        types[line[1]] = line[2]
    if self._keys != keys:
        self.log.warn('keys mismatch')
        return False
    for key in self._keys:
        if types[key] != self._types[key]:
            self.log.warn('type mismatch: %s: %s != %s' % (key, types[key], self._types[key]))
            return False
    return True