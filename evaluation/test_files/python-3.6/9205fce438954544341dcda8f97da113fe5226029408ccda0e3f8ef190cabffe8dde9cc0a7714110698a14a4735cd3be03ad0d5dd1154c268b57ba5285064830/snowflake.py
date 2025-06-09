import os
import time
import random
import logging
import threading
from multiprocessing.dummy import Pool as ThreadPool
from concurrent import futures
from concurrent.futures import ThreadPoolExecutor, wait

class InvalidSystemClock(Exception):
    """ Clock callback exception """

class IdGenerator(object):
    DATA_CENTER_ID_BITS = 5
    WORKER_ID_BITS = 5
    SEQUENCE_BITS = 12
    MAX_WORKER_ID = -1 ^ -1 << WORKER_ID_BITS
    MAX_DATA_CENTER_ID = -1 ^ -1 << DATA_CENTER_ID_BITS
    WORKER_ID_SHIFT = SEQUENCE_BITS
    DATA_CENTER_ID_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS
    TIMESTAMP_LEFT_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS + DATA_CENTER_ID_BITS
    SEQUENCE_MASK = -1 ^ -1 << SEQUENCE_BITS
    TW_EPOCH = 1288834974657

    def __init_instance(self, data_center_id=None, worker_id=None, did_wid=-1, sequence=0):
        """
        初始化
        :param data_center_id: 数据中心（机器区域）ID
        :param worker_id: 机器ID
        :param did_wid: 数据中心和机器id合成10位二进制，用十进制0-1023表示，通过算法会拆分成 data_center_id 和 worker_id
        :param sequence: 起始序号
        """
        if did_wid > 0:
            data_center_id = did_wid >> 5
            worker_id = did_wid ^ data_center_id << 5
        if worker_id and (worker_id > self.MAX_WORKER_ID or worker_id < 0):
            raise ValueError('worker_id值越界')
        if data_center_id and (data_center_id > self.MAX_DATA_CENTER_ID or data_center_id < 0):
            raise ValueError('datacenter_id值越界')
        self.data_center_id = data_center_id or random.randint(0, self.MAX_DATA_CENTER_ID)
        self.worker_id = worker_id or random.randint(0, self.MAX_WORKER_ID)
        self.sequence = sequence
        self.last_timestamp = self._gen_timestamp()

    def __new__(cls, *args, **kwargs):
        """ 单例模式, 每次实例化时，实例的属性相同(注意) """
        if not hasattr(cls, '_instance'):
            cls._instance = super(IdGenerator, cls).__new__(cls)
            cls._instance.lock = threading.Lock()
            cls._instance.__init_instance(*args, **kwargs)
        return cls._instance

    def _gen_timestamp(self):
        """
        生成整数时间戳
        :return:int timestamp
        """
        return int(time.time() * 1000)

    def _til_next_millis(self, last_timestamp):
        """ 等到下一毫秒 """
        timestamp = self._gen_timestamp()
        while timestamp <= last_timestamp:
            timestamp = self._gen_timestamp()
        return timestamp

    def get_id(self, *args, **kw):
        """
        获取雪花算法 ID，重复率为: 0
        经多线程粗略测试计算， QPS: 155000 req/s, 155 req/ms, QPS 完全够用
        """
        with self.lock:
            timestamp = self._gen_timestamp()
            if timestamp < self.last_timestamp:
                logging.error('clock is moving backwards. Rejecting requests until {}'.format(self.last_timestamp))
                raise InvalidSystemClock
            if timestamp == self.last_timestamp:
                self.sequence = self.sequence + 1 & self.SEQUENCE_MASK
                if self.sequence == 0:
                    timestamp = self._til_next_millis(self.last_timestamp)
            else:
                self.sequence = 0
            self.last_timestamp = timestamp
            uid = timestamp - self.TW_EPOCH << self.TIMESTAMP_LEFT_SHIFT | self.data_center_id << self.DATA_CENTER_ID_SHIFT | self.worker_id << self.WORKER_ID_SHIFT | self.sequence
            return uid

def test_by_ThreadPool():
    """ from multiprocessing.dummy import Pool as ThreadPool
    本机一千万测试结果如下:
        实际执行总数: 10000000
        实际不重复总数: 10000000, 是否重复：True
        ID 重复率: 0.0%, 耗时: 46.7184s
        QPS: 21.4048w
    """
    concurrency_max = 10000000
    start_time = time.time()
    pool = ThreadPool()
    ret = pool.map(IdGenerator(1, 2).get_id, range(concurrency_max))
    pool.close()
    pool.join()
    end_time = time.time()
    actual_cnt = len(ret)
    no_repeat_cnt = len(set(ret))
    repeat_rate = (len(ret) - len(set(ret))) * 1.0 / len(ret) * 100
    cost_time = end_time - start_time
    qps = no_repeat_cnt * 1.0 / cost_time / 10000.0
    msg = '实际执行总数:   %s\n实际不重复总数: %s, 是否重复：%s\nID 重复率: %s%%, 耗时: %.4fs\nQPS: %.4fw'
    args = (actual_cnt, no_repeat_cnt, no_repeat_cnt == concurrency_max, repeat_rate, cost_time, qps)
    print(msg % args)

def test_by_ThreadPoolExecutor():
    """ 使用 concurrent.futures
    本机一百万测试结果如下:

    future_list = [executor.submit(IdGenerator(2, 3).get_id) for i in range(concurrency_max)]

    (1): executor.map
        gen = executor.map(IdGenerator(2, 3).get_id, range(concurrency_max))
        result = list(gen)

        ThreadPoolExecutor: 1000000
        ThreadPoolExecutor: 1000000
        ThreadPoolExecutor: True
        ThreadPoolExecutor 重复率: 0.0 60.61892819404602

    (2): wait
        ret_futures = wait(future_list)
        done_result = [f.result() for f in ret_futures.done]
        # not_done_result = [nf.result() for nf in ret_futures.not_done]
        result = done_result

        ThreadPoolExecutor: 1000000
        ThreadPoolExecutor: 1000000
        ThreadPoolExecutor: True
        ThreadPoolExecutor 重复率: 0.0 59.86428761482239

    (3): futures.as_completed
        result = [future.result() for future in futures.as_completed(future_list)]

        ThreadPoolExecutor: 1000000
        ThreadPoolExecutor: 1000000
        ThreadPoolExecutor: True
        ThreadPoolExecutor 重复率: 0.0 59.72651958465576
    """
    concurrency_max = 1000000
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        future_list = [executor.submit(IdGenerator(2, 3).get_id) for i in range(concurrency_max)]
        result = [future.result() for future in futures.as_completed(future_list)]
    end_time = time.time()
    print('ThreadPoolExecutor:', len(result))
    print('ThreadPoolExecutor:', len(set(result)))
    print('ThreadPoolExecutor:', len(set(result)) == concurrency_max)
    print('ThreadPoolExecutor 重复率:', (len(result) - len(set(result))) * 1.0 / len(result) * 100, end_time - start_time)
if __name__ == '__main__':
    test_by_ThreadPool()