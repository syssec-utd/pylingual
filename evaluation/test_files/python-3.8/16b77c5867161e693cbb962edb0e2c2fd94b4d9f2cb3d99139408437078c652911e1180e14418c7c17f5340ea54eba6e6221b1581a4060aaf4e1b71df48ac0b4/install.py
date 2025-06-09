import click
from ...utils.download import download
from ...utils.run import run
from .. import DOWNLOADS, SHELL
from . import KEY_NAME, KEY_URL, NAME, SOURCES_LIST, SOURCES_LIST_PATH, TRUSTED_KEY_PATH

@click.command()
def main() -> None:
    key_path = DOWNLOADS / KEY_NAME
    download(url=KEY_URL, output=key_path)
    run('sudo', 'gpg', '--dearmor', '--output', str(TRUSTED_KEY_PATH), str(key_path))
    run('sudo', str(SHELL), '-c', f'echo "{SOURCES_LIST}" > "{SOURCES_LIST_PATH}"')
    run('sudo', 'apt', 'update')
    run('sudo', 'apt', 'install', NAME)