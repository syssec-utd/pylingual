from __future__ import absolute_import, division, print_function
__metaclass__ = type
import pytest
from ansible_collections.community.postgresql.plugins.modules.postgresql_set import pretty_to_bytes

@pytest.mark.parametrize('input_,expected', [('', ''), ('test', 'test'), ('0.1', 0.1), ('1024', 1024), ('1024B', 1024), ('1kB', 1024), ('100kB', 102400), ('1MB', 1048576), ('100MB', 104857600), ('1GB', 1073741824), ('10GB', 10737418240)])
def test_pretty_to_bytes(input_, expected):
    assert pretty_to_bytes(input_) == expected