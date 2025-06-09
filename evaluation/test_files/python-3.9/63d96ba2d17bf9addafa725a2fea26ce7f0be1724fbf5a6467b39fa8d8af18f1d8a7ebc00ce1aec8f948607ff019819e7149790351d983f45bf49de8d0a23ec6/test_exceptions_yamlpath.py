import pytest
from yamlpath.exceptions import YAMLPathException

class Test_exceptions_YAMLPathException:

    def test_str_segmentless(self):
        with pytest.raises(YAMLPathException) as ex:
            raise YAMLPathException('Test message', 'test')
        assert str(ex.value) == "Test message, 'test'."

    def test_str_segmentfull(self):
        with pytest.raises(YAMLPathException) as ex:
            raise YAMLPathException('Test message', 'test', 'st')
        assert str(ex.value) == "Test message at 'st' in 'test'."