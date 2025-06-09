import os
import pytest
from frictionless import Resource, FrictionlessException, helpers
from frictionless.plugins.json import JsonDialect
IS_UNIX = not helpers.is_platform('windows')
BASEURL = 'https://raw.githubusercontent.com/frictionlessdata/frictionless-py/master/%s'

def test_resource_dialect():
    dialect = {'delimiter': '|', 'quoteChar': '#', 'escapeChar': '-', 'doubleQuote': False, 'skipInitialSpace': False}
    descriptor = {'name': 'name', 'profile': 'tabular-data-resource', 'path': 'dialect.csv', 'schema': 'resource-schema.json', 'dialect': dialect}
    resource = Resource(descriptor, basepath='data')
    assert resource.dialect == dialect
    assert resource.read_rows() == [{'id': 1, 'name': 'english'}, {'id': 2, 'name': ' |##'}]

def test_resource_dialect_from_path():
    resource = Resource('data/resource-with-dereferencing.json')
    assert resource == {'name': 'name', 'path': 'table.csv', 'dialect': 'dialect.json', 'schema': 'schema.json'}
    assert resource.dialect == {'delimiter': ';'}

@pytest.mark.vcr
def test_resource_dialect_from_path_remote():
    resource = Resource(BASEURL % 'data/resource-with-dereferencing.json')
    assert resource == {'name': 'name', 'path': 'table.csv', 'dialect': 'dialect.json', 'schema': 'schema.json'}
    assert resource.dialect == {'delimiter': ';'}

def test_resource_dialect_from_path_error_path_not_safe():
    dialect = os.path.abspath('data/dialect.json')
    with pytest.raises(FrictionlessException) as excinfo:
        Resource({'name': 'name', 'path': 'path', 'dialect': dialect})
    error = excinfo.value.error
    assert error.code == 'resource-error'
    assert error.note.count('dialect.json')

def test_resource_dialect_csv_default():
    with Resource('data/table.csv') as resource:
        assert resource.header == ['id', 'name']
        assert resource.dialect.delimiter == ','
        assert resource.dialect.line_terminator == '\r\n'
        assert resource.dialect.double_quote is True
        assert resource.dialect.quote_char == '"'
        assert resource.dialect.skip_initial_space is False
        assert resource.layout.header is True
        assert resource.layout.header_rows == [1]
        assert resource.dialect == {}
        assert resource.layout == {}
        assert resource.read_rows() == [{'id': 1, 'name': 'english'}, {'id': 2, 'name': '中国人'}]

def test_resource_dialect_csv_delimiter():
    with Resource('data/delimiter.csv') as resource:
        assert resource.header == ['id', 'name']
        assert resource.dialect == {'delimiter': ';'}
        assert resource.read_rows() == [{'id': 1, 'name': 'english'}, {'id': 2, 'name': '中国人'}]

def test_resource_dialect_json_property():
    source = b'{"root": [["header1", "header2"], ["value1", "value2"]]}'
    dialect = JsonDialect(property='root')
    with Resource(source, format='json', dialect=dialect) as resource:
        assert resource.header == ['header1', 'header2']
        assert resource.read_rows() == [{'header1': 'value1', 'header2': 'value2'}]

@pytest.mark.skip
def test_resource_dialect_bad_property():
    resource = Resource('data/table.csv', dialect={'bad': True})
    with pytest.raises(FrictionlessException) as excinfo:
        resource.open()
    error = excinfo.value.error
    assert error.code == 'dialect-error'
    assert error.note.count('bad')

def test_resource_dialect_header_false_official():
    descriptor = {'name': 'name', 'profile': 'tabular-data-resource', 'path': 'without-headers.csv', 'dialect': {'header': False}, 'schema': 'resource-schema.json'}
    resource = Resource(descriptor, basepath='data')
    assert resource.read_rows() == [{'id': 1, 'name': 'english'}, {'id': 2, 'name': '中国人'}, {'id': 3, 'name': 'german'}]