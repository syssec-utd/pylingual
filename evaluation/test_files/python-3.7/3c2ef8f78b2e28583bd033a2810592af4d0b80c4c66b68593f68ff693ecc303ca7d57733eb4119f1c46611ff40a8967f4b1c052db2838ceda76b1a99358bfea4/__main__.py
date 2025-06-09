import logging
import optilibre.cli as cli
from optilibre import __version__

def main():
    logging.info('Optilibre v{}'.format(__version__))
    cli.cli()
if __name__ == '__main__':
    main()