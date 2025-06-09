import re
import sys
from argparse import Action
from dataclasses import dataclass, fields, is_dataclass
from inspect import getfullargspec, isclass
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, Optional, Sequence, Type, TypeVar, Union
from omegaconf import MISSING, DictConfig, ListConfig
from omegaconf.errors import ConfigKeyError, ValidationError
from typing_extensions import Concatenate, ParamSpec
from .core import from_dataclass, from_file, from_none, from_options, merge, to_yaml, unsafe_merge
from .flexyclasses import is_flexyclass
from .logging import configure_logging
from .nicknames import NicknameRegistry
from .rich_utils import RichArgumentParser, add_pretty_traceback, print_config_as_tree, print_table
MP = ParamSpec('MP')
CT = TypeVar('CT')
RT = TypeVar('RT')

@dataclass
class Flag:
    name: str
    help: str
    action: str = MISSING
    default: Optional[Any] = MISSING
    nargs: Optional[Union[str, int]] = MISSING
    metavar: Optional[str] = MISSING
    usage_extras: Optional[str] = MISSING
    choices: Optional[Sequence[Any]] = MISSING

    @property
    def short(self) -> str:
        return f'-{self.name[0]}'

    @property
    def usage(self) -> str:
        extras = '' if self.usage_extras is MISSING else f' {self.usage_extras}'
        return f'{{{self}{extras}}}'

    @property
    def long(self) -> str:
        return f'--{self.name}'

    def add_argparse(self, parser: RichArgumentParser) -> Action:
        kwargs: Dict[str, Any] = {'help': self.help}
        if self.action is not MISSING:
            kwargs['action'] = self.action
        if self.default is not MISSING:
            kwargs['default'] = self.default
        if self.nargs is not MISSING:
            kwargs['nargs'] = self.nargs
        if self.metavar is not MISSING:
            kwargs['metavar'] = self.metavar
        return parser.add_argument(self.short, self.long, **kwargs)

    def __str__(self) -> str:
        return f'{self.short}/{self.long}'

@dataclass
class CliFlags:
    config: Flag = Flag(name='config', help='Either a path to a YAML file containing a configuration, or a nickname for a configuration in the registry. Multiple configurations can be specified with additional -c flags, and they will be merged in the order they are provided.', default=[], action='append', metavar='/path/to/config.yaml')
    options: Flag = Flag(name='options', help='Print all default options and CLI flags.', action='store_true')
    inputs: Flag = Flag(name='inputs', help='Print the input configuration.', action='store_true')
    parsed: Flag = Flag(name='parsed', help='Print the parsed configuration.', action='store_true')
    log_level: Flag = Flag(name='log-level', help='Logging level to use for this program. Can be one of CRITICAL, ERROR, WARNING, INFO, or DEBUG. Defaults to WARNING.', default='WARNING', nargs=1, choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'])
    debug: Flag = Flag(name='debug', help="Enable debug mode; equivalent to '--log-level DEBUG'.", action='store_true')
    quiet: Flag = Flag(name='quiet', help='If provided, it does not print the configuration when running.', action='store_true')
    resolvers: Flag = Flag(name='resolvers', help='Print all registered resolvers in OmegaConf, Springs, and current codebase.', action='store_true')
    nicknames: Flag = Flag(name='nicknames', help='Print all registered nicknames in Springs.', action='store_true')
    save: Flag = Flag(name='save', help='Save the configuration to a YAML file and exit.', default=None, nargs=1, metavar='/path/to/destination.yaml')

    @property
    def flags(self) -> Iterable[Flag]:
        for f in fields(self):
            maybe_flag = getattr(self, f.name)
            if isinstance(maybe_flag, Flag):
                yield maybe_flag

    def add_argparse(self, parser: RichArgumentParser) -> Sequence[Action]:
        return [flag.add_argparse(parser) for flag in self.flags]

    def make_cli(self, func: Callable, name: str) -> RichArgumentParser:
        """Sets up argument parser ahead of running the CLI. This includes
        creating a help message, and adding a series of flags."""
        ap = RichArgumentParser(description=f'Parser for configuration {name}', entrypoint=sys.argv[0], arguments='param1=value1 … paramN=valueN')
        self.add_argparse(ap)
        return ap

def check_if_callable_can_be_decorated(func: Callable):
    expected_args = getfullargspec(func).args
    if len(expected_args) == 0:
        msg = f'Function `{func.__name__}` cannot be decorated by `config_to_program` because it does not accept any argument.'
        raise RuntimeError(msg)
    elif len(expected_args) > 1:
        msg = f'Function `{func.__name__}` cannot be decorated by  `config_to_program` because it expects {len(expected_args)} > 1; If you want to pass extra arguments to this function, use kwargs with default values.'
        raise RuntimeError(msg)

def check_if_valid_main_args(func: Callable, args: Sequence[Any]):
    if len(args):
        msg = f'After decorating `{func.__name__}` with `config_to_program`, do not provide any additional arguments while invoking it; any additional parameter should be passed as a keyword argument.'
        raise RuntimeError(msg)
C = TypeVar('C', DictConfig, ListConfig)

def merge_and_catch(c1: C, c2: Union[DictConfig, ListConfig]) -> C:
    """Improves printing of errors when merging configs in cli."""
    try:
        return merge(c1, c2)
    except Exception as e:
        prefix = 'Error when merging cli options and files with struct config:'
        if isinstance(e, ConfigKeyError):
            (msg, *_) = e.args[0].split('\n')
        elif isinstance(e, ValidationError):
            (msg, key, *_) = e.args[0].split('\n')
            (_, key) = key.split('full_key: ', 1)
            msg = f"{msg} for key '{key}'"
        else:
            msg = str(e.args)
        raise type(e)(f'{prefix} {msg}!')

def validate_leftover_args(args: Sequence[str]):
    var_pattern = '[a-zA-Z_]+[a-zA-Z0-9_]*'
    re_valid = re.compile(f'({var_pattern}\\.?)*{var_pattern}=.+')
    for arg in args:
        if not re_valid.match(arg):
            raise ValueError(f"'{arg}' is not an option and it does not match the pattern 'path.to.key=value' expected for a cli config override.")

def load_from_file_or_nickname(config_path_or_nickname: Union[str, Path]) -> Union[DictConfig, ListConfig]:
    if not isinstance(config_path_or_nickname, Path) and re.match('^{.*}$', config_path_or_nickname):
        config_path_or_nickname = config_path_or_nickname[1:-1]
        loaded_config = NicknameRegistry.get(name=config_path_or_nickname, raise_if_missing=True)
        if is_dataclass(loaded_config):
            loaded_config = from_dataclass(loaded_config)
        elif is_flexyclass(loaded_config):
            loaded_config = loaded_config.to_dict_config()
        elif not isinstance(loaded_config, (DictConfig, ListConfig)):
            raise ValueError(f"Nickname '{config_path_or_nickname}' is not a DictConfig or ListConfig.")
    else:
        loaded_config = from_file(config_path_or_nickname)
    return loaded_config

def wrap_main_method(func: Callable[Concatenate[Any, MP], RT], name: str, config_node: DictConfig, *args: MP.args, **kwargs: MP.kwargs) -> RT:
    if not isinstance(config_node, DictConfig):
        raise TypeError('Config node must be a DictConfig')
    check_if_callable_can_be_decorated(func=func)
    check_if_valid_main_args(func=func, args=args)
    ap = CliFlags().make_cli(func=func, name=name)
    (opts, leftover_args) = ap.parse_known_args()
    validate_leftover_args(leftover_args)
    configure_logging(logging_level='DEBUG' if opts.debug else opts.log_level)
    do_no_run = opts.options or opts.inputs or opts.parsed or opts.resolvers or opts.nicknames or opts.save
    if opts.resolvers:
        from .resolvers import all_resolvers
        print_table(title='Registered Resolvers', columns=['Resolver Name'], values=[(r,) for r in sorted(all_resolvers())], caption="Resolvers use syntax ${resolver_name:'arg1','arg2'}.\nFor more information, visit https://omegaconf.readthedocs.io/en/latest/custom_resolvers.html")
    if opts.nicknames:
        print_table(title='Registered Nicknames', columns=['Nickname', 'Path'], values=NicknameRegistry().all(), caption="Nicknames are invoked via: ${sp.ref:nickname,'path.to.key1=value1',...}. \nOverride keys are optional (but quotes are required).")
    if opts.options:
        print_config_as_tree(title='Default Options', config=config_node, title_color='green', print_help=True)
    accumulator_config = unsafe_merge(config_node)
    for config_file in opts.config:
        file_config = load_from_file_or_nickname(config_file)
        if opts.inputs:
            print_config_as_tree(title=f'Input From File {config_file}', config=file_config, title_color='green', print_help=False)
        accumulator_config = unsafe_merge(accumulator_config, file_config)
    cli_config = from_options(leftover_args)
    if opts.inputs:
        print_config_as_tree(title='Input From Command Line', config=cli_config, title_color='green', print_help=False)
    accumulator_config = unsafe_merge(accumulator_config, cli_config)
    if do_no_run and (not opts.parsed):
        sys.exit(0)
    parsed_config = merge_and_catch(config_node, accumulator_config)
    if not opts.quiet or opts.parsed:
        print_config_as_tree(title='Parsed Config', config=parsed_config, title_color='green', print_help=False)
    if opts.save is not None:
        with open(opts.save, 'w') as f:
            f.write(to_yaml(parsed_config))
    if do_no_run:
        sys.exit(0)
    else:
        return func(parsed_config, *args, **kwargs)

def cli(config_node_cls: Optional[Type[CT]]=None) -> Callable[[Callable[Concatenate[CT, MP], RT]], Callable[MP, RT]]:
    """
    Create a command-line interface for a method that uses a config file.
    The parsed configuration will be passed as the first argument to the
    decorated method.

    Example usage:

    ```python

    import springs as sp

    @sp.dataclass
    class Config:
        greeting: str = "Hello"
        name: str = "World"


    @sp.cli(Config)
    def main(cfg: Config):
        print(f"{cfg.greeting}, {cfg.name}!")
    ```

    A structured configuration is not required, but it is recommended,
    as it will allow for type checking at runtime and type hints during
    development.

    Args:
        config_node_cls (Optional[type]): The class of the configuration
            node. If not provided, no type checking will be performed.

    Returns:
        Callable: A decorator that can be used to decorate a method.
    """
    add_pretty_traceback()
    if config_node_cls is None:
        config_node = from_none()
        name = '<unnamed>'
    elif not (isclass(config_node_cls) and is_dataclass(config_node_cls)):
        msg = '`config_node` must be be decorated as a dataclass'
        raise ValueError(msg)
    else:
        config_node = from_dataclass(config_node_cls)
        name = config_node_cls.__name__

    def wrapper(func: Callable[Concatenate[CT, MP], RT]) -> Callable[MP, RT]:

        def wrapping(*args: MP.args, **kwargs: MP.kwargs) -> RT:
            return wrap_main_method(func, name, config_node, *args, **kwargs)
        return wrapping
    return wrapper