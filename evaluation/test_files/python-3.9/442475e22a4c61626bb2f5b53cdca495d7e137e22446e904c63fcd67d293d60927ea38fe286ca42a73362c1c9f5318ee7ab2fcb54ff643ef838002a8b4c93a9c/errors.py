"""Error class definitions."""
from lark.exceptions import UnexpectedToken, UnexpectedCharacters
from collections import OrderedDict
import re
import sys
TEMPLATE = '{error_class}\tkeyword:{keyword}\tentry:{entry}\tline:{line_number}\tcolumn:{column}\turl:{url}\thint:{hint}'

class _Error:
    """Base class for all errors."""

    def __init__(self):
        self.class_name = self.__class__.__name__
        self.value_dict = OrderedDict([('error_class', self.class_name), ('url', None), ('keyword', None), ('entry', None), ('line_number', None), ('column', None), ('hint', None)])

    def to_dict(self):
        """Format the properties of error into a dictionary."""
        raise NotImplementedError('to_dict have to be implemented in {}'.format(self.__class__.__name__))

    def to_string(self) -> str:
        """Format the output to a string."""
        self.value_dict.update(self.to_dict())
        return TEMPLATE.format(**self.value_dict)

    def __str__(self):
        return self.to_string()

class NotInNamespacePattern(_Error):
    """Error in entry link to a namespace defined as pattern in the header but does not fit the pattern."""

    def __init__(self, keyword: str, entry: str, line_number: int, column: int):
        """Initialize error class.

        :param keyword: Error class type.
        :param entry: String representation where error occurred.
        :param line_number: Line number where error was found.
        :param column: Column number where error was found.
        """
        super(NotInNamespacePattern, self).__init__()
        self.ns_keyword = keyword
        self.entry = entry
        self.line_number = line_number
        self.column = column

    def to_dict(self) -> dict:
        """Format the properties of error into a dictionary."""
        return {'error_class': self.class_name, 'keyword': self.ns_keyword, 'entry': re.sub('[\n\r]', '', self.entry), 'line_number': self.line_number, 'column': self.column}

class NotInAnnotationPattern(_Error):
    """Error in entry links to a namespace defined as patter in the header but not fits the pattern."""

    def __init__(self, keyword: str, entry: str, line_number: int, column: int):
        """Initialize error class.

        :param keyword: Error class type.
        :param entry: String representation where error occurred.
        :param line_number: Line number where error was found.
        :param column: Column number where error was found.
        """
        super(NotInAnnotationPattern, self).__init__()
        self.ns_keyword = keyword
        self.entry = entry
        self.line_number = line_number
        self.column = column

    def to_dict(self) -> dict:
        """Format the properties of error into a dictionary."""
        return {'error_class': self.class_name, 'keyword': self.ns_keyword, 'entry': re.sub('[\n\r]', '', self.entry), 'line_number': self.line_number, 'column': self.column}

class WithoutDefinedAnnotation(_Error):
    """Error in entry without a defined annotation."""

    def __init__(self, entry: str, keyword: str, line_number: int, column: int):
        """Initialize error class.

        :param keyword: Error class type.
        :param entry: String representation where error occurred.
        :param line_number: Line number where error was found.
        :param column: Column number where error was found.
        """
        super(WithoutDefinedAnnotation, self).__init__()
        self.entry = entry
        self.keyword = keyword
        self.line_number = line_number
        self.column = column

    def to_dict(self) -> dict:
        """Format the properties of error into a dictionary."""
        return {'error_class': self.class_name, 'keyword': self.keyword, 'entry': re.sub('[\n\r]', '', self.entry), 'line_number': self.line_number, 'column': self.column}

class WithoutDefinedNamespace(_Error):
    """Error in entry without a defined namespace."""

    def __init__(self, entry: str, keyword: str, line_number: int, column: int):
        """Initialize error class.

        :param keyword: Error class type.
        :param entry: String representation where error occurred.
        :param line_number: Line number where error was found.
        :param column: Column number where error was found.
        """
        super(WithoutDefinedNamespace, self).__init__()
        self.entry = entry
        self.keyword = keyword
        self.line_number = line_number
        self.column = column

    def to_dict(self) -> dict:
        """Format the properties of error into a dictionary."""
        return {'error_class': self.class_name, 'keyword': self.keyword, 'entry': re.sub('[\n\r]', '', self.entry), 'line_number': self.line_number, 'column': self.column}

class NotInNamespaceUrl(_Error):
    """Error in entry links to a namespace defined in the header but does not exist in namespace url."""

    def __init__(self, keyword: str, url_or_path: str, entry: str, line_number: int, column: int, hint: str):
        """Initialize error class.

        :param keyword: Error class type.
        :param url_or_path: URL or directory path to namespace or annotation file.
        :param hint: Sentence or string to give the user in the error report to help solve error.
        :param line_number: Line number where error was found.
        :param column: Column number where error was found.
        :param entry: String representation where error occurred.
        """
        super(NotInNamespaceUrl, self).__init__()
        self.ns_keyword = keyword
        self.url_or_path = url_or_path
        self.entry = entry
        self.line_number = line_number
        self.column = column
        self.hint = hint

    def to_dict(self) -> dict:
        """Format the properties of error into a dictionary."""
        return {'error_class': self.class_name, 'url': self.url_or_path, 'keyword': self.ns_keyword, 'entry': re.sub('[\n\r]', '', self.entry), 'line_number': self.line_number, 'column': self.column, 'hint': self.hint}

class NotInAnnotationUrl(_Error):
    """Error in entry links to an annotation defined in the header but not exists in namespace url."""

    def __init__(self, keyword: str, url_or_path: str, entry: str, line_number: int, column: int, hint: str):
        """Initialize error class.

        :param keyword: Error class type.
        :param url_or_path: URL or directory path to namespace or annotation file.
        :param hint: Sentence or string to give the user in the error report to help solve error.
        :param line_number: Line number where error was found.
        :param column: Column number where error was found.
        :param entry: String representation where error occurred.
        """
        super(NotInAnnotationUrl, self).__init__()
        self.ns_keyword = keyword
        self.url_or_path = url_or_path
        self.entry = entry
        self.line_number = line_number
        self.column = column
        self.hint = hint

    def to_dict(self) -> dict:
        """Format the properties of error into a dictionary."""
        return {'error_class': self.class_name, 'url': self.url_or_path, 'keyword': self.ns_keyword, 'entry': re.sub('[\n\r]', '', self.entry), 'line_number': self.line_number, 'column': self.column, 'hint': self.hint}

class NotInNamespaceList(_Error):
    """Error in entry links to a namespace defined in the header but not exists in namespace list."""

    def __init__(self, keyword: str, entry: str, line_number: int, column: int):
        """Initialize error class.

        :param keyword: Error class type.
        :param entry: String representation where error occurred.
        :param line_number: Line number where error was found.
        :param column: Column number where error was found.
        """
        super(NotInNamespaceList, self).__init__()
        self.ns_keyword = keyword
        self.entry = entry
        self.line_number = line_number
        self.column = column

    def to_dict(self) -> dict:
        """Format the properties of error into a dictionary."""
        return {'error_class': self.class_name, 'keyword': self.ns_keyword, 'entry': re.sub('[\n\r]', '', self.entry), 'line_number': self.line_number, 'column': self.column}

class NotInAnnotationList(_Error):
    """Entry links to an annotation defined in the header but does not exist in the annotation list."""

    def __init__(self, keyword: str, entry: str, line_number: int, column: int):
        """Initialize error class.

        :param keyword: Error class type.
        :param entry: String representation where error occurred.
        :param line_number: Line number where error was found.
        :param column: Column number where error was found.
        """
        super(NotInAnnotationList, self).__init__()
        self.ns_keyword = keyword
        self.entry = entry
        self.line_number = line_number
        self.column = column

    def to_dict(self) -> dict:
        """Format the properties of error into a dictionary."""
        return {'error_class': self.class_name, 'keyword': self.ns_keyword, 'entry': re.sub('[\n\r]', '', self.entry), 'line_number': self.line_number, 'column': self.column}

class BelSyntaxError(_Error):
    """Syntax error."""

    def __init__(self, exception, line_number: int, line: str):
        """Initialize error class.

        :param exception: Error class type.
        :param line_number: URL or directory path to namespace or annotation file.
        :param line: Line where error occurred.
        """
        super(BelSyntaxError, self).__init__()
        self.line_number = line_number
        self.line = line
        self.exception = exception

    def to_dict(self) -> dict:
        """Format the properties of error into a dictionary."""
        hint = ('%s >>>>>> %s' % (self.line[:self.exception.column - 1], self.line[self.exception.column - 1:])).strip()
        value_dict = {'line_number': self.line_number, 'hint': re.sub('[\n\r]', '', hint)}
        if isinstance(self.exception, UnexpectedCharacters):
            offset = self.exception.column
            value_dict.update({'error_class': self.__class__.__name__ + '_unexpected_input', 'entry': self.line[offset:offset + 5], 'column': self.exception.column})
        elif isinstance(self.exception, UnexpectedToken):
            value_dict.update({'error_class': self.__class__.__name__ + '_unexpected_token', 'entry': re.sub('[\n\r]', '', self.exception.token), 'column': self.exception.column})
        else:
            print('Not covered by library: lark.expections type {}'.format(type(self.exception)), sys.exc_info()[0])
            raise
        return value_dict

class NotDownloadedFromUrl(_Error):
    """Error in entry links to an annotation defined in the header but not exists in namespace url."""

    def __init__(self, keyword: str, url_or_path: str, hint: str, line: int=None, column: int=None):
        """Initialize error class.

        :param keyword: Error class type.
        :param url_or_path: URL or directory path to namespace or annotation file.
        :param hint: Sentence or string to give the user in the error report to help solve error.
        :param line: Line number where error was found.
        :param column: Column number where error was found.
        """
        super(NotDownloadedFromUrl, self).__init__()
        self.ns_keyword = keyword
        self.url_or_path = url_or_path
        self.hint = hint
        self.line = line
        self.column = column

    def to_dict(self) -> dict:
        """Format the properties of error into a dictionary."""
        return {'error_class': self.class_name, 'url': self.url_or_path, 'keyword': self.ns_keyword, 'column': self.column, 'line_number': self.line, 'hint': self.hint}