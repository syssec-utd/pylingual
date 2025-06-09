import doctest
import pytest
from insights.core.exceptions import ParseException, SkipComponent
from insights.parsers import lssap
from insights.tests import context_wrap
from insights.util import keys_in
Lssap_BAD = '\n - lssap version 1.0 -\n ==========================================\n   SID   Nr   Instance    SAPLOCALHOST                        Version                 DIR_EXECUTABLE\n   HA2|  16|       D16|         lu0417\n==========================================\n'.strip()
Lssap_BAD1 = '\n   HA2|  16|       D16|         lu0417\n'.strip()
Lssap_BAD2 = ''
Lssap_nw_TEST = '\n - lssap version 1.0 -\n==========================================\n  SID   Nr   Instance    SAPLOCALHOST                        Version                 DIR_EXECUTABLE\n  HA2|  16|       D16|         lu0417|749, patch 10, changelist 1698137|          /usr/sap/HA2/D16/exe\n  HA2|  22|       D22|         lu0417|749, patch 10, changelist 1698137|          /usr/sap/HA2/D22/exe\n  HA2|  50|       D50|         lu0417|749, patch 10, changelist 1698137|          /usr/sap/HA2/D50/exe\n  HA2|  51|       D51|         lu0417|749, patch 10, changelist 1698137|          /usr/sap/HA2/D51/exe\n==========================================\n'.strip()
Lssap_hana_TEST = '\n - lssap version 1.0 -\n==========================================\n  SID   Nr   Instance    SAPLOCALHOST                        Version                 DIR_EXECUTABLE\n  HA2|  16|       HDB16|         lu0417|749, patch 10, changelist 1698137|          /usr/sap/HA2/HDB16/exe\n==========================================\n'.strip()
Lssap_ascs_TEST = '\n - lssap version 1.0 -\n==========================================\n  SID   Nr   Instance    SAPLOCALHOST                        Version                 DIR_EXECUTABLE\n  HA2|  16|       ASCS16|         lu0417|749, patch 10, changelist 1698137|          /usr/sap/HA2/ASCS16/exe\n==========================================\n'.strip()
Lssap_runAll_Test = '\n - lssap version 1.0 -\n==========================================\n  SID   Nr   Instance    SAPLOCALHOST                        Version                 DIR_EXECUTABLE\n  HA2|  16|       D16|         lu0417|749, patch 10, changelist 1698137|          /usr/sap/HA2/D16/exe\n  HA2|  22|       D22|         lu0417|749, patch 10, changelist 1698137|          /usr/sap/HA2/D22/exe\n  HA2|  16|     HDB16|         lu0417|749, patch 10, changelist 1698137|          /usr/sap/HA2/HDB16/exe\n  HA2|  16|    ASCS16|         lu0417|749, patch 10, changelist 1698137|          /usr/sap/HA2/ASCS16/exe\n  DA1|  97|    SMDA97|         l0116a|745, patch 100, changelist 1652052|         /usr/sap/DA1/SMDA97/exe\n  DAA|  98|    SMDA98|         l0116a|745, patch 100, changelist 1652052|         /usr/sap/DAA/SMDA98/exe\n  MHP|  00|     HDB00|         l0116a|749, patch 315, changelist 1787247|         /usr/sap/MHP/HDB00/exe\n  MEP|  02|    ASCS02|         l0116a|745, patch 600, changelist 1791210|         /usr/sap/MEP/ASCS02/exe\n  MEP|  01| DVEBMGS01|         l0116a|745, patch 600, changelist 1791210|         /usr/sap/MEP/DVEBMGS01/exe\n==========================================\n'.strip()
Lssap_BAD_1 = '\n/usr/sap/hostctrl/lssap: command or file not found\n'
Lssap_BAD_2 = '\nHA2 | N16|  D16\n'.strip()
Lssap_BAD_3 = '\nHA2 | N16 | D16\nHB2 | foo | bar\n'.strip()
Lssap_extra_lines = '\n*** ERROR => CTrcOpen: fopen dev_lssap\n\n---------------------------------------------------\ntrc file: "dev_lssap", trc level: 1, release: "721"\n---------------------------------------------------\n - lssap version 1.0 -\n==========================================\n  SID   Nr   Instance   SAPLOCALHOST                        Version                 DIR_EXECUTABLE\n D02|  50|       D50|     sapcbapp09|722, patch 201, changelist 1718183|         /usr/sap/D02/D50/exe\n==========================================\n'.strip()

def test_doc_examples():
    env = {'lssap': lssap.Lssap(context_wrap(Lssap_nw_TEST))}
    (failed, total) = doctest.testmod(lssap, globs=env)
    assert failed == 0

def test_lssap_netweaver():
    sap = lssap.Lssap(context_wrap(Lssap_nw_TEST))
    data = sap.data
    assert keys_in(['SID', 'Nr', 'Instance', 'SAPLOCALHOST', 'Version', 'DIR_EXECUTABLE'], data[0])
    assert data[0] == {'SID': 'HA2', 'Nr': '16', 'Instance': 'D16', 'SAPLOCALHOST': 'lu0417', 'Version': '749, patch 10, changelist 1698137', 'DIR_EXECUTABLE': '/usr/sap/HA2/D16/exe'}
    assert data[2]['Instance'] == 'D50'
    assert data[-1]['SAPLOCALHOST'] == 'lu0417'
    assert sap.is_netweaver() is True
    assert sap.is_hana() is False
    assert sap.is_ascs() is False

def test_lssap_hana():
    sap = lssap.Lssap(context_wrap(Lssap_hana_TEST))
    data = sap.data
    assert data[0] == {'SID': 'HA2', 'Nr': '16', 'Instance': 'HDB16', 'SAPLOCALHOST': 'lu0417', 'Version': '749, patch 10, changelist 1698137', 'DIR_EXECUTABLE': '/usr/sap/HA2/HDB16/exe'}
    assert data[0]['SAPLOCALHOST'] == 'lu0417'
    assert sap.is_hana() is True
    assert sap.is_netweaver() is False
    assert sap.is_ascs() is False

def test_lssap_ascs():
    sap = lssap.Lssap(context_wrap(Lssap_ascs_TEST))
    assert sap.is_hana() is False
    assert sap.is_netweaver() is False
    assert sap.is_ascs() is True

def test_all():
    sap = lssap.Lssap(context_wrap(Lssap_runAll_Test))
    assert sap.sid == ['DA1', 'DAA', 'HA2', 'MEP', 'MHP']
    assert sap.instances == ['D16', 'D22', 'HDB16', 'ASCS16', 'SMDA97', 'SMDA98', 'HDB00', 'ASCS02', 'DVEBMGS01']
    assert sap.data[1] == {'SID': 'HA2', 'Nr': '22', 'Instance': 'D22', 'SAPLOCALHOST': 'lu0417', 'Version': '749, patch 10, changelist 1698137', 'DIR_EXECUTABLE': '/usr/sap/HA2/D22/exe'}
    assert sap.is_netweaver() is True
    assert sap.is_hana() is True
    assert sap.is_ascs() is True
    assert 'SMDA' in sap.instance_types
    assert 'DVEBMGS01' in sap.instances
    assert sap.version('D16') == '749, patch 10, changelist 1698137'
    assert sap.version('D06') is None

def test_fail():
    with pytest.raises(ParseException) as excinfo:
        lssap.Lssap(context_wrap(Lssap_BAD_1))
    assert "Lssap: Unable to parse 1 line(s) of content: (['/usr/sap/hostctrl/lssap: command or file not found'])" in str(excinfo)
    with pytest.raises(ParseException) as excinfo:
        lssap.Lssap(context_wrap(Lssap_BAD_2))
    assert "Lssap: Unable to parse 1 line(s) of content: (['HA2 | N16|  D16'])" in str(excinfo)
    with pytest.raises(ParseException) as excinfo:
        lssap.Lssap(context_wrap(Lssap_BAD_3))
    assert "Lssap: Unable to parse 2 line(s) of content: (['HA2 | N16 | D16', 'HB2 | foo | bar'])" in str(excinfo)
    with pytest.raises(ParseException) as excinfo:
        lssap.Lssap(context_wrap(Lssap_BAD1))
    assert "Lssap: Unable to parse 1 line(s) of content: (['HA2|  16|       D16|         lu0417'])" in str(excinfo)
    with pytest.raises(SkipComponent) as excinfo:
        lssap.Lssap(context_wrap(Lssap_BAD2))
    with pytest.raises(ParseException) as excinfo:
        lssap.Lssap(context_wrap('test'))
    assert "Lssap: Unable to parse 1 line(s) of content: (['test'])" in str(excinfo)

def test_valid_extra_lines():
    sap = lssap.Lssap(context_wrap(Lssap_extra_lines))
    assert sap is not None