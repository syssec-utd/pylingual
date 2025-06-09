import os
import queue
import threading
import time

def haha(*, LogPath: str, LogName: str, Mode: str='a'):

    def __wrapper__(func):

        def __inner__(msg: dict):
            logger = smile.log(path=LogPath, file_name=LogName, mode=Mode)
            logger.append_msg(msg=msg)
            logger.printer(func)
        return __inner__
    return __wrapper__
lock = threading.Lock()

class SmileVoice(threading.Thread):
    ThreadName = 'Smile Log Thread'

    def __init__(self, path, file_name='orange.log', mode='a'):
        super().__init__(name=SmileVoice.ThreadName)
        self.path = path
        self.queue = queue.Queue()
        self.file_name = file_name
        self.__formatter = None
        self.mode = mode
        self.start()

    def append_msg(self, *, msg: dict) -> None:
        self.queue.put(msg)

    def printer(self, formatter) -> None:
        """
        set how to write the log
        :param formatter:
        :return:
        """
        self.__formatter = formatter

    def run(self) -> None:
        """
        日志线程结束条件：没有输出的消息 及 主线程已结束
        """
        while True:
            if not self.queue.empty():
                msg = self.queue.get()
                with open(os.path.join(self.path, self.file_name), self.mode, encoding='utf-8') as f:
                    self.__formatter(msg, f)
            if self.queue.empty() and (not threading.main_thread().is_alive()):
                break

class Smile(object):
    """
    control log thread
    one log file , one log thread
    """

    def __init__(self):
        self.loggers = {}

    def log(self, *, path: str, file_name: str, mode: str) -> SmileVoice:
        """
        创建记录日志的线程
        如果记录的日志线程已存在，则不会创建新线程
        :param path: 日志存放路径
        :param file_name: 日志文件名
        :param mode: 写文件的模式
        :return:
        """
        try:
            lock.acquire()
            if self.loggers.get(file_name) is None:
                self.loggers[file_name] = SmileVoice(path=path, file_name=file_name, mode=mode)
            return self.loggers.get(file_name)
        finally:
            lock.release()
smile = Smile()