"""
Process json logs. Default: Output to colorized ansi dev logs.

When lines cannot be json loaded we print them on stderr

"""
import sys, os, json, time
from devapp.tools import skip_flag_defines, exists, to_list, repl_dollar_var_with_env_val, project, read_file, write_file
skip_flag_defines.append('structlogging.sl')
from structlogging import sl
from devapp.app import FLG, app, run_app, do, system
from devapp import tools
from structlog import PrintLogger
levels = sl.log_levels

class Flags(sl.flags):
    autoshort = ''

    class file_name:
        n = 'file name of log file with json. "-": read from stdin'
        d = '-'

    class to_json:
        n = 'just print json loadable lines to stdout, rest to stderr. No ansi. Basically a filter, making jq work, when bogus lines are in.'
        d = False

def colorize(s, rend, p=PrintLogger(file=sys.stdout), levels=levels):
    try:
        s = json.loads(s)
        l = s['level']
        if levels[l] < app.log_level:
            return
        sys.stdout.write(rend(p, s['level'], s) + '\n')
    except:
        print(s, file=sys.stderr)

def run():
    fn = FLG.file_name
    if fn == '-':
        fd = sys.stdin
    else:
        if not exists(fn):
            app.die('not found', fn=fn)
        fd = open(fn)
    rend = sl.setup_logging(get_renderer=True)
    while True:
        s = fd.readline()
        if s:
            colorize(s, rend=rend)
            continue
        time.sleep(0.1)
main = lambda: run_app(run, flags=Flags)