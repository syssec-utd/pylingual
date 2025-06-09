def peek(iterable):
    """
	Get the next value from an iterable, but also return an iterable
	that will subsequently return that value and the rest of the
	original iterable.

	>>> l = iter([1,2,3])
	>>> val, l = peek(l)
	>>> val
	1
	>>> list(l)
	[1, 2, 3]
	"""
    (peeker, original) = itertools.tee(iterable)
    return (next(peeker), original)