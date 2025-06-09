import errno
import shutil
import os
import platform
from os.path import expanduser, exists, dirname
from configobj import ConfigObj

def config_location():
    if 'XDG_CONFIG_HOME' in os.environ:
        return '%s/irissqlcli/' % expanduser(os.environ['XDG_CONFIG_HOME'])
    elif platform.system() == 'Windows':
        return os.getenv('USERPROFILE') + '\\AppData\\Local\\dbcli\\irissqlcli\\'
    else:
        return expanduser('~/.config/irissqlcli/')

def load_config(usr_cfg, def_cfg=None):
    cfg = ConfigObj()
    cfg.merge(ConfigObj(def_cfg, interpolation=False))
    cfg.merge(ConfigObj(expanduser(usr_cfg), interpolation=False, encoding='utf-8'))
    cfg.filename = expanduser(usr_cfg)
    return cfg

def ensure_dir_exists(path):
    parent_dir = expanduser(dirname(path))
    try:
        if parent_dir:
            os.makedirs(parent_dir)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise

def write_default_config(source, destination, overwrite=False):
    destination = expanduser(destination)
    if not overwrite and exists(destination):
        return
    ensure_dir_exists(destination)
    shutil.copyfile(source, destination)

def upgrade_config(config, def_config):
    cfg = load_config(config, def_config)
    cfg.write()

def get_config(irissqlclirc_file=None):
    from irissqlcli import __file__ as package_root
    package_root = os.path.dirname(package_root)
    irissqlclirc_file = irissqlclirc_file or '%sconfig' % config_location()
    default_config = os.path.join(package_root, 'irissqlclirc')
    write_default_config(default_config, irissqlclirc_file)
    return load_config(irissqlclirc_file, default_config)