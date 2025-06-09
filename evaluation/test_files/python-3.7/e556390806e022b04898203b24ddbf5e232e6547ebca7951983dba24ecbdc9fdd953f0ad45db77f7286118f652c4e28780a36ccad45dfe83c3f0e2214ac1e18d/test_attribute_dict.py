from insights.core import AttributeDict
DICT = {'dmode': '0500', 'relatime': True, 'uid': '0', 'iocharset': 'utf8', 'gid': '0', 'mode': '0400', 'ro': True, 'nosuid': True, 'uhelper': 'udisks2', 'nodev': True}

def test_attribute_dict():
    d_obj = AttributeDict(DICT)
    assert d_obj['dmode'] == '0500'
    assert d_obj.get('relatime') is True
    assert d_obj.nosuid is True
    assert 'uid' in d_obj
    assert d_obj.get('mode', None) == '0400'
    assert d_obj.get('xmode', None) is None
    for (d, v) in d_obj.items():
        if d.startswith('nod'):
            assert v is True