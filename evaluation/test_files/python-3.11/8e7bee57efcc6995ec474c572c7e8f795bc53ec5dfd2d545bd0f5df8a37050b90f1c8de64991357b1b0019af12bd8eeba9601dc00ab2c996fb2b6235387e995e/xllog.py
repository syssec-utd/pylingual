import os
import concurrent.futures
import math
import time
import sys
from pyxllib.text.pupil import shorten
from pyxllib.prog.pupil import EmptyPoolExecutor
from pyxllib.debug.pupil import format_exception
XLLOG_CONF_FILE = 'xllog.yaml'
____xllog = '\n'

def get_xllog(name='xllog', *, log_file=None):
    """ 获得pyxllib库的日志类

    :param log_file: 增加输出到一个日志文件，该功能仅在首次初始化时有效
        注意这个是'w'机制，会删除之前的日志文件
        # TODO 这样的功能设计问题挺大的，工程逻辑很莫名其妙，有空要把日志功能修缮下
        #   例如一个通用的初始化类，然后xllog只是一个特定的实例日志类

    TODO 增加输出到钉钉机器人、邮箱的Handler？
    """
    import logging, coloredlogs
    if 'pyxllib.' + name in logging.root.manager.loggerDict:
        return logging.getLogger('pyxllib.' + name)
    if name == 'xllog':
        if os.path.isfile(XLLOG_CONF_FILE):
            import logging.config
            from pyxllib.file.specialist import File
            data = File(XLLOG_CONF_FILE).read()
            if isinstance(data, dict):
                logging.config.dictConfig(data)
            else:
                logging.config.fileConfig(XLLOG_CONF_FILE)
        else:
            xllog = logging.getLogger('pyxllib.xllog')
            fmt = '%(asctime)s %(message)s'
            if log_file:
                file_handler = logging.FileHandler(f'{log_file}', 'w')
                file_handler.setLevel(logging.DEBUG)
                file_handler.setFormatter(logging.Formatter(fmt))
                xllog.addHandler(file_handler)
            coloredlogs.install(level='DEBUG', logger=xllog, fmt=fmt)
    elif name == 'location':
        loclog = logging.getLogger('pyxllib.location')
        coloredlogs.install(level='DEBUG', logger=loclog, fmt='%(filename)s/%(lineno)d: %(message)s')
    return logging.getLogger('pyxllib.' + name)

class Iterate:
    """ 迭代器类，用来封装一些特定模式的for循环操作

    TODO 双循环，需要内部两两对比的迭代功能

    200920周日18:20，最初设计的时候，是提供run_pair、run_pair2的功能的
        不过后来想想，这个其实就是排列组合，在itertools里有combinations, permutations可以代替
        甚至有放回的组合也有combinations_with_replacement，我实在是不需要再这里写这些冗余的功能
        所以就移除了
    """

    def __init__(self, items):
        self.items = tuple(items)
        self.n_items = len(self.items)
        self.format_width = math.ceil(math.log10(self.n_items + 1))
        self.xllog = get_xllog()

    def _format_pinterval(self, pinterval=None):
        if isinstance(pinterval, str) and pinterval.endswith('%'):
            return int(round(self.n_items * float(pinterval[:-1]) / 100))
        else:
            return pinterval

    def _step1_check_number(self, pinterval, func):
        if pinterval:
            sys.stdout.flush()
            self.xllog.info(f'使用 {func} 处理 {self.n_items} 个数据 {shorten(str(self.items), 30)}')

    def _step2_check_range(self, start, end):
        if start:
            self.xllog.info(f'使用start参数，只处理≥{start}的条目')
        else:
            start = 0
        if end:
            self.xllog.info(f'使用 end 参数，只处理<{end}的条目')
        else:
            end = len(self.items)
        return (start, end)

    def _step3_executor(self, pinterval, max_workers):
        if max_workers == 1:
            executor = EmptyPoolExecutor()
        else:
            executor = concurrent.futures.ThreadPoolExecutor(max_workers)
            if pinterval:
                self.xllog.info(f'多线程执行，当前迭代所用线程数：{executor._max_workers}')
        return executor

    def _step4_iter(self, i, pinterval, executor):
        while executor._work_queue.qsize():
            pass
        if pinterval and (i or pinterval == 1) and (i % pinterval == 0):
            message = f' {self.items[i]}' if pinterval == 1 else ''
            self.xllog.info(f'{i:{self.format_width}d}/{self.n_items}={i / self.n_items:6.2%}{message}')

    def _step5_finish(self, pinterval, interrupt, start_time):
        from humanfriendly import format_timespan
        end_time = time.time()
        span = end_time - start_time
        if span:
            speed = self.n_items / span
            msg = f'总用时：{format_timespan(span)}，速度：{speed:.2f}it/s'
        else:
            msg = f'总用时：{format_timespan(span)}'
        if not interrupt and pinterval:
            self.xllog.info(f'{self.n_items / self.n_items:6.2%} 完成迭代，{msg}')
            sys.stderr.flush()

    def run(self, func, start=0, end=None, pinterval=None, max_workers=1, interrupt=True):
        """
        :param func: 对每个item执行的功能
        :param start: 跳过<start的数据，只处理>=start编号以上
        :param end: 只处理 < end 的数据
        :param pinterval: 每隔多少条目输出进度日志，默认不输出进度日志（但是错误日志依然会输出）
            支持按百分比进度显示，例如每20%，pinterval='20%'，不过一些底层实现机制原因，会有些许误差
            TODO 支持按指定时间间隔显示？ 例如每15秒，pinterval='15s' 感觉这种功能太花哨了，没必要搞
        :param max_workers: 默认线程数，默认1，即串行
        :type max_workers: int, None
        :param interrupt: 出现错误时是否中断，默认True会终止程序，否则只会输出错误日志
        :return:
        """
        pinterval = self._format_pinterval(pinterval)
        self._step1_check_number(pinterval, func)
        start, end = self._step2_check_range(start, end)
        error = False
        executor = self._step3_executor(pinterval, max_workers)

        def wrap_func(func, i):
            nonlocal error
            item = self.items[i]
            try:
                func(item)
            except Exception as e:
                error = e
                self.xllog.error(f'💔idx={i}运行出错：{item}\n{format_exception(e)}')
        start_time = time.time()
        for i in range(start, end):
            self._step4_iter(i, pinterval, executor)
            executor.submit(wrap_func, func, i)
            if interrupt and error:
                raise error
        executor.shutdown()
        self._step5_finish(pinterval, interrupt and error, start_time)