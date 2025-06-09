import logging
import os
_old_factory = logging.getLogRecordFactory()

def record_factory(*args, **kwargs):
    record = _old_factory(*args, **kwargs)
    return record
logging.setLogRecordFactory(record_factory)
logging.basicConfig(level=os.environ.get('LOG_LEVEL', 'WARNING').upper(), format='%(levelname_colored)s: %(message)s')
log = logging.getLogger()