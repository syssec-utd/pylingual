import logging, threading
from localstack import config as localstack_config
from localstack.aws.accounts import REQUEST_CTX_TLS, get_default_account_id
from localstack.constants import LS_LOG_TRACE_INTERNAL

def _patch_account_id_resolver():
    import localstack as A

    def B():
        try:
            return REQUEST_CTX_TLS.account_id
        except AttributeError:
            if localstack_config.LS_LOG and localstack_config.LS_LOG == LS_LOG_TRACE_INTERNAL:
                logging.debug('No Account ID in thread-local storage for thread %s', threading.current_thread().ident)
            return get_default_account_id()
    A.aws.accounts.account_id_resolver = B

def _patch_get_account_id_from_access_key_id():
    from localstack.aws import accounts as A

    def B(access_key_id):
        A = C(access_key_id)
        REQUEST_CTX_TLS.account_id = A
        return A
    C = A.get_account_id_from_access_key_id
    A.get_account_id_from_access_key_id = B