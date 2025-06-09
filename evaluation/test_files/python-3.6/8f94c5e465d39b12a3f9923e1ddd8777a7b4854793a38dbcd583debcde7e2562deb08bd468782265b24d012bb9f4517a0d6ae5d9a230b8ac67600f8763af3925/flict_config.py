import json
import os
from osadl_matrix import OSADL_MATRIX

def read_user_config():
    for path in [os.environ.get('FLICT_USERCONFIG'), os.path.join(os.environ.get('HOME', '/does/not/exist'), '.flict.cfg')]:
        try:
            with open(path) as i:
                return json.load(i)
        except Exception:
            pass
    return {}
_userconfig = read_user_config()
flict_version = '1.0.22'
SCRIPT_DIR = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))
VAR_DIR = os.path.join(SCRIPT_DIR, 'var')
BUILTIN_ALIAS_FILE = os.path.join(VAR_DIR, 'alias.json')
DEFAULT_FLICT_ALIAS_FILE = os.path.join(VAR_DIR, BUILTIN_ALIAS_FILE)
DEFAULT_MATRIX_FILE = _userconfig.get('matrix-file', OSADL_MATRIX)
DEFAULT_OUTPUT_FORMAT = _userconfig.get('output-format', 'JSON')