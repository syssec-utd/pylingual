"""Misc utilities for the Plom Server"""
import importlib.resources as resources
import logging
from pathlib import Path
import plom
from plom import Default_Port
from plom.server import specdir, confdir
server_dirs = (Path('.'), specdir, confdir, Path('pages'), Path('pages') / 'discardedPages', Path('pages') / 'collidingPages', Path('pages') / 'unknownPages', Path('pages') / 'originalPages', Path('markedQuestions'), Path('markedQuestions') / 'plomFiles', Path('userRubricPaneData'), Path('solutionImages'))

def build_server_directories(basedir=Path('.')):
    """Build some directories the server will need"""
    log = logging.getLogger('server')
    for d in server_dirs:
        log.debug('Making directory {}'.format(d))
        (basedir / d).mkdir(exist_ok=True)

def check_server_directories(basedir=Path('.')):
    """Ensure some server directories exist"""
    for d in server_dirs:
        if not (basedir / d).is_dir():
            raise FileNotFoundError("Required directory '{}' are not present. Have you run 'plom-server init'?".format(d))

def check_server_fully_configured(basedir):
    if not (basedir / confdir / 'serverDetails.toml').exists():
        raise FileNotFoundError("Server configuration file not present. Have you run 'plom-server init'?")
    if not ((basedir / confdir).glob('*.key') and (basedir / confdir).glob('*.crt')):
        raise FileNotFoundError("SSL keys not present. Have you run 'plom-server init'?")

def create_server_config(dur=confdir, *, port=None, name=None):
    """Create a default server configuration file.

    args:
        dur (pathlib.Path): where to put the file.

    keyword args:
        port (int/None): port on which to run the server.
        name (str/None): the name of your server such as
            "plom.example.com" or an IP address.  Defaults to
            "localhost" which is usually fine but may cause trouble
            with SSL certificates.

    raises:
        FileExistsError: file is already there.
    """
    sd = Path(dur) / 'serverDetails.toml'
    if sd.exists():
        raise FileExistsError('Config already exists in {}'.format(sd))
    template = resources.read_text(plom, 'serverDetails.toml')
    if name:
        template = template.replace('localhost', name)
    if port:
        template = template.replace(f'{Default_Port}', str(port))
    with open(sd, 'w') as fh:
        fh.write(template)

def create_blank_predictions(dur=specdir):
    """Create empty prediction list to store machine-read student IDs.

    args:
        dur (str/pathlib.Path): where to put the file.

    raises:
        FileExistsError: file is already there.
    """
    pl = Path(dur) / 'predictionlist.csv'
    if pl.exists():
        raise FileExistsError(f'{pl} already exists.')
    with open(pl, 'w') as fh:
        fh.write('test, id\n')