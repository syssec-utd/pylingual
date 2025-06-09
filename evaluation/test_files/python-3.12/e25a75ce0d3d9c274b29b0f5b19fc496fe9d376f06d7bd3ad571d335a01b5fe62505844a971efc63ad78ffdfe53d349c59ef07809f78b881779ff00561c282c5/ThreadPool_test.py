import unittest
import os
import sys
import random
import struct
import binascii
import time
import json
from nxswriter.ThreadPool import ThreadPool
from nxswriter.Errors import ThreadError
IS64BIT = struct.calcsize('P') == 8
if sys.version_info > (3,):
    long = int

class Source(object):

    def __init__(self):
        self.ljson = None
        self.gjson = None

    def setJSON(self, gjson, ljson=None):
        self.ljson = ljson
        self.gjson = gjson

class H5(object):

    def __init__(self):
        self.closed = False

    def close(self):
        self.closed = True

class Job(object):

    def __init__(self):
        self.counter = 0
        self.error = None

    def run(self):
        self.counter += 1

class EJob(object):

    def __init__(self):
        self.counter = 0
        self.error = None
        self.message = ('Error', 'My Error')
        self.canfail = None
        self.markfail = 0
        self.error = None

    def run(self):
        self.counter += 1
        self.error = self.message

    def markFailed(self, error=None):
        self.markfail += 1
        self.error = error

class SOJob(object):

    def __init__(self):
        self.counter = 0
        self.error = None
        self.message = ('Error', 'My Error')
        self.source = Source()
        self.h5Object = H5()

    def run(self):
        time.sleep(0.01)
        self.counter += 1

class WJob(object):

    def __init__(self):
        pass

class ThreadPoolTest(unittest.TestCase):

    def __init__(self, methodName):
        unittest.TestCase.__init__(self, methodName)
        self._tfname = 'field'
        self._tfname = 'group'
        self._fattrs = {'short_name': 'test', 'units': 'm'}
        self._bint = 'int64' if IS64BIT else 'int32'
        self._buint = 'uint64' if IS64BIT else 'uint32'
        self._bfloat = 'float64' if IS64BIT else 'float32'
        try:
            self.__seed = long(binascii.hexlify(os.urandom(16)), 16)
        except NotImplementedError:
            import time
            self.__seed = long(time.time() * 256)
        self.__rnd = random.Random(self.__seed)

    def myAssertRaise(self, exception, method, *args, **kwargs):
        try:
            error = False
            method(*args, **kwargs)
        except Exception:
            error = True
        self.assertEqual(error, True)

    def setUp(self):
        print('\nsetting up...')
        print('SEED = %s' % self.__seed)

    def tearDown(self):
        print('tearing down ...')

    def test_constructor(self):
        fun = sys._getframe().f_code.co_name
        print('Run: %s.%s() ' % (self.__class__.__name__, fun))
        nth = self.__rnd.randint(1, 10)
        el = ThreadPool(nth)
        self.assertEqual(el.numberOfThreads, nth)

    def test_run_append_join_wait(self):
        fun = sys._getframe().f_code.co_name
        print('Run: %s.%s() ' % (self.__class__.__name__, fun))
        nth = self.__rnd.randint(1, 10)
        el = ThreadPool(nth)
        self.assertEqual(el.numberOfThreads, nth)
        jlist = [Job() for c in range(self.__rnd.randint(1, 20))]
        for jb in jlist:
            self.assertEqual(el.append(jb), None)
        self.assertEqual(el.run(), None)
        self.assertEqual(el.join(), None)
        for c in jlist:
            self.assertEqual(c.counter, 1)
        self.assertEqual(el.run(), None)
        self.assertEqual(el.join(), None)
        for c in jlist:
            self.assertEqual(c.counter, 2)
        self.assertEqual(el.runAndWait(), None)
        for c in jlist:
            self.assertEqual(c.counter, 3)
        self.assertEqual(el.run(), None)
        self.assertEqual(el.join(), None)
        for c in jlist:
            self.assertEqual(c.counter, 4)
        self.assertEqual(el.runAndWait(), None)
        for c in jlist:
            self.assertEqual(c.counter, 5)

    def test_errors(self):
        fun = sys._getframe().f_code.co_name
        print('Run: %s.%s() ' % (self.__class__.__name__, fun))
        nth = self.__rnd.randint(1, 10)
        el = ThreadPool(nth)
        self.assertEqual(el.numberOfThreads, nth)
        jlist = [EJob() for c in range(self.__rnd.randint(1, 20))]
        for jb in jlist:
            self.assertEqual(el.append(jb), None)
        self.assertEqual(el.checkErrors(), None)
        self.assertEqual(el.run(), None)
        self.assertEqual(el.join(), None)
        for c in jlist:
            self.assertEqual(c.counter, 1)
        self.myAssertRaise(ThreadError, el.checkErrors)
        self.assertEqual(el.run(), None)
        self.assertEqual(el.join(), None)
        for c in jlist:
            self.assertEqual(c.counter, 2)
        self.assertEqual(el.runAndWait(), None)
        self.myAssertRaise(ThreadError, el.checkErrors)

    def test_errors_canfail(self):
        fun = sys._getframe().f_code.co_name
        print('Run: %s.%s() ' % (self.__class__.__name__, fun))
        nth = self.__rnd.randint(1, 10)
        el = ThreadPool(nth)
        self.assertEqual(el.numberOfThreads, nth)
        jlist = [EJob() for c in range(self.__rnd.randint(1, 20))]
        for jb in jlist:
            self.assertEqual(el.append(jb), None)
        self.assertEqual(el.checkErrors(), None)
        self.assertEqual(el.run(), None)
        self.assertEqual(el.join(), None)
        for c in jlist:
            self.assertEqual(c.counter, 1)
        self.myAssertRaise(ThreadError, el.checkErrors)
        for jb in jlist:
            self.assertEqual(jb.markfail, 0)
            jb.canfail = True
        self.assertEqual(el.run(), None)
        self.assertEqual(el.join(), None)
        for c in jlist:
            self.assertEqual(c.counter, 2)
        self.assertEqual(el.runAndWait(), None)
        el.checkErrors()
        for jb in jlist:
            self.assertEqual(jb.markfail, 1)

    def test_setJSON(self):
        fun = sys._getframe().f_code.co_name
        print('Run: %s.%s() ' % (self.__class__.__name__, fun))
        gjson = json.loads('{"data":{"a":"1"}}')
        ljson = json.loads('{"data":{"n":2}}')
        nth = self.__rnd.randint(1, 10)
        el = ThreadPool(nth)
        self.assertEqual(el.numberOfThreads, nth)
        jlist = [SOJob() for c in range(self.__rnd.randint(1, 20))]
        for jb in jlist:
            self.assertEqual(el.append(jb), None)
        self.assertEqual(el.setJSON(gjson), el)
        for jb in jlist:
            self.assertEqual(jb.source.gjson, gjson)
            self.assertEqual(jb.source.ljson, None)
        self.assertEqual(el.run(), None)
        self.assertEqual(el.join(), None)
        for jb in jlist:
            self.assertEqual(jb.source.gjson, gjson)
            self.assertEqual(jb.source.ljson, None)
        for c in jlist:
            self.assertEqual(c.counter, 1)
        self.assertEqual(el.setJSON(gjson, ljson), el)
        for jb in jlist:
            self.assertEqual(jb.source.gjson, gjson)
            self.assertEqual(jb.source.ljson, ljson)
        self.assertEqual(el.run(), None)
        self.assertEqual(el.join(), None)
        for jb in jlist:
            self.assertEqual(jb.counter, 2)
            self.assertEqual(jb.source.gjson, gjson)
            self.assertEqual(jb.source.ljson, ljson)

    def test_close(self):
        fun = sys._getframe().f_code.co_name
        print('Run: %s.%s() ' % (self.__class__.__name__, fun))
        nth = self.__rnd.randint(1, 10)
        el = ThreadPool(nth)
        self.assertEqual(el.numberOfThreads, nth)
        jlist = [SOJob() for c in range(self.__rnd.randint(1, 20))]
        for jb in jlist:
            self.assertEqual(el.append(jb), None)
        for jb in jlist:
            self.assertTrue(not jb.h5Object.closed)
        self.assertEqual(el.run(), None)
        self.assertEqual(el.join(), None)
        for jb in jlist:
            self.assertTrue(not jb.h5Object.closed)
        self.assertEqual(el.close(), None)
        for jb in jlist:
            self.assertTrue(jb.h5Object.closed)
if __name__ == '__main__':
    unittest.main()