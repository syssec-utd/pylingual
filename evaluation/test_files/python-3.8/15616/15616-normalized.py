def sum(self):
    """Gets the sum of the data portions of all datapoints within"""
    raw = self.raw()
    s = 0
    for i in range(len(raw)):
        s += raw[i]['d']
    return s