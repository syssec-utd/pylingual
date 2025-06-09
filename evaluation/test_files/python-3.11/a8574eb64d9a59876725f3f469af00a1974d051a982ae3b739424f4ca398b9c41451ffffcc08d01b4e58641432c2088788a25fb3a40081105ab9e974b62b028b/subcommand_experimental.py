import argparse
from typing import Optional
import annofabcli
import annofabcli.common.cli
from annofabcli.experimental import list_out_of_range_annotation_for_movie

def parse_args(parser: argparse.ArgumentParser):
    subparsers = parser.add_subparsers(dest='subcommand_name')
    list_out_of_range_annotation_for_movie.add_parser(subparsers)

def add_parser(subparsers: Optional[argparse._SubParsersAction]=None):
    subcommand_name = 'experimental'
    subcommand_help = 'アルファ版のサブコマンド'
    description = 'アルファ版のサブコマンド。予告なしに削除されたり、コマンドライン引数が変わったりします。'
    parser = annofabcli.common.cli.add_parser(subparsers, subcommand_name, subcommand_help, description, is_subcommand=False)
    parse_args(parser)
    return parser