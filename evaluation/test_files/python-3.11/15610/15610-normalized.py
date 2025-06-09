def sort(self, f=lambda d: d['t']):
    """Sort here works by sorting by timestamp by default"""
    list.sort(self, key=f)
    return self