import sys
from typing import Iterable, TextIO

def reprint(hostnames: Iterable[str], outputs: Iterable[str], file: TextIO=sys.stdout) -> None:
    """
    Reprints outputs from multiple hosts with the hostname as a prefix.

    :param hostnames: Hostnames or IP addresses
    :param outputs: Output for every host
    :param file: Output to print to
    """
    for (hostname, output) in zip(hostnames, outputs):
        for line in output.splitlines():
            print(f'[{hostname}] {line}', file=file)