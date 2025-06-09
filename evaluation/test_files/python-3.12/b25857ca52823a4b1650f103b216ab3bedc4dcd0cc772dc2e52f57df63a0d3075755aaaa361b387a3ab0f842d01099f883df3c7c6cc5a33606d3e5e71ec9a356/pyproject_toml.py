import dataclasses
import datetime
import logging
from pathlib import Path
from typing import Optional
import tomlkit
from bx_py_utils.path import assert_is_dir, assert_is_file
from tomlkit import TOMLDocument
from tomlkit.items import Table
from manageprojects.constants import APPLIED_MIGRATIONS, COOKIECUTTER_CONTEXT, COOKIECUTTER_DIRECTORY, COOKIECUTTER_TEMPLATE, INITIAL_DATE, INITIAL_REVISION
from manageprojects.data_classes import ManageProjectsMeta
from manageprojects.exceptions import NoPyProjectTomlFound
from manageprojects.utilities.log_utils import log_func_call
logger = logging.getLogger(__name__)

@dataclasses.dataclass
class TomlDocument:
    file_path: Path
    doc: TOMLDocument

def get_toml_document(path: Path) -> TomlDocument:
    """
    Read the file path and returns the TOMLDocument.
    Just use unwrap() if a normal dict is needed, e.g.:

        doc: TOMLDocument = get_toml_document(path)
        toml: dict = doc.unwrap()
    """
    assert_is_file(path)
    doc: TOMLDocument = tomlkit.parse(path.read_text(encoding='UTF-8'))
    return TomlDocument(file_path=path, doc=doc)

def find_pyproject_toml(file_path: Path) -> Optional[Path]:
    """
    Go back down the directory tree to find the "pyproject.toml" file.
    """
    if file_path.is_file():
        return find_pyproject_toml(file_path.parent)
    pyproject_toml = file_path / 'pyproject.toml'
    if pyproject_toml.is_file():
        return pyproject_toml
    if (parent_path := file_path.parent):
        if parent_path != file_path:
            return find_pyproject_toml(parent_path)
    return None

def get_pyproject_toml(*, file_path: Optional[Path]=None) -> TomlDocument:
    """
    Find the "pyproject.toml" and return it.
    """
    if not file_path:
        file_path = Path.cwd()
    pyproject_toml_path = find_pyproject_toml(file_path=file_path)
    if not pyproject_toml_path:
        raise NoPyProjectTomlFound(f'Can not find "pyproject.toml" in {file_path}')
    assert_is_file(pyproject_toml_path)
    toml_document: TomlDocument = get_toml_document(pyproject_toml_path)
    return toml_document

class PyProjectToml:
    """
    Helper for manageprojects meta information in 'pyproject.toml'
    """

    def __init__(self, project_path: Path):
        assert_is_dir(project_path)
        self.path = project_path / 'pyproject.toml'
        if self.path.exists():
            logger.debug('Read existing pyproject.toml')
            self.doc: TOMLDocument = tomlkit.parse(self.path.read_text(encoding='UTF-8'))
        else:
            logger.debug('Create new pyproject.toml')
            self.doc: TOMLDocument = tomlkit.document()
            self.doc.add(tomlkit.comment('Created by manageprojects'))
        self.mp_table: Table = self.doc.get('manageprojects')
        if not self.mp_table:
            if self.path.exists():
                self.doc.add(tomlkit.ws('\n\n'))
            self.mp_table = tomlkit.table()
            self.mp_table.comment('https://github.com/jedie/manageprojects')
            self.doc.append('manageprojects', self.mp_table)

    def init(self, revision, dt: datetime.datetime, template: str, directory: Optional[str]) -> None:
        assert INITIAL_REVISION not in self.mp_table
        assert INITIAL_DATE not in self.mp_table
        assert COOKIECUTTER_TEMPLATE not in self.mp_table
        self.mp_table.add(INITIAL_REVISION, revision)
        self.mp_table.add(INITIAL_DATE, dt)
        self.mp_table.add(COOKIECUTTER_TEMPLATE, template)
        if directory:
            self.mp_table.add(COOKIECUTTER_DIRECTORY, directory)

    def create_or_update_cookiecutter_context(self, context: dict) -> None:
        context['cookiecutter'] = {k: v for k, v in context['cookiecutter'].items() if k != '_output_dir'}
        self.mp_table[COOKIECUTTER_CONTEXT] = tomlkit.item(context)

    def add_applied_migrations(self, git_hash: str, dt: datetime.datetime) -> None:
        if not (applied_migrations := self.mp_table.get(APPLIED_MIGRATIONS)):
            applied_migrations = tomlkit.array()
            applied_migrations.multiline(multiline=True)
            self.mp_table.add(APPLIED_MIGRATIONS, applied_migrations)
        applied_migrations.add_line(git_hash, comment=dt.isoformat())

    def dumps(self) -> str:
        return self.doc.as_string()

    def save(self) -> None:
        content = self.dumps()
        self.path.write_text(content, encoding='UTF-8')

    def get_mp_meta(self) -> ManageProjectsMeta:
        data = self.mp_table.unwrap()
        result: ManageProjectsMeta = log_func_call(logger=logger, func=ManageProjectsMeta, initial_revision=data.get(INITIAL_REVISION), initial_date=data.get(INITIAL_DATE), applied_migrations=data.get(APPLIED_MIGRATIONS, []), cookiecutter_template=data.get(COOKIECUTTER_TEMPLATE), cookiecutter_directory=data.get(COOKIECUTTER_DIRECTORY), cookiecutter_context=data.get(COOKIECUTTER_CONTEXT))
        return result