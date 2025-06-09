import logging
import os
import configparser
from lxml import etree
from itertools import chain
from odoo import api, models, fields
from odoo.tools.config import config as system_base_config
from odoo.addons.base_sparse_field.models.fields import Serialized
from .system_info import get_server_environment
_logger = logging.getLogger(__name__)
try:
    from odoo.addons import server_environment_files
    _dir = os.path.dirname(server_environment_files.__file__)
except ImportError:
    _logger.info('not using server_environment_files for configuration, no directory found')
    _dir = None
ENV_VAR_NAMES = ('SERVER_ENV_CONFIG', 'SERVER_ENV_CONFIG_SECRET')
_boolean_states = {'1': True, 'yes': True, 'true': True, 'on': True, '0': False, 'no': False, 'false': False, 'off': False}

def _load_running_env():
    if not system_base_config.get('running_env'):
        _logger.info('`running_env` not found. Using default = `test`.')
        _logger.info('We strongly recommend against using the rc file but instead use an explicit config file or env variable.')
        system_base_config['running_env'] = 'test'
_load_running_env()
ck_path = None
if _dir:
    ck_path = os.path.join(_dir, system_base_config['running_env'])
    if not os.path.exists(ck_path):
        raise Exception('Provided server environment does not exist, please add a folder %s' % ck_path)

def setboolean(obj, attr, _bool=None):
    """Replace the attribute with a boolean."""
    if _bool is None:
        _bool = dict(_boolean_states)
    res = _bool[getattr(obj, attr).lower()]
    setattr(obj, attr, res)
    return res

def _escape(s):
    """Convert the characters &<>'" in string s to HTML-safe sequences."""
    return str(s).replace('&', '&amp;').replace('>', '&gt;').replace('<', '&lt;').replace("'", '&#39;').replace('"', '&#34;')

def _listconf(env_path):
    """List configuration files in a folder."""
    files = [os.path.join(env_path, name) for name in sorted(os.listdir(env_path)) if name.endswith('.conf')]
    return files

def _load_config_from_server_env_files(config_p):
    default = os.path.join(_dir, 'default')
    running_env = os.path.join(_dir, system_base_config['running_env'])
    if os.path.isdir(default):
        conf_files = _listconf(default) + _listconf(running_env)
    else:
        conf_files = _listconf(running_env)
    try:
        config_p.read(conf_files)
    except Exception as e:
        raise Exception('Cannot read config files "%s":  %s' % (conf_files, e))

def _load_config_from_rcfile(config_p):
    config_p.read(system_base_config.rcfile)
    config_p.remove_section('options')

def _load_config_from_env(config_p):
    for varname in ENV_VAR_NAMES:
        env_config = os.getenv(varname)
        if env_config:
            try:
                config_p.read_string(env_config)
            except configparser.Error as err:
                raise Exception('%s content could not be parsed: %s' % (varname, err))

def _load_config():
    """Load the configuration and return a ConfigParser instance."""
    config_p = configparser.SafeConfigParser()
    config_p.optionxform = str
    if _dir:
        _load_config_from_server_env_files(config_p)
    _load_config_from_rcfile(config_p)
    _load_config_from_env(config_p)
    return config_p
serv_config = _load_config()

class _Defaults(dict):
    __slots__ = ()

    def __setitem__(self, key, value):

        def func(*a):
            return str(value)
        return dict.__setitem__(self, key, func)

class ServerConfiguration(models.TransientModel):
    """Display server configuration."""
    _name = 'server.config'
    _description = 'Display server configuration'
    _conf_defaults = _Defaults()
    config = Serialized()

    @classmethod
    def _build_model(cls, pool, cr):
        """Add columns to model dynamically
        and init some properties

        """
        ModelClass = super(ServerConfiguration, cls)._build_model(pool, cr)
        ModelClass._add_columns()
        ModelClass._arch = None
        ModelClass._build_osv()
        return ModelClass

    @classmethod
    def _format_key(cls, section, key):
        return '%s_I_%s' % (section, key)

    @property
    def show_passwords(self):
        return system_base_config['running_env'] in ('dev',)

    @classmethod
    def _format_key_display_name(cls, key_name):
        return key_name.replace('_I_', ' | ')

    @classmethod
    def _add_columns(cls):
        """Add columns to model dynamically"""
        cols = chain(list(cls._get_base_cols().items()), list(cls._get_env_cols().items()), list(cls._get_system_cols().items()))
        for (col, value) in cols:
            col_name = col.replace('.', '_')
            setattr(ServerConfiguration, col_name, fields.Char(string=cls._format_key_display_name(col_name), sparse='config', readonly=True))
            cls._conf_defaults[col_name] = value

    @classmethod
    def _get_base_cols(cls):
        """ Compute base fields"""
        res = {}
        for (col, item) in list(system_base_config.options.items()):
            key = cls._format_key('odoo', col)
            res[key] = item
        return res

    @classmethod
    def _get_env_cols(cls, sections=None):
        """ Compute base fields"""
        res = {}
        sections = sections if sections else serv_config.sections()
        for section in sections:
            for (col, item) in serv_config.items(section):
                key = cls._format_key(section, col)
                res[key] = item
        return res

    @classmethod
    def _get_system_cols(cls):
        """ Compute system fields"""
        res = {}
        for (col, item) in get_server_environment():
            key = cls._format_key('system', col)
            res[key] = item
        return res

    @classmethod
    def _group(cls, items):
        """Return an XML chunk which represents a group of fields."""
        names = []
        for key in sorted(items):
            names.append(key.replace('.', '_'))
        return '<group col="2" colspan="4">' + ''.join(['<field name="%s" readonly="1"/>' % _escape(name) for name in names]) + '</group>'

    @classmethod
    def _build_osv(cls):
        """Build the view for the current configuration."""
        arch = '<form string="Configuration Form"><notebook colspan="4">'
        rcfile = system_base_config.rcfile
        items = cls._get_base_cols()
        arch += '<page string="Odoo">'
        arch += '<separator string="%s" colspan="4"/>' % _escape(rcfile)
        arch += cls._group(items)
        arch += '<separator colspan="4"/></page>'
        arch += '<page string="Environment based configurations">'
        for section in sorted(serv_config.sections()):
            items = cls._get_env_cols(sections=[section])
            arch += '<separator string="[%s]" colspan="4"/>' % _escape(section)
            arch += cls._group(items)
        arch += '<separator colspan="4"/></page>'
        arch += '<page string="System">'
        arch += '<separator string="Server Environment" colspan="4"/>'
        arch += cls._group(cls._get_system_cols())
        arch += '<separator colspan="4"/></page>'
        arch += '</notebook></form>'
        cls._arch = etree.fromstring(arch)

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        """Overwrite the default method to render the custom view."""
        res = super(ServerConfiguration, self).fields_view_get(view_id, view_type, toolbar)
        View = self.env['ir.ui.view']
        if view_type == 'form':
            arch_node = self._arch
            (xarch, xfields) = View.postprocess_and_fields(self._name, arch_node, view_id)
            res['arch'] = xarch
            res['fields'] = xfields
        return res

    @api.model
    def _is_secret(self, key):
        """
        This method is intended to be inherited to defined which keywords
        should be secret.
        :return: list of secret keywords
        """
        secret_keys = ['passw', 'key', 'secret', 'token']
        return any((secret_key in key for secret_key in secret_keys))

    @api.model
    def default_get(self, fields_list):
        res = {}
        if not self.env.user.has_group('server_environment.has_server_configuration_access'):
            return res
        for key in self._conf_defaults:
            if not self.show_passwords and self._is_secret(key=key):
                res[key] = '**********'
            else:
                res[key] = self._conf_defaults[key]()
        return res