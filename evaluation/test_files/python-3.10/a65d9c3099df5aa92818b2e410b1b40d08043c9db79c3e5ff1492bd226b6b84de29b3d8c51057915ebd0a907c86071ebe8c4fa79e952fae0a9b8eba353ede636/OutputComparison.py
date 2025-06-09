""" Tools to compare outputs of compiled and not compiled programs.

There is a couple of replacements to be done for compiled programs to
make the diff meaningful. The compiled type representations are just
an example.

"""
import difflib
import os
import re
from nuitka.Tracing import my_print
ran_tests_re = re.compile('^(Ran \\d+ tests? in )\\-?\\d+\\.\\d+s$')
instance_re = re.compile('at (?:0x)?[0-9a-fA-F]+(;?\\s|\\>)')
thread_re = re.compile('[Tt]hread 0x[0-9a-fA-F]+')
compiled_types_re = re.compile('compiled_(module|function|generator|method|frame|coroutine|async_generator|cell)')
module_repr_re = re.compile("(\\<module '.*?' from ').*?('\\>)")
global_name_error_re = re.compile("global (name ')(.*?)(' is not defined)")
non_ascii_error_rt = re.compile('(SyntaxError: Non-ASCII character.*? on line) \\d+')
python_win_lib_re = re.compile('[a-zA-Z]:\\\\\\\\?[Pp]ython(.*?\\\\\\\\?)[Ll]ib')
local_port_re = re.compile('(127\\.0\\.0\\.1):\\d{2,5}')
traceback_re = re.compile('(F|f)ile "(.*?)", line (\\d+)')

def traceback_re_callback(match):
    return '%sile "%s", line %s' % (match.group(1), os.path.realpath(os.path.abspath(match.group(2))), match.group(3))
importerror_re = re.compile('(ImportError(?:\\("|: )cannot import name \'\\w+\' from \'.*?\' )\\((.*?)\\)')

def import_re_callback(match):
    return '%s( >> %s)' % (match.group(1), os.path.realpath(os.path.abspath(match.group(2))))
tempfile_re = re.compile('/tmp/tmp[a-z0-9_]*')
logging_info_re = re.compile('^Nuitka.*?:INFO')
logging_warning_re = re.compile('^Nuitka.*?:WARNING')
syntax_error_caret_re = re.compile('^\\s*~*\\^*~*$')
timing_re = re.compile('in [0-9]+.[0-9][0-9](s| seconds)')

def makeDiffable(output, ignore_warnings, syntax_errors):
    result = []
    m = re.match(b'\\x1b\\[[^h]+h', output)
    if m:
        output = output[len(m.group()):]
    lines = output.split(b'\n')
    if syntax_errors:
        for line in lines:
            if line.startswith(b'SyntaxError:'):
                lines = [line]
                break
    for line in lines:
        if type(line) is not str:
            try:
                line = line.decode('utf-8' if os.name != 'nt' else 'cp850')
            except UnicodeDecodeError:
                line = repr(line)
        if line.endswith('\r'):
            line = line[:-1]
        if line.startswith('REFCOUNTS'):
            first_value = line[line.find('[') + 1:line.find(',')]
            last_value = line[line.rfind(' ') + 1:line.rfind(']')]
            line = line.replace(first_value, 'xxxxx').replace(last_value, 'xxxxx')
        if line.startswith('[') and line.endswith('refs]'):
            continue
        if ignore_warnings and logging_warning_re.match(line):
            continue
        if logging_info_re.match(line):
            continue
        if line.startswith('Nuitka-Inclusion:WARNING: Cannot follow import to module'):
            continue
        if line.startswith('Nuitka:WARNING: Cannot detect Linux distribution'):
            continue
        if line.startswith('Nuitka-Options:WARNING: You did not specify to follow or include'):
            continue
        if line.startswith('Nuitka:WARNING: Using very slow fallback for ordered sets'):
            continue
        if line.startswith('Nuitka:WARNING: On Windows, support for input/output'):
            continue
        if line.startswith('Nuitka:WARNING:     Complex topic'):
            continue
        if syntax_error_caret_re.match(line):
            continue
        line = instance_re.sub('at 0xxxxxxxxx\\1', line)
        line = thread_re.sub('Thread 0xXXXXXXXX', line)
        line = compiled_types_re.sub('\\1', line)
        line = global_name_error_re.sub('\\1\\2\\3', line)
        line = module_repr_re.sub('\\1xxxxx\\2', line)
        line = non_ascii_error_rt.sub('\\1 xxxx', line)
        line = timing_re.sub('in x.xx seconds', line)
        line = line.replace('ntpath', 'posixpath')
        line = line.replace('http://www.python.org/peps/pep-0263.html', 'http://python.org/dev/peps/pep-0263/')
        line = ran_tests_re.sub('\\1x.xxxs', line)
        line = traceback_re.sub(traceback_re_callback, line)
        line = importerror_re.sub(import_re_callback, line)
        line = tempfile_re.sub('/tmp/tmpxxxxxxx', line)
        if line == "Exception RuntimeError: 'maximum recursion depth exceeded while calling a Python object' in <type 'exceptions.AttributeError'> ignored":
            continue
        if re.match('Exception ignored in:.*__del__', line):
            continue
        line = python_win_lib_re.sub('C:\\\\Python\\1Lib', line)
        line = local_port_re.sub('\\1:xxxxx', line)
        if line == '/usr/bin/ld: warning: .init_array section has zero size':
            continue
        if re.match('.*ld: skipping incompatible .* when searching for .*', line):
            continue
        if '() possibly used unsafely' in line or '() is almost always misused' in line:
            continue
        if 'skipping incompatible /usr/lib/libpython2.6.so' in line:
            continue
        if "is dangerous, better use `mkstemp'" in line or "In function `posix_tempnam'" in line or "In function `posix_tmpnam'" in line:
            continue
        if 'clcache: persistent json file' in line or 'clcache: manifest file' in line:
            continue
        line = line.replace('super() argument 1 must be a type, not NoneType', 'super() argument 1 must be type, not None')
        line = line.replace('super() argument 1 must be a type', 'super() argument 1 must be type')
        result.append(line)
    return result

def compareOutput(kind, out_cpython, out_nuitka, ignore_warnings, syntax_errors, trace_result=True):
    from_date = ''
    to_date = ''
    diff = difflib.unified_diff(makeDiffable(out_cpython, ignore_warnings, syntax_errors), makeDiffable(out_nuitka, ignore_warnings, syntax_errors), '{program} ({detail})'.format(program=os.environ['PYTHON'], detail=kind), '{program} ({detail})'.format(program='nuitka', detail=kind), from_date, to_date, n=3)
    result = list(diff)
    if result:
        if trace_result:
            for line in result:
                my_print(line, end='\n' if not line.startswith('---') else '')
        return 1
    else:
        return 0