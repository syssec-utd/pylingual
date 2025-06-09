import pytest
from petisco import LogMessage

@pytest.mark.unit
def test_should_create_a_log_message_and_convert_to_dict(given_any_info_id):
    log_message = LogMessage(layer='use_case', operation='test', info_id=given_any_info_id, data={'message': 'ok'})
    dict_message = log_message.to_dict()
    assert dict_message == {'data': {'message': 'ok'}, 'meta': {'layer': 'use_case', 'operation': 'test', 'info_id': given_any_info_id.to_dict()}}

@pytest.mark.unit
def test_should_create_a_log_message_and_convert_to_dict_without_info_id():
    log_message = LogMessage(layer='use_case', operation='test', data={'message': 'ok'})
    dict_message = log_message.to_dict()
    assert dict_message == {'data': {'message': 'ok'}, 'meta': {'layer': 'use_case', 'operation': 'test'}}

@pytest.mark.unit
def test_should_create_a_log_message_and_convert_to_dict_and_add_meta_level():
    log_message = LogMessage(layer='use_case', operation='test', data={'message': 'ok'})
    dict_message = log_message.to_dict()
    dict_message['meta']['level'] = 'info'
    assert dict_message == {'data': {'message': 'ok'}, 'meta': {'level': 'info', 'layer': 'use_case', 'operation': 'test'}}

@pytest.mark.unit
def test_should_create_a_log_message_without_layer():
    log_message = LogMessage(operation='test', data={'message': 'ok'})
    dict_message = log_message.to_dict()
    dict_message['meta']['level'] = 'info'
    assert dict_message == {'data': {'message': 'ok'}, 'meta': {'level': 'info', 'operation': 'test'}}

@pytest.mark.unit
def test_should_create_a_log_message_without_operation():
    log_message = LogMessage(layer='use_case', data={'message': 'ok'})
    dict_message = log_message.to_dict()
    dict_message['meta']['level'] = 'info'
    assert dict_message == {'data': {'message': 'ok'}, 'meta': {'level': 'info', 'layer': 'use_case'}}