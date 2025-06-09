"""sys.excepthook for IPython itself, leaves a detailed report on disk.

Authors:

* Fernando Perez
* Brian E. Granger
"""
import sys
import traceback
from pprint import pformat
from pathlib import Path
from IPython.core import ultratb
from IPython.core.release import author_email
from IPython.utils.sysinfo import sys_info
from IPython.utils.py3compat import input
from IPython.core.release import __version__ as version
from typing import Optional
_default_message_template = "Oops, {app_name} crashed. We do our best to make it stable, but...\n\nA crash report was automatically generated with the following information:\n  - A verbatim copy of the crash traceback.\n  - A copy of your input history during this session.\n  - Data on your current {app_name} configuration.\n\nIt was left in the file named:\n\t'{crash_report_fname}'\nIf you can email this file to the developers, the information in it will help\nthem in understanding and correcting the problem.\n\nYou can mail it to: {contact_name} at {contact_email}\nwith the subject '{app_name} Crash Report'.\n\nIf you want to do it now, the following command will work (under Unix):\nmail -s '{app_name} Crash Report' {contact_email} < {crash_report_fname}\n\nIn your email, please also include information about:\n- The operating system under which the crash happened: Linux, macOS, Windows,\n  other, and which exact version (for example: Ubuntu 16.04.3, macOS 10.13.2,\n  Windows 10 Pro), and whether it is 32-bit or 64-bit;\n- How {app_name} was installed: using pip or conda, from GitHub, as part of\n  a Docker container, or other, providing more detail if possible;\n- How to reproduce the crash: what exact sequence of instructions can one\n  input to get the same crash? Ideally, find a minimal yet complete sequence\n  of instructions that yields the crash.\n\nTo ensure accurate tracking of this issue, please file a report about it at:\n{bug_tracker}\n"
_lite_message_template = '\nIf you suspect this is an IPython {version} bug, please report it at:\n    https://github.com/ipython/ipython/issues\nor send an email to the mailing list at {email}\n\nYou can print a more detailed traceback right now with "%tb", or use "%debug"\nto interactively debug it.\n\nExtra-detailed tracebacks for bug-reporting purposes can be enabled via:\n    {config}Application.verbose_crash=True\n'

class CrashHandler(object):
    """Customizable crash handlers for IPython applications.

    Instances of this class provide a :meth:`__call__` method which can be
    used as a ``sys.excepthook``.  The :meth:`__call__` signature is::

        def __call__(self, etype, evalue, etb)
    """
    message_template = _default_message_template
    section_sep = '\n\n' + '*' * 75 + '\n\n'

    def __init__(self, app, contact_name: Optional[str]=None, contact_email: Optional[str]=None, bug_tracker: Optional[str]=None, show_crash_traceback: bool=True, call_pdb: bool=False):
        """Create a new crash handler

        Parameters
        ----------
        app : Application
            A running :class:`Application` instance, which will be queried at
            crash time for internal information.
        contact_name : str
            A string with the name of the person to contact.
        contact_email : str
            A string with the email address of the contact.
        bug_tracker : str
            A string with the URL for your project's bug tracker.
        show_crash_traceback : bool
            If false, don't print the crash traceback on stderr, only generate
            the on-disk report
        call_pdb
            Whether to call pdb on crash

        Attributes
        ----------
        These instances contain some non-argument attributes which allow for
        further customization of the crash handler's behavior. Please see the
        source for further details.

        """
        self.crash_report_fname = 'Crash_report_%s.txt' % app.name
        self.app = app
        self.call_pdb = call_pdb
        self.show_crash_traceback = show_crash_traceback
        self.info = dict(app_name=app.name, contact_name=contact_name, contact_email=contact_email, bug_tracker=bug_tracker, crash_report_fname=self.crash_report_fname)

    def __call__(self, etype, evalue, etb):
        """Handle an exception, call for compatible with sys.excepthook"""
        sys.excepthook = sys.__excepthook__
        color_scheme = 'NoColor'
        try:
            rptdir = self.app.ipython_dir
        except:
            rptdir = Path.cwd()
        if rptdir is None or not Path.is_dir(rptdir):
            rptdir = Path.cwd()
        report_name = rptdir / self.crash_report_fname
        self.crash_report_fname = report_name
        self.info['crash_report_fname'] = report_name
        TBhandler = ultratb.VerboseTB(color_scheme=color_scheme, long_header=1, call_pdb=self.call_pdb)
        if self.call_pdb:
            TBhandler(etype, evalue, etb)
            return
        else:
            traceback = TBhandler.text(etype, evalue, etb, context=31)
        if self.show_crash_traceback:
            print(traceback, file=sys.stderr)
        try:
            report = open(report_name, 'w', encoding='utf-8')
        except:
            print('Could not create crash report on disk.', file=sys.stderr)
            return
        with report:
            print('\n' + '*' * 70 + '\n', file=sys.stderr)
            print(self.message_template.format(**self.info), file=sys.stderr)
            report.write(self.make_report(traceback))
        input('Hit <Enter> to quit (your terminal may close):')

    def make_report(self, traceback):
        """Return a string containing a crash report."""
        sec_sep = self.section_sep
        report = ['*' * 75 + '\n\n' + 'IPython post-mortem report\n\n']
        rpt_add = report.append
        rpt_add(sys_info())
        try:
            config = pformat(self.app.config)
            rpt_add(sec_sep)
            rpt_add('Application name: %s\n\n' % self.app_name)
            rpt_add('Current user configuration structure:\n\n')
            rpt_add(config)
        except:
            pass
        rpt_add(sec_sep + 'Crash traceback:\n\n' + traceback)
        return ''.join(report)

def crash_handler_lite(etype, evalue, tb):
    """a light excepthook, adding a small message to the usual traceback"""
    traceback.print_exception(etype, evalue, tb)
    from IPython.core.interactiveshell import InteractiveShell
    if InteractiveShell.initialized():
        config = '%config '
    else:
        config = 'c.'
    print(_lite_message_template.format(email=author_email, config=config, version=version), file=sys.stderr)