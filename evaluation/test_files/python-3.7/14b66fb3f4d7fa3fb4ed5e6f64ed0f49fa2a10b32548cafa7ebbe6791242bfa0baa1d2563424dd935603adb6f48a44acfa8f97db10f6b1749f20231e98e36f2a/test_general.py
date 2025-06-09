import json
import pytest
import pathlib
from frictionless import Package, Resource, Schema, Field, Detector, helpers
IS_UNIX = not helpers.is_platform('windows')

def test_validate_package():
    package = Package({'resources': [{'path': 'data/table.csv'}]})
    report = package.validate()
    assert report.valid

def test_validate_package_from_dict():
    with open('data/package/datapackage.json') as file:
        package = Package(json.load(file), basepath='data/package')
        report = package.validate()
        assert report.valid

def test_validate_package_from_dict_invalid():
    with open('data/invalid/datapackage.json') as file:
        package = Package(json.load(file), basepath='data/invalid')
        report = package.validate()
        assert report.flatten(['taskPosition', 'rowPosition', 'fieldPosition', 'code']) == [[1, 3, None, 'blank-row'], [1, 3, None, 'primary-key-error'], [2, 4, None, 'blank-row']]

def test_validate_package_from_path():
    package = Package('data/package/datapackage.json')
    report = package.validate()
    assert report.valid

def test_validate_package_from_path_invalid():
    package = Package('data/invalid/datapackage.json')
    report = package.validate()
    assert report.flatten(['taskPosition', 'rowPosition', 'fieldPosition', 'code']) == [[1, 3, None, 'blank-row'], [1, 3, None, 'primary-key-error'], [2, 4, None, 'blank-row']]

def test_validate_package_from_zip():
    package = Package('data/package.zip')
    report = package.validate()
    assert report.valid

def test_validate_package_from_zip_invalid():
    package = Package('data/package-invalid.zip')
    report = package.validate()
    assert report.flatten(['taskPosition', 'rowPosition', 'fieldPosition', 'code']) == [[1, 3, None, 'blank-row'], [1, 3, None, 'primary-key-error'], [2, 4, None, 'blank-row']]

def test_validate_package_with_non_tabular():
    package = Package({'resources': [{'path': 'data/table.csv'}, {'path': 'data/file.txt'}]})
    report = package.validate()
    assert report.valid

@pytest.mark.skip
def test_validate_package_invalid_descriptor_path():
    package = Package('bad/datapackage.json')
    report = package.validate()
    assert report['stats']['errors'] == 1
    error = report['errors'][0]
    assert error['code'] == 'package-error'
    assert error['note'].count('[Errno 2]') and error['note'].count('bad/datapackage.json')

def test_validate_package_invalid_package():
    package = Package({'resources': [{'path': 'data/table.csv', 'schema': 'bad'}]})
    report = package.validate()
    assert report['stats']['errors'] == 1
    error = report['errors'][0]
    assert error['code'] == 'schema-error'
    assert error['note'].count('[Errno 2]') and error['note'].count("'bad'")

def test_validate_package_invalid_package_original():
    package = Package({'resources': [{'path': 'data/table.csv'}]})
    report = package.validate(original=True)
    assert report.flatten(['code', 'note']) == [['resource-error', '"{\'path\': \'data/table.csv\', \'stats\': {}} is not valid under any of the given schemas" at "" in metadata and at "oneOf" in profile']]

def test_validate_package_invalid_table():
    package = Package({'resources': [{'path': 'data/invalid.csv'}]})
    report = package.validate()
    assert report.flatten(['rowPosition', 'fieldPosition', 'code']) == [[None, 3, 'blank-label'], [None, 4, 'duplicate-label'], [2, 3, 'missing-cell'], [2, 4, 'missing-cell'], [3, 3, 'missing-cell'], [3, 4, 'missing-cell'], [4, None, 'blank-row'], [5, 5, 'extra-cell']]

def test_validate_package_pathlib_source():
    package = Package(pathlib.Path('data/package/datapackage.json'))
    report = package.validate()
    assert report.valid

def test_validate_package_infer():
    package = Package('data/infer/datapackage.json')
    report = package.validate()
    assert report.valid

def test_validate_package_dialect_header_false():
    descriptor = {'resources': [{'name': 'name', 'data': [['John', '22'], ['Alex', '33'], ['Paul', '44']], 'schema': {'fields': [{'name': 'name'}, {'name': 'age', 'type': 'integer'}]}, 'layout': {'header': False}}]}
    package = Package(descriptor)
    report = package.validate()
    assert report.valid

def test_validate_package_with_schema_as_string():
    package = Package({'resources': [{'path': 'data/table.csv', 'schema': 'data/schema.json'}]})
    report = package.validate()
    assert report.valid

def test_validate_package_single_resource():
    package = Package('data/datapackage.json')
    report = package.validate(resource_name='number-two')
    assert report.valid

def test_validate_package_single_resource_wrong_resource_name():
    package = Package('data/datapackage.json')
    report = package.validate(resource_name='number-twoo')
    assert report.flatten(['code', 'message']) == [['package-error', 'The data package has an error: resource "number-twoo" does not exist']]

def test_validate_package_mixed_issue_170():
    package = Package('data/infer/datapackage.json')
    report = package.validate()
    assert report.valid

@pytest.mark.skip
def test_validate_package_invalid_json_issue_192():
    package = Package('data/invalid.json')
    report = package.validate()
    assert report.flatten(['code', 'note']) == [['package-error', 'cannot extract metadata "data/invalid.json" because "Expecting property name enclosed in double quotes: line 2 column 5 (char 6)"']]

def test_validate_package_composite_primary_key_unique_issue_215():
    source = {'resources': [{'name': 'name', 'data': [['id1', 'id2'], ['a', '1'], ['a', '2']], 'schema': {'fields': [{'name': 'id1'}, {'name': 'id2'}], 'primaryKey': ['id1', 'id2']}}]}
    package = Package(source)
    report = package.validate()
    assert report.valid

def test_validate_package_composite_primary_key_not_unique_issue_215():
    descriptor = {'resources': [{'name': 'name', 'data': [['id1', 'id2'], ['a', '1'], ['a', '1']], 'schema': {'fields': [{'name': 'id1'}, {'name': 'id2'}], 'primaryKey': ['id1', 'id2']}}]}
    package = Package(descriptor)
    report = package.validate(skip_errors=['duplicate-row'])
    assert report.flatten(['rowPosition', 'fieldPosition', 'code']) == [[3, None, 'primary-key-error']]

def test_validate_package_geopoint_required_constraint_issue_231():
    package = Package('data/geopoint/datapackage.json')
    report = package.validate()
    assert not report.valid

def test_validate_package_number_test_issue_232():
    package = Package('data/number/datapackage.json')
    report = package.validate()
    assert not report.valid

def test_validate_package_with_schema_issue_348():
    descriptor = {'resources': [{'name': 'people', 'data': [['id', 'name', 'surname'], ['p1', 'Tom', 'Hanks'], ['p2', 'Meryl', 'Streep']], 'schema': {'fields': [{'name': 'id', 'type': 'string'}, {'name': 'name', 'type': 'string'}, {'name': 'surname', 'type': 'string'}, {'name': 'dob', 'type': 'date'}]}}]}
    package = Package(descriptor)
    report = package.validate()
    assert report.flatten(['rowPosition', 'fieldPosition', 'code']) == [[None, 4, 'missing-label'], [2, 4, 'missing-cell'], [3, 4, 'missing-cell']]

@pytest.mark.ci
@pytest.mark.vcr
def test_validate_package_uppercase_format_issue_494():
    with pytest.warns(UserWarning):
        package = Package('data/issue-494.package.json')
        report = package.validate()
        assert report.valid
        assert report.stats['tasks'] == 1

@pytest.mark.skip
def test_validate_package_using_detector_schema_sync_issue_847():
    package = Package(resources=[Resource(data=[['f1'], ['v1'], ['v2'], ['v3']], schema=Schema(fields=[Field(name='f1'), Field(name='f2')]))])
    report = package.validate()
    for resource in package.resources:
        resource.detector = Detector(schema_sync=True)
    package = Package(package)
    assert report.valid

def test_validate_package_descriptor_type_package():
    package = Package(descriptor='data/package/datapackage.json')
    report = package.validate()
    assert report.valid

def test_validate_package_descriptor_type_package_invalid():
    package = Package(descriptor='data/invalid/datapackage.json')
    report = package.validate()
    assert report.flatten() == [[1, 3, None, 'blank-row'], [1, 3, None, 'primary-key-error'], [2, 4, None, 'blank-row']]

def test_validate_package_with_diacritic_symbol_issue_905():
    package = Package(descriptor='data/issue-905/datapackage.json')
    report = package.validate()
    assert report.stats['tasks'] == 3

def test_validate_package_with_resource_data_is_a_string_issue_977():
    package = Package(descriptor='data/issue-977.json')
    report = package.validate()
    assert report.flatten() == [[None, None, None, 'package-error']]

def test_validate_package_metadata_errors_with_missing_values_993():
    package = Package(descriptor='data/package-with-missingvalues-993.json')
    assert package.metadata_errors[0].code == 'package-error'
    assert package.metadata_errors[0].note == '"missingValues" should be set as "resource.schema.missingValues" (not "package.missingValues").'

def test_validate_package_metadata_errors_with_fields_993():
    package = Package(descriptor='data/package-with-fields-993.json')
    assert package.metadata_errors[0].code == 'package-error'
    assert package.metadata_errors[0].note == '"fields" should be set as "resource.schema.fields" (not "package.fields").'

def test_validate_package_errors_with_missing_values_993():
    package = Package(descriptor='data/package-with-missingvalues-993.json')
    report = package.validate()
    assert report.flatten(['code', 'message']) == [['package-error', 'The data package has an error: "missingValues" should be set as "resource.schema.missingValues" (not "package.missingValues").']]

def test_validate_package_errors_with_fields_993():
    package = Package(descriptor='data/package-with-fields-993.json')
    report = package.validate()
    assert report.flatten(['code', 'message']) == [['package-error', 'The data package has an error: "fields" should be set as "resource.schema.fields" (not "package.fields").']]