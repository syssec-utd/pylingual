def make_rows(num_columns, seq):
    """
	Make a sequence into rows of num_columns columns.

	>>> tuple(make_rows(2, [1, 2, 3, 4, 5]))
	((1, 4), (2, 5), (3, None))
	>>> tuple(make_rows(3, [1, 2, 3, 4, 5]))
	((1, 3, 5), (2, 4, None))
	"""
    (num_rows, partial) = divmod(len(seq), num_columns)
    if partial:
        num_rows += 1
    try:
        result = more_itertools.grouper(seq, num_rows)
    except TypeError:
        result = more_itertools.grouper(num_rows, seq)
    return zip(*result)