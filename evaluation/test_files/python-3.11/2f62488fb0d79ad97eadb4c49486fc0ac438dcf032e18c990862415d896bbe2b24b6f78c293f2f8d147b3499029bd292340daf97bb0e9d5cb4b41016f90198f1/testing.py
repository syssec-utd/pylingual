import os
from now.constants import EXECUTOR_PREFIX

def handle_test_mode(config):
    if os.environ.get('NOW_TESTING', False):
        from now.executor.autocomplete import NOWAutoCompleteExecutor2
        from now.executor.indexer.elastic import NOWElasticIndexer
        from now.executor.preprocessor import NOWPreprocessor
        if NOWPreprocessor and NOWAutoCompleteExecutor2 and NOWElasticIndexer:
            pass
        for k, v in config.items():
            if not (isinstance(v, str) and v.startswith(EXECUTOR_PREFIX)):
                continue
            if k == 'INDEXER_NAME':
                config[k] = 'NOWElasticIndexer'
            elif k == 'AUTOCOMPLETE_EXECUTOR_NAME':
                config[k] = 'NOWAutoCompleteExecutor2'
            elif k == 'PREPROCESSOR_NAME':
                config[k] = 'NOWPreprocessor'
            else:
                continue