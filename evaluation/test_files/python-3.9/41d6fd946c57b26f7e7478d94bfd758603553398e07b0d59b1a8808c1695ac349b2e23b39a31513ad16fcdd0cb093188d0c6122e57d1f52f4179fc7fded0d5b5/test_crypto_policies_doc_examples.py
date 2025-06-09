from insights.tests import context_wrap
from insights.parsers import crypto_policies
from insights.parsers.crypto_policies import CryptoPoliciesOpensshserver, CryptoPoliciesConfig, CryptoPoliciesStateCurrent, CryptoPoliciesBind
import doctest
OPENSSHSERVER = "\nCRYPTO_POLICY='-oCiphers=aes256-gcm@openssh.com,3des-cbc -oMACs=umac-128-etm@openssh.com'\n".strip()
CONFIG = '\nLEGACY\n'.strip()
STATECURRENT = '\nLEGACY\n'.strip()
BIND = '\ndisable-algorithms "." {\nRSAMD5;\nDSA;\n};\ndisable-ds-digests "." {\nGOST;\n};\n'.strip()

def test_crypto_policies_doc():
    env = {'cp_os': CryptoPoliciesOpensshserver(context_wrap(OPENSSHSERVER)), 'cp_c': CryptoPoliciesConfig(context_wrap(CONFIG, path='/etc/crypto-policies/config')), 'cp_sc': CryptoPoliciesStateCurrent(context_wrap(STATECURRENT, path='/etc/crypto-policies/state/current')), 'cp_bind': CryptoPoliciesBind(context_wrap(BIND))}
    (failed, total) = doctest.testmod(crypto_policies, globs=env)
    assert failed == 0