import argparse
import atexit
import importlib
import logging
import os
import signal
import sys
import time
from remoulade import Worker, __version__, get_broker, get_logger
RET_OK = 0
RET_KILLED = 1
RET_IMPORT = 2
RET_CONNECT = 3
RET_PIDFILE = 4
RET_WORKER_STOP = 5
logformat = '[%(asctime)s] [%(threadName)s] [%(name)s] [%(levelname)s] %(message)s'
verbosity = {0: logging.INFO, 1: logging.DEBUG}
HELP_EPILOG = 'examples:\n  # Run remoulade workers with actors defined in `./some_module.py`.\n  $ remoulade some_module\n\n  # Run remoulade with 1 thread per process.\n  $ remoulade --threads 1 some_module\n\n  # Run remoulade with gevent.  Make sure you `pip install gevent` first.\n  $ remoulade-gevent --threads 1024 some_module\n\n  # Import extra modules.  Useful when your main module doesn\'t import\n  # all the modules you need.\n  $ remoulade some_module some_other_module\n\n  # Listen only to the "foo" and "bar" queues.\n  $ remoulade some_module -Q foo bar\n\n  # Write the main process pid to a file.\n  $ remoulade some_module --pid-file /tmp/remoulade.pid\n\n  # Write logs to a file.\n  $ remoulade some_module --log-file /tmp/remoulade.log\n'

def parse_arguments():
    parser = argparse.ArgumentParser(prog='remoulade', description='Run remoulade workers.', formatter_class=argparse.RawDescriptionHelpFormatter, epilog=HELP_EPILOG)
    parser.add_argument('modules', metavar='module', nargs='*', help='additional python modules to import')
    parser.add_argument('--threads', '-t', default=8, type=int, help='the number of worker threads per process (default: 8)')
    parser.add_argument('--prefetch-multiplier', default=2, type=int, help='\n            the number of messages to prefetch at a time to be multiplied by the number of concurrent processes\n            (default:2)\n        ')
    parser.add_argument('--path', '-P', default='.', nargs='*', type=str, help='the module import path (default: .)')
    parser.add_argument('--queues', '-Q', nargs='*', type=str, help='listen to a subset of queues (default: all queues)')
    parser.add_argument('--pid-file', type=str, help='write the PID of the master process to a file (default: no pid file)')
    parser.add_argument('--log-file', type=argparse.FileType(mode='a', encoding='utf-8'), help='write all logs to a file (default: sys.stderr)')
    parser.add_argument('--termination-timeout', type=int, help='The number of seconds to wait for everything to shut down (default: 10 min)', default=600)
    parser.add_argument('--version', action='version', version=__version__)
    parser.add_argument('--verbose', '-v', action='count', default=0, help='turn on verbose log output')
    return parser.parse_args()

def setup_pidfile(filename):
    try:
        pid = os.getpid()
        with open(filename) as pid_file:
            old_pid = int(pid_file.read().strip())
            if old_pid == pid:
                return pid
        try:
            os.kill(old_pid, 0)
            raise RuntimeError('Remoulade is already running with PID %d.' % old_pid)
        except OSError:
            try:
                os.remove(filename)
            except FileNotFoundError:
                pass
    except FileNotFoundError:
        pass
    except ValueError as e:
        raise RuntimeError('PID file contains garbage. Aborting.') from e
    try:
        with open(filename, 'w') as pid_file:
            pid_file.write(str(pid))
        os.chmod(filename, 420)
        return pid
    except (FileNotFoundError, PermissionError) as e:
        raise RuntimeError(f'Failed to write PID file {e.filename!r}. {e.strerror}.') from e

def remove_pidfile(filename, logger):
    try:
        logger.debug('Removing PID file %r.', filename)
        os.remove(filename)
    except FileNotFoundError:
        logger.debug("Failed to remove PID file. It's gone.")

def setup_logging(args, *, stream=sys.stderr):
    level = verbosity.get(args.verbose, logging.DEBUG)
    logging.basicConfig(level=level, format=logformat, stream=stream)
    return get_logger('remoulade')

def start_worker(args, logger):
    try:
        for module in args.modules:
            importlib.import_module(module)
        broker = get_broker()
        broker.emit_after('process_boot')
        worker = Worker(broker, queues=args.queues, worker_threads=args.threads, prefetch_multiplier=args.prefetch_multiplier)
        worker.start()
    except ImportError:
        logger.exception('Failed to import module.')
        return os._exit(RET_IMPORT)

    def termhandler(signum, frame):
        nonlocal running
        if running:
            logger.info('Stopping worker...')
            running = False
        else:
            logger.warning('Killing worker...')
            return os._exit(RET_KILLED)
    logger.info('Worker is ready for action.')
    signal.signal(signal.SIGINT, termhandler)
    signal.signal(signal.SIGTERM, termhandler)
    signal.signal(signal.SIGHUP, termhandler)
    running = True
    ret_code = RET_OK
    while running:
        if worker.consumer_stopped:
            running = False
            ret_code = RET_CONNECT
        if worker.worker_stopped:
            running = False
            ret_code = RET_OK
            logger.info('Worker thread is not running anymore, stopping Worker.')
        else:
            time.sleep(1)
    worker.stop(args.termination_timeout * 1000)
    broker.emit_before('process_stop')
    broker.close()
    return ret_code

def main():
    args = parse_arguments()
    for path in args.path:
        sys.path.insert(0, path)
    try:
        if args.pid_file:
            setup_pidfile(args.pid_file)
    except RuntimeError as e:
        logger = setup_logging(args, stream=args.log_file or sys.stderr)
        logger.critical(e)
        return RET_PIDFILE
    logger = setup_logging(args, stream=args.log_file or sys.stderr)
    logger.info('Remoulade %r is booting up.' % __version__)
    if args.pid_file:
        atexit.register(remove_pidfile, args.pid_file, logger)
    return start_worker(args, logger)
if __name__ == '__main__':
    sys.exit(main())