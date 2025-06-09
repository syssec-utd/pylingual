from secrets import token_bytes
import pytest
import pyseto
from pyseto import DecryptError, EncryptError, Key, VerifyError
from pyseto.versions.v4 import V4Local, V4Public
from .utils import load_key

class TestV4Local:
    """
    Tests for v4.local.
    """

    @pytest.mark.parametrize('key, msg', [(b'', 'key must be specified.'), (token_bytes(65), 'key length must be up to 64 bytes.')])
    def test_v4_local_new_with_invalid_arg(self, key, msg):
        with pytest.raises(ValueError) as err:
            Key.new(4, 'local', key)
            pytest.fail('Key.new() should fail.')
        assert msg in str(err.value)

    def test_v4_local_decrypt_via_decode_with_wrong_key(self):
        k1 = Key.new(4, 'local', b'our-secret')
        k2 = Key.new(4, 'local', b'others-secret')
        token = pyseto.encode(k1, b'Hello world!')
        with pytest.raises(DecryptError) as err:
            pyseto.decode(k2, token)
            pytest.fail('pyseto.decode() should fail.')
        assert 'Failed to decrypt.' in str(err.value)

    def test_v4_local_encrypt_with_invalid_arg(self):
        k = Key.new(4, 'local', b'our-secret')
        with pytest.raises(EncryptError) as err:
            k.encrypt(None)
            pytest.fail('pyseto.encrypt() should fail.')
        assert 'Failed to encrypt.' in str(err.value)

    @pytest.mark.parametrize('nonce', [token_bytes(1), token_bytes(8), token_bytes(31), token_bytes(33), token_bytes(64)])
    def test_v4_local_encrypt_via_encode_with_wrong_nonce(self, nonce):
        k = Key.new(4, 'local', b'our-secret')
        with pytest.raises(ValueError) as err:
            pyseto.encode(k, b'Hello world!', nonce=nonce)
            pytest.fail('pyseto.encode() should fail.')
        assert 'nonce must be 32 bytes long.' in str(err.value)

    @pytest.mark.parametrize('paserk, msg', [('xx.local.AAAAAAAAAAAAAAAA', 'Invalid PASERK version: xx.'), ('k1.local.AAAAAAAAAAAAAAAA', 'Invalid PASERK version: k1.'), ('k4.local.xxx.AAAAAAAAAAAAAAAA', 'Invalid PASERK format.'), ('k4.public.xxx.AAAAAAAAAAAAAAAA', 'Invalid PASERK format.'), ('k4.xxx.AAAAAAAAAAAAAAAA', 'Invalid PASERK type: xxx.'), ('k4.public.AAAAAAAAAAAAAAAA', 'Invalid PASERK type: public.')])
    def test_v4_local_from_paserk_with_invalid_args(self, paserk, msg):
        with pytest.raises(ValueError) as err:
            V4Local.from_paserk(paserk)
            pytest.fail('Key.from_paserk should fail.')
        assert msg in str(err.value)

    def test_v4_local_to_peer_paserk_id(self):
        k = Key.new(4, 'local', b'our-secret')
        assert k.to_peer_paserk_id() == ''

class TestV4Public:
    """
    Tests for v4.public.
    """

    def test_v4_public_to_paserk_id(self):
        sk = Key.new(4, 'public', load_key('keys/private_key_ed25519.pem'))
        pk = Key.new(4, 'public', load_key('keys/public_key_ed25519.pem'))
        assert sk.to_peer_paserk_id() == pk.to_paserk_id()
        assert pk.to_peer_paserk_id() == ''

    def test_v4_public_verify_via_encode_with_wrong_key(self):
        sk = Key.new(4, 'public', load_key('keys/private_key_ed25519.pem'))
        pk = Key.new(4, 'public', load_key('keys/public_key_ed25519_2.pem'))
        token = pyseto.encode(sk, b'Hello world!')
        with pytest.raises(VerifyError) as err:
            pyseto.decode(pk, token)
            pytest.fail('pyseto.decode() should fail.')
        assert 'Failed to verify.' in str(err.value)

    @pytest.mark.parametrize('paserk, msg', [('xx.public.AAAAAAAAAAAAAAAA', 'Invalid PASERK version: xx.'), ('k1.public.AAAAAAAAAAAAAAAA', 'Invalid PASERK version: k1.'), ('k4.public.xxx.AAAAAAAAAAAAAAAA', 'Invalid PASERK format.'), ('k4.local.xxx.AAAAAAAAAAAAAAAA', 'Invalid PASERK format.'), ('k4.xxx.AAAAAAAAAAAAAAAA', 'Invalid PASERK type: xxx.'), ('k4.local.AAAAAAAAAAAAAAAA', 'Invalid PASERK type: local.')])
    def test_v4_public_from_paserk_with_invalid_args(self, paserk, msg):
        with pytest.raises(ValueError) as err:
            V4Public.from_paserk(paserk)
            pytest.fail('Key.from_paserk should fail.')
        assert msg in str(err.value)