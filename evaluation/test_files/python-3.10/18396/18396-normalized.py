def getMetricsColumnLengths(self):
    """
        Gets the maximum length of each column
        """
    displayLen = 0
    descLen = 0
    for m in self.metrics:
        displayLen = max(displayLen, len(m['displayName']))
        descLen = max(descLen, len(m['description']))
    return (displayLen, descLen)