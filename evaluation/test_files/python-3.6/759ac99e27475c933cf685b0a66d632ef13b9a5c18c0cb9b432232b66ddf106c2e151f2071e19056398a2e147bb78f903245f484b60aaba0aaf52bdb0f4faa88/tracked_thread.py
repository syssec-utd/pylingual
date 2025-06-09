import logging
import functools
import os
import sys
import threading
import time
_exc_info = sys.exc_info
do_threads_debug = os.getenv('MOLER_DEBUG_THREADS', 'True').lower() in ('true', 't', 'yes', 'y', '1')

def log_exit_exception(fun):

    @functools.wraps(fun)
    def thread_exceptions_catcher(*args, **kwargs):
        logger = logging.getLogger('moler_threads')
        thread_name = threading.current_thread().name
        try:
            result = fun(*args, **kwargs)
            return result
        except SystemExit:
            pass
        except:
            th_exc_info = _exc_info()
            try:
                logger.error('Exception in thread {}'.format(thread_name), exc_info=th_exc_info)
            finally:
                del th_exc_info
    return thread_exceptions_catcher

def report_alive(report_tick=5.0):
    last_report_time = time.time()
    do_report = True
    while True:
        yield do_report
        now = time.time()
        delay = now - last_report_time
        if delay >= report_tick:
            last_report_time = now
            do_report = do_threads_debug
        else:
            do_report = False

def threads_dumper(report_tick=10.0):
    while True:
        time.sleep(report_tick)
        logging.getLogger('moler_threads').info('ACTIVE: {}'.format(threading.enumerate()))

def start_threads_dumper():
    if do_threads_debug:
        dumper = threading.Thread(target=threads_dumper)
        dumper.daemon = True
        dumper.start()