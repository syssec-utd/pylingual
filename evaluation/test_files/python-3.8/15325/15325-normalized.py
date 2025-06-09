def every_other(iterable):
    """
	Yield every other item from the iterable

	>>> ' '.join(every_other('abcdefg'))
	'a c e g'
	"""
    items = iter(iterable)
    while True:
        try:
            yield next(items)
            next(items)
        except StopIteration:
            return