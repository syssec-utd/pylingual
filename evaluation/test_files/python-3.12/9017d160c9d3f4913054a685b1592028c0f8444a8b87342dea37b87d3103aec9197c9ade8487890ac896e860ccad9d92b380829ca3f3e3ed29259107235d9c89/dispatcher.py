"""Dispatcher.

The configuration file is watched with inotify. If needed, the reload of the
configuration file can be triggered with a `kill -10 <dispatcher pid>`.
"""
import argparse
import sys
from trollmoves.dispatcher import Dispatcher
from trollmoves.logging import setup_logging, add_logging_options_to_parser

def parse_args():
    """Parse commandline arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('config_file', help='The configuration file to run on.')
    parser.add_argument('-p', '--publish-port', type=int, dest='pub_port', nargs='?', const=0, default=None, help='Publish messages for dispatched files on this port. Default: no publishing.')
    parser.add_argument('-n', '--publish-nameserver', nargs='*', dest='pub_nameservers', help='Nameserver for publisher to connect to')
    add_logging_options_to_parser(parser, legacy=True)
    return parser.parse_args()

def main():
    """Start and run the dispatcher."""
    cmd_args = parse_args()
    logger = setup_logging('dispatcher', cmd_args)
    logger.info('Starting up.')
    try:
        dispatcher = Dispatcher(cmd_args.config_file, publish_port=cmd_args.pub_port, publish_nameservers=cmd_args.pub_nameservers)
    except Exception as err:
        logger.error('Dispatcher crashed: %s', str(err))
        sys.exit(1)
    try:
        dispatcher.run()
    except KeyboardInterrupt:
        logger.debug('Interrupting')
    finally:
        dispatcher.close()
if __name__ == '__main__':
    main()