import os
import re
import sys
import pipes
import shutil
import logging
import subprocess
from functools import lru_cache
from typing import Dict, Tuple, Optional, Union, Any
from pathlib import Path
from . import errors
from .types import Binary, Target, Strategy, check_target
from .utils import get_env_dir, env_to_bool, maybe_decode
log: logging.Logger = logging.getLogger(__name__)
ENV_DIR: Path = get_env_dir()
BINARIES_DIR: Path = ENV_DIR / 'bin'
USE_GLOBAL_NODE = env_to_bool('PYRIGHT_PYTHON_GLOBAL_NODE', default=True)
VERSION_RE = re.compile('\\d+\\.\\d+\\.\\d+')

def _ensure_available(target: Target) -> Binary:
    """Ensure the target node executable is available"""
    path = None
    if USE_GLOBAL_NODE:
        path = _get_global_binary(target)
    if path is not None:
        return Binary(path=path, strategy=Strategy.GLOBAL)
    return Binary(path=_ensure_node_env(target), strategy=Strategy.NODEENV)

def _ensure_node_env(target: Target) -> Path:
    log.debug('Checking for nodeenv %s binary', target)
    if not ENV_DIR.exists():
        log.debug('Environment not found at %s', ENV_DIR)
        _install_node_env()
    else:
        log.debug('Environment exists at %s', ENV_DIR)
    path = BINARIES_DIR.joinpath(target)
    if not path.exists():
        _install_node_env()
    if not path.exists():
        raise errors.BinaryNotFound(path=path, target=target)
    return path

def _get_global_binary(target: Target) -> Optional[Path]:
    log.debug('Checking for global target binary: %s', target)
    which = shutil.which(target)
    if which is not None:
        log.debug('Found global binary at: %s', which)
        path = Path(which)
        if path.exists():
            log.debug('Global binary exists at: %s', which)
            return path
    log.debug('Global target binary: %s not found', target)
    return None

def _install_node_env() -> None:
    log.debug('Installing nodeenv to %s', ENV_DIR)
    args = [sys.executable, '-m', 'nodeenv', str(ENV_DIR)]
    log.debug('Running command with args: %s', args)
    subprocess.run(args, check=True)

def run(target: Target, *args: str, **kwargs: Any) -> Union['subprocess.CompletedProcess[bytes]', 'subprocess.CompletedProcess[str]']:
    check_target(target)
    binary = _ensure_available(target)
    env = os.environ.copy()
    if binary.strategy == Strategy.NODEENV:
        env.update(get_env_variables())
        if shutil.which('bash'):
            activate = binary.path.parent / 'activate'
            node_args = ['bash', '-c', f". {pipes.quote(str(activate))} && {' '.join([target, *args])}"]
        else:
            if not env_to_bool('PYRIGHT_PYTHON_IGNORE_WARNINGS', default=False):
                print('WARNING: nodeenv usage without access to bash, this is untested behaviour.\n')
            node_args = [str(binary.path), *args]
    elif binary.strategy == Strategy.GLOBAL:
        node_args = [str(binary.path), *args]
    else:
        raise RuntimeError(f'Unknown strategy: {binary.strategy}')
    log.debug('Running node command with args: %s', node_args)
    return subprocess.run(node_args, env=env, **kwargs)

def version(target: Target) -> Tuple[int, ...]:
    proc = run(target, '--version', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = maybe_decode(proc.stdout)
    match = VERSION_RE.search(output)
    if not match:
        print(output, file=sys.stderr)
        raise errors.VersionCheckFailed(f'Could not find version from `{target} --version`, see output above')
    info = tuple((int(value) for value in match.group(0).split('.')))
    log.debug('Version check for %s returning %s', target, info)
    return info

@lru_cache(maxsize=None)
def latest(package: str) -> str:
    """Return the latest version for the given package"""
    proc = run('npm', 'info', package, 'version', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout = maybe_decode(proc.stdout)
    if proc.returncode != 0:
        print(stdout, file=sys.stderr)
        raise errors.VersionCheckFailed(f'Version check for {package} failed, see output above.')
    match = VERSION_RE.search(stdout)
    if not match:
        print(stdout, file=sys.stderr)
        raise errors.VersionCheckFailed(f'Could not find version for {package}, see output above')
    value = match.group(0)
    log.debug('Version check for %s returning %s', package, value)
    return value

def get_env_variables() -> Dict[str, Any]:
    """Return the environmental variables that should be passed to a binary"""
    return {'NODE_PATH': str(ENV_DIR / 'lib' / 'node_modules'), 'NPM_CONFIG_PREFIX': str(ENV_DIR), 'npm_config_prefix': str(ENV_DIR)}