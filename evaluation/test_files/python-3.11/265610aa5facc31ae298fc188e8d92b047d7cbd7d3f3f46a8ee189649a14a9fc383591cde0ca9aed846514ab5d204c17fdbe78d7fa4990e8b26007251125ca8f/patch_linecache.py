import linecache

class BPythonLinecache(dict):
    """Replaces the cache dict in the standard-library linecache module,
    to also remember (in an unerasable way) rp console input."""

    def __init__(self, *args, **kwargs):
        super(BPythonLinecache, self).__init__(*args, **kwargs)
        self.bpython_history = []

    def is_bpython_filename(self, fname):
        try:
            return fname.startswith('<rp-input-')
        except AttributeError:
            return False

    def get_bpython_history(self, key):
        """Given a filename provided by remember_bpython_input,
        returns the associated source string."""
        try:
            idx = int(key.split('-')[2][:-1])
            return self.bpython_history[idx]
        except (IndexError, ValueError):
            raise KeyError

    def remember_bpython_input(self, source):
        """Remembers a string of source code, and returns
        a fake filename to use to retrieve it later."""
        filename = '<rp-input-%s>' % len(self.bpython_history)
        self.bpython_history.append((len(source), None, source.splitlines(True), filename))
        return filename

    def __getitem__(self, key):
        if self.is_bpython_filename(key):
            return self.get_bpython_history(key)
        return super(BPythonLinecache, self).__getitem__(key)

    def __contains__(self, key):
        if self.is_bpython_filename(key):
            try:
                self.get_bpython_history(key)
                return True
            except KeyError:
                return False
        return super(BPythonLinecache, self).__contains__(key)

    def __delitem__(self, key):
        if not self.is_bpython_filename(key):
            return super(BPythonLinecache, self).__delitem__(key)

def _bpython_clear_linecache():
    try:
        bpython_history = linecache.cache.bpython_history
    except AttributeError:
        bpython_history = []
    linecache.cache = BPythonLinecache()
    linecache.cache.bpython_history = bpython_history
linecache.cache = BPythonLinecache(linecache.cache)
linecache.clearcache = _bpython_clear_linecache

def filename_for_console_input(code_string):
    """Remembers a string of source code, and returns
    a fake filename to use to retrieve it later."""
    try:
        return linecache.cache.remember_bpython_input(code_string)
    except AttributeError:
        return '<input>'
fc = filename_for_console_input
import code
interpereter = code.InteractiveInterpreter()

def run_code(code, mode, namespace, exv):
    import sys
    old_tracer = sys.gettrace()
    try:
        return exv(interpereter.compile(code, fc(code), mode), namespace, namespace)
    finally:
        sys.settrace(old_tracer)