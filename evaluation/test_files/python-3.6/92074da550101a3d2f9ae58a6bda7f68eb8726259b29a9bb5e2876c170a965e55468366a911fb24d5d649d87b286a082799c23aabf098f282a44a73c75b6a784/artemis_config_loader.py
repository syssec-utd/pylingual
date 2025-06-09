"""
This module loads all of the config files in the config directory.
"""
import os
import sys
from glob import glob
import importlib.util

def load_config_modules():
    """
    This function loads all of the config files in the config directory.
    """
    file_dir = os.path.dirname(os.path.realpath(__file__))
    config_modules = glob(os.path.join(file_dir, '*.py'))
    for config_module in config_modules:
        config_module_name = os.path.basename(config_module).replace('.py', '')
        module = importlib.import_module('artemis_labs.temp.' + config_module_name, package=__name__)
        sys.modules[config_module_name] = module