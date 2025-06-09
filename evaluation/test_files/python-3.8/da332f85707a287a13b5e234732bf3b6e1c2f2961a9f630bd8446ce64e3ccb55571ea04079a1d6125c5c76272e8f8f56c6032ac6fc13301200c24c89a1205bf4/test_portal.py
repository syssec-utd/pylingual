import os
from satcfdi.portal.utils import generate_token, verify_token, action_url
from satcfdi.portal import SATPortal
from tests.utils import get_signer
current_dir = os.path.dirname(__file__)
test_dir = os.path.join(current_dir, 'test_portal')
session_file = os.path.join(test_dir, 'session')

def test_portal_get_token():
    code = 'MjFhYzNkODAtN2MxMC00NGU5LWI5NDYtMThmZWZmMjM5OTQ1'
    signer = get_signer('cacx7605101p8')
    token = generate_token(signer, code=code)
    assert code == verify_token(certificate=signer, token=token)

def test_action_url():
    target_url = action_url(action='/nidp/app/login?id=fiel&sid=0&option=credential&sid=0', url='https://loginda.siat.sat.gob.mx/nidp/app/login?id=fiel')
    assert target_url == 'https://loginda.siat.sat.gob.mx/nidp/app/login?id=fiel&sid=0&option=credential&sid=0'
    target_url = action_url(action=None, url='https://loginda.siat.sat.gob.mx/nidp/app/login?id=fiel')
    assert target_url == 'https://loginda.siat.sat.gob.mx/nidp/app/login?id=fiel'
    target_url = action_url(action='http://aaaa.bbb', url='https://loginda.siat.sat.gob.mx/nidp/app/login?id=fiel')
    assert target_url == 'http://aaaa.bbb'

def test_start_session():
    signer = get_signer('cacx7605101p8')
    res = SATPortal(signer)
    try:
        with open(session_file, 'rb') as f:
            res.load_session(f)
        print('Session Loaded')
    except FileNotFoundError:
        print('FileNotFound')
    os.makedirs(test_dir, exist_ok=True)
    with open(session_file, 'wb') as f:
        res.save_session(f)