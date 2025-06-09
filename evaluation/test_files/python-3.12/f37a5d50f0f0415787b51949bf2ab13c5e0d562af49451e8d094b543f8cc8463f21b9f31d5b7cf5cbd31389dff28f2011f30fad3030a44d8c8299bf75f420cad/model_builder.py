import inspect
from pathlib import Path
from typing import ClassVar
import jinja2
from sqlalchemy import Table
from ..generator.model_template_generator import model_template_gen
from ..utils.import_builder import ImportBuilder

class ModelCodeGen:

    def __init__(self, file_name, db_type):
        self.file_name = file_name
        self.table_list = {}
        self.code = ''
        self.model_code = ''
        self.import_helper = ImportBuilder()
        self.import_helper.add(import_=set(['dataclass', 'field']), from_='dataclasses')
        self.import_helper.add(import_=set(['datetime', 'timedelta', 'date', 'time']), from_='datetime')
        self.import_helper.add(import_=set(['Decimal']), from_='decimal')
        self.import_helper.add(import_=set(['Optional', 'List', 'Union', 'NewType']), from_='typing')
        self.import_helper.add(import_=set(['pydantic']))
        self.import_helper.add(import_=set(['BaseModel']), from_='pydantic')
        self.import_helper.add(import_=set(['Query', 'Body']), from_='fastapi')
        self.import_helper.add(import_=set(['*']), from_='sqlalchemy')
        self.import_helper.add(import_=set(['*']), from_=f'sqlalchemy.dialects.{db_type}')
        self.import_helper.add(import_=set(['value_of_list_to_str', 'ExcludeUnsetBaseModel', 'filter_none']), from_=f'fastapi_quick_crud_template.common.utils')
        self.import_helper.add(import_=set(['Base']), from_=f'fastapi_quick_crud_template.common.db')
        self.import_helper.add(import_=set(['ItemComparisonOperators', 'PGSQLMatchingPatternInString', 'ExtraFieldTypePrefix', 'RangeToComparisonOperators', 'MatchingPatternInStringBase', 'RangeFromComparisonOperators']), from_=f'fastapi_quick_crud_template.common.typing')
        self.import_helper.add(import_='uuid')

    def gen(self):
        return model_template_gen.add_model(self.file_name, self.import_helper.to_code() + '\n\n' + self.model_code + '\n\n' + self.code)

    def gen_model(self, model):
        if isinstance(model, Table):
            raise TypeError('not support table yet')
        model_code = inspect.getsource(model)
        self.model_code += '\n\n\n' + model_code

    def build_base_model(self, *, class_name, fields, description=None, orm_mode=True, value_of_list_to_str_columns=None, filter_none=None):
        TEMPLATE_FILE_PATH: ClassVar[str] = 'pydantic/BaseModel.jinja2'
        template_file_path = Path(TEMPLATE_FILE_PATH)
        TEMPLATE_DIR: Path = Path(__file__).parents[0] / 'template'
        templateLoader = jinja2.FileSystemLoader(str(TEMPLATE_DIR / template_file_path.parent))
        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_FILE = 'BaseModel.jinja2'
        template = templateEnv.get_template(TEMPLATE_FILE)
        code = template.render({'class_name': class_name, 'fields': fields, 'description': description, 'orm_mode': orm_mode, 'value_of_list_to_str_columns': value_of_list_to_str_columns, 'filter_none': filter_none})
        self.table_list[class_name] = code
        self.code += '\n\n\n' + code

    def build_base_model_root(self, *, class_name, field, description=None, base_model='BaseModel', value_of_list_to_str_columns=None, filter_none=None):
        if class_name in self.table_list:
            return self.table_list[class_name]
        TEMPLATE_FILE_PATH: ClassVar[str] = 'pydantic/BaseModel.jinja2'
        template_file_path = Path(TEMPLATE_FILE_PATH)
        TEMPLATE_DIR: Path = Path(__file__).parents[0] / 'template'
        templateLoader = jinja2.FileSystemLoader(str(TEMPLATE_DIR / template_file_path.parent))
        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_FILE = 'BaseModel_root.jinja2'
        template = templateEnv.get_template(TEMPLATE_FILE)
        code = template.render({'class_name': class_name, 'field': field, 'description': description, 'base_model': base_model, 'value_of_list_to_str_columns': value_of_list_to_str_columns, 'filter_none': filter_none})
        self.table_list[class_name] = code
        self.code += '\n\n\n' + code

    def build_dataclass(self, *, class_name, fields, description=None, value_of_list_to_str_columns=None, filter_none=None):
        if class_name in self.table_list:
            return self.table_list[class_name]
        TEMPLATE_FILE_PATH: ClassVar[str] = 'pydantic/BaseModel.jinja2'
        template_file_path = Path(TEMPLATE_FILE_PATH)
        TEMPLATE_DIR: Path = Path(__file__).parents[0] / 'template'
        templateLoader = jinja2.FileSystemLoader(str(TEMPLATE_DIR / template_file_path.parent))
        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_FILE = 'dataclass.jinja2'
        template = templateEnv.get_template(TEMPLATE_FILE)
        code = template.render({'class_name': class_name, 'fields': fields, 'description': description, 'value_of_list_to_str_columns': value_of_list_to_str_columns, 'filter_none': filter_none})
        self.code += '\n\n\n' + code

    def build_constant(self, *, constants):
        TEMPLATE_FILE_PATH: ClassVar[str] = ''
        template_file_path = Path(TEMPLATE_FILE_PATH)
        TEMPLATE_DIR: Path = Path(__file__).parents[0] / 'template'
        templateLoader = jinja2.FileSystemLoader(str(TEMPLATE_DIR / template_file_path.parent))
        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_FILE = 'Constant.jinja2'
        template = templateEnv.get_template(TEMPLATE_FILE)
        code = template.render({'constants': constants})
        self.code += '\n\n\n' + code