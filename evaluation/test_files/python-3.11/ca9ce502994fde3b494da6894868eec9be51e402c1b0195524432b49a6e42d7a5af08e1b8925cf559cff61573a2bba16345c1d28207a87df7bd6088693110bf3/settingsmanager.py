import logging
from contextlib import contextmanager
import simplejson
log = logging.getLogger(__name__)

class SettingsSynchroniser(object):
    RESERVED_ATTRIBUTES = {'set', 'applyMessage', 'dumpState', 'restoreState', 'modify', 'reset'}

    def __init__(self, dispatcher, attributes):
        self._dispatch = dispatcher
        self._attributes = dict(attributes)
        for k, v in self._attributes.items():
            if k.startswith('_') or k in self.RESERVED_ATTRIBUTES:
                raise KeyError('{} is not a valid attribute name'.format(k))
            setattr(self, k, v)

    def dumpState(self):
        return {attr_name: value for attr_name, default in self._attributes.items() if (value := getattr(self, attr_name)) != default}

    def restoreState(self, data):
        for attr_name, default_value in self._attributes.items():
            setattr(self, attr_name, data.get(attr_name, default_value))

    def set(self, **kwargs):
        for k, v in kwargs.items():
            if k not in self._attributes:
                raise KeyError('Unknown attribute: {!r}'.format(k))
        self._dispatch(simplejson.dumps(kwargs).encode('utf-8'))

    def reset(self, sync=True):
        if sync:
            self.set(**self._attributes)
        else:
            for k, v in self._attributes.items():
                setattr(self, k, v)

    @contextmanager
    def modify(self, **kwargs):
        old = {k: getattr(self, k) for k in kwargs}
        try:
            self.set(**kwargs)
            yield
        finally:
            self.set(**old)

    def applyMessage(self, data):
        for k, v in list(simplejson.loads(data.decode('utf-8')).items()):
            if k not in self._attributes:
                log.error('%s: received unknown attribute %s', self, k)
            else:
                setattr(self, k, v)