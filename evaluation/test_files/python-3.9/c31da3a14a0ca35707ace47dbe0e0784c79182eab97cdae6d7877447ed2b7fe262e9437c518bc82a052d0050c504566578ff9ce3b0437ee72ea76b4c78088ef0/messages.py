import os
import sys
import re
from typing import NamedTuple, Union, Optional, Dict, List
import yaml
from trubar import jaml
from trubar.config import config

class MsgNode(NamedTuple):
    value: Union['MsgDict', str, bool, None]
    comments: Optional[List[str]] = None
MsgDict = Dict[str, MsgNode]
PureDict = Dict[str, Union[bool, None, str, 'PureDict']]

def load(filename: str) -> MsgDict:
    if not os.path.exists(filename):
        print(f'File not found: {filename}')
        sys.exit(2)
    is_yaml = os.path.splitext(filename)[1] == '.yaml'
    try:
        if is_yaml:
            with open(filename, encoding=config.encoding) as f:
                messages = yaml.load(f, Loader=yaml.Loader)
        else:
            messages = jaml.readfile(filename, encoding=config.encoding)
    except (jaml.JamlError, yaml.YAMLError) as exc:
        print(f'Error in {filename}:\n{exc}')
        sys.exit(3)
    if is_yaml:
        messages = dict_to_msg_nodes(messages)
    if not check_sanity(messages, filename):
        sys.exit(4)
    return messages

def check_sanity(message_dict: MsgDict, filename: Optional[str]=None):
    key_re = re.compile('^((def)|(class)) `\\w+`')
    sane = True

    def fail(msg):
        nonlocal sane
        if sane and filename is not None:
            print(f'Errors in {filename}:')
        print(msg)
        sane = False

    def check_sane(messages: MsgDict, path: str):
        for (key, obj) in messages.items():
            npath = f'{path}/{key}'
            if key_re.fullmatch(key) is None:
                if isinstance(obj.value, dict):
                    fail(f'{npath}: Unexpectedly a namespace')
            elif not isinstance(obj.value, dict):
                fail(f'{npath}: Unexpectedly not a namespace')
            else:
                check_sane(obj.value, f'{npath}')
    for (fname, fspace) in message_dict.items():
        if isinstance(fspace.value, dict):
            check_sane(fspace.value, fname)
    return sane

def dict_to_msg_nodes(messages: PureDict) -> Dict[str, MsgDict]:
    return {key: MsgNode(dict_to_msg_nodes(value) if isinstance(value, dict) else value) for (key, value) in messages.items()}

def dict_from_msg_nodes(messages: MsgDict) -> PureDict:
    return {key: dict_from_msg_nodes(node.value) if isinstance(node.value, dict) else node.value for (key, node) in messages.items()}

def dump(messages: MsgDict, filename: str) -> None:
    if os.path.splitext(filename)[1] == '.jaml':
        with open(filename, 'w', encoding=config.encoding) as f:
            f.write(jaml.dump(messages))
    else:
        messages = dict_from_msg_nodes(messages)
        with open(filename, 'wb') as f:
            f.write(yaml.dump(messages, indent=4, sort_keys=False, encoding='utf-8', allow_unicode=True))