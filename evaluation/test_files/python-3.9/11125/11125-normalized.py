def format_numbers(data, headers, column_types=(), integer_format=None, float_format=None, **_):
    """Format numbers according to a format specification.

    This uses Python's format specification to format numbers of the following
    types: :class:`int`, :class:`py2:long` (Python 2), :class:`float`, and
    :class:`~decimal.Decimal`. See the :ref:`python:formatspec` for more
    information about the format strings.

    .. NOTE::
       A column is only formatted if all of its values are the same type
       (except for :data:`None`).

    :param iterable data: An :term:`iterable` (e.g. list) of rows.
    :param iterable headers: The column headers.
    :param iterable column_types: The columns' type objects (e.g. int or float).
    :param str integer_format: The format string to use for integer columns.
    :param str float_format: The format string to use for float columns.
    :return: The processed data and headers.
    :rtype: tuple

    """
    if integer_format is None and float_format is None or not column_types:
        return (iter(data), headers)

    def _format_number(field, column_type):
        if integer_format and column_type is int and (type(field) in int_types):
            return format(field, integer_format)
        elif float_format and column_type is float and (type(field) in float_types):
            return format(field, float_format)
        return field
    data = ([_format_number(v, column_types[i]) for (i, v) in enumerate(row)] for row in data)
    return (data, headers)