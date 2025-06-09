"""Service create tests."""

def test_default(app, service, identity_simple, input_data):
    """Create a record (normal path)."""
    item = service._create(service.record_cls, identity_simple, input_data)
    assert item.id
    assert item.data['metadata']

def test_create_but_report_missing_required_field(app, service, identity_simple):
    """Create a record without required fields."""
    input_data = {'metadata': {}}
    item = service._create(service.record_cls, identity_simple, input_data, raise_errors=False)
    item_dict = item.to_dict()
    assert item.id
    assert item_dict['metadata'] == {}
    errors = [{'field': 'metadata.title', 'messages': ['Missing data for required field.']}]
    assert errors == item_dict['errors']

def test_create_but_report_incorrect_field(app, service, identity_simple):
    input_data = {'metadata': {'title': 10}}
    item = service._create(service.record_cls, identity_simple, input_data, raise_errors=False)
    item_dict = item.to_dict()
    assert item.id
    assert item_dict['metadata'] == {}
    errors = [{'field': 'metadata.title', 'messages': ['Not a valid string.']}]
    assert errors == item_dict['errors']