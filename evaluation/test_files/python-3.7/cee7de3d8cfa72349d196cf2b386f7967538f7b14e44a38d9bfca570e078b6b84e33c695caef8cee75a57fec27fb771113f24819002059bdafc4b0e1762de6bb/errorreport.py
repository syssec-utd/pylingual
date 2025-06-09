"""
errorhandler.py: ErrorHandler class
"""
from typing import Union, cast

class ErrorReport:
    """
    Error handling
    """

    def __init__(self, cont: bool=False) -> None:
        self._errordata: list[Exception | 'ErrorReport'] = []
        self._exit: bool = not cont

    def submit(self, err: Union[Exception, 'ErrorReport', None]=None) -> bool:
        if err is not None and err is not self:
            self._errordata.append(err)
        return self._exit

    def new_subreport(self) -> 'ErrorReport':
        return self.__class__(not self._exit)

    def haserror(self) -> bool:
        return len(self._errordata) > 0

    def get_errors(self) -> list[Exception]:
        errors: list[Exception] = []
        for err in self._errordata:
            if type(err) is ErrorReport:
                errors += err.get_errors()
            else:
                err = cast(Exception, err)
                errors.append(err)
        return errors

    def dump(self) -> str:
        dumpstrings: list[str] = []
        errstr: str
        errors: list[Exception] = self.get_errors()
        for err in errors:
            if isinstance(err, SyntaxError):
                errstr = f'{err.filename}:{err.lineno}:{err.offset} '
                if err.end_offset is not None:
                    errstr += f'- {err.end_lineno}:{err.end_offset} '
                errstr += f'{type(err).__name__}: {str(err)}\n'
                errstr += f'> {err.text}'
                if err.offset is not None:
                    errstr += '\n>' + ' ' * err.offset + '^'
            else:
                errstr = str(err)
            dumpstrings.append(errstr)
        return '\n'.join(dumpstrings)