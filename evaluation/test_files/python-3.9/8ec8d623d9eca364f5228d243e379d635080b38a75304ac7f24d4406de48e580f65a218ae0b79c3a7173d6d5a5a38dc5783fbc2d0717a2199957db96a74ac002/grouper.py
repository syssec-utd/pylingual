def grouper(iterable, n):
    from itertools import zip_longest
    args = [iter(iterable)] * n
    result = zip_longest(*args, fillvalue=None)
    return [list(filter(None.__ne__, x)) for x in result]