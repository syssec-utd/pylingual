import os
from json import loads, dumps
import logging
from lcyframe.libs import utils

class NsqTask(object):
    """订阅队列"""
    _workers = {}

    def __init__(self, topic, channel):
        self.topic = topic
        self.channel = channel

    def __call__(self, _handler):
        setattr(_handler, 'topic', self.topic)
        setattr(_handler, 'channel', self.channel)
        self._workers[_handler.__name__] = _handler
        return _handler

    @classmethod
    def get_workers(cls, ROOT, workers_path):
        if not ROOT:
            raise Exception('the project dir path must been give， and None.')
        if not isinstance(workers_path, list):
            workers_path = [workers_path]
        if workers_path is None:
            raise Exception('nsq workers_path is not allow empty')
        if not cls._workers:
            for work in workers_path:
                for (root, dirs, files) in os.walk(utils.fix_path(os.path.join(ROOT, work))):
                    for file in files:
                        if file.startswith('__'):
                            continue
                        if file.endswith('.pyc'):
                            continue
                        if not file.endswith('.py'):
                            continue
                        model_name = root.replace(ROOT, '').lstrip('/').replace('/', '.') + '.' + file.rstrip('.py')
                        __import__(model_name, globals(), locals(), [model_name], 0)
                        logging.debug('register nsq workers [%s.py] success!' % model_name)
        return cls._workers

class ReadNsq(object):
    """
    消费者：当接收新消息后调用该方法
    """

    @classmethod
    def message_handler(cls, message):
        msg = loads(message.body.decode('utf-8'))
        event = msg.pop('event', None)
        if not hasattr(cls, event):
            logging.warning(dumps(msg))
            logging.warning("has a event '%s' not realized in Class %s" % (event, cls.__name__))
            return True
        return getattr(cls, event)(**msg)

class WriteNsq(object):
    """
    生产者：向已订阅的topic里发送消息
    """
    _nsq = None

    def __init__(self, nsq_conn=None):
        if nsq_conn is None:
            try:
                from .singleton import NsqCon
                nsq_conn = NsqCon.get_connection()
            except:
                raise Exception('your must register nsq conn before start.')
        self._nsq = nsq_conn

    def __getattr__(self, name):
        if hasattr(self.__class__, '__events__'):
            if name not in self.__class__.__events__:
                raise Exception("Event '%s' is not exists in your Producer Class" % name)
        if name not in self.__dict__:
            self.__dict__[name] = pub = AgentNsq(self._nsq, name, self.topic)
            return pub
        else:
            return self.__dict__[name]

class AgentNsq:

    def __init__(self, _nsq, event, topic):
        self.event = event
        self.topic = topic
        self._nsq = _nsq

    def __repr__(self):
        return "event '%s'" % self.event

    def __call__(self, kwargs):
        kwargs['event'] = self.event
        self._nsq.pub(self.topic, dumps(kwargs).encode('utf-8'))