import configparser
import os.path
from dataclasses import dataclass
from .paths import config_file_path
from .utils.string_utils import convert_to_bool

@dataclass
class ConfigResponse:
    response: str = ''

    def as_bool(self) -> bool:
        return convert_to_bool(self.response)

def read_section(section_name: str) -> dict:
    config = configparser.ConfigParser()
    config.read(config_file_path)
    if not config.sections():
        raise FileNotFoundError("Configuration file not found. Try calling 'config.create_default_config_file()'")
    try:
        section = config[section_name]
        return dict(section)
    except KeyError:
        raise Exception('Invalid section name.')

def read_entry(section_name: str, entry: str) -> ConfigResponse:
    section = read_section(section_name)
    try:
        value = section[entry]
        return ConfigResponse(response=value)
    except KeyError:
        raise Exception('Invalid section or entry name.')

def update_entry(section_name: str, entry: str, value: str) -> None:
    config = configparser.ConfigParser()
    config.read(config_file_path)
    config.set(section_name, entry, value)
    with open(config_file_path, mode='w') as configfile:
        config.write(configfile)

def create_default_config_file():
    if os.path.isfile(config_file_path):
        return
    config = configparser.ConfigParser()
    config['General'] = {'prefix': '>', 'enable-warnings': 'true'}
    config['DefaultTheme'] = {'primary': 'white', 'warning': 'yellow', 'error': 'red', 'critical': 'red [bold]'}
    with open(config_file_path, mode='w') as configfile:
        config.write(configfile)