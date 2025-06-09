import os.path
from cwrap import BaseCClass
from ecl.util.util import StringHash
from ert._c_wrappers import ResPrototype
from ert._c_wrappers.config.config_content import ConfigContent
from ert._c_wrappers.config.unrecognized_enum import UnrecognizedEnum

class ConfigValidationError(ValueError):

    def __init__(self, errors, config_file=None):
        self.config_file = config_file
        self.errors = errors
        super().__init__(f'Parsing config file `{self.config_file}` resulted in the errors: {self.errors}' if self.config_file else f'{self.errors}')

class ConfigParser(BaseCClass):
    TYPE_NAME = 'config_parser'
    _alloc = ResPrototype('void* config_alloc()', bind=False)
    _add = ResPrototype('schema_item_ref config_add_schema_item(config_parser, char*, bool)')
    _free = ResPrototype('void config_free(config_parser)')
    _parse = ResPrototype('config_content_obj config_parse(config_parser,                                          char*,                                          char*,                                          char*,                                          char*,                                          hash,                                          config_unrecognized_enum,                                          bool)')
    _size = ResPrototype('int config_get_schema_size(config_parser)')
    _get_schema_item = ResPrototype('schema_item_ref config_get_schema_item(config_parser, char*)')
    _has_schema_item = ResPrototype('bool config_has_schema_item(config_parser, char*)')
    _add_key_value = ResPrototype('bool config_parser_add_key_values(config_parser,                                            config_content,                                            char*,                                            stringlist,                                            config_path_elm,                                            char*,                                            config_unrecognized_enum)')
    _validate = ResPrototype('void config_validate(config_parser, config_content)')

    def __init__(self):
        c_ptr = self._alloc()
        super().__init__(c_ptr)

    def __contains__(self, keyword):
        return self._has_schema_item(keyword)

    def __len__(self):
        return self._size()

    def __repr__(self):
        return self._create_repr(f'size={len(self)}')

    def add(self, keyword, required=False, value_type=None):
        item = self._add(keyword, required).setParent(self)
        if value_type:
            item.iset_type(0, value_type)
        return item

    def __getitem__(self, keyword):
        if keyword in self:
            item = self._get_schema_item(keyword)
            item.setParent(self)
            return item
        else:
            raise KeyError(f'Config parser does not have item:{keyword}')

    def parse(self, config_file, comment_string='--', include_kw='INCLUDE', define_kw='DEFINE', pre_defined_kw_map=None, unrecognized=UnrecognizedEnum.CONFIG_UNRECOGNIZED_WARN, validate=True) -> ConfigContent:
        assert isinstance(unrecognized, UnrecognizedEnum)
        hash_value = StringHash()
        if pre_defined_kw_map is not None:
            for key in pre_defined_kw_map:
                hash_value[key] = pre_defined_kw_map[key]
        if not os.path.exists(config_file):
            raise IOError(f'File: {config_file} does not exists')
        if not os.access(config_file, os.R_OK):
            raise IOError(f'We do not have read permissions for file: {config_file}')
        config_content = self._parse(config_file, comment_string, include_kw, define_kw, hash_value, unrecognized, validate)
        config_content.setParser(self)
        if validate and (not config_content.isValid()):
            raise ConfigValidationError(config_file=config_file, errors=config_content.getErrors())
        return config_content

    def free(self):
        self._free()

    def validate(self, config_content):
        self._validate(config_content)

    def add_key_value(self, config_content, key, value, path_elm=None, config_filename=None, unrecognized_action=UnrecognizedEnum.CONFIG_UNRECOGNIZED_WARN):
        return self._add_key_value(config_content, key, value, path_elm, config_filename, unrecognized_action)