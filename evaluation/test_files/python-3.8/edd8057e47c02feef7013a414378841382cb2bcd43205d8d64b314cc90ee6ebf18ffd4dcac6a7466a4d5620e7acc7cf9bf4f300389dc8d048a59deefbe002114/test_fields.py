from ironic.common import exception
from ironic.objects import fields
from ironic.tests import base as test_base

class TestMacAddressField(test_base.TestCase):

    def setUp(self):
        super(TestMacAddressField, self).setUp()
        self.field = fields.MACAddressField()

    def test_coerce(self):
        values = {'aa:bb:cc:dd:ee:ff': 'aa:bb:cc:dd:ee:ff', 'AA:BB:CC:DD:EE:FF': 'aa:bb:cc:dd:ee:ff', 'AA:bb:cc:11:22:33': 'aa:bb:cc:11:22:33'}
        for k in values:
            self.assertEqual(values[k], self.field.coerce('obj', 'attr', k))

    def test_coerce_bad_values(self):
        for v in ('invalid-mac', 'aa-bb-cc-dd-ee-ff'):
            self.assertRaises(exception.InvalidMAC, self.field.coerce, 'obj', 'attr', v)

class TestFlexibleDictField(test_base.TestCase):

    def setUp(self):
        super(TestFlexibleDictField, self).setUp()
        self.field = fields.FlexibleDictField()

    def test_coerce(self):
        d = {'foo_1': 'bar', 'foo_2': 2, 'foo_3': [], 'foo_4': {}}
        self.assertEqual(d, self.field.coerce('obj', 'attr', d))
        self.assertEqual({'foo': 'bar'}, self.field.coerce('obj', 'attr', '{"foo": "bar"}'))

    def test_coerce_bad_values(self):
        self.assertRaises(TypeError, self.field.coerce, 'obj', 'attr', 123)
        self.assertRaises(TypeError, self.field.coerce, 'obj', 'attr', True)

    def test_coerce_nullable_translation(self):
        self.assertRaises(ValueError, self.field.coerce, 'obj', 'attr', None)
        self.field = fields.FlexibleDictField(nullable=True)
        self.assertEqual({}, self.field.coerce('obj', 'attr', None))

class TestStringFieldThatAcceptsCallable(test_base.TestCase):

    def setUp(self):
        super(TestStringFieldThatAcceptsCallable, self).setUp()

        def test_default_function():
            return 'default value'
        self.field = fields.StringFieldThatAcceptsCallable(default=test_default_function)

    def test_coerce_string(self):
        self.assertEqual('value', self.field.coerce('obj', 'attr', 'value'))

    def test_coerce_function(self):

        def test_function():
            return 'value'
        self.assertEqual('value', self.field.coerce('obj', 'attr', test_function))

    def test_coerce_invalid_type(self):
        self.assertRaises(ValueError, self.field.coerce, 'obj', 'attr', ('invalid', 'tuple'))

    def test_coerce_function_invalid_type(self):

        def test_function():
            return ('invalid', 'tuple')
        self.assertRaises(ValueError, self.field.coerce, 'obj', 'attr', test_function)

    def test_coerce_default_as_function(self):
        self.assertEqual('default value', self.field.coerce('obj', 'attr', None))

    def test__repr__includes_default_function_name_and_source_hash(self):
        expected = 'StringAcceptsCallable(default=<function test_default_function>,nullable=False)'
        self.assertEqual(expected, repr(self.field))

class TestNotificationLevelField(test_base.TestCase):

    def setUp(self):
        super(TestNotificationLevelField, self).setUp()
        self.field = fields.NotificationLevelField()

    def test_coerce_good_value(self):
        self.assertEqual(fields.NotificationLevel.WARNING, self.field.coerce('obj', 'attr', 'warning'))

    def test_coerce_bad_value(self):
        self.assertRaises(ValueError, self.field.coerce, 'obj', 'attr', 'not_a_priority')

class TestNotificationStatusField(test_base.TestCase):

    def setUp(self):
        super(TestNotificationStatusField, self).setUp()
        self.field = fields.NotificationStatusField()

    def test_coerce_good_value(self):
        self.assertEqual(fields.NotificationStatus.START, self.field.coerce('obj', 'attr', 'start'))

    def test_coerce_bad_value(self):
        self.assertRaises(ValueError, self.field.coerce, 'obj', 'attr', 'not_a_priority')