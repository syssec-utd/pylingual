__all__ = ('query_datasets_options',)
import click
from ..utils import OptionGroup, unwrap, where_help
from .arguments import glob_argument, repo_argument
from .options import collections_option, dataset_type_option, where_option

class query_datasets_options(OptionGroup):

    def __init__(self, repo: bool=True, showUri: bool=True, useArguments: bool=True) -> None:
        self.decorators = []
        if repo:
            if not useArguments:
                raise RuntimeError('repo as an option is not currently supported.')
            self.decorators.append(repo_argument(required=True))
        if useArguments:
            self.decorators.append(glob_argument(help=unwrap('GLOB is one or more glob-style expressions that fully or partially identify the\n                            dataset type names to be queried.')))
        else:
            self.decorators.append(dataset_type_option(help=unwrap('One or more glob-style expressions that fully or partially identify the dataset\n                            type names to be queried.')))
        self.decorators.extend([collections_option(), where_option(help=where_help), click.option('--find-first', is_flag=True, help=unwrap("For each result data ID, only yield one DatasetRef of each\n                                     DatasetType, from the first collection in which a dataset of that dataset\n                                     type appears (according to the order of 'collections' passed in).  If\n                                     used, 'collections' must specify at least one expression and must not\n                                     contain wildcards."))])
        if showUri:
            self.decorators.append(click.option('--show-uri', is_flag=True, help='Show the dataset URI in results.'))