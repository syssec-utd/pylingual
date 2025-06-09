import os
import pytest
from z3c.dependencychecker.dotted_name import DottedName
from z3c.dependencychecker.package import Package
EMPTY_FILE = ''
IGNORE_OTHER_KEYS = '[servers]\none = "1.2.3.4"\n'
ONLY_TOOL_TABLE = '[tool]\ntwo = "5.6.7.8"\n'
EMPTY_DEPENDENCY_TABLE_NESTED = '[tool]\n    [dependencycheker]\n'
EMPTY_DEPENDENCY_TABLE_MERGED = '[tool.dependencychecker]'
ONE_MAPPING = '[tool.dependencychecker]\nZope2 = ["Products.Five", ]\n'
MORE_MAPPINGS = '[tool.dependencychecker]\nZope2 = ["Products.Five", ]\nZope4 = ["Products.Counter", "Products.Max" ]\n'
SUBTABLES = '[tool.dependencychecker]\nZope2 = ["Products.Five", ]\n[tool.dependencychecker.options]\n'
IGNORE_PACKAGES_NO_LIST = "[tool.dependencychecker]\nignore-packages = 'oops'\n"
IGNORE_PACKAGES = "[tool.dependencychecker]\nignore-packages = ['django-toolbar', 'plone.reload']\n"
ZOPE_MAPPING = "[tool.dependencychecker]\nZope = ['django-toolbar', 'plone.reload']\n"

def _write_user_config(path, content):
    file_path = os.sep.join([path, 'pyproject.toml'])
    with open(file_path, 'w') as config_file:
        config_file.write(content)

def _update_requires_txt(path, package_name, packages):
    file_path = os.sep.join([path, f'{package_name}.egg-info', 'requires.txt'])
    with open(file_path, 'w') as config_file:
        for package in packages:
            config_file.write(f'{package}\n')

def test_no_file(minimal_structure):
    path, package_name = minimal_structure
    package = Package(path)
    package.set_user_mappings()
    assert package.imports.user_mappings == {}

@pytest.mark.parametrize('config', (EMPTY_FILE, IGNORE_OTHER_KEYS, ONLY_TOOL_TABLE, EMPTY_DEPENDENCY_TABLE_NESTED, EMPTY_DEPENDENCY_TABLE_MERGED))
def test_valid_configuration(minimal_structure, config):
    path, package_name = minimal_structure
    _write_user_config(path, config)
    package = Package(path)
    package.set_user_mappings()
    assert package.imports.user_mappings == {}

def test_ignore_user_mappings(minimal_structure):
    path, package_name = minimal_structure
    _write_user_config(path, ONE_MAPPING)
    package = Package(path)
    package.inspect()
    assert len(package.imports.user_mappings) == 0

def test_one_user_mapping(minimal_structure):
    path, package_name = minimal_structure
    _write_user_config(path, ONE_MAPPING)
    _update_requires_txt(path, package_name, ['Zope2'])
    package = Package(path)
    package.inspect()
    five_dotted_name = DottedName('Products.Five')
    zope_dotted_name = DottedName('Zope2')
    assert len(package.imports.user_mappings) == 1
    assert zope_dotted_name in package.imports.user_mappings
    mappings = package.imports.user_mappings[zope_dotted_name]
    assert len(mappings) == 1
    assert {five_dotted_name} == mappings

def test_filter_out_mappings_on_test(minimal_structure):
    path, package_name = minimal_structure
    _write_user_config(path, ONE_MAPPING)
    _update_requires_txt(path, package_name, ['plone.reload', '[test]', 'Zope2'])
    package = Package(path)
    package.inspect()
    five_dotted_name = DottedName('Products.Five')
    plone_reload_dotted_name = DottedName('plone.reload')
    zope_dotted_name = DottedName('Zope2')
    assert len(package.imports.user_mappings) == 1
    assert zope_dotted_name in package.imports.user_mappings
    assert package.imports._filter_out_mappings_on_test(plone_reload_dotted_name)
    assert package.imports._filter_out_mappings_on_test(five_dotted_name)
    assert package.imports._filter_out_mappings_on_test(zope_dotted_name)

def test_more_user_mappings(minimal_structure):
    path, package_name = minimal_structure
    _write_user_config(path, MORE_MAPPINGS)
    _update_requires_txt(path, package_name, ['Zope2', 'Zope4'])
    package = Package(path)
    package.inspect()
    zope2_dotted_name = DottedName('Zope2')
    zope4_dotted_name = DottedName('Zope4')
    assert len(package.imports.user_mappings) == 2
    assert zope2_dotted_name in package.imports.user_mappings
    assert zope4_dotted_name in package.imports.user_mappings
    assert len(package.imports.user_mappings[zope4_dotted_name]) == 2

def test_subtables(minimal_structure):
    path, package_name = minimal_structure
    _write_user_config(path, SUBTABLES)
    _update_requires_txt(path, package_name, ['Zope2'])
    package = Package(path)
    package.inspect()
    zope2_dotted_name = DottedName('Zope2')
    assert len(package.imports.user_mappings) == 1
    assert zope2_dotted_name in package.imports.user_mappings

def test_ignore_packages_no_list(minimal_structure):
    path, package_name = minimal_structure
    _write_user_config(path, IGNORE_PACKAGES_NO_LIST)
    package = Package(path)
    package.inspect()
    assert len(package.imports.user_mappings) == 0

def test_ignore_packages(minimal_structure):
    path, package_name = minimal_structure
    _write_user_config(path, IGNORE_PACKAGES)
    _update_requires_txt(path, package_name, ['Zope2', 'plone.reload', 'django-toolbar'])
    package = Package(path)
    package.inspect()
    django_toolbar = DottedName('django-toolbar')
    plone_reload = DottedName('plone.reload')
    ignored_packages = package.imports.ignored_packages
    assert len(package.imports.user_mappings) == 0
    assert len(ignored_packages) == 2
    assert django_toolbar in ignored_packages
    assert plone_reload in ignored_packages

def test_no_ignore_zope_user_mapping(minimal_structure):
    path, package_name = minimal_structure
    _write_user_config(path, ZOPE_MAPPING)
    package = Package(path)
    package.inspect()
    assert len(package.imports.user_mappings) == 1