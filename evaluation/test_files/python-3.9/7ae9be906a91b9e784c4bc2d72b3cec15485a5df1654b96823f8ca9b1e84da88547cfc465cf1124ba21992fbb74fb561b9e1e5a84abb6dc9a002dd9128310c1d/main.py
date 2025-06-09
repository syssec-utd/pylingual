"""
``clang_tools.main``
--------------------

The module containing main entrypoint function.
"""
import argparse
from typing import List
from .install import install_clang_tools

def parse_args(args: List[str]=None) -> argparse.Namespace:
    """Get and parse args given on the CLI.

    :param args: The arguments given on the command line. If specified, this does not
        need to include the name of the program (ie "clang_tools").
    """
    parser = argparse.ArgumentParser(prog='clang-tools')
    parser.add_argument('-i', '--install', default='13', help='Install clang-tools with specific version. default is 13.')
    parser.add_argument('-d', '--directory', default='', help='The directory where is the clang-tools install.')
    parser.add_argument('-f', action='store_true', dest='overwrite', help='Force overwriting the symlink to the installed binary. This will only overwrite an existing symlink.')
    return parser.parse_args(args)

def main():
    """The main entrypoint to the CLI program."""
    args = parse_args()
    install_clang_tools(args.install, args.directory, args.overwrite)
if __name__ == '__main__':
    main()