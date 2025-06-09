from __future__ import absolute_import, division, print_function
__metaclass__ = type
import os
import json
import pytest
import sys
if sys.version_info < (2, 7):
    pytestmark = pytest.mark.skip('F5 Ansible modules require Python >= 2.7')
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.f5networks.f5_modules.plugins.modules.bigip_firewall_rule_list import ModuleParameters, ModuleManager, ArgumentSpec
from ansible_collections.f5networks.f5_modules.tests.unit.compat import unittest
from ansible_collections.f5networks.f5_modules.tests.unit.compat.mock import Mock, patch
from ansible_collections.f5networks.f5_modules.tests.unit.modules.utils import set_module_args
fixture_path = os.path.join(os.path.dirname(__file__), 'fixtures')
fixture_data = {}

def load_fixture(name):
    path = os.path.join(fixture_path, name)
    if path in fixture_data:
        return fixture_data[path]
    with open(path) as f:
        data = f.read()
    try:
        data = json.loads(data)
    except Exception:
        pass
    fixture_data[path] = data
    return data

class TestParameters(unittest.TestCase):

    def test_module_parameters(self):
        args = dict(name='foo', description='my description', rules=['rule1', 'rule2', 'rule3'])
        p = ModuleParameters(params=args)
        assert p.name == 'foo'
        assert p.description == 'my description'
        assert p.rules == ['rule1', 'rule2', 'rule3']

class TestManager(unittest.TestCase):

    def setUp(self):
        self.spec = ArgumentSpec()
        self.p2 = patch('ansible_collections.f5networks.f5_modules.plugins.modules.bigip_firewall_rule_list.tmos_version')
        self.p3 = patch('ansible_collections.f5networks.f5_modules.plugins.modules.bigip_firewall_rule_list.send_teem')
        self.m2 = self.p2.start()
        self.m2.return_value = '14.1.0'
        self.m3 = self.p3.start()
        self.m3.return_value = True

    def tearDown(self):
        self.p2.stop()
        self.p3.stop()

    def test_create(self, *args):
        set_module_args(dict(name='foo', description='this is a description', rules=['rule1', 'rule2', 'rule3'], provider=dict(server='localhost', password='password', user='admin')))
        module = AnsibleModule(argument_spec=self.spec.argument_spec, supports_check_mode=self.spec.supports_check_mode)
        mm = ModuleManager(module=module)
        mm.exists = Mock(side_effect=[False, True])
        mm.create_on_device = Mock(return_value=True)
        results = mm.exec_module()
        assert results['changed'] is True
        assert 'rules' in results
        assert len(results['rules']) == 3
        assert results['description'] == 'this is a description'