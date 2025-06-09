"""
Module contains tools for processing files into DataFrames or other objects
"""
from __future__ import annotations
from collections import abc
import csv
import sys
from textwrap import fill
from typing import IO, Any, Callable, NamedTuple
import warnings
import numpy as np
import pandas._libs.lib as lib
from pandas._libs.parsers import STR_NA_VALUES
from pandas._typing import ArrayLike, CompressionOptions, CSVEngine, DtypeArg, FilePath, ReadCsvBuffer, StorageOptions
from pandas.errors import AbstractMethodError, ParserWarning
from pandas.util._decorators import Appender, deprecate_nonkeyword_arguments
from pandas.util._exceptions import find_stack_level
from pandas.util._validators import validate_bool_kwarg
from pandas.core.dtypes.common import is_file_like, is_float, is_integer, is_list_like
from pandas.core.frame import DataFrame
from pandas.core.indexes.api import RangeIndex
from pandas.core.shared_docs import _shared_docs
from pandas.io.common import IOHandles, get_handle, validate_header_arg
from pandas.io.parsers.arrow_parser_wrapper import ArrowParserWrapper
from pandas.io.parsers.base_parser import ParserBase, is_index_col, parser_defaults
from pandas.io.parsers.c_parser_wrapper import CParserWrapper
from pandas.io.parsers.python_parser import FixedWidthFieldParser, PythonParser
_doc_read_csv_and_table = '\n{summary}\n\nAlso supports optionally iterating or breaking of the file\ninto chunks.\n\nAdditional help can be found in the online docs for\n`IO Tools <https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html>`_.\n\nParameters\n----------\nfilepath_or_buffer : str, path object or file-like object\n    Any valid string path is acceptable. The string could be a URL. Valid\n    URL schemes include http, ftp, s3, gs, and file. For file URLs, a host is\n    expected. A local file could be: file://localhost/path/to/table.csv.\n\n    If you want to pass in a path object, pandas accepts any ``os.PathLike``.\n\n    By file-like object, we refer to objects with a ``read()`` method, such as\n    a file handle (e.g. via builtin ``open`` function) or ``StringIO``.\nsep : str, default {_default_sep}\n    Delimiter to use. If sep is None, the C engine cannot automatically detect\n    the separator, but the Python parsing engine can, meaning the latter will\n    be used and automatically detect the separator by Python\'s builtin sniffer\n    tool, ``csv.Sniffer``. In addition, separators longer than 1 character and\n    different from ``\'\\s+\'`` will be interpreted as regular expressions and\n    will also force the use of the Python parsing engine. Note that regex\n    delimiters are prone to ignoring quoted data. Regex example: ``\'\\r\\t\'``.\ndelimiter : str, default ``None``\n    Alias for sep.\nheader : int, list of int, None, default \'infer\'\n    Row number(s) to use as the column names, and the start of the\n    data.  Default behavior is to infer the column names: if no names\n    are passed the behavior is identical to ``header=0`` and column\n    names are inferred from the first line of the file, if column\n    names are passed explicitly then the behavior is identical to\n    ``header=None``. Explicitly pass ``header=0`` to be able to\n    replace existing names. The header can be a list of integers that\n    specify row locations for a multi-index on the columns\n    e.g. [0,1,3]. Intervening rows that are not specified will be\n    skipped (e.g. 2 in this example is skipped). Note that this\n    parameter ignores commented lines and empty lines if\n    ``skip_blank_lines=True``, so ``header=0`` denotes the first line of\n    data rather than the first line of the file.\nnames : array-like, optional\n    List of column names to use. If the file contains a header row,\n    then you should explicitly pass ``header=0`` to override the column names.\n    Duplicates in this list are not allowed.\nindex_col : int, str, sequence of int / str, or False, optional, default ``None``\n  Column(s) to use as the row labels of the ``DataFrame``, either given as\n  string name or column index. If a sequence of int / str is given, a\n  MultiIndex is used.\n\n  Note: ``index_col=False`` can be used to force pandas to *not* use the first\n  column as the index, e.g. when you have a malformed file with delimiters at\n  the end of each line.\nusecols : list-like or callable, optional\n    Return a subset of the columns. If list-like, all elements must either\n    be positional (i.e. integer indices into the document columns) or strings\n    that correspond to column names provided either by the user in `names` or\n    inferred from the document header row(s). If ``names`` are given, the document\n    header row(s) are not taken into account. For example, a valid list-like\n    `usecols` parameter would be ``[0, 1, 2]`` or ``[\'foo\', \'bar\', \'baz\']``.\n    Element order is ignored, so ``usecols=[0, 1]`` is the same as ``[1, 0]``.\n    To instantiate a DataFrame from ``data`` with element order preserved use\n    ``pd.read_csv(data, usecols=[\'foo\', \'bar\'])[[\'foo\', \'bar\']]`` for columns\n    in ``[\'foo\', \'bar\']`` order or\n    ``pd.read_csv(data, usecols=[\'foo\', \'bar\'])[[\'bar\', \'foo\']]``\n    for ``[\'bar\', \'foo\']`` order.\n\n    If callable, the callable function will be evaluated against the column\n    names, returning names where the callable function evaluates to True. An\n    example of a valid callable argument would be ``lambda x: x.upper() in\n    [\'AAA\', \'BBB\', \'DDD\']``. Using this parameter results in much faster\n    parsing time and lower memory usage.\nsqueeze : bool, default False\n    If the parsed data only contains one column then return a Series.\n\n    .. deprecated:: 1.4.0\n        Append ``.squeeze("columns")`` to the call to ``{func_name}`` to squeeze\n        the data.\nprefix : str, optional\n    Prefix to add to column numbers when no header, e.g. \'X\' for X0, X1, ...\n\n    .. deprecated:: 1.4.0\n       Use a list comprehension on the DataFrame\'s columns after calling ``read_csv``.\nmangle_dupe_cols : bool, default True\n    Duplicate columns will be specified as \'X\', \'X.1\', ...\'X.N\', rather than\n    \'X\'...\'X\'. Passing in False will cause data to be overwritten if there\n    are duplicate names in the columns.\ndtype : Type name or dict of column -> type, optional\n    Data type for data or columns. E.g. {{\'a\': np.float64, \'b\': np.int32,\n    \'c\': \'Int64\'}}\n    Use `str` or `object` together with suitable `na_values` settings\n    to preserve and not interpret dtype.\n    If converters are specified, they will be applied INSTEAD\n    of dtype conversion.\nengine : {{\'c\', \'python\', \'pyarrow\'}}, optional\n    Parser engine to use. The C and pyarrow engines are faster, while the python engine\n    is currently more feature-complete. Multithreading is currently only supported by\n    the pyarrow engine.\n\n    .. versionadded:: 1.4.0\n\n        The "pyarrow" engine was added as an *experimental* engine, and some features\n        are unsupported, or may not work correctly, with this engine.\nconverters : dict, optional\n    Dict of functions for converting values in certain columns. Keys can either\n    be integers or column labels.\ntrue_values : list, optional\n    Values to consider as True.\nfalse_values : list, optional\n    Values to consider as False.\nskipinitialspace : bool, default False\n    Skip spaces after delimiter.\nskiprows : list-like, int or callable, optional\n    Line numbers to skip (0-indexed) or number of lines to skip (int)\n    at the start of the file.\n\n    If callable, the callable function will be evaluated against the row\n    indices, returning True if the row should be skipped and False otherwise.\n    An example of a valid callable argument would be ``lambda x: x in [0, 2]``.\nskipfooter : int, default 0\n    Number of lines at bottom of file to skip (Unsupported with engine=\'c\').\nnrows : int, optional\n    Number of rows of file to read. Useful for reading pieces of large files.\nna_values : scalar, str, list-like, or dict, optional\n    Additional strings to recognize as NA/NaN. If dict passed, specific\n    per-column NA values.  By default the following values are interpreted as\n    NaN: \'' + fill("', '".join(sorted(STR_NA_VALUES)), 70, subsequent_indent='    ') + '\'.\nkeep_default_na : bool, default True\n    Whether or not to include the default NaN values when parsing the data.\n    Depending on whether `na_values` is passed in, the behavior is as follows:\n\n    * If `keep_default_na` is True, and `na_values` are specified, `na_values`\n      is appended to the default NaN values used for parsing.\n    * If `keep_default_na` is True, and `na_values` are not specified, only\n      the default NaN values are used for parsing.\n    * If `keep_default_na` is False, and `na_values` are specified, only\n      the NaN values specified `na_values` are used for parsing.\n    * If `keep_default_na` is False, and `na_values` are not specified, no\n      strings will be parsed as NaN.\n\n    Note that if `na_filter` is passed in as False, the `keep_default_na` and\n    `na_values` parameters will be ignored.\nna_filter : bool, default True\n    Detect missing value markers (empty strings and the value of na_values). In\n    data without any NAs, passing na_filter=False can improve the performance\n    of reading a large file.\nverbose : bool, default False\n    Indicate number of NA values placed in non-numeric columns.\nskip_blank_lines : bool, default True\n    If True, skip over blank lines rather than interpreting as NaN values.\nparse_dates : bool or list of int or names or list of lists or dict, default False\n    The behavior is as follows:\n\n    * boolean. If True -> try parsing the index.\n    * list of int or names. e.g. If [1, 2, 3] -> try parsing columns 1, 2, 3\n      each as a separate date column.\n    * list of lists. e.g.  If [[1, 3]] -> combine columns 1 and 3 and parse as\n      a single date column.\n    * dict, e.g. {{\'foo\' : [1, 3]}} -> parse columns 1, 3 as date and call\n      result \'foo\'\n\n    If a column or index cannot be represented as an array of datetimes,\n    say because of an unparsable value or a mixture of timezones, the column\n    or index will be returned unaltered as an object data type. For\n    non-standard datetime parsing, use ``pd.to_datetime`` after\n    ``pd.read_csv``. To parse an index or column with a mixture of timezones,\n    specify ``date_parser`` to be a partially-applied\n    :func:`pandas.to_datetime` with ``utc=True``. See\n    :ref:`io.csv.mixed_timezones` for more.\n\n    Note: A fast-path exists for iso8601-formatted dates.\ninfer_datetime_format : bool, default False\n    If True and `parse_dates` is enabled, pandas will attempt to infer the\n    format of the datetime strings in the columns, and if it can be inferred,\n    switch to a faster method of parsing them. In some cases this can increase\n    the parsing speed by 5-10x.\nkeep_date_col : bool, default False\n    If True and `parse_dates` specifies combining multiple columns then\n    keep the original columns.\ndate_parser : function, optional\n    Function to use for converting a sequence of string columns to an array of\n    datetime instances. The default uses ``dateutil.parser.parser`` to do the\n    conversion. Pandas will try to call `date_parser` in three different ways,\n    advancing to the next if an exception occurs: 1) Pass one or more arrays\n    (as defined by `parse_dates`) as arguments; 2) concatenate (row-wise) the\n    string values from the columns defined by `parse_dates` into a single array\n    and pass that; and 3) call `date_parser` once for each row using one or\n    more strings (corresponding to the columns defined by `parse_dates`) as\n    arguments.\ndayfirst : bool, default False\n    DD/MM format dates, international and European format.\ncache_dates : bool, default True\n    If True, use a cache of unique, converted dates to apply the datetime\n    conversion. May produce significant speed-up when parsing duplicate\n    date strings, especially ones with timezone offsets.\n\n    .. versionadded:: 0.25.0\niterator : bool, default False\n    Return TextFileReader object for iteration or getting chunks with\n    ``get_chunk()``.\n\n    .. versionchanged:: 1.2\n\n       ``TextFileReader`` is a context manager.\nchunksize : int, optional\n    Return TextFileReader object for iteration.\n    See the `IO Tools docs\n    <https://pandas.pydata.org/pandas-docs/stable/io.html#io-chunking>`_\n    for more information on ``iterator`` and ``chunksize``.\n\n    .. versionchanged:: 1.2\n\n       ``TextFileReader`` is a context manager.\n{decompression_options}\n\n    .. versionchanged:: 1.4.0 Zstandard support.\n\nthousands : str, optional\n    Thousands separator.\ndecimal : str, default \'.\'\n    Character to recognize as decimal point (e.g. use \',\' for European data).\nlineterminator : str (length 1), optional\n    Character to break file into lines. Only valid with C parser.\nquotechar : str (length 1), optional\n    The character used to denote the start and end of a quoted item. Quoted\n    items can include the delimiter and it will be ignored.\nquoting : int or csv.QUOTE_* instance, default 0\n    Control field quoting behavior per ``csv.QUOTE_*`` constants. Use one of\n    QUOTE_MINIMAL (0), QUOTE_ALL (1), QUOTE_NONNUMERIC (2) or QUOTE_NONE (3).\ndoublequote : bool, default ``True``\n   When quotechar is specified and quoting is not ``QUOTE_NONE``, indicate\n   whether or not to interpret two consecutive quotechar elements INSIDE a\n   field as a single ``quotechar`` element.\nescapechar : str (length 1), optional\n    One-character string used to escape other characters.\ncomment : str, optional\n    Indicates remainder of line should not be parsed. If found at the beginning\n    of a line, the line will be ignored altogether. This parameter must be a\n    single character. Like empty lines (as long as ``skip_blank_lines=True``),\n    fully commented lines are ignored by the parameter `header` but not by\n    `skiprows`. For example, if ``comment=\'#\'``, parsing\n    ``#empty\\na,b,c\\n1,2,3`` with ``header=0`` will result in \'a,b,c\' being\n    treated as the header.\nencoding : str, optional\n    Encoding to use for UTF when reading/writing (ex. \'utf-8\'). `List of Python\n    standard encodings\n    <https://docs.python.org/3/library/codecs.html#standard-encodings>`_ .\n\n    .. versionchanged:: 1.2\n\n       When ``encoding`` is ``None``, ``errors="replace"`` is passed to\n       ``open()``. Otherwise, ``errors="strict"`` is passed to ``open()``.\n       This behavior was previously only the case for ``engine="python"``.\n\n    .. versionchanged:: 1.3.0\n\n       ``encoding_errors`` is a new argument. ``encoding`` has no longer an\n       influence on how encoding errors are handled.\n\nencoding_errors : str, optional, default "strict"\n    How encoding errors are treated. `List of possible values\n    <https://docs.python.org/3/library/codecs.html#error-handlers>`_ .\n\n    .. versionadded:: 1.3.0\n\ndialect : str or csv.Dialect, optional\n    If provided, this parameter will override values (default or not) for the\n    following parameters: `delimiter`, `doublequote`, `escapechar`,\n    `skipinitialspace`, `quotechar`, and `quoting`. If it is necessary to\n    override values, a ParserWarning will be issued. See csv.Dialect\n    documentation for more details.\nerror_bad_lines : bool, optional, default ``None``\n    Lines with too many fields (e.g. a csv line with too many commas) will by\n    default cause an exception to be raised, and no DataFrame will be returned.\n    If False, then these "bad lines" will be dropped from the DataFrame that is\n    returned.\n\n    .. deprecated:: 1.3.0\n       The ``on_bad_lines`` parameter should be used instead to specify behavior upon\n       encountering a bad line instead.\nwarn_bad_lines : bool, optional, default ``None``\n    If error_bad_lines is False, and warn_bad_lines is True, a warning for each\n    "bad line" will be output.\n\n    .. deprecated:: 1.3.0\n       The ``on_bad_lines`` parameter should be used instead to specify behavior upon\n       encountering a bad line instead.\non_bad_lines : {{\'error\', \'warn\', \'skip\'}} or callable, default \'error\'\n    Specifies what to do upon encountering a bad line (a line with too many fields).\n    Allowed values are :\n\n        - \'error\', raise an Exception when a bad line is encountered.\n        - \'warn\', raise a warning when a bad line is encountered and skip that line.\n        - \'skip\', skip bad lines without raising or warning when they are encountered.\n\n    .. versionadded:: 1.3.0\n\n        - callable, function with signature\n          ``(bad_line: list[str]) -> list[str] | None`` that will process a single\n          bad line. ``bad_line`` is a list of strings split by the ``sep``.\n          If the function returns ``None``, the bad line will be ignored.\n          If the function returns a new list of strings with more elements than\n          expected, a ``ParserWarning`` will be emitted while dropping extra elements.\n          Only supported when ``engine="python"``\n\n    .. versionadded:: 1.4.0\n\ndelim_whitespace : bool, default False\n    Specifies whether or not whitespace (e.g. ``\' \'`` or ``\'\t\'``) will be\n    used as the sep. Equivalent to setting ``sep=\'\\s+\'``. If this option\n    is set to True, nothing should be passed in for the ``delimiter``\n    parameter.\nlow_memory : bool, default True\n    Internally process the file in chunks, resulting in lower memory use\n    while parsing, but possibly mixed type inference.  To ensure no mixed\n    types either set False, or specify the type with the `dtype` parameter.\n    Note that the entire file is read into a single DataFrame regardless,\n    use the `chunksize` or `iterator` parameter to return the data in chunks.\n    (Only valid with C parser).\nmemory_map : bool, default False\n    If a filepath is provided for `filepath_or_buffer`, map the file object\n    directly onto memory and access the data directly from there. Using this\n    option can improve performance because there is no longer any I/O overhead.\nfloat_precision : str, optional\n    Specifies which converter the C engine should use for floating-point\n    values. The options are ``None`` or \'high\' for the ordinary converter,\n    \'legacy\' for the original lower precision pandas converter, and\n    \'round_trip\' for the round-trip converter.\n\n    .. versionchanged:: 1.2\n\n{storage_options}\n\n    .. versionadded:: 1.2\n\nReturns\n-------\nDataFrame or TextParser\n    A comma-separated values (csv) file is returned as two-dimensional\n    data structure with labeled axes.\n\nSee Also\n--------\nDataFrame.to_csv : Write DataFrame to a comma-separated values (csv) file.\nread_csv : Read a comma-separated values (csv) file into DataFrame.\nread_fwf : Read a table of fixed-width formatted lines into DataFrame.\n\nExamples\n--------\n>>> pd.{func_name}(\'data.csv\')  # doctest: +SKIP\n'
_c_parser_defaults = {'delim_whitespace': False, 'na_filter': True, 'low_memory': True, 'memory_map': False, 'float_precision': None}
_fwf_defaults = {'colspecs': 'infer', 'infer_nrows': 100, 'widths': None}
_c_unsupported = {'skipfooter'}
_python_unsupported = {'low_memory', 'float_precision'}
_pyarrow_unsupported = {'skipfooter', 'float_precision', 'chunksize', 'comment', 'nrows', 'thousands', 'memory_map', 'dialect', 'warn_bad_lines', 'error_bad_lines', 'on_bad_lines', 'delim_whitespace', 'quoting', 'lineterminator', 'converters', 'decimal', 'iterator', 'dayfirst', 'infer_datetime_format', 'verbose', 'skipinitialspace', 'low_memory'}

class _DeprecationConfig(NamedTuple):
    default_value: Any
    msg: str | None
_deprecated_defaults: dict[str, _DeprecationConfig] = {'error_bad_lines': _DeprecationConfig(None, 'Use on_bad_lines in the future.'), 'warn_bad_lines': _DeprecationConfig(None, 'Use on_bad_lines in the future.'), 'squeeze': _DeprecationConfig(None, 'Append .squeeze("columns") to the call to squeeze.'), 'prefix': _DeprecationConfig(None, 'Use a list comprehension on the column names in the future.')}

def validate_integer(name, val, min_val=0):
    """
    Checks whether the 'name' parameter for parsing is either
    an integer OR float that can SAFELY be cast to an integer
    without losing accuracy. Raises a ValueError if that is
    not the case.

    Parameters
    ----------
    name : str
        Parameter name (used for error reporting)
    val : int or float
        The value to check
    min_val : int
        Minimum allowed value (val < min_val will result in a ValueError)
    """
    msg = f"'{name:s}' must be an integer >={min_val:d}"
    if val is not None:
        if is_float(val):
            if int(val) != val:
                raise ValueError(msg)
            val = int(val)
        elif not (is_integer(val) and val >= min_val):
            raise ValueError(msg)
    return val

def _validate_names(names):
    """
    Raise ValueError if the `names` parameter contains duplicates or has an
    invalid data type.

    Parameters
    ----------
    names : array-like or None
        An array containing a list of the names used for the output DataFrame.

    Raises
    ------
    ValueError
        If names are not unique or are not ordered (e.g. set).
    """
    if names is not None:
        if len(names) != len(set(names)):
            raise ValueError('Duplicate names are not allowed.')
        if not (is_list_like(names, allow_sets=False) or isinstance(names, abc.KeysView)):
            raise ValueError('Names should be an ordered collection.')

def _read(filepath_or_buffer: FilePath | ReadCsvBuffer[bytes] | ReadCsvBuffer[str], kwds):
    """Generic reader of line files."""
    if kwds.get('date_parser', None) is not None and kwds.get('parse_dates', None) is None:
        kwds['parse_dates'] = True
    elif kwds.get('parse_dates', None) is None:
        kwds['parse_dates'] = False
    iterator = kwds.get('iterator', False)
    chunksize = kwds.get('chunksize', None)
    if kwds.get('engine') == 'pyarrow':
        if iterator:
            raise ValueError("The 'iterator' option is not supported with the 'pyarrow' engine")
        if chunksize is not None:
            raise ValueError("The 'chunksize' option is not supported with the 'pyarrow' engine")
    else:
        chunksize = validate_integer('chunksize', kwds.get('chunksize', None), 1)
    nrows = kwds.get('nrows', None)
    _validate_names(kwds.get('names', None))
    parser = TextFileReader(filepath_or_buffer, **kwds)
    if chunksize or iterator:
        return parser
    with parser:
        return parser.read(nrows)

@deprecate_nonkeyword_arguments(version=None, allowed_args=['filepath_or_buffer'], stacklevel=3)
@Appender(_doc_read_csv_and_table.format(func_name='read_csv', summary='Read a comma-separated values (csv) file into DataFrame.', _default_sep="','", storage_options=_shared_docs['storage_options'], decompression_options=_shared_docs['decompression_options']))
def read_csv(filepath_or_buffer: FilePath | ReadCsvBuffer[bytes] | ReadCsvBuffer[str], sep=lib.no_default, delimiter=None, header='infer', names=lib.no_default, index_col=None, usecols=None, squeeze=None, prefix=lib.no_default, mangle_dupe_cols=True, dtype: DtypeArg | None=None, engine: CSVEngine | None=None, converters=None, true_values=None, false_values=None, skipinitialspace=False, skiprows=None, skipfooter=0, nrows=None, na_values=None, keep_default_na=True, na_filter=True, verbose=False, skip_blank_lines=True, parse_dates=None, infer_datetime_format=False, keep_date_col=False, date_parser=None, dayfirst=False, cache_dates=True, iterator=False, chunksize=None, compression: CompressionOptions='infer', thousands=None, decimal: str='.', lineterminator=None, quotechar='"', quoting=csv.QUOTE_MINIMAL, doublequote=True, escapechar=None, comment=None, encoding=None, encoding_errors: str | None='strict', dialect=None, error_bad_lines=None, warn_bad_lines=None, on_bad_lines=None, delim_whitespace=False, low_memory=_c_parser_defaults['low_memory'], memory_map=False, float_precision=None, storage_options: StorageOptions=None):
    kwds = locals().copy()
    del kwds['filepath_or_buffer']
    del kwds['sep']
    kwds_defaults = _refine_defaults_read(dialect, delimiter, delim_whitespace, engine, sep, error_bad_lines, warn_bad_lines, on_bad_lines, names, prefix, defaults={'delimiter': ','})
    kwds.update(kwds_defaults)
    return _read(filepath_or_buffer, kwds)

@deprecate_nonkeyword_arguments(version=None, allowed_args=['filepath_or_buffer'], stacklevel=3)
@Appender(_doc_read_csv_and_table.format(func_name='read_table', summary='Read general delimited file into DataFrame.', _default_sep="'\\\\t' (tab-stop)", storage_options=_shared_docs['storage_options'], decompression_options=_shared_docs['decompression_options']))
def read_table(filepath_or_buffer: FilePath | ReadCsvBuffer[bytes] | ReadCsvBuffer[str], sep=lib.no_default, delimiter=None, header='infer', names=lib.no_default, index_col=None, usecols=None, squeeze=None, prefix=lib.no_default, mangle_dupe_cols=True, dtype: DtypeArg | None=None, engine: CSVEngine | None=None, converters=None, true_values=None, false_values=None, skipinitialspace=False, skiprows=None, skipfooter=0, nrows=None, na_values=None, keep_default_na=True, na_filter=True, verbose=False, skip_blank_lines=True, parse_dates=False, infer_datetime_format=False, keep_date_col=False, date_parser=None, dayfirst=False, cache_dates=True, iterator=False, chunksize=None, compression: CompressionOptions='infer', thousands=None, decimal: str='.', lineterminator=None, quotechar='"', quoting=csv.QUOTE_MINIMAL, doublequote=True, escapechar=None, comment=None, encoding=None, encoding_errors: str | None='strict', dialect=None, error_bad_lines=None, warn_bad_lines=None, on_bad_lines=None, delim_whitespace=False, low_memory=_c_parser_defaults['low_memory'], memory_map=False, float_precision=None, storage_options: StorageOptions=None):
    kwds = locals().copy()
    del kwds['filepath_or_buffer']
    del kwds['sep']
    kwds_defaults = _refine_defaults_read(dialect, delimiter, delim_whitespace, engine, sep, error_bad_lines, warn_bad_lines, on_bad_lines, names, prefix, defaults={'delimiter': '\t'})
    kwds.update(kwds_defaults)
    return _read(filepath_or_buffer, kwds)

@deprecate_nonkeyword_arguments(version=None, allowed_args=['filepath_or_buffer'], stacklevel=2)
def read_fwf(filepath_or_buffer: FilePath | ReadCsvBuffer[bytes] | ReadCsvBuffer[str], colspecs: list[tuple[int, int]] | str | None='infer', widths: list[int] | None=None, infer_nrows: int=100, **kwds) -> DataFrame | TextFileReader:
    """
    Read a table of fixed-width formatted lines into DataFrame.

    Also supports optionally iterating or breaking of the file
    into chunks.

    Additional help can be found in the `online docs for IO Tools
    <https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html>`_.

    Parameters
    ----------
    filepath_or_buffer : str, path object, or file-like object
        String, path object (implementing ``os.PathLike[str]``), or file-like
        object implementing a text ``read()`` function.The string could be a URL.
        Valid URL schemes include http, ftp, s3, and file. For file URLs, a host is
        expected. A local file could be:
        ``file://localhost/path/to/table.csv``.
    colspecs : list of tuple (int, int) or 'infer'. optional
        A list of tuples giving the extents of the fixed-width
        fields of each line as half-open intervals (i.e.,  [from, to[ ).
        String value 'infer' can be used to instruct the parser to try
        detecting the column specifications from the first 100 rows of
        the data which are not being skipped via skiprows (default='infer').
    widths : list of int, optional
        A list of field widths which can be used instead of 'colspecs' if
        the intervals are contiguous.
    infer_nrows : int, default 100
        The number of rows to consider when letting the parser determine the
        `colspecs`.
    **kwds : optional
        Optional keyword arguments can be passed to ``TextFileReader``.

    Returns
    -------
    DataFrame or TextFileReader
        A comma-separated values (csv) file is returned as two-dimensional
        data structure with labeled axes.

    See Also
    --------
    DataFrame.to_csv : Write DataFrame to a comma-separated values (csv) file.
    read_csv : Read a comma-separated values (csv) file into DataFrame.

    Examples
    --------
    >>> pd.read_fwf('data.csv')  # doctest: +SKIP
    """
    if colspecs is None and widths is None:
        raise ValueError('Must specify either colspecs or widths')
    elif colspecs not in (None, 'infer') and widths is not None:
        raise ValueError("You must specify only one of 'widths' and 'colspecs'")
    if widths is not None:
        (colspecs, col) = ([], 0)
        for w in widths:
            colspecs.append((col, col + w))
            col += w
    assert colspecs is not None
    names = kwds.get('names')
    if names is not None:
        if len(names) != len(colspecs) and colspecs != 'infer':
            len_index = 0
            if kwds.get('index_col') is not None:
                index_col: Any = kwds.get('index_col')
                if index_col is not False:
                    if not is_list_like(index_col):
                        len_index = 1
                    else:
                        len_index = len(index_col)
            if len(names) + len_index != len(colspecs):
                raise ValueError('Length of colspecs must match length of names')
    kwds['colspecs'] = colspecs
    kwds['infer_nrows'] = infer_nrows
    kwds['engine'] = 'python-fwf'
    return _read(filepath_or_buffer, kwds)

class TextFileReader(abc.Iterator):
    """

    Passed dialect overrides any of the related parser options

    """

    def __init__(self, f: FilePath | ReadCsvBuffer[bytes] | ReadCsvBuffer[str] | list, engine: CSVEngine | None=None, **kwds):
        if engine is not None:
            engine_specified = True
        else:
            engine = 'python'
            engine_specified = False
        self.engine = engine
        self._engine_specified = kwds.get('engine_specified', engine_specified)
        _validate_skipfooter(kwds)
        dialect = _extract_dialect(kwds)
        if dialect is not None:
            if engine == 'pyarrow':
                raise ValueError("The 'dialect' option is not supported with the 'pyarrow' engine")
            kwds = _merge_with_dialect_properties(dialect, kwds)
        if kwds.get('header', 'infer') == 'infer':
            kwds['header'] = 0 if kwds.get('names') is None else None
        self.orig_options = kwds
        self._currow = 0
        options = self._get_options_with_defaults(engine)
        options['storage_options'] = kwds.get('storage_options', None)
        self.chunksize = options.pop('chunksize', None)
        self.nrows = options.pop('nrows', None)
        self._check_file_or_buffer(f, engine)
        (self.options, self.engine) = self._clean_options(options, engine)
        self.squeeze = self.options.pop('squeeze', False)
        if 'has_index_names' in kwds:
            self.options['has_index_names'] = kwds['has_index_names']
        self.handles: IOHandles | None = None
        self._engine = self._make_engine(f, self.engine)

    def close(self):
        if self.handles is not None:
            self.handles.close()
        self._engine.close()

    def _get_options_with_defaults(self, engine):
        kwds = self.orig_options
        options = {}
        default: object | None
        for (argname, default) in parser_defaults.items():
            value = kwds.get(argname, default)
            if engine == 'pyarrow' and argname in _pyarrow_unsupported and (value != default) and (value != getattr(value, 'value', default)):
                if argname == 'on_bad_lines' and kwds.get('error_bad_lines') is not None:
                    argname = 'error_bad_lines'
                elif argname == 'on_bad_lines' and kwds.get('warn_bad_lines') is not None:
                    argname = 'warn_bad_lines'
                raise ValueError(f"The {repr(argname)} option is not supported with the 'pyarrow' engine")
            elif argname == 'mangle_dupe_cols' and value is False:
                raise ValueError('Setting mangle_dupe_cols=False is not supported yet')
            else:
                options[argname] = value
        for (argname, default) in _c_parser_defaults.items():
            if argname in kwds:
                value = kwds[argname]
                if engine != 'c' and value != default:
                    if 'python' in engine and argname not in _python_unsupported:
                        pass
                    elif value == _deprecated_defaults.get(argname, _DeprecationConfig(default, None)).default_value:
                        pass
                    else:
                        raise ValueError(f'The {repr(argname)} option is not supported with the {repr(engine)} engine')
            else:
                value = _deprecated_defaults.get(argname, _DeprecationConfig(default, None)).default_value
            options[argname] = value
        if engine == 'python-fwf':
            for (argname, default) in _fwf_defaults.items():
                options[argname] = kwds.get(argname, default)
        return options

    def _check_file_or_buffer(self, f, engine):
        if is_file_like(f) and engine != 'c' and (not hasattr(f, '__iter__')):
            raise ValueError("The 'python' engine cannot iterate through this file buffer.")

    def _clean_options(self, options, engine):
        result = options.copy()
        fallback_reason = None
        if engine == 'c':
            if options['skipfooter'] > 0:
                fallback_reason = "the 'c' engine does not support skipfooter"
                engine = 'python'
        sep = options['delimiter']
        delim_whitespace = options['delim_whitespace']
        if sep is None and (not delim_whitespace):
            if engine in ('c', 'pyarrow'):
                fallback_reason = f"the '{engine}' engine does not support sep=None with delim_whitespace=False"
                engine = 'python'
        elif sep is not None and len(sep) > 1:
            if engine == 'c' and sep == '\\s+':
                result['delim_whitespace'] = True
                del result['delimiter']
            elif engine not in ('python', 'python-fwf'):
                fallback_reason = f"the '{engine}' engine does not support regex separators (separators > 1 char and different from '\\s+' are interpreted as regex)"
                engine = 'python'
        elif delim_whitespace:
            if 'python' in engine:
                result['delimiter'] = '\\s+'
        elif sep is not None:
            encodeable = True
            encoding = sys.getfilesystemencoding() or 'utf-8'
            try:
                if len(sep.encode(encoding)) > 1:
                    encodeable = False
            except UnicodeDecodeError:
                encodeable = False
            if not encodeable and engine not in ('python', 'python-fwf'):
                fallback_reason = f"the separator encoded in {encoding} is > 1 char long, and the '{engine}' engine does not support such separators"
                engine = 'python'
        quotechar = options['quotechar']
        if quotechar is not None and isinstance(quotechar, (str, bytes)):
            if len(quotechar) == 1 and ord(quotechar) > 127 and (engine not in ('python', 'python-fwf')):
                fallback_reason = f"ord(quotechar) > 127, meaning the quotechar is larger than one byte, and the '{engine}' engine does not support such quotechars"
                engine = 'python'
        if fallback_reason and self._engine_specified:
            raise ValueError(fallback_reason)
        if engine == 'c':
            for arg in _c_unsupported:
                del result[arg]
        if 'python' in engine:
            for arg in _python_unsupported:
                if fallback_reason and result[arg] != _c_parser_defaults[arg]:
                    raise ValueError(f"Falling back to the 'python' engine because {fallback_reason}, but this causes {repr(arg)} to be ignored as it is not supported by the 'python' engine.")
                del result[arg]
        if fallback_reason:
            warnings.warn(f"Falling back to the 'python' engine because {fallback_reason}; you can avoid this warning by specifying engine='python'.", ParserWarning, stacklevel=find_stack_level())
        index_col = options['index_col']
        names = options['names']
        converters = options['converters']
        na_values = options['na_values']
        skiprows = options['skiprows']
        validate_header_arg(options['header'])
        for arg in _deprecated_defaults.keys():
            parser_default = _c_parser_defaults.get(arg, parser_defaults[arg])
            depr_default = _deprecated_defaults[arg]
            if result.get(arg, depr_default) != depr_default.default_value:
                msg = f'The {arg} argument has been deprecated and will be removed in a future version. {depr_default.msg}\n\n'
                warnings.warn(msg, FutureWarning, stacklevel=find_stack_level())
            else:
                result[arg] = parser_default
        if index_col is True:
            raise ValueError("The value of index_col couldn't be 'True'")
        if is_index_col(index_col):
            if not isinstance(index_col, (list, tuple, np.ndarray)):
                index_col = [index_col]
        result['index_col'] = index_col
        names = list(names) if names is not None else names
        if converters is not None:
            if not isinstance(converters, dict):
                raise TypeError(f'Type converters must be a dict or subclass, input was a {type(converters).__name__}')
        else:
            converters = {}
        keep_default_na = options['keep_default_na']
        (na_values, na_fvalues) = _clean_na_values(na_values, keep_default_na)
        if engine == 'pyarrow':
            if not is_integer(skiprows) and skiprows is not None:
                raise ValueError("skiprows argument must be an integer when using engine='pyarrow'")
        else:
            if is_integer(skiprows):
                skiprows = list(range(skiprows))
            if skiprows is None:
                skiprows = set()
            elif not callable(skiprows):
                skiprows = set(skiprows)
        result['names'] = names
        result['converters'] = converters
        result['na_values'] = na_values
        result['na_fvalues'] = na_fvalues
        result['skiprows'] = skiprows
        result['squeeze'] = False if options['squeeze'] is None else options['squeeze']
        return (result, engine)

    def __next__(self):
        try:
            return self.get_chunk()
        except StopIteration:
            self.close()
            raise

    def _make_engine(self, f: FilePath | ReadCsvBuffer[bytes] | ReadCsvBuffer[str] | list | IO, engine: CSVEngine='c'):
        mapping: dict[str, type[ParserBase]] = {'c': CParserWrapper, 'python': PythonParser, 'pyarrow': ArrowParserWrapper, 'python-fwf': FixedWidthFieldParser}
        if engine not in mapping:
            raise ValueError(f'Unknown engine: {engine} (valid options are {mapping.keys()})')
        if not isinstance(f, list):
            is_text = True
            mode = 'r'
            if engine == 'pyarrow':
                is_text = False
                mode = 'rb'
            self.handles = get_handle(f, mode, encoding=self.options.get('encoding', None), compression=self.options.get('compression', None), memory_map=self.options.get('memory_map', False), is_text=is_text, errors=self.options.get('encoding_errors', 'strict'), storage_options=self.options.get('storage_options', None))
            assert self.handles is not None
            f = self.handles.handle
        elif engine != 'python':
            msg = f'Invalid file path or buffer object type: {type(f)}'
            raise ValueError(msg)
        try:
            return mapping[engine](f, **self.options)
        except Exception:
            if self.handles is not None:
                self.handles.close()
            raise

    def _failover_to_python(self):
        raise AbstractMethodError(self)

    def read(self, nrows=None):
        if self.engine == 'pyarrow':
            try:
                df = self._engine.read()
            except Exception:
                self.close()
                raise
        else:
            nrows = validate_integer('nrows', nrows)
            try:
                (index, columns, col_dict) = self._engine.read(nrows)
            except Exception:
                self.close()
                raise
            if index is None:
                if col_dict:
                    new_rows = len(next(iter(col_dict.values())))
                    index = RangeIndex(self._currow, self._currow + new_rows)
                else:
                    new_rows = 0
            else:
                new_rows = len(index)
            df = DataFrame(col_dict, columns=columns, index=index)
            self._currow += new_rows
        if self.squeeze and len(df.columns) == 1:
            return df.squeeze('columns').copy()
        return df

    def get_chunk(self, size=None):
        if size is None:
            size = self.chunksize
        if self.nrows is not None:
            if self._currow >= self.nrows:
                raise StopIteration
            size = min(size, self.nrows - self._currow)
        return self.read(nrows=size)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

def TextParser(*args, **kwds):
    """
    Converts lists of lists/tuples into DataFrames with proper type inference
    and optional (e.g. string to datetime) conversion. Also enables iterating
    lazily over chunks of large files

    Parameters
    ----------
    data : file-like object or list
    delimiter : separator character to use
    dialect : str or csv.Dialect instance, optional
        Ignored if delimiter is longer than 1 character
    names : sequence, default
    header : int, default 0
        Row to use to parse column labels. Defaults to the first row. Prior
        rows will be discarded
    index_col : int or list, optional
        Column or columns to use as the (possibly hierarchical) index
    has_index_names: bool, default False
        True if the cols defined in index_col have an index name and are
        not in the header.
    na_values : scalar, str, list-like, or dict, optional
        Additional strings to recognize as NA/NaN.
    keep_default_na : bool, default True
    thousands : str, optional
        Thousands separator
    comment : str, optional
        Comment out remainder of line
    parse_dates : bool, default False
    keep_date_col : bool, default False
    date_parser : function, optional
    skiprows : list of integers
        Row numbers to skip
    skipfooter : int
        Number of line at bottom of file to skip
    converters : dict, optional
        Dict of functions for converting values in certain columns. Keys can
        either be integers or column labels, values are functions that take one
        input argument, the cell (not column) content, and return the
        transformed content.
    encoding : str, optional
        Encoding to use for UTF when reading/writing (ex. 'utf-8')
    squeeze : bool, default False
        returns Series if only one column.
    infer_datetime_format: bool, default False
        If True and `parse_dates` is True for a column, try to infer the
        datetime format based on the first datetime string. If the format
        can be inferred, there often will be a large parsing speed-up.
    float_precision : str, optional
        Specifies which converter the C engine should use for floating-point
        values. The options are `None` or `high` for the ordinary converter,
        `legacy` for the original lower precision pandas converter, and
        `round_trip` for the round-trip converter.

        .. versionchanged:: 1.2
    """
    kwds['engine'] = 'python'
    return TextFileReader(*args, **kwds)

def _clean_na_values(na_values, keep_default_na=True):
    na_fvalues: set | dict
    if na_values is None:
        if keep_default_na:
            na_values = STR_NA_VALUES
        else:
            na_values = set()
        na_fvalues = set()
    elif isinstance(na_values, dict):
        old_na_values = na_values.copy()
        na_values = {}
        for (k, v) in old_na_values.items():
            if not is_list_like(v):
                v = [v]
            if keep_default_na:
                v = set(v) | STR_NA_VALUES
            na_values[k] = v
        na_fvalues = {k: _floatify_na_values(v) for (k, v) in na_values.items()}
    else:
        if not is_list_like(na_values):
            na_values = [na_values]
        na_values = _stringify_na_values(na_values)
        if keep_default_na:
            na_values = na_values | STR_NA_VALUES
        na_fvalues = _floatify_na_values(na_values)
    return (na_values, na_fvalues)

def _floatify_na_values(na_values):
    result = set()
    for v in na_values:
        try:
            v = float(v)
            if not np.isnan(v):
                result.add(v)
        except (TypeError, ValueError, OverflowError):
            pass
    return result

def _stringify_na_values(na_values):
    """return a stringified and numeric for these values"""
    result: list[int | str | float] = []
    for x in na_values:
        result.append(str(x))
        result.append(x)
        try:
            v = float(x)
            if v == int(v):
                v = int(v)
                result.append(f'{v}.0')
                result.append(str(v))
            result.append(v)
        except (TypeError, ValueError, OverflowError):
            pass
        try:
            result.append(int(x))
        except (TypeError, ValueError, OverflowError):
            pass
    return set(result)

def _refine_defaults_read(dialect: str | csv.Dialect, delimiter: str | object, delim_whitespace: bool, engine: CSVEngine | None, sep: str | object, error_bad_lines: bool | None, warn_bad_lines: bool | None, on_bad_lines: str | Callable | None, names: ArrayLike | None | object, prefix: str | None | object, defaults: dict[str, Any]):
    """Validate/refine default values of input parameters of read_csv, read_table.

    Parameters
    ----------
    dialect : str or csv.Dialect
        If provided, this parameter will override values (default or not) for the
        following parameters: `delimiter`, `doublequote`, `escapechar`,
        `skipinitialspace`, `quotechar`, and `quoting`. If it is necessary to
        override values, a ParserWarning will be issued. See csv.Dialect
        documentation for more details.
    delimiter : str or object
        Alias for sep.
    delim_whitespace : bool
        Specifies whether or not whitespace (e.g. ``' '`` or ``'	'``) will be
        used as the sep. Equivalent to setting ``sep='\\s+'``. If this option
        is set to True, nothing should be passed in for the ``delimiter``
        parameter.
    engine : {{'c', 'python'}}
        Parser engine to use. The C engine is faster while the python engine is
        currently more feature-complete.
    sep : str or object
        A delimiter provided by the user (str) or a sentinel value, i.e.
        pandas._libs.lib.no_default.
    error_bad_lines : str or None
        Whether to error on a bad line or not.
    warn_bad_lines : str or None
        Whether to warn on a bad line or not.
    on_bad_lines : str, callable or None
        An option for handling bad lines or a sentinel value(None).
    names : array-like, optional
        List of column names to use. If the file contains a header row,
        then you should explicitly pass ``header=0`` to override the column names.
        Duplicates in this list are not allowed.
    prefix : str, optional
        Prefix to add to column numbers when no header, e.g. 'X' for X0, X1, ...
    defaults: dict
        Default values of input parameters.

    Returns
    -------
    kwds : dict
        Input parameters with correct values.

    Raises
    ------
    ValueError :
        If a delimiter was specified with ``sep`` (or ``delimiter``) and
        ``delim_whitespace=True``.
        If on_bad_lines is specified(not ``None``) and ``error_bad_lines``/
        ``warn_bad_lines`` is True.
    """
    delim_default = defaults['delimiter']
    kwds: dict[str, Any] = {}
    if dialect is not None:
        kwds['sep_override'] = delimiter is None and (sep is lib.no_default or sep == delim_default)
    if delimiter and sep is not lib.no_default:
        raise ValueError('Specified a sep and a delimiter; you can only specify one.')
    if names is not None and names is not lib.no_default and (prefix is not None) and (prefix is not lib.no_default):
        raise ValueError('Specified named and prefix; you can only specify one.')
    kwds['names'] = None if names is lib.no_default else names
    kwds['prefix'] = None if prefix is lib.no_default else prefix
    if delimiter is None:
        delimiter = sep
    if delim_whitespace and delimiter is not lib.no_default:
        raise ValueError('Specified a delimiter with both sep and delim_whitespace=True; you can only specify one.')
    if delimiter == '\n':
        raise ValueError('Specified \\n as separator or delimiter. This forces the python engine which does not accept a line terminator. Hence it is not allowed to use the line terminator as separator.')
    if delimiter is lib.no_default:
        kwds['delimiter'] = delim_default
    else:
        kwds['delimiter'] = delimiter
    if engine is not None:
        kwds['engine_specified'] = True
    else:
        kwds['engine'] = 'c'
        kwds['engine_specified'] = False
    if on_bad_lines is not None:
        if error_bad_lines is not None or warn_bad_lines is not None:
            raise ValueError('Both on_bad_lines and error_bad_lines/warn_bad_lines are set. Please only set on_bad_lines.')
        if on_bad_lines == 'error':
            kwds['on_bad_lines'] = ParserBase.BadLineHandleMethod.ERROR
        elif on_bad_lines == 'warn':
            kwds['on_bad_lines'] = ParserBase.BadLineHandleMethod.WARN
        elif on_bad_lines == 'skip':
            kwds['on_bad_lines'] = ParserBase.BadLineHandleMethod.SKIP
        elif callable(on_bad_lines):
            if engine != 'python':
                raise ValueError("on_bad_line can only be a callable function if engine='python'")
            kwds['on_bad_lines'] = on_bad_lines
        else:
            raise ValueError(f'Argument {on_bad_lines} is invalid for on_bad_lines')
    elif error_bad_lines is not None:
        validate_bool_kwarg(error_bad_lines, 'error_bad_lines')
        if error_bad_lines:
            kwds['on_bad_lines'] = ParserBase.BadLineHandleMethod.ERROR
        elif warn_bad_lines is not None:
            validate_bool_kwarg(warn_bad_lines, 'warn_bad_lines')
            if warn_bad_lines:
                kwds['on_bad_lines'] = ParserBase.BadLineHandleMethod.WARN
            else:
                kwds['on_bad_lines'] = ParserBase.BadLineHandleMethod.SKIP
        else:
            kwds['on_bad_lines'] = ParserBase.BadLineHandleMethod.WARN
    else:
        kwds['on_bad_lines'] = ParserBase.BadLineHandleMethod.ERROR
    return kwds

def _extract_dialect(kwds: dict[str, Any]) -> csv.Dialect | None:
    """
    Extract concrete csv dialect instance.

    Returns
    -------
    csv.Dialect or None
    """
    if kwds.get('dialect') is None:
        return None
    dialect = kwds['dialect']
    if dialect in csv.list_dialects():
        dialect = csv.get_dialect(dialect)
    _validate_dialect(dialect)
    return dialect
MANDATORY_DIALECT_ATTRS = ('delimiter', 'doublequote', 'escapechar', 'skipinitialspace', 'quotechar', 'quoting')

def _validate_dialect(dialect: csv.Dialect) -> None:
    """
    Validate csv dialect instance.

    Raises
    ------
    ValueError
        If incorrect dialect is provided.
    """
    for param in MANDATORY_DIALECT_ATTRS:
        if not hasattr(dialect, param):
            raise ValueError(f'Invalid dialect {dialect} provided')

def _merge_with_dialect_properties(dialect: csv.Dialect, defaults: dict[str, Any]) -> dict[str, Any]:
    """
    Merge default kwargs in TextFileReader with dialect parameters.

    Parameters
    ----------
    dialect : csv.Dialect
        Concrete csv dialect. See csv.Dialect documentation for more details.
    defaults : dict
        Keyword arguments passed to TextFileReader.

    Returns
    -------
    kwds : dict
        Updated keyword arguments, merged with dialect parameters.
    """
    kwds = defaults.copy()
    for param in MANDATORY_DIALECT_ATTRS:
        dialect_val = getattr(dialect, param)
        parser_default = parser_defaults[param]
        provided = kwds.get(param, parser_default)
        conflict_msgs = []
        if provided != parser_default and provided != dialect_val:
            msg = f"Conflicting values for '{param}': '{provided}' was provided, but the dialect specifies '{dialect_val}'. Using the dialect-specified value."
            if not (param == 'delimiter' and kwds.pop('sep_override', False)):
                conflict_msgs.append(msg)
        if conflict_msgs:
            warnings.warn('\n\n'.join(conflict_msgs), ParserWarning, stacklevel=find_stack_level())
        kwds[param] = dialect_val
    return kwds

def _validate_skipfooter(kwds: dict[str, Any]) -> None:
    """
    Check whether skipfooter is compatible with other kwargs in TextFileReader.

    Parameters
    ----------
    kwds : dict
        Keyword arguments passed to TextFileReader.

    Raises
    ------
    ValueError
        If skipfooter is not compatible with other parameters.
    """
    if kwds.get('skipfooter'):
        if kwds.get('iterator') or kwds.get('chunksize'):
            raise ValueError("'skipfooter' not supported for iteration")
        if kwds.get('nrows'):
            raise ValueError("'skipfooter' not supported with 'nrows'")