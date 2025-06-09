"""Utilities for logging in the command line interface context."""
import logging
import click
from .echo import COLORS

class CliHandler(logging.Handler):
    """Handler for writing to the console using click."""

    def emit(self, record):
        """Emit log record via click.

        Can make use of special attributes 'nl' (whether to add newline) and 'err' (whether to print to stderr), which
        can be set via the 'extra' dictionary parameter of the logging methods.
        """
        try:
            nl = record.nl
        except AttributeError:
            nl = True
        try:
            err = record.err
        except AttributeError:
            err = False
        try:
            prefix = record.prefix
        except AttributeError:
            prefix = True
        record.prefix = prefix
        try:
            msg = self.format(record)
            click.echo(msg, err=err, nl=nl)
        except Exception:
            self.handleError(record)

class CliFormatter(logging.Formatter):
    """Formatter that automatically prefixes log messages with a colored version of the log level."""

    @staticmethod
    def format(record):
        """Format the record using the style required for the command line interface."""
        try:
            fg = COLORS[record.levelname.lower()]
        except KeyError:
            fg = 'white'
        try:
            prefix = record.prefix
        except AttributeError:
            prefix = None
        if prefix:
            return f'{click.style(record.levelname.capitalize(), fg=fg, bold=True)}: {record.msg % record.args}'
        if record.args:
            return f'{record.msg % record.args}'
        return record.msg