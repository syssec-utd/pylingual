import os
import logging
from typing import List, Sequence
LOG_FORMAT = '%(asctime)s Model-Deployment-Controller {} %(levelname)s %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
BLANK_FORMAT = logging.Formatter(fmt='')
_loggers = dict()

class CustomLogRecord(logging.LogRecord):
    """Custom log record.

    We use a custom log record in order to create custom and compound log
    elements that can be used by the Formatter just like standard properties.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.origin = f'{self.module}:{self.lineno}'
        self.levelname = f'[{self.levelname}]'

def _suppress_handlers(log: logging.Logger) -> List[List[logging.Formatter]]:

    def _suppress_handlers_for_logger(log: logging.Logger) -> List[logging.Formatter]:
        formatters = []
        for h in log.handlers:
            formatters.append(h.formatter)
            h.setFormatter(BLANK_FORMAT)
        return formatters
    formatters = [_suppress_handlers_for_logger(log)]
    while log.propagate and log.parent:
        log = log.parent
        formatters.append(_suppress_handlers_for_logger(log))
    return formatters

def _restore_handlers(log: logging.Logger, formatters: Sequence[logging.Formatter]) -> None:
    for i in range(len(formatters)):
        for handler, fmt in zip(log.handlers, formatters[i]):
            handler.setFormatter(fmt)
        log = log.parent

class ControllerLogger(logging.Logger):

    def newline(self, lines: int=1):
        original_formatters = _suppress_handlers(self)
        for _ in range(lines):
            self.info('')
        _restore_handlers(self, original_formatters)
logging.setLogRecordFactory(CustomLogRecord)
logging.setLoggerClass(ControllerLogger)

def _configure_handler(handler, level, formatter):
    handler.setLevel(level)
    handler.setFormatter(formatter)

def get_or_create_logger(module, name=None, level=logging.INFO, fmt=None, file_level=logging.DEBUG, file_fmt=None, log_path=None):
    """Get or create and return module's logger.

    Args:
        module: the module for which we request a logger
        name: the name/title of the logger if default format is used
        level: logging level for StreamHandlers
        fmt: override default format
        file_level: logging level for FileHandlers
        file_fmt: override default file format
        log_path: logfile path (if None, then no FileHandler is created)
    """
    global _loggers
    log = _loggers.get(module)
    if log:
        for h in log.handlers:
            if isinstance(h, logging.FileHandler):
                h.setLevel(file_level)
            elif isinstance(h, logging.StreamHandler):
                h.setLevel(level)
        return log
    log = logging.getLogger(module)
    log.propagate = False
    log.setLevel(logging.DEBUG)
    log_fmt = fmt or LOG_FORMAT.format('%s' % name if name else '%(origin)s')
    stream_handler = logging.StreamHandler()
    _configure_handler(stream_handler, level, logging.Formatter(log_fmt, DATE_FORMAT))
    log.addHandler(stream_handler)
    if log_path:
        if os.path.dirname(log_path):
            os.makedirs(os.path.dirname(log_path), exist_ok=True)
        file_handler = logging.FileHandler(filename=os.path.abspath(log_path), mode='a')
        _configure_handler(file_handler, file_level, logging.Formatter(file_fmt or log_fmt, DATE_FORMAT))
        log.addHandler(file_handler)
    _loggers[module] = log
    return log