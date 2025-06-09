import unittest
from mlogpp.scope import *

class ScopesTestCase(unittest.TestCase):

    def test_variables_functions(self):
        Scopes.push('test_scope')
        Scopes.add(VariableValue(Type.NUM, 'var_a'))
        Scopes.add(VariableValue(Type.NUM, 'var_b'))
        Scopes.add(Function('fun_a', [], Type.NUM))
        self.assertTrue(isinstance(Scopes.get('var_a'), VariableValue))
        self.assertTrue(isinstance(Scopes.get('var_b'), VariableValue))
        self.assertTrue(isinstance(Scopes.get('@counter'), VariableValue))
        self.assertTrue(isinstance(Scopes.get('fun_a'), Function))
        Scopes.pop()
        self.assertFalse(isinstance(Scopes.get('var_a'), VariableValue))
        self.assertFalse(isinstance(Scopes.get('var_b'), VariableValue))
        self.assertTrue(isinstance(Scopes.get('@counter'), VariableValue))
        self.assertFalse(isinstance(Scopes.get('fun_a'), Function))

    def test_reset(self):
        Scopes.add(VariableValue(Type.STR, 'test'))
        Scopes.reset()
        self.assertEqual(Scopes.get('test'), None)
if __name__ == '__main__':
    unittest.main()