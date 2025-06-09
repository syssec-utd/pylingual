import signal
from contextlib import contextmanager
import psutil

def _session_terminator(signum, frame):
    print(f'Encountered Signal {signum}!')
    print('Terminating SSM session')
    for to_be_terminated in psutil.process_iter():
        if to_be_terminated.name() == 'session-manager-plugin':
            to_be_terminated.terminate()
            print('>>> Terminated')

@contextmanager
def interrupt_handler():
    signal.signal(signal.SIGINT, _session_terminator)
    signal.signal(signal.SIGABRT, _session_terminator)
    signal.signal(signal.SIGTERM, _session_terminator)
    yield