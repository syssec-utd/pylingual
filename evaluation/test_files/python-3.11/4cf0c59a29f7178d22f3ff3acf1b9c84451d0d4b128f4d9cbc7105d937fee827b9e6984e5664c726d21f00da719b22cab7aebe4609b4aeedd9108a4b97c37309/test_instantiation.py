import unittest
from dslibrary import parse_verb_and_args, instantiate_class_and_args, DSLibrary
from dslibrary.transport.to_local import DSLibraryLocal
from dslibrary.utils.instantiation import import_named_object, valueize

class TestInstantiation(unittest.TestCase):

    def test_valueize(self):
        assert valueize('1') == 1
        assert valueize('1.5') == 1.5
        assert valueize('1x') == '1x'

    def test_parse_verb_and_args(self):
        verb, args, kwargs = parse_verb_and_args('A:v1:x=1:y=2:z=z')
        assert verb == 'A'
        assert args == ('v1',)
        assert kwargs == {'x': 1, 'y': 2, 'z': 'z'}

    def test_instantiate_class_and_args(self):
        dsl = instantiate_class_and_args('dslibrary.transport.to_local.DSLibraryLocal:ROOT', DSLibrary)
        assert isinstance(dsl, DSLibraryLocal)
        assert dsl._root == 'ROOT'

    def test_instantiate_class_and_args__wrong_type(self):
        self.assertRaises(ValueError, lambda: instantiate_class_and_args('pathlib.Path:abc', DSLibrary))

    def test_import_named_object(self):
        loads = import_named_object('json.loads')
        assert loads('{}') == {}