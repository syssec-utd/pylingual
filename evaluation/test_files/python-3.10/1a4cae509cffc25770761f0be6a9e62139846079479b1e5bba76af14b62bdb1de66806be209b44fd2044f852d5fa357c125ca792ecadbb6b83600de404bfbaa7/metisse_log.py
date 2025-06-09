import logging
import os

class MetisseLogger(logging.Logger):

    def __init__(self, logger_name, log_level=logging.INFO, log_file=None):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(log_level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        if log_file:
            self.set_log_file(log_file, formatter)

    def set_log_file(self, log_file, formatter):
        if not os.path.exists(os.path.dirname(log_file)):
            os.makedirs(os.path.dirname(log_file))
        self.file_handler = logging.FileHandler(log_file)
        self.file_handler.setFormatter(formatter)
        self.logger.addHandler(self.file_handler)

    def close(self):
        if hasattr(self, 'file_handler'):
            self.file_handler.close()
            self.logger.removeHandler(self.file_handler)

    def debug(self, msg, *args, exc_info=None, stack_info=False, stacklevel=1, extra=None):
        self.logger.debug(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)

    def info(self, msg, *args, exc_info=None, stack_info=False, stacklevel=1, extra=None):
        self.logger.info(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)

    def warning(self, msg, *args, exc_info=None, stack_info=False, stacklevel=1, extra=None):
        self.logger.warning(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)

    def error(self, msg, *args, exc_info=None, stack_info=False, stacklevel=1, extra=None):
        self.logger.error(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)

    def critical(self, msg, *args, exc_info=None, stack_info=False, stacklevel=1, extra=None):
        self.logger.critical(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)