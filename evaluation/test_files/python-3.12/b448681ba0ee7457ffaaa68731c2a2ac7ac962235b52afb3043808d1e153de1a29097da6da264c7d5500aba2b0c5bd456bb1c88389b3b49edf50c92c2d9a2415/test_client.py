"""Client-side integration tests."""
from unittest.mock import Mock
import pytest
from httpyexpect.client import ExceptionMapping, ResponseTranslator
from httpyexpect.models import HttpExceptionBody

class ExceptionA(RuntimeError):
    """An Exception."""

class ExceptionB(RuntimeError):
    """Another Exception"""

class ExceptionC(RuntimeError):
    """Yet, another Exception"""

@pytest.mark.parametrize('status_code, body, expected_exception', [(400, HttpExceptionBody(exception_id='testA', description='test', data={'test': 'test'}), ExceptionA), (400, HttpExceptionBody(exception_id='testB', description='test', data={'test': 'test'}), ExceptionB), (500, HttpExceptionBody(exception_id='testC', description='test', data={'test': 'test'}), ExceptionC)])
def test_typical_client_usage(status_code: int, body: HttpExceptionBody, expected_exception: type[Exception]):
    """Test the typical way how the client may use the `ResponseTranslator` together
    with the `ExceptionMapping` classes."""
    spec = {400: {'testA': lambda exception_id, description, data: ExceptionA(), 'testB': lambda data: ExceptionB()}, 500: {'testC': lambda: ExceptionC()}}
    response = Mock()
    response.status_code = status_code
    response.json.return_value = body.dict()
    exception_map = ExceptionMapping(spec)
    translator = ResponseTranslator(response, exception_map=exception_map)
    obtained_exception = translator.get_error()
    assert isinstance(obtained_exception, expected_exception)
    with pytest.raises(expected_exception):
        translator.raise_for_error()